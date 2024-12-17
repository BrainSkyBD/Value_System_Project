from django.shortcuts import render
from assembliesApp.models import Assemblies_Code_L1_Table, Assemblies_Code_L2_Table, Assemblies_Code_L3_Table, Estimation_Assemblies_Table, Estimation_Assemblies_Resource_Details_Table
from companyApp.models  import CompanyDetailsTable

import json
from django.shortcuts import render
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
import json
from django.db.models import Sum
from expenseApp.models import ExpenseTable



# Create your views here.
# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import MainContract, MainContractDetail, SubContractTable
from companyApp.models import CompanyDetailsTable
from decimal import Decimal, InvalidOperation
import re

def clean_decimal(value):
    """Remove any characters that are not digits or a decimal point and convert to Decimal."""
    clean_value = re.sub(r'[^\d.]', '', value)
    try:
        return Decimal(clean_value)
    except InvalidOperation:
        return Decimal(0)  # or handle this in a way that suits your needs

@login_required
def save_contract(request):
    if request.method == 'POST':
        print(request.POST)
        contract_name = request.POST.get('contract_name')
        comb_assem_code = request.POST.get('Comb_Assem_Code')
        number_input = request.POST.get('numberInput')
        numberInput_id = request.POST.get('numberInput_id')
        item_description = request.POST.get('Item_Description')

        totalBudgetCosts = request.POST.get('totalBudgetCosts')
        totalMarkupAmount = request.POST.get('totalMarkupAmount')
        totalTotalPrice = request.POST.get('totalTotalPrice')
        totalTargetProfit = request.POST.get('totalTargetProfit')
        rows = request.POST.getlist('rows[]')

        print(totalBudgetCosts, totalMarkupAmount, totalTotalPrice, totalTargetProfit)

        print(numberInput_id)
        print('numberInput_id')

        print(rows)
        print(type(rows))

        if not rows:
            return JsonResponse({'status': 'error', 'message': 'No rows provided'}, status=400)

        company_details_record = CompanyDetailsTable.objects.filter(User=request.user).last()

        if not company_details_record:
            return JsonResponse({'status': 'error', 'message': 'No company details found for the user'}, status=400)

        # Create the MainContract
        main_contract = MainContract.objects.create(
            company_details=company_details_record,
            contract_name=contract_name,
            contract_total_budget_costs=clean_decimal(totalBudgetCosts),
            contract_total_markup_amount=clean_decimal(totalMarkupAmount),
            contract_total_price=clean_decimal(totalTotalPrice),
            contract_total_target_profit=clean_decimal(totalTargetProfit),
        )
        print('main_contract')
        print(main_contract)

        # Create MainContractDetail instances
        for row in rows:
            data = row.split(',')
            print('data')
            print(data)
            print(type(data))
            print(data[0])

            print(data[0])
            print(data[1])
            print(data[2])
            print(data[3])
            print(clean_decimal(data[4]))
            print(clean_decimal(data[5]))
            print(clean_decimal(data[6]))
            print(clean_decimal(data[7]))
            print(clean_decimal(data[8]))
            print(clean_decimal(data[9]))
            print(clean_decimal(data[10]))
            print(clean_decimal(data[11]))

            print('ssss')

            if len(data) >= 12:  # Ensure there are enough elements in the data list
                # try:
                MainContractDetail.objects.create(
                    main_contract=main_contract,
                    comb_assem_code=data[0],
                    assembly_name=data[1],
                    assembly_row = Estimation_Assemblies_Table.objects.filter(id=numberInput_id).last(),
                    unit=item_description,
                    item_description=number_input,
                    unit_cost=clean_decimal(data[2]),
                    budget_quantity=clean_decimal(data[3]),
                    budget_costs=clean_decimal(data[5]),
                    markup=clean_decimal(data[6]),
                    markup_amount=clean_decimal(data[7]),
                    unit_price=clean_decimal(data[8]),
                    total_price=clean_decimal(data[9]),
                    target_profit=clean_decimal(data[10])
                )
                # except (IndexError, InvalidOperation) as e:
                #     print(f"Error processing row {row}: {e}")
                #     return JsonResponse({'status': 'error', 'message': f"Error processing row {row}: {e}"}, status=400)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)





@login_required
def contract_list(request):
    company_details_record = CompanyDetailsTable.objects.filter(User=request.user).last()
    contracts = MainContract.objects.filter(company_details=company_details_record).order_by('-id')
    
    return render(request, 'contractApp/contract_list.html', {'contracts': contracts})







@login_required
def view_contract(request, contract_id):
    # Fetch the contract using the contract ID, or return a 404 if not found
    contract = get_object_or_404(MainContract, id=contract_id)

    # Fetch the related MainContractDetail records
    contract_details = MainContractDetail.objects.filter(main_contract=contract)

    filter_expense = ExpenseTable.objects.filter(contract_value=contract)
    print(filter_expense)
    total_cost = sum(expense.total_cost for expense in filter_expense)

    filter_subcontracts = SubContractTable.objects.filter(contract_value=contract)
    subcontract_total_cost = sum(subcontract.contract_total_price for subcontract in filter_subcontracts)

    context = {
        'contract': contract,
        'contract_details': contract_details,
        'filter_expense':filter_expense,
        'total_cost':total_cost,
        'filter_subcontracts':filter_subcontracts,
        'subcontract_total_cost':subcontract_total_cost
    }
    return render(request, 'contractApp/view_contract.html', context)


@login_required
def delete_contract(request, contract_id):
    # Get the contract, or return a 404 if not found
    contract = get_object_or_404(MainContract, id=contract_id)

    # Check if the user is authorized to delete this contract (optional)
    if contract.company_details.User != request.user:
        return JsonResponse({'status': 'error', 'message': 'You do not have permission to delete this contract.'}, status=403)

    # Delete the contract
    contract.delete()

    # Redirect to contract list or return success message
    return JsonResponse({'status': 'success'})


# @login_required
# def create_contract(request):
#     company_details_record = CompanyDetailsTable.objects.filter(User=request.user).last()

#     filter_Estimation_Assemblies_Table = Estimation_Assemblies_Table.objects.filter(Company_Details=company_details_record)
#     filter_Estimation_Assemblies_list = list(filter_Estimation_Assemblies_Table.values('id', 'Assembly_Name', 'Unit_of_Measure', 'Assemblies_Code_L1__Assemblies_Code_L1', 'Assemblies_Code_L2__Assemblies_Code_L2', 'Assemblies_Code_L3__Assemblies_Code_L3', 'Assembly_Unit_Cost'))
#     filter_Assemblies_json = json.dumps(filter_Estimation_Assemblies_list, cls=DateTimeEncoder)

#     context = {'filter_Assemblies_json': filter_Assemblies_json}
#     return render(request, "contractApp/create_contract.html", context)



@login_required
def create_contract(request):
    company_details_record = CompanyDetailsTable.objects.filter(User=request.user).last()
    filter_Estimation_Assemblies_Table = Estimation_Assemblies_Table.objects.filter(Company_Details=company_details_record)

    # Gather assemblies and resource totals
    assemblies_data = []
    for assembly in filter_Estimation_Assemblies_Table:
        assemblies_data.append({
            'id': assembly.id,
            'assembly_name': assembly.Assembly_Name,
            'unit_of_measure': assembly.Unit_of_Measure,
            'assembly_unit_cost': assembly.Assembly_Unit_Cost,
            'resource_code_totals': assembly.get_resource_code_totals(),
        })

    context = {
        'assemblies_data': json.dumps(assemblies_data),  # Pass as JSON for easy JS access
    }
    return render(request, "contractApp/create_contract.html", context)





def Contract_Management(request):
    company_details_record = CompanyDetailsTable.objects.filter(User=request.user).last()
    print('company_details_record')
    print(company_details_record)
    if request.method == "POST":
        if 'add_assemblies' in request.POST:
            parent_type = request.POST['parent_type']
            assemblies_name = request.POST['assemblies_name']
            if parent_type == 'level1':
                Assemblies_Code_L1_Table.objects.create(
                    Company_Details=company_details_record,
                    Assemblies_Code_L1=assemblies_name
                )
            elif parent_type == 'level2':
                Assemblies_Code_L2_Table.objects.create(
                    Company_Details=company_details_record,
                    Assemblies_Code_L1_id=request.POST['parent_id'],
                    Assemblies_Code_L2=assemblies_name
                )
            elif parent_type == 'level3':
                Assemblies_Code_L3_Table.objects.create(
                    Company_Details=company_details_record,
                    Assemblies_Code_L2_id=request.POST['parent_id'],
                    Assemblies_Code_L3=assemblies_name
                )
        elif 'delete_assemblies' in request.POST:
            parent_type = request.POST['parent_type']
            parent_id = request.POST['parent_id']
            if parent_type == 'level1':
                Assemblies_Code_L1_Table.objects.filter(id=parent_id).delete()
            elif parent_type == 'level2':
                Assemblies_Code_L2_Table.objects.filter(id=parent_id).delete()
            elif parent_type == 'level3':
                Assemblies_Code_L3_Table.objects.filter(id=parent_id).delete()

        return redirect('Assemblies_Management')

    level1_assemblies = Assemblies_Code_L1_Table.objects.all()
    data = []
    for level1 in level1_assemblies:
        level2_assemblies = Assemblies_Code_L2_Table.objects.filter(Assemblies_Code_L1=level1)
        level1_data = {
            'level1': level1,
            'level2': []
        }
        for level2 in level2_assemblies:
            level3_assemblies = Assemblies_Code_L3_Table.objects.filter(Assemblies_Code_L2=level2)
            level1_data['level2'].append({
                'level2': level2,
                'level3': level3_assemblies
            })
        data.append(level1_data)

    context = {
        'data': data
    }
    return render(request, 'contractApp/Contract_management.html', context)


@login_required
def create_subcontract(request):
    company_details_record = CompanyDetailsTable.objects.filter(User=request.user).last()
    filter_Estimation_Assemblies_Table = Estimation_Assemblies_Table.objects.filter(Company_Details=company_details_record)

    # Gather assemblies and resource totals
    assemblies_data = []
    for assembly in filter_Estimation_Assemblies_Table:
        assemblies_data.append({
            'id': assembly.id,
            'assembly_name': assembly.Assembly_Name,
            'unit_of_measure': assembly.Unit_of_Measure,
            'assembly_unit_cost': assembly.Assembly_Unit_Cost,
            'resource_code_totals': assembly.get_resource_code_totals(),
        })

    # Filter main contract 
    filter_MainContract_query = MainContract.objects.filter(company_details=company_details_record)
    filter_MainContract_list = list(filter_MainContract_query.values('id', 'contract_name'))
    filter_MainContract_json = json.dumps(filter_MainContract_list, cls=DateTimeEncoder)

    context = {
        'assemblies_data': json.dumps(assemblies_data),  # Pass as JSON for easy JS access
        'filter_MainContract_json':filter_MainContract_json
    }
    return render(request, "contractApp/create_subcontract.html", context)




@login_required
def save_subcontract(request):
    if request.method == 'POST':
        print(request.POST)
        subcontract_name = request.POST.get('subcontract_name')
        comb_assem_code = request.POST.get('Comb_Assem_Code')
        hiddencontractInputId = request.POST.get('hiddencontractInputId')
        hiddenassemblyInputId = request.POST.get('hiddenassemblyInputId')
        item_description = request.POST.get('Item_Description')

        totalTotalPrice = request.POST.get('totalTotalPrice')
        rows = request.POST.getlist('rows[]')

        print(hiddencontractInputId, hiddenassemblyInputId, totalTotalPrice, subcontract_name)


        print(rows)
        print(type(rows))

        if not rows:
            return JsonResponse({'status': 'error', 'message': 'No rows provided'}, status=400)

        company_details_record = CompanyDetailsTable.objects.filter(User=request.user).last()

        if not company_details_record:
            return JsonResponse({'status': 'error', 'message': 'No company details found for the user'}, status=400)

        # Create the MainContract
        sub_contract = SubContractTable.objects.create(
            company_details=company_details_record,
            contract_value=MainContract.objects.filter(id=hiddencontractInputId).last(),
            subcontract_name=subcontract_name,
            contract_total_price=clean_decimal(totalTotalPrice),
        )
        print('sub_contract')
        print(sub_contract)

        # Create MainContractDetail instances
        for row in rows:
            data = row.split(',')
            print('data')
            print(data)
            print(type(data))

            print(data[0])
            print(data[1])
            print(data[2])
            print(data[3])


            if len(data) >= 12:  # Ensure there are enough elements in the data list
                try:
                    SubContractDetail.objects.create(
                        sub_contract=sub_contract,
                        comb_assem_code=comb_assem_code,
                        assembly_value = Estimation_Assemblies_Table.objects.filter(id=hiddenassemblyInputId).last(),
                        item_description=item_description,
                        unit=data[0],
                        unit_cost=clean_decimal(data[1]),
                        subcontract_quantity=clean_decimal(data[2]),
                        subcontract_total_price=clean_decimal(data[3]),
                        
                    )
                except (IndexError, InvalidOperation) as e:
                    print(f"Error processing row {row}: {e}")
                    return JsonResponse({'status': 'error', 'message': f"Error processing row {row}: {e}"}, status=400)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)



@login_required
def subcontract_list(request):
    company_details_record = CompanyDetailsTable.objects.filter(User=request.user).last()
    contracts = SubContractTable.objects.filter(company_details=company_details_record).order_by('-id')
    
    return render(request, 'contractApp/subcontract_list.html', {'contracts': contracts})



def SubContract_Management(request):
    company_details_record = CompanyDetailsTable.objects.filter(User=request.user).last()
    print('company_details_record')
    print(company_details_record)
    if request.method == "POST":
        if 'add_assemblies' in request.POST:
            parent_type = request.POST['parent_type']
            assemblies_name = request.POST['assemblies_name']
            if parent_type == 'level1':
                Assemblies_Code_L1_Table.objects.create(
                    Company_Details=company_details_record,
                    Assemblies_Code_L1=assemblies_name
                )
            elif parent_type == 'level2':
                Assemblies_Code_L2_Table.objects.create(
                    Company_Details=company_details_record,
                    Assemblies_Code_L1_id=request.POST['parent_id'],
                    Assemblies_Code_L2=assemblies_name
                )
            elif parent_type == 'level3':
                Assemblies_Code_L3_Table.objects.create(
                    Company_Details=company_details_record,
                    Assemblies_Code_L2_id=request.POST['parent_id'],
                    Assemblies_Code_L3=assemblies_name
                )
        elif 'delete_assemblies' in request.POST:
            parent_type = request.POST['parent_type']
            parent_id = request.POST['parent_id']
            if parent_type == 'level1':
                Assemblies_Code_L1_Table.objects.filter(id=parent_id).delete()
            elif parent_type == 'level2':
                Assemblies_Code_L2_Table.objects.filter(id=parent_id).delete()
            elif parent_type == 'level3':
                Assemblies_Code_L3_Table.objects.filter(id=parent_id).delete()

        return redirect('Assemblies_Management')

    level1_assemblies = Assemblies_Code_L1_Table.objects.all()
    data = []
    for level1 in level1_assemblies:
        level2_assemblies = Assemblies_Code_L2_Table.objects.filter(Assemblies_Code_L1=level1)
        level1_data = {
            'level1': level1,
            'level2': []
        }
        for level2 in level2_assemblies:
            level3_assemblies = Assemblies_Code_L3_Table.objects.filter(Assemblies_Code_L2=level2)
            level1_data['level2'].append({
                'level2': level2,
                'level3': level3_assemblies
            })
        data.append(level1_data)

    context = {
        'data': data
    }
    return render(request, 'contractApp/SubContract_management.html', context)