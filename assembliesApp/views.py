import json
from datetime import datetime

from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from companyApp.models import (
    CompanyDetailsTable,
    CompanyResourcesTable,
    Resource_Code_L1_Table,
    Resource_Code_L2_Table,
    Resource_Code_L3_Table,
)

from .models import (
    Assemblies_Code_L1_Table,
    Assemblies_Code_L2_Table,
    Assemblies_Code_L3_Table,
    CompanyDetailsTable,
    CompanyResourcesTable,
    Estimation_Assemblies_Resource_Details_Table,
    Estimation_Assemblies_Table,
)

# Create your views here.


# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from .models import Assemblies_Code_L1_Table, CompanyDetailsTable, CompanyResourcesTable


# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


@login_required
def estimate_assemblies(request):
    try:
        # Retrieve the latest company details for the user
        company_details_record = request.user.company_details

        if not company_details_record:
            # Handle case where no company details are found
            messages.error(request, "please setup your company first")
            return redirect("company_settings")
            # return render(
            #     request,
            #     "company_settings",
            #     {"message": "No company details found for the user."},
            # )
            # return render(request, "assembliesApp/error.html", {"message": "No company details found for the user."})

        # Filter resources and assemblies related to the company
        filter_resources_query = CompanyResourcesTable.objects.filter(
            Company_Details=company_details_record
        ).select_related("Resource_Code_L3")
        filter_company_Assemblies_Code_L1_query = (
            Assemblies_Code_L1_Table.objects.filter(
                Company_Details=company_details_record
            )
        )

        # Convert the QuerySets to lists of dictionaries
        filter_resources_list = list(
            filter_resources_query.values(
                "id",
                "Unit_of_Measure",
                "Resource_Code_L1__Resource_Code_L1",
                "Resource_Code_L2__Resource_Code_L2",
                "Resource_Code_L3__Resource_Code_L3",
                "Resource_Name",
                "Resource_Title",
                "Budget_Unit_Cost",
            )
        )
        # filter_resources_list = list(filter_resources_query.values())
        filter_company_Assemblies_Code_L1_query_list = list(
            filter_company_Assemblies_Code_L1_query.values()
        )

        # Use the custom JSON encoder to handle datetime objects
        filter_resources_json = json.dumps(filter_resources_list, cls=DateTimeEncoder)
        filter_company_Assemblies_Code_L1_query_json = json.dumps(
            filter_company_Assemblies_Code_L1_query_list, cls=DateTimeEncoder
        )

        context = {
            "filter_resources": filter_resources_query,
            "filter_resources_json": filter_resources_json,
            "filter_company_Assemblies_Code_L1_query": filter_company_Assemblies_Code_L1_query,
            "filter_company_Assemblies_Code_L1_query_json": filter_company_Assemblies_Code_L1_query_json,
        }
        return render(request, "assembliesApp/estimate_assemblies.html", context)

    except Exception as e:
        # Handle unexpected errors
        return render(request, "assembliesApp/error.html", {"message": str(e)})


@login_required
def company_assembly_record(request):
    company_details_record = request.user.company_details
    if request.method == "POST":
        list_resourses_ids_json = request.POST.get("list_resourses_ids")
        try:
            # Parse the JSON data
            list_resourses_ids = json.loads(list_resourses_ids_json)
        except json.JSONDecodeError:
            list_resourses_ids = []
        print(list_resourses_ids)
        Assembly_Title = request.POST.get("Assembly_Title")
        Assembly_Name = request.POST.get("Assembly_Name")
        Assemblies_Code_L1_id = request.POST.get("Assemblies_Code_L1")
        Assemblies_Code_L2_id = request.POST.get("Assemblies_Code_L2")
        Assemblies_Code_L3_id = request.POST.get("Assemblies_Code_L3")
        Unit_of_Measure = request.POST.get("Assembly_Unit_of_Measure_Show")
        Assembly_Quantity_Show = request.POST.get("Assembly_Quantity_Show")
        Assembly_Unit_Cost = request.POST.get("Assembly_Unit_Cost")
        Total_Cost = request.POST.get("Total_Cost")

        print("Unit_of_Measure")
        print(Unit_of_Measure)
        print("Unit_of_Measure")

        var_Estimation_Assemblies = Estimation_Assemblies_Table(
            Company_Details=company_details_record,
            Assembly_Title=Assembly_Title,
            Assembly_Name=Assembly_Name,
            Assemblies_Code_L1=Assemblies_Code_L1_Table.objects.filter(
                id=Assemblies_Code_L1_id
            ).last(),
            Assemblies_Code_L2=Assemblies_Code_L2_Table.objects.filter(
                id=Assemblies_Code_L2_id
            ).last(),
            Assemblies_Code_L3=Assemblies_Code_L3_Table.objects.filter(
                id=Assemblies_Code_L3_id
            ).last(),
            Unit_of_Measure=Unit_of_Measure,
            Assembly_Quantity=Assembly_Quantity_Show,
            Assembly_Unit_Cost=Assembly_Unit_Cost,
        )
        var_Estimation_Assemblies.save()

        for resource_id in list_resourses_ids:
            print(resource_id)
            print("resource_id")
            resource_record_row = CompanyResourcesTable.objects.get(id=resource_id[0])
            var_Estimation_Assemblies_Resource_Details = (
                Estimation_Assemblies_Resource_Details_Table(
                    Company_Details=company_details_record,
                    Estimation_Assemblies=var_Estimation_Assemblies,
                    Resource_record=resource_record_row,
                    Resource_Budget_Unit_Cost=resource_record_row.Budget_Unit_Cost,
                    Resource_Quantity=resource_id[4],
                    Assembly_Quantity=resource_id[5],
                    Quantity=resource_id[1],
                    Unit_of_Measure=resource_id[3],
                    Unit_Cost=float(resource_record_row.Budget_Unit_Cost)
                    * float(resource_id[1]),
                ).save()
            )
        messages.success(request, "Assembly saved successfully!")
        return redirect("estimate_assemblies")


def duplicate_assembly(request, assembly_id):
    # Fetch the existing assembly record
    original_assembly = get_object_or_404(Estimation_Assemblies_Table, id=assembly_id)

    # Create a new assembly record with "Duplicate" appended to the name
    new_assembly = Estimation_Assemblies_Table(
        Company_Details=original_assembly.Company_Details,
        Assembly_Name=f"{original_assembly.Assembly_Name} - Duplicate",
        Assemblies_Code_L1=original_assembly.Assemblies_Code_L1,
        Assemblies_Code_L2=original_assembly.Assemblies_Code_L2,
        Assemblies_Code_L3=original_assembly.Assemblies_Code_L3,
        Unit_of_Measure=original_assembly.Unit_of_Measure,
        Assembly_Unit_Cost=original_assembly.Assembly_Unit_Cost,
    )
    new_assembly.save()

    # Fetch and duplicate the associated resource details
    original_resources = Estimation_Assemblies_Resource_Details_Table.objects.filter(
        Estimation_Assemblies=original_assembly
    )
    for resource in original_resources:
        new_resource = Estimation_Assemblies_Resource_Details_Table(
            Company_Details=resource.Company_Details,
            Estimation_Assemblies=new_assembly,
            Resource_record=resource.Resource_record,
            Resource_Budget_Unit_Cost=resource.Resource_Budget_Unit_Cost,
            Quantity=resource.Quantity,
            Unit_of_Measure=resource.Unit_of_Measure,
            Unit_Cost=resource.Unit_Cost,
        )
        new_resource.save()

    # Notify the user and redirect
    messages.success(request, "Assembly duplicated successfully!")
    return redirect("assemblies_list")


@login_required
def save_edit_company_assembly_record(request):
    get_assembly_record_id = request.POST.get("get_assembly_record_id")
    company_details_record = request.user.company_details
    assembly = get_object_or_404(
        Estimation_Assemblies_Table,
        id=get_assembly_record_id,
        Company_Details=company_details_record,
    )

    if request.method == "POST":
        # Parse the JSON data for resources
        list_resourses_ids_json = request.POST.get("list_resourses_ids")
        try:
            list_resourses_ids = json.loads(list_resourses_ids_json)
        except json.JSONDecodeError:
            list_resourses_ids = []

        # e=request.POST.get('Assembly_Name')
        # eq=request.POST.get('Assemblies_Code_L1')
        # eqq=request.POST.get('Assemblies_Code_L2')
        # eee=request.POST.get('Assemblies_Code_L3')
        # sse=request.POST.get('Unit_of_Measure')
        # qwwe=request.POST.get('Assembly_Unit_Cost')

        # Update the assembly record
        assembly.Assembly_Name = request.POST.get("Assembly_Name")
        assembly.Assembly_Title = request.POST.get("Assembly_Title")
        assembly.Assemblies_Code_L1 = Assemblies_Code_L1_Table.objects.filter(
            id=request.POST.get("Assemblies_Code_L1")
        ).last()
        assembly.Assemblies_Code_L2 = Assemblies_Code_L2_Table.objects.filter(
            id=request.POST.get("Assemblies_Code_L2")
        ).last()
        assembly.Assemblies_Code_L3 = Assemblies_Code_L3_Table.objects.filter(
            id=request.POST.get("Assemblies_Code_L3")
        ).last()
        assembly.Unit_of_Measure = request.POST.get("Assembly_Unit_of_Measure_Show")
        assembly.Assembly_Unit_Cost = request.POST.get("Assembly_Unit_Cost")
        assembly.save()

        # Delete existing resource details for this assembly
        # Estimation_Assemblies_Resource_Details_Table.objects.filter(Estimation_Assemblies=assembly).delete()

        # Add new resource details
        for resource_id in list_resourses_ids:
            if resource_id[4] == "existing":
                # exist_row = Estimation_Assemblies_Resource_Details_Table.objects.get(id=resource_id[3])
                # exist_row.Quantity=resource_id[1]
                # exist_row.Unit_of_Measure=resource_id[2]
                # exist_row.Unit_Cost=float(resource_record_row.Budget_Unit_Cost) * float(resource_id[1])
                # exist_row.save()
                pass

            if resource_id[4] == "new":
                resource_record_row = CompanyResourcesTable.objects.get(
                    id=resource_id[0]
                )
                Estimation_Assemblies_Resource_Details_Table.objects.create(
                    Company_Details=company_details_record,
                    Estimation_Assemblies=assembly,
                    Resource_record=resource_record_row,
                    Resource_Budget_Unit_Cost=resource_record_row.Budget_Unit_Cost,
                    Resource_Quantity=resource_id[4],
                    Assembly_Quantity=resource_id[5],
                    Quantity=resource_id[1],
                    Unit_of_Measure=resource_id[3],
                    Unit_Cost=float(resource_record_row.Budget_Unit_Cost)
                    * float(resource_id[1]),
                )

        messages.success(request, "Assembly updated successfully!")
        # return redirect('estimate_assemblies')
        return redirect("assemblies_list")

    return render(
        request,
        "assembliesApp/edit_estimate_assemblies.html",
        {
            "assembly": assembly,
            "filter_company_Assemblies_Code_L1_query": Assemblies_Code_L1_Table.objects.filter(
                Company_Details=company_details_record
            ),
            "filter_Estimation_Assemblies_Resource_Details": Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Estimation_Assemblies=assembly
            ),
        },
    )


@login_required
def assemblies_list(request):
    company_details_record = request.user.company_details
    filter_Estimation_Assemblies = Estimation_Assemblies_Table.objects.filter(
        Company_Details=company_details_record
    )
    context = {"filter_Estimation_Assemblies": filter_Estimation_Assemblies}
    return render(request, "assembliesApp/assemblies_list.html", context)


@login_required
def edit_assembly(request, pk):
    try:
        # Retrieve the latest company details for the user
        company_details_record = request.user.company_details

        if not company_details_record:
            # Handle case where no company details are found
            return render(
                request,
                "assembliesApp/error.html",
                {"message": "No company details found for the user."},
            )

        get_assembly_record = Estimation_Assemblies_Table.objects.filter(id=pk).last()
        filter_Estimation_Assemblies_Resource_Details = (
            Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Estimation_Assemblies=get_assembly_record
            )
        )

        # Filter resources and assemblies related to the company
        filter_resources_query = CompanyResourcesTable.objects.filter(
            Company_Details=company_details_record
        ).select_related("Resource_Code_L3")
        filter_company_Assemblies_Code_L1_query = (
            Assemblies_Code_L1_Table.objects.filter(
                Company_Details=company_details_record
            )
        )

        # Convert the QuerySets to lists of dictionaries
        filter_resources_list = list(
            filter_resources_query.values(
                "id",
                "Unit_of_Measure",
                "Resource_Code_L1__Resource_Code_L1",
                "Resource_Code_L2__Resource_Code_L2",
                "Resource_Code_L3__Resource_Code_L3",
                "Resource_Name",
                "Resource_Title",
                "Budget_Unit_Cost",
            )
        )
        # filter_resources_list = list(filter_resources_query.values())
        filter_company_Assemblies_Code_L1_query_list = list(
            filter_company_Assemblies_Code_L1_query.values()
        )

        # Use the custom JSON encoder to handle datetime objects
        filter_resources_json = json.dumps(filter_resources_list, cls=DateTimeEncoder)
        filter_company_Assemblies_Code_L1_query_json = json.dumps(
            filter_company_Assemblies_Code_L1_query_list, cls=DateTimeEncoder
        )

        context = {
            "filter_resources": filter_resources_query,
            "filter_resources_json": filter_resources_json,
            "filter_company_Assemblies_Code_L1_query": filter_company_Assemblies_Code_L1_query,
            "filter_company_Assemblies_Code_L1_query_json": filter_company_Assemblies_Code_L1_query_json,
            "get_assembly_record": get_assembly_record,
            "filter_Estimation_Assemblies_Resource_Details": filter_Estimation_Assemblies_Resource_Details,
        }
        return render(request, "assembliesApp/edit_estimate_assemblies.html", context)

    except Exception as e:
        # Handle unexpected errors
        return render(request, "assembliesApp/error.html", {"message": str(e)})


def assemblies_Delete(request, pk):
    try:
        get_assembly = Estimation_Assemblies_Table.objects.get(id=pk).delete()
        messages.success(request, "Assembly Deleted Successfully!")
        return redirect("assemblies_list")
    except Exception as exc:
        messages.success(request, f"{exc}")
        return redirect("assemblies_list")


def delete_resource(request):
    if request.method == "POST":
        print("sohel")
        try:
            data = json.loads(request.body)
            resource_id = data.get("resource_id")
            print("resource_idresource_id")
            print(data)
            print(resource_id)

            Estimation_Assemblies_Resource_Details_Table.objects.get(
                id=resource_id
            ).delete()

            # Delete the resource from the database
            # Example:
            # ResourceModel.objects.filter(id=resource_id).delete()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method"})


@login_required
def Assemblies_Code_L1_module(request):
    company_details_record = request.user.company_details
    if request.method == "POST":
        Assemblies_Code_L1 = request.POST.get("Assemblies_Code_L1")
        var_Assemblies_Code_L1 = Assemblies_Code_L1_Table(
            Company_Details=company_details_record,
            Assemblies_Code_L1=Assemblies_Code_L1,
        ).save()
        messages.success(
            request, f"{Assemblies_Code_L1} - Assemblies Code L1 Created Successfully!"
        )
        return redirect("Assemblies_Code_L1_module")
    filter_company_Assemblies_Code_L1_query = Assemblies_Code_L1_Table.objects.filter(
        Company_Details=company_details_record
    )
    context = {
        "filter_company_Assemblies_Code_L1_query": filter_company_Assemblies_Code_L1_query
    }
    return render(request, "assembliesApp/Assemblies_Code_L1_module.html", context)


@login_required
def Assemblies_Code_L2_module(request):
    company_details_record = request.user.company_details
    if request.method == "POST":
        Assemblies_Code_L2 = request.POST.get("Assemblies_Code_L2")
        Assemblies_Code_L1_id = request.POST.get("Assemblies_Code_L1")

        var_Assemblies_Code_L2 = Assemblies_Code_L2_Table(
            Company_Details=company_details_record,
            Assemblies_Code_L1=Assemblies_Code_L1_Table.objects.filter(
                id=Assemblies_Code_L1_id
            ).last(),
            Assemblies_Code_L2=Assemblies_Code_L2,
        ).save()
        messages.success(
            request, f"{Assemblies_Code_L2} - Assemblies Code L2 Created Successfully!"
        )
        return redirect("Assemblies_Code_L2_module")
    filter_company_Assemblies_Code_L1_query = Assemblies_Code_L1_Table.objects.filter(
        Company_Details=company_details_record
    )
    filter_company_Assemblies_Code_L2_query = Assemblies_Code_L2_Table.objects.filter(
        Company_Details=company_details_record
    )
    context = {
        "filter_company_Assemblies_Code_L2_query": filter_company_Assemblies_Code_L2_query,
        "filter_company_Assemblies_Code_L1_query": filter_company_Assemblies_Code_L1_query,
    }
    return render(request, "assembliesApp/Assemblies_Code_L2_module.html", context)


@login_required
def Assemblies_Code_L3_module(request):
    company_details_record = request.user.company_details
    if request.method == "POST":
        Assemblies_Code_L1_id = request.POST.get("Assemblies_Code_L1")
        Assemblies_Code_L2_id = request.POST.get("Assemblies_Code_L2")
        Assemblies_Code_L3 = request.POST.get("Assemblies_Code_L3")
        var_Assemblies_Code_L3 = Assemblies_Code_L3_Table(
            Company_Details=company_details_record,
            Assemblies_Code_L1=Assemblies_Code_L1_Table.objects.filter(
                id=Assemblies_Code_L1_id
            ).last(),
            Assemblies_Code_L2=Assemblies_Code_L2_Table.objects.filter(
                id=Assemblies_Code_L2_id
            ).last(),
            Assemblies_Code_L3=Assemblies_Code_L3,
        ).save()
        messages.success(
            request, f"{Assemblies_Code_L3} - Assemblies Code L3 Created Successfully!"
        )
        return redirect("Assemblies_Code_L3_module")
    filter_company_Assemblies_Code_L1_query = Assemblies_Code_L1_Table.objects.filter(
        Company_Details=company_details_record
    )
    filter_company_Assemblies_Code_L3_query = Assemblies_Code_L3_Table.objects.filter(
        Company_Details=company_details_record
    )

    context = {
        "filter_company_Assemblies_Code_L1_query": filter_company_Assemblies_Code_L1_query,
        "filter_company_Assemblies_Code_L3_query": filter_company_Assemblies_Code_L3_query,
    }
    return render(request, "assembliesApp/Assemblies_Code_L3_module.html", context)


@login_required
def get_Assemblies_code_l2(request):
    Assemblies_code_l1_id = request.GET.get("Assemblies_code_l1_id")
    Assemblies_code_l2_options = Assemblies_Code_L2_Table.objects.filter(
        Assemblies_Code_L1_id=Assemblies_code_l1_id
    ).values("id", "Assemblies_Code_L2")
    return JsonResponse(list(Assemblies_code_l2_options), safe=False)


@login_required
def get_Assemblies_code_l3(request):
    Assemblies_code_l2_id = request.GET.get("Assemblies_code_l2_id")
    data = []

    if Assemblies_code_l2_id:
        # Fetch Assemblies_Code_L3 records related to the selected Assemblies_Code_L2
        Assemblies_codes_l3 = Assemblies_Code_L3_Table.objects.filter(
            Assemblies_Code_L2_id=Assemblies_code_l2_id
        ).values("id", "Assemblies_Code_L3")

        for Assemblies_code in Assemblies_codes_l3:
            data.append(
                {
                    "id": Assemblies_code["id"],
                    "Assemblies_Code_L3": Assemblies_code["Assemblies_Code_L3"],
                }
            )

    return JsonResponse(data, safe=False)


@login_required
def Assemblies_Desplay(request):
    Assemblies_codes_level_1 = Assemblies_Code_L1_Table.objects.prefetch_related(
        "assemblies_code_l2_table_set__assemblies_code_l3_table_set"
    )
    return render(
        request,
        "assembliesApp/Assemblies_Desplay.html",
        {"Assemblies_codes_level_1": Assemblies_codes_level_1},
    )


def Assemblies_Management(request):
    company_details_record = request.user.company_details
    print("company_details_record")
    print(company_details_record)
    if request.method == "POST":
        if "add_assemblies" in request.POST:
            parent_type = request.POST["parent_type"]
            assemblies_name = request.POST["assemblies_name"]
            if parent_type == "level1":
                Assemblies_Code_L1_Table.objects.create(
                    Company_Details=company_details_record,
                    Assemblies_Code_L1=assemblies_name,
                )
            elif parent_type == "level2":
                Assemblies_Code_L2_Table.objects.create(
                    Company_Details=company_details_record,
                    Assemblies_Code_L1_id=request.POST["parent_id"],
                    Assemblies_Code_L2=assemblies_name,
                )
            elif parent_type == "level3":
                Assemblies_Code_L3_Table.objects.create(
                    Company_Details=company_details_record,
                    Assemblies_Code_L2_id=request.POST["parent_id"],
                    Assemblies_Code_L3=assemblies_name,
                )
        elif "delete_assemblies" in request.POST:
            parent_type = request.POST["parent_type"]
            parent_id = request.POST["parent_id"]
            if parent_type == "level1":
                Assemblies_Code_L1_Table.objects.filter(id=parent_id).delete()
            elif parent_type == "level2":
                Assemblies_Code_L2_Table.objects.filter(id=parent_id).delete()
            elif parent_type == "level3":
                Assemblies_Code_L3_Table.objects.filter(id=parent_id).delete()

        return redirect("Assemblies_Management")

    level1_assemblies = Assemblies_Code_L1_Table.objects.filter(
        Company_Details=company_details_record
    )
    data = []
    for level1 in level1_assemblies:
        level2_assemblies = Assemblies_Code_L2_Table.objects.filter(
            Company_Details=company_details_record, Assemblies_Code_L1=level1
        )
        level1_data = {"level1": level1, "level2": []}
        for level2 in level2_assemblies:
            level3_assemblies = Assemblies_Code_L3_Table.objects.filter(
                Company_Details=company_details_record, Assemblies_Code_L2=level2
            )
            level1_data["level2"].append(
                {
                    "level2": level2,
                    # 'level3': level3_assemblies
                    "level3": [
                        {
                            "assembly": level3,
                            "assemblies": Estimation_Assemblies_Table.objects.filter(
                                Company_Details=company_details_record,
                                Assemblies_Code_L3=level3,
                            ),
                        }
                        for level3 in level3_assemblies
                    ],
                }
            )
        data.append(level1_data)

    context = {"data": data}
    return render(request, "assembliesApp/Assemblies_management.html", context)
