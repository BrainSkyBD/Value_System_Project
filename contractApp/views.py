from django.shortcuts import render
from assembliesApp.models import Assemblies_Code_L1_Table, Assemblies_Code_L2_Table, Assemblies_Code_L3_Table, Estimation_Assemblies_Table, Estimation_Assemblies_Resource_Details_Table
from companyApp.models  import CompanyDetailsTable, Resource_Code_L1_Table

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
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from storeApp.models import StoreTable

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
from .models import MainContract, MainContractDetail, SubContractTable, SubContractDetail, MainContractBudgetCostTable, MainContractInvoiceTable, MainContractInvoiceDetailsTable, SubContractInvoiceTable, SubContractInvoiceDetailsTable
from companyApp.models import CompanyDetailsTable
from decimal import Decimal, InvalidOperation
import re
from django.db.models import Sum, F


def clean_decimal(value):
    """Remove any characters that are not digits or a decimal point and convert to Decimal."""
    clean_value = re.sub(r'[^\d.]', '', value)
    try:
        return Decimal(clean_value)
    except InvalidOperation:
        return Decimal(0)  # or handle this in a way that suits your needs

@login_required
def save_contract(request):
    company_details_record = request.user.company_details
    if request.method == 'POST':
        print(request.POST)
        contract_name = request.POST.get('contract_name')
        comb_assem_code = request.POST.get('Comb_Assem_Code')
        number_input = request.POST.get('numberInput')
        numberInput_id = request.POST.get('numberInput_id')
        item_description = request.POST.get('Item_Description')
        print(contract_name, comb_assem_code, number_input, numberInput_id, item_description)

        totalBudgetCosts = request.POST.get('totalBudgetCosts')
        totalMarkupAmount = request.POST.get('totalMarkupAmount')
        totalTotalPrice = request.POST.get('totalTotalPrice')
        totalTargetProfit = request.POST.get('totalTargetProfit')
        rows = request.POST.getlist('rows[]')

        print(totalBudgetCosts, totalMarkupAmount, totalTotalPrice, totalTargetProfit)

        print('------------------------------')

        print(rows)
        print(type(rows))

        if not rows:
            return JsonResponse({'status': 'error', 'message': 'No rows provided'}, status=400)

        company_details_record = request.user.company_details

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
                get_estimated_assembly = Estimation_Assemblies_Table.objects.filter(id=data[14]).last()
                var_contract_detail_record_save = MainContractDetail(
                    main_contract=main_contract,
                    comb_assem_code=data[0],
                    assembly_name=data[1],
                    assembly_row = get_estimated_assembly,
                    unit=get_estimated_assembly.Unit_of_Measure,
                    item_description=data[13],
                    unit_cost=clean_decimal(data[3]),
                    budget_quantity=clean_decimal(data[5]),
                    contract_quantity=clean_decimal(data[4]),
                    budget_costs=clean_decimal(data[6]),
                    markup=clean_decimal(data[7]),
                    markup_amount=clean_decimal(data[8]),
                    unit_price=clean_decimal(data[9]),
                    total_price=clean_decimal(data[10]),
                    target_profit=clean_decimal(data[11])
                )
                var_contract_detail_record_save.save()
                # except (IndexError, InvalidOperation) as e:
                #     print(f"Error processing row {row}: {e}")
                #     return JsonResponse({'status': 'error', 'message': f"Error processing row {row}: {e}"}, status=400)

                filter_Estimation_Assemblies_Resource_Details = Estimation_Assemblies_Resource_Details_Table.objects.filter(Estimation_Assemblies=get_estimated_assembly)
                for estimated_assembly in filter_Estimation_Assemblies_Resource_Details:
                    var_MainContractBudgetCost = MainContractBudgetCostTable(
                        company_details = company_details_record,
                        contract_details = var_contract_detail_record_save,
                        Resource_Code = estimated_assembly.Resource_record,
                        budget_unit_rates = estimated_assembly.Resource_record.Budget_Unit_Cost,
                        budget_cost = float(estimated_assembly.Resource_record.Budget_Unit_Cost)*int(clean_decimal(data[4]))
                    )
                    var_MainContractBudgetCost.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)





@login_required
def contract_list(request):
    company_details_record = request.user.company_details
    contracts = MainContract.objects.filter(company_details=company_details_record).order_by('-id')
    
    return render(request, 'contractApp/contract_list.html', {'contracts': contracts})




@login_required
@csrf_exempt
def create_invoice(request):
    if request.method == 'POST':
        invoice_qty = []
        contract_details_id = []
        
        for key in request.POST:
            if key.startswith('invoice_qty_'):
                invoice_qty.append(request.POST[key])
            if key.startswith('contract_details_id_'):
                contract_details_id.append(request.POST[key])


        contract_id= request.POST.get('contract_id')
        try:
            get_contract = MainContract.objects.get(id=contract_id)
        except Exception as exc:
            print(exc)
            messages.error(request, f"Error : {exc}")
            return redirect('view_contract', contract_id)


        var_MainContractInvoice = MainContractInvoiceTable(
            invoice_contract_row = get_contract
        )
        var_MainContractInvoice.save()

        
        # Debugging step: Print the extracted lists
        print("Invoice Quantities:", invoice_qty)
        print("Contract Details IDs:", contract_details_id)

        # Process each contract detail
        for cd_id, inv_qty in zip(contract_details_id, invoice_qty):
            print('cd_id, inv_qty')
            print(cd_id, inv_qty)

            contract_details_id = cd_id
            invoice_quantity = inv_qty

            print("contract_details_id, invoice_quantity")
            print(contract_details_id, invoice_quantity)

        
            try:
                get_contract_details = MainContractDetail.objects.get(id=contract_details_id)
            except Exception as exc:
                print(exc)
                messages.error(request, f"Error : {exc}")
                return redirect('view_contract', contract_id)

            get_remain_invoice = get_contract_details.calculate_remaining_quantity()
            if int(get_remain_invoice) < int(invoice_quantity):
                messages.error(request, f"Error : Your remain invoice quantity is {get_remain_invoice}, you trying to add {invoice_quantity}")
                return redirect('view_contract', contract_id)
            
            

            var_MainContractInvoice_details = MainContractInvoiceDetailsTable(
                main_contract_invoice = var_MainContractInvoice,
                main_contract_assembly = get_contract_details,
                Invoice_Quantity = invoice_quantity,
                Invoice_Revenue = float(get_contract_details.unit_price)*float(invoice_quantity)
            )
            var_MainContractInvoice_details.save()
        
        # return redirect('success_url')  # Redirect to a success page
        messages.success(request, f"Invoice Quantity Added!")
        return redirect('view_contract', contract_id)



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
    # subcontract_total_cost = sum(subcontract.contract_total_price for subcontract in filter_subcontracts)
    # subcontract_total_cost = sum(detail.total_Sub_Contract_Cost_Calculation() for detail in contract_details)

    filter_expense = ExpenseTable.objects.filter(contract_value=contract)
    expense_total_cost = sum(expense.total_cost for expense in filter_expense)
    
    filter_stores = StoreTable.objects.filter(contract_value=contract, stock_trasaction_status="Stock-Out")
    store_total_cost = sum(store.total_cost for store in filter_stores)

    # Sum_Total_Actual_Resources_Cost = subcontract_total_cost + expense_total_cost + store_total_cost
    Sum_Total_Actual_Resources_Cost = sum(detail.Total_Actual_Resources_Cost() for detail in contract_details)

    
    main_contract_budget_costs = MainContractBudgetCostTable.objects.filter(contract_details__in=contract_details)
    sum_contract_budget_cost = sum(float(budget_cost_row.budget_cost) for budget_cost_row in main_contract_budget_costs)

    filter_main_contract_invoice = MainContractInvoiceTable.objects.filter(
        invoice_contract_row=contract
    )

    filter_resoures_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=contract.company_details)



    context = {
        'contract': contract,
        'contract_details': contract_details,
        'filter_expense':filter_expense,
        'total_cost':total_cost,
        'filter_subcontracts':filter_subcontracts,
        # 'subcontract_total_cost':subcontract_total_cost,
        'expense_total_cost':expense_total_cost,
        'store_total_cost':store_total_cost,
        'Sum_Total_Actual_Resources_Cost':Sum_Total_Actual_Resources_Cost,
        'main_contract_budget_costs':main_contract_budget_costs,
        'sum_contract_budget_cost':sum_contract_budget_cost,
        'filter_main_contract_invoice':filter_main_contract_invoice,
        'filter_resoures_level_1':filter_resoures_level_1,
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
#     company_details_record = request.user.company_details

#     filter_Estimation_Assemblies_Table = Estimation_Assemblies_Table.objects.filter(Company_Details=company_details_record)
#     filter_Estimation_Assemblies_list = list(filter_Estimation_Assemblies_Table.values('id', 'Assembly_Name', 'Unit_of_Measure', 'Assemblies_Code_L1__Assemblies_Code_L1', 'Assemblies_Code_L2__Assemblies_Code_L2', 'Assemblies_Code_L3__Assemblies_Code_L3', 'Assembly_Unit_Cost'))
#     filter_Assemblies_json = json.dumps(filter_Estimation_Assemblies_list, cls=DateTimeEncoder)

#     context = {'filter_Assemblies_json': filter_Assemblies_json}
#     return render(request, "contractApp/create_contract.html", context)



@login_required
def create_contract(request):
    company_details_record = request.user.company_details
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
            'Assemblies_Code_L1': assembly.Assemblies_Code_L1.Assemblies_Code_L1,
            'Assemblies_Code_L2': assembly.Assemblies_Code_L2.Assemblies_Code_L2,
            'Assemblies_Code_L3': assembly.Assemblies_Code_L3.Assemblies_Code_L3,
        })

    context = {
        'assemblies_data': json.dumps(assemblies_data),  # Pass as JSON for easy JS access
    }
    return render(request, "contractApp/create_contract.html", context)





def Contract_Management(request):
    company_details_record = request.user.company_details
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
                'level3': [
                    {
                        'assembly': level3,
                        'assemblies': Estimation_Assemblies_Table.objects.filter(Assemblies_Code_L3=level3),
                        'main_contracts': MainContract.objects.filter(
                            details__assembly_row__Assemblies_Code_L3=level3
                        ).distinct()
                    }
                    for level3 in level3_assemblies
                ]
            })
        data.append(level1_data)

    context = {
        'data': data
    }
    return render(request, 'contractApp/Contract_management.html', context)




def Contract_Management_pro(request):
    company_details_record = request.user.company_details

    my_contracts = MainContract.objects.filter(company_details=company_details_record)
    data = []
    for main_contract in my_contracts:
        estimation_assemblies = Estimation_Assemblies_Table.objects.filter(
            id__in=MainContractDetail.objects.filter(main_contract=main_contract).values_list('assembly_row_id', flat=True)
        )
        level1_assemblies = Assemblies_Code_L1_Table.objects.filter(
            id__in=estimation_assemblies.values_list('Assemblies_Code_L1_id', flat=True)
        )
        level1_data = {
            'contract': main_contract,
            'level1': []
        }
        for level1 in level1_assemblies:
            level2_assemblies = Assemblies_Code_L2_Table.objects.filter(Assemblies_Code_L1=level1)
            level2_list = []  # List to hold level2 data for the current level1
            for level2 in level2_assemblies:
                level3_assemblies = Assemblies_Code_L3_Table.objects.filter(Assemblies_Code_L2=level2)
                level2_list.append({
                    'level2': level2,
                    'level3': [
                        {
                            'assembly': level3,
                            'assemblies': Estimation_Assemblies_Table.objects.filter(Assemblies_Code_L3=level3),
                            
                        }
                        for level3 in level3_assemblies
                    ]
                })
            level1_data['level1'].append({
                'level1': level1,
                'level2': level2_list
            })
        data.append(level1_data)
    # print(data)
    for dat in data:
        print(dat)
    context = {
        'data': data
    }
    return render(request, 'contractApp/Contract_Management_pro.html', context)



def Contract_Management_main(request):
    company_details_record = request.user.company_details

    # my_contracts = MainContract.objects.filter(company_details=company_details_record)
    my_contracts = MainContract.objects.filter(company_details=company_details_record).order_by('-id').prefetch_related(
        'details__assembly_row__Assemblies_Code_L1',
        'details__assembly_row__Assemblies_Code_L2',
        'details__assembly_row__Assemblies_Code_L3'
    )
    context = {
        'my_contracts': my_contracts
    }
    return render(request, 'contractApp/Contract_Management_main.html', context)



def contract_assembly_resource_details_management(request):
    company_details_record = request.user.company_details

    # my_contracts = MainContract.objects.filter(company_details=company_details_record)
    my_contracts = MainContract.objects.filter(company_details=company_details_record).order_by('-id').prefetch_related(
        'details__assembly_row__Assemblies_Code_L1',
        'details__assembly_row__Assemblies_Code_L2',
        'details__assembly_row__Assemblies_Code_L3'
    )
    filter_resoures_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=company_details_record)
    filter_assemblies_level_1 = Assemblies_Code_L1_Table.objects.filter(Company_Details=company_details_record)
    context = {
        'my_contracts': my_contracts,
        'filter_resoures_level_1':filter_resoures_level_1,
        'filter_assemblies_level_1':filter_assemblies_level_1
    }
    return render(request, 'contractApp/contract_assembly_resource_details_management.html', context)


@login_required
def create_subcontract(request):
    company_details_record = request.user.company_details
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
            'Assemblies_Code_L1': assembly.Assemblies_Code_L1.Assemblies_Code_L1,
            'Assemblies_Code_L2': assembly.Assemblies_Code_L2.Assemblies_Code_L2,
            'Assemblies_Code_L3': assembly.Assemblies_Code_L3.Assemblies_Code_L3,
            
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
        print('subcontract')
        print(request.POST)
        subcontract_name = request.POST.get('subcontract_name')
        comb_assem_code = request.POST.get('Comb_Assem_Code')
        hiddencontractInputId = request.POST.get('hiddencontractInputId')
        hiddenassemblyInputId = request.POST.get('hiddenassemblyInputId')
        item_description = request.POST.get('Item_Description')

        totalTotalPrice = request.POST.get('totalTotalPrice')
        rows = request.POST.getlist('rows[]')

        print("hiddencontractInputId, hiddenassemblyInputId, totalTotalPrice, subcontract_name")
        print(hiddencontractInputId, hiddenassemblyInputId, totalTotalPrice, subcontract_name)


        print(rows)
        print(type(rows))

        if not rows:
            return JsonResponse({'status': 'error', 'message': 'No rows provided'}, status=400)

        company_details_record = request.user.company_details

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


            # if len(data) >= 12:  # Ensure there are enough elements in the data list
                # try:
            get_subcontract_detail_row = Estimation_Assemblies_Table.objects.filter(id=data[6]).last()
            print(get_subcontract_detail_row)
            var_subcontract = SubContractDetail(
                sub_contract=sub_contract,
                comb_assem_code=comb_assem_code,
                assembly_value = get_subcontract_detail_row,
                item_description=data[5],
                unit=data[0],
                unit_cost=clean_decimal(data[1]),
                subcontract_quantity=clean_decimal(data[2]),
                subcontract_total_price=clean_decimal(data[3]),
                
            )
            var_subcontract.save()

                # except (IndexError, InvalidOperation) as e:
                #     print(f"Error processing row {row}: {e}")
                #     return JsonResponse({'status': 'error', 'message': f"Error processing row {row}: {e}"}, status=400)
        messages.success(request, "Sub-Contract saved successfully.")
        # return redirect('subcontract_list')
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)



@login_required
def subcontract_list(request):
    company_details_record = request.user.company_details
    contracts = SubContractTable.objects.filter(company_details=company_details_record).order_by('-id')
    
    return render(request, 'contractApp/subcontract_list.html', {'contracts': contracts})



def SubContract_Management(request):
    company_details_record = request.user.company_details
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

                'level3': [
                    {
                        'assembly': level3,
                        'assemblies': Estimation_Assemblies_Table.objects.filter(Assemblies_Code_L3=level3),
                        'sub_contracts': SubContractTable.objects.filter(
                            details__assembly_value__Assemblies_Code_L3=level3
                        ).distinct()
                    }
                    for level3 in level3_assemblies
                ]
            })
        data.append(level1_data)

    context = {
        'data': data
    }
    return render(request, 'contractApp/SubContract_management.html', context)


    
def SubContract_Management_main(request):
    company_details_record = request.user.company_details

    my_contracts = SubContractTable.objects.filter(company_details=company_details_record).order_by('-id').prefetch_related(
        'details__assembly_value__Assemblies_Code_L1',
        'details__assembly_value__Assemblies_Code_L2',
        'details__assembly_value__Assemblies_Code_L3'
    )
    context = {
        'my_contracts': my_contracts
    }
    return render(request, 'contractApp/SubContract_Management_main.html', context)





@login_required
@csrf_exempt
def subcontract_create_invoice(request):
    if request.method == 'POST':
        invoice_qty = []
        contract_details_id = []
        
        for key in request.POST:
            if key.startswith('invoice_qty_'):
                invoice_qty.append(request.POST[key])
            if key.startswith('contract_details_id_'):
                contract_details_id.append(request.POST[key])


        contract_id= request.POST.get('contract_id')
        try:
            get_contract = SubContractTable.objects.get(id=contract_id)
        except Exception as exc:
            print(exc)
            messages.error(request, f"Error : {exc}")
            return redirect('view_contract', contract_id)


        var_MainContractInvoice = SubContractInvoiceTable(
            invoice_contract_row = get_contract
        )
        var_MainContractInvoice.save()

        
        # Debugging step: Print the extracted lists
        print("Invoice Quantities:", invoice_qty)
        print("Contract Details IDs:", contract_details_id)

        # Process each contract detail
        for cd_id, inv_qty in zip(contract_details_id, invoice_qty):
            print('cd_id, inv_qty')
            print(cd_id, inv_qty)

            contract_details_id = cd_id
            invoice_quantity = inv_qty

            print("contract_details_id, invoice_quantity")
            print(contract_details_id, invoice_quantity)

        
            try:
                get_contract_details = SubContractDetail.objects.get(id=contract_details_id)
            except Exception as exc:
                print(exc)
                messages.error(request, f"Error : {exc}")
                return redirect('view_contract', contract_id)

            get_remain_invoice = get_contract_details.calculate_remaining_quantity()
            if int(get_remain_invoice) < int(invoice_quantity):
                messages.error(request, f"Error : Your remain invoice quantity is {get_remain_invoice}, you trying to add {invoice_quantity}")
                return redirect('view_contract', contract_id)
            
            

            var_MainContractInvoice_details = SubContractInvoiceDetailsTable(
                sub_contract_invoice = var_MainContractInvoice,
                sub_contract_assembly = get_contract_details,
                Invoice_Quantity = invoice_quantity,
                Invoice_Revenue = float(get_contract_details.unit_cost)*float(invoice_quantity)
            )
            var_MainContractInvoice_details.save()
        
        # return redirect('success_url')  # Redirect to a success page
        messages.success(request, f"Invoice Quantity Added!")
        return redirect('view_subcontract', contract_id)



@login_required
def view_subcontract(request, subcontract_id):
    # Fetch the contract using the contract ID, or return a 404 if not found
    contract = get_object_or_404(SubContractTable, id=subcontract_id)

    # Fetch the related MainContractDetail records
    contract_details = SubContractDetail.objects.filter(sub_contract=contract)


    filter_main_contract_invoice = SubContractInvoiceTable.objects.filter(
        invoice_contract_row=contract
    )
    context = {
        'contract': contract,
        'contract_details': contract_details,
        'filter_main_contract_invoice':filter_main_contract_invoice
    }
    return render(request, 'contractApp/view_subcontract.html', context)


@login_required
def delete_subcontract(request, subcontract_id):
    # Get the contract, or return a 404 if not found
    contract = get_object_or_404(MainContract, id=contract_id)

    # Check if the user is authorized to delete this contract (optional)
    if contract.company_details.User != request.user:
        return JsonResponse({'status': 'error', 'message': 'You do not have permission to delete this contract.'}, status=403)

    # Delete the contract
    contract.delete()

    # Redirect to contract list or return success message
    return JsonResponse({'status': 'success'})

