from django.shortcuts import render
from companyApp.models import Resource_Code_L3_Table, CompanyDetailsTable, CompanyResourcesTable
# Create your views here.
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from assembliesApp.models import (
    Estimation_Assemblies_Table, 
    Estimation_Assemblies_Resource_Details_Table
)
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from assembliesApp.models import (
    Estimation_Assemblies_Table, 
    Estimation_Assemblies_Resource_Details_Table
)
from django.http import JsonResponse

from contractApp.models import MainContract, MainContractDetail



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ExpenseTable
import json

from django.shortcuts import render, get_object_or_404, redirect
from companyApp.models import Resource_Code_L3_Table, CompanyDetailsTable, CompanyResourcesTable, Resource_Code_L2_Table, Resource_Code_L1_Table


# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)



# @login_required
# def calculate_expenses(request):
#     company_details_record = request.user.company_details
#     filter_users_Resource_Code_L3 = Resource_Code_L3_Table.objects.filter(Company_Details=company_details_record)

#     # Filter resources 
#     filter_resources_query = CompanyResourcesTable.objects.filter(Company_Details=company_details_record).select_related('Resource_Code_L3')
#     filter_resources_list = list(filter_resources_query.values('id', 'Unit_of_Measure', 'Resource_Code_L1__Resource_Code_L1', 'Resource_Code_L2__Resource_Code_L2', 'Resource_Code_L3__Resource_Code_L3', 'Resource_Name', 'Budget_Unit_Cost'))
#     filter_resources_json = json.dumps(filter_resources_list, cls=DateTimeEncoder)

    
#     context = {'company_details_record':company_details_record, 'filter_resources_json':filter_resources_json}
#     return render(request, "expenseApp/calculate_expenses.html", context)




class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


@login_required
def calculate_expenses(request):
    company_details_record = request.user.company_details

    
    # Filter main contract 
    filter_MainContract_query = MainContract.objects.filter(company_details=company_details_record)
    filter_MainContract_list = list(filter_MainContract_query.values('id', 'contract_name'))
    filter_MainContract_json = json.dumps(filter_MainContract_list, cls=DateTimeEncoder)

    # Filter resources 
    filter_resources_query = CompanyResourcesTable.objects.filter(Company_Details=company_details_record).select_related('Resource_Code_L3')
    filter_resources_list = list(filter_resources_query.values('id', 'Unit_of_Measure', 'Resource_Code_L1__Resource_Code_L1', 'Resource_Code_L2__Resource_Code_L2', 'Resource_Code_L3__Resource_Code_L3', 'Resource_Name', 'Budget_Unit_Cost'))
    filter_resources_json = json.dumps(filter_resources_list, cls=DateTimeEncoder)

    context = {'company_details_record': company_details_record, 'filter_resources_json': filter_resources_json, 'filter_MainContract_json':filter_MainContract_json}
    return render(request, "expenseApp/calculate_expenses.html", context)


@login_required
def fetch_assemblies_by_contract(request, contract_id):
    print(f'Getting assemblies for Contract ID: {contract_id}')
    company_details_record = request.user.company_details

    if not company_details_record:
        return JsonResponse({'error': 'Company details not found'}, status=404)

    get_contract = MainContract.objects.get(id=contract_id)

    get_contract_assemblies = MainContractDetail.objects.filter(main_contract=get_contract).select_related('assembly_row').values(
        'assembly_row__id',
        'assembly_row__Assembly_Title',
        'assembly_row__Assembly_Name',
        'assembly_row__Unit_of_Measure',
        'assembly_row__Assembly_Unit_Cost',
        'assembly_row__Assembly_Quantity',
        'budget_quantity'
    )

    # Filter assemblies containing the selected resource
    # assemblies_with_resource = Estimation_Assemblies_Resource_Details_Table.objects.filter(
    #     Company_Details=company_details_record,
    #     Resource_record_id=contract_id  # Ensure this filters properly
    # ).select_related('Estimation_Assemblies').values(
    #     'Estimation_Assemblies__id',
    #     'Estimation_Assemblies__Assembly_Name',
    #     'Estimation_Assemblies__Unit_of_Measure',
    #     'Estimation_Assemblies__Assembly_Unit_Cost'
    # )

    # print(assemblies_with_resource)

    assemblies_list = []
    for assembly in get_contract_assemblies:
        # Verify that the fetched assembly belongs to the selected resource
        totals = Estimation_Assemblies_Resource_Details_Table.objects.filter(
            Estimation_Assemblies_id=assembly['assembly_row__id']
        ).values_list('Resource_record__Resource_Code_L3__Resource_Code_L3', 'Resource_Budget_Unit_Cost')

        resource_code_totals = {resource_code: budget_unit_cost for resource_code, budget_unit_cost in totals}

        assemblies_list.append({
            'id': assembly['assembly_row__id'],
            'assembly_title': assembly['assembly_row__Assembly_Title'] or 'Untitle Assembly',
            'assembly_name': assembly['assembly_row__Assembly_Name'] or 'Unnamed Assembly',
            'unit_of_measure': assembly['assembly_row__Unit_of_Measure'] or 'N/A',
            'assembly_unit_cost': assembly['assembly_row__Assembly_Unit_Cost'] or 0,
            'resource_code_totals': resource_code_totals,
            'Assembly_Quantity' : assembly['assembly_row__Assembly_Quantity'] or 0,
            'contract_Assembly_budget_Quantity' : assembly['budget_quantity'] or 0
        })
    
    print(assemblies_list)

    return JsonResponse(assemblies_list, safe=False)





@login_required
def fetch_resorce_by_assemblies(request, assembly_id):
    print(f'Getting resoures for assembly ID: {assembly_id}')
    company_details_record = request.user.company_details

    if not company_details_record:
        return JsonResponse({'error': 'Company details not found'}, status=404)

    get_assembly = Estimation_Assemblies_Table.objects.get(id=assembly_id)

    get_assembly_resources = Estimation_Assemblies_Resource_Details_Table.objects.filter(Estimation_Assemblies=get_assembly).select_related('Resource_record').values(
        'Resource_record__id',
        'Resource_record__Resource_Title',
        'Resource_record__Resource_Name',
        'Resource_record__Resource_Code_L3__Resource_Code_L3',
        'Resource_record__Unit_of_Measure',
        'Resource_record__Budget_Unit_Cost'
    )

    resourse_list = []
    for resourse in get_assembly_resources:

        print(resourse)
        

        resourse_list.append({
            'id': resourse['Resource_record__id'],
            'Resource_Title': resourse['Resource_record__Resource_Title'] or 'Unnamed Resource',
            'Resource_Name': resourse['Resource_record__Resource_Name'] or 'Unnamed Resource',
            'Resource_Code_L3': resourse['Resource_record__Resource_Code_L3__Resource_Code_L3'] or 'N/A',
            'Unit_of_Measure': resourse['Resource_record__Unit_of_Measure'] or 'N/A',
            'Budget_Unit_Cost': resourse['Resource_record__Budget_Unit_Cost'] or 0,
            
        })
    
    print(resourse_list)

    return JsonResponse(resourse_list, safe=False)


@csrf_exempt
def save_expense(request):
    print("saving expense ...")
    company_details_record = request.user.company_details
    if request.method == 'POST':
        try:
            # print(request.body)
            # data = json.loads(request.body)
            # print(data)
            # combAssemCode = data['combAssemCode']
            # contractValue= data['contractValue']
            # assemblyValue = data['assemblyValue']
            # resourceValue = data['resourceValue']
            # quantity = data['quantity']
            # unitCost = data['unitCost']
            # totalCost = data['totalCost']
            comb_assem_code = request.POST.get('combAssemCode')
            contract_value = request.POST.get('contractValue')
            assembly_value = request.POST.get('assemblyValue')
            resource_value = request.POST.get('resourceValue')
            quantity = request.POST.get('quantity')
            unit_cost = request.POST.get('unitCost')
            total_cost = request.POST.get('totalCost')

            Calculate_Manual_Unit_Cost_name = request.POST.get('Calculate_Manual_Unit_Cost_name')

            print(Calculate_Manual_Unit_Cost_name)
            print('Calculate_Manual_Unit_Cost')

            # print(comb_assem_code)
            # print(contract_value)
            # print(assembly_value)
            # print(resource_value)
            # print(quantity)
            # print(unit_cost)
            # print(total_cost)

            print('Calculate_Manual_Unit_Cost_name')
            print(Calculate_Manual_Unit_Cost_name)

            if Calculate_Manual_Unit_Cost_name == 'true':
                Calculate_Manual_Unit_Cost_name = True
            else:
                Calculate_Manual_Unit_Cost_name = False

            print(Calculate_Manual_Unit_Cost_name)

            expense = ExpenseTable.objects.create(
                Company_Details=company_details_record,
                comb_assem_code=comb_assem_code,
                contract_value=MainContract.objects.get(id=contract_value),
                assembly_value=Estimation_Assemblies_Table.objects.get(id=assembly_value),
                resource_value=CompanyResourcesTable.objects.get(id=resource_value),
                quantity=quantity,
                unit_cost=unit_cost,
                total_cost=total_cost,
                Calculate_Manual_Unit_Cost = Calculate_Manual_Unit_Cost_name
            )
            return JsonResponse({'message': 'Expense saved successfully', 'id': expense.id}, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



@login_required
# Read/ List Expenses
def expense_list(request):
    company_details_record = request.user.company_details
    expenses = ExpenseTable.objects.filter(Company_Details=company_details_record).order_by('-id')
    return render(request, "expenseApp/expense_list.html", {"expenses": expenses})




# Edit an Expense
@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(ExpenseTable, pk=pk)

    company_details_record = request.user.company_details
    
    # Filter main contract 
    filter_MainContract_query = MainContract.objects.filter(company_details=company_details_record)
    filter_MainContract_list = list(filter_MainContract_query.values('id', 'contract_name'))
    filter_MainContract_json = json.dumps(filter_MainContract_list, cls=DateTimeEncoder)

    # Filter resources 
    filter_resources_query = CompanyResourcesTable.objects.filter(Company_Details=company_details_record).select_related('Resource_Code_L3')
    filter_resources_list = list(filter_resources_query.values('id', 'Unit_of_Measure', 'Resource_Code_L1__Resource_Code_L1', 'Resource_Code_L2__Resource_Code_L2', 'Resource_Code_L3__Resource_Code_L3', 'Resource_Name', 'Budget_Unit_Cost'))
    filter_resources_json = json.dumps(filter_resources_list, cls=DateTimeEncoder)

    context = {'expense':expense, 'company_details_record': company_details_record, 'filter_resources_json': filter_resources_json, 'filter_MainContract_json':filter_MainContract_json}
    return render(request, "expenseApp/edit_expenses.html", context)



@csrf_exempt
def save_expense_edit(request):
    print("saving expense ...")
    company_details_record = request.user.company_details
    if request.method == 'POST':
        try:
            expense_id = request.POST.get('expense_id')
            comb_assem_code = request.POST.get('combAssemCode')
            contract_value = request.POST.get('contractValue')
            assembly_value = request.POST.get('assemblyValue')
            resource_value = request.POST.get('resourceValue')
            quantity = request.POST.get('quantity')
            unit_cost = request.POST.get('unitCost')
            total_cost = request.POST.get('totalCost')

            Calculate_Manual_Unit_Cost_name = request.POST.get('Calculate_Manual_Unit_Cost_name')

            print(Calculate_Manual_Unit_Cost_name)
            print('Calculate_Manual_Unit_Cost')


            print('Calculate_Manual_Unit_Cost_name')
            print(Calculate_Manual_Unit_Cost_name)

            if Calculate_Manual_Unit_Cost_name == 'true':
                Calculate_Manual_Unit_Cost_name = True
            else:
                Calculate_Manual_Unit_Cost_name = False
            
            get_expense = ExpenseTable.objects.get(id=expense_id)
            get_expense.Company_Details=company_details_record
            get_expense.comb_assem_code=comb_assem_code
            get_expense.contract_value=MainContract.objects.get(id=contract_value)
            get_expense.assembly_value=Estimation_Assemblies_Table.objects.get(id=assembly_value)
            get_expense.resource_value=CompanyResourcesTable.objects.get(id=resource_value)
            get_expense.quantity=quantity
            get_expense.unit_cost=unit_cost
            get_expense.total_cost=total_cost
            get_expense.Calculate_Manual_Unit_Cost = Calculate_Manual_Unit_Cost_name
            get_expense.save()

            
            return JsonResponse({'message': 'Expense Updated successfully', 'id': get_expense.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



# Delete an Expense
@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(ExpenseTable, pk=pk)
    if request.method == "POST":
        expense.delete()
        return redirect("expense_list")
    return render(request, "expenseApp/delete_expense.html", {"expense": expense})




@login_required
def expenses_management(request):
    company_details_record = request.user.company_details

    level1_resources = Resource_Code_L1_Table.objects.filter(Company_Details=company_details_record)
    data = []
    for level1 in level1_resources:
        level2_resources = Resource_Code_L2_Table.objects.filter(Resource_Code_L1=level1)
        level1_data = {
            'level1': level1,
            'level2': []
        }
        for level2 in level2_resources:
            level3_resources = Resource_Code_L3_Table.objects.filter(Resource_Code_L2=level2)
            level1_data['level2'].append({
                'level2': level2,
                'level3': [
                    {
                        'resource': level3,
                        'resources': CompanyResourcesTable.objects.filter(Resource_Code_L3=level3)
                    }
                    for level3 in level3_resources
                ]
            })
        data.append(level1_data)

    context = {
        'data': data
    }
    return render(request, 'expenseApp/expenses_management.html', context)
