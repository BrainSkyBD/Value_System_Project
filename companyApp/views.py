from django.shortcuts import render

from .models import CompanyDetailsTable, ProjectTable
# Create your views here.

from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CompanyDetailsTable, CompanyResourcesTable, Resource_Code_L1_Table, Resource_Code_L2_Table, Resource_Code_L3_Table
from authenticationApp.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from assembliesApp.models import Estimation_Assemblies_Resource_Details_Table
@login_required
def company_settings(request):
    # Retrieve the latest company details for the current user
    company_details = request.user.company_details

    if request.method == "POST":
        # Extract POST data
        company_data = {
            'Company_Legal_Name': request.POST.get('Company_Legal_Name'),
            'Company_Type': request.POST.get('Company_Type'),
            'Email': request.POST.get('Email'),
            'Telephone': request.POST.get('Telephone'),
            'Address': request.POST.get('Address'),
            'Company_Website': request.POST.get('Company_Website'),
            'Tax_Identification_Number': request.POST.get('Tax_Identification_Number'),
            'Country': request.POST.get('Country'),
            'Primary_Contact_Person': request.POST.get('Primary_Contact_Person'),
        }

        # Handle file upload for the company logo
        company_logo = request.FILES.get('Company_Logo')
        print('company_logo')
        print(company_logo)

        if company_details:
            # Update existing company details
            for key, value in company_data.items():
                setattr(company_details, key, value)
            
            # Update the company logo if a new one is uploaded
            if company_logo:
                company_details.Company_Logo = company_logo

            company_details.save()
            messages.success(request, "Company details updated successfully.")
        else:
            # Create new company details
            company_details = CompanyDetailsTable(
                User=request.user,
                Company_Legal_Name=company_data['Company_Legal_Name'],
                Company_Type=company_data['Company_Type'],
                Email=company_data['Email'],
                Telephone=company_data['Telephone'],
                Address=company_data['Address'],
                Company_Website=company_data['Company_Website'],
                Tax_Identification_Number=company_data['Tax_Identification_Number'],
                Country=company_data['Country'],
                Primary_Contact_Person=company_data['Primary_Contact_Person'],
                Company_Logo=company_logo
            )
            company_details.save()
            messages.success(request, "Company details saved successfully.")

        return redirect('company_settings')  # Redirect to avoid re-submission on refresh

    # Pass the latest company details to the template
    countries = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", 
        "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", 
        "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", 
        "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", 
        "Congo (Democratic Republic of the)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", 
        "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", 
        "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", 
        "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", 
        "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", 
        "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", 
        "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", 
        "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (formerly Burma)", "Namibia", "Nauru", 
        "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", 
        "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", 
        "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
        "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", 
        "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", 
        "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", 
        "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", 
        "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", 
        "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ]

    context = {'Company_details': company_details, 'countries':countries}
    return render(request, "companyApp/company_settings.html", context)




@login_required
def company_subscription(request):
    return render(request, "companyApp/company_subscription.html")


@login_required
def create_project(request):
    if request.method == 'POST':
        # Get data from the form
        project_name = request.POST.get('project_name')
        project_start_date = request.POST.get('project_start_date')
        short_description = request.POST.get('short_description')
        default_workflow = request.POST.get('default_workflow')
        note_book = request.POST.get('note_book')

        assign_user_lists = request.POST.getlist('assign_user_lists')
        print('assign_user_lists')
        print(assign_user_lists)

        company_details_record = request.user.company_details

        # Create a new ProjectTable instance
        project = ProjectTable(
            Company_Details=company_details_record,
            Project_Name=project_name,
            Project_Start_Date=project_start_date,
            Short_Description=short_description,
            Default_Workflow=default_workflow,
            Note_book=note_book
        )
        project.save()  # Save the instance to the database
        for user in assign_user_lists:
            project.Assigned_User.add(user)
        messages.success(request, "Company details updated successfully.")
        return redirect('list_project')  # Redirect after successful save
    filter_users = User.objects.filter(created_by = request.user)
    context = {'filter_users':filter_users}
    return render(request, "companyApp/create_project.html", context)




@login_required
def list_project(request):
    company_details_record = request.user.company_details
    all_project_filter = ProjectTable.objects.filter(Company_Details=company_details_record)
    # print(all_project_filter)
    context = {'all_project_filter':all_project_filter}
    return render(request, "companyApp/project_list.html", context)



@login_required
def view_project(request, project_id):
    project = get_object_or_404(ProjectTable, id=project_id)
    return render(request, 'companyApp/view_project.html', {'project': project})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(ProjectTable, id=project_id)
    
    if request.method == 'POST':
        project.Project_Name = request.POST.get('project_name')
        project.Project_Start_Date = request.POST.get('project_start_date')
        project.Short_Description = request.POST.get('short_description')
        project.Default_Workflow = request.POST.get('default_workflow')
        project.Note_book = request.POST.get('note_book')
        
        assign_user_lists = request.POST.getlist('assign_user_lists')
        project.Assigned_User.set(assign_user_lists)
        
        project.save()
        return redirect('list_project')
    
    filter_users = User.objects.filter(created_by=request.user)
    context = {
        'project': project,
        'filter_users': filter_users
    }
    return render(request, "companyApp/edit_project.html", context)

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(ProjectTable, id=project_id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully.")
        return redirect('list_project')
    return render(request, 'companyApp/delete_project.html', {'project': project})


    
@login_required
def create_user(request):
    if request.method == 'POST':
        # Get data from the form
        # username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        user_role = request.POST.get('user_role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('create_user')  # Redirect back to the form
        company_details_record = request.user.company_details

        if User.objects.filter(username=email):
            messages.error(request, "Email is already in use!")
            return redirect('create_user')
        # Create a new User instance
        user = User(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,  # Assuming your custom user model has this field
            User_Role=user_role,  # Assuming your custom user model has this field
            created_by = request.user
        )
        user.password = make_password(password)  # Hash the password before saving
        user.company_details = company_details_record
        user.save()

        messages.success(request, "User successfully registered!")
        return redirect('user_list')
    return render(request, "companyApp/create_user.html")
    

@login_required
def user_list(request):
    company_details_record = request.user.company_details
    
    filter_users = User.objects.filter(company_details = company_details_record).exclude()
    context = {'filter_users':filter_users}
    return render(request, "companyApp/user_list.html", context)



@login_required
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'companyApp/view_user.html', {'user': user})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.user_role = request.POST.get('user_role')
        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('user_list')
    return render(request, 'companyApp/edit_user.html', {'user': user})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('user_list')
    return render(request, 'companyApp/delete_user.html', {'user': user})



def Resource_Code_L1_module(request):
    company_details_record = request.user.company_details
    if request.method == "POST":
        Resource_Code_L1 = request.POST.get('Resource_Code_L1')
        var_Resource_Code_L1 = Resource_Code_L1_Table(
            Company_Details = company_details_record,
            Resource_Code_L1 = Resource_Code_L1
        ).save()
        messages.success(request, f"{Resource_Code_L1} - Resource Code L1 Created Successfully!")    
        return redirect('Resource_Code_L1_module')
    filter_company_Resource_Code_L1_query = Resource_Code_L1_Table.objects.filter(Company_Details = company_details_record)
    context = {'filter_company_Resource_Code_L1_query':filter_company_Resource_Code_L1_query}
    return render(request, "companyApp/Resource_Code_L1_module.html", context)



def Resource_Code_L2_module(request):
    company_details_record = request.user.company_details
    if request.method == "POST":
        Resource_Code_L2 = request.POST.get('Resource_Code_L2')
        Resource_Code_L1_id = request.POST.get('Resource_Code_L1')
        
        var_Resource_Code_L2 = Resource_Code_L2_Table(
            Company_Details = company_details_record,
            Resource_Code_L1= Resource_Code_L1_Table.objects.filter(id=Resource_Code_L1_id).last(),
            Resource_Code_L2 = Resource_Code_L2
        ).save()
        messages.success(request, f"{Resource_Code_L2} - Resource Code L2 Created Successfully!")    
        return redirect('Resource_Code_L2_module')
    filter_company_Resource_Code_L1_query = Resource_Code_L1_Table.objects.filter(Company_Details = company_details_record)
    filter_company_Resource_Code_L2_query = Resource_Code_L2_Table.objects.filter(Company_Details = company_details_record)
    context = {'filter_company_Resource_Code_L2_query':filter_company_Resource_Code_L2_query, 'filter_company_Resource_Code_L1_query': filter_company_Resource_Code_L1_query}
    return render(request, "companyApp/Resource_Code_L2_module.html", context)



def Resource_Code_L3_module(request):
    company_details_record = request.user.company_details
    if request.method == "POST":
        Resource_Code_L1_id = request.POST.get('Resource_Code_L1')
        Resource_Code_L2_id = request.POST.get('Resource_Code_L2')
        Resource_Code_L3 = request.POST.get('Resource_Code_L3')
        var_Resource_Code_L3 = Resource_Code_L3_Table(
            Company_Details = company_details_record,
            Resource_Code_L1= Resource_Code_L1_Table.objects.filter(id=Resource_Code_L1_id).last(),
            Resource_Code_L2 = Resource_Code_L2_Table.objects.filter(id=Resource_Code_L2_id).last(),
            Resource_Code_L3 = Resource_Code_L3
        ).save()
        messages.success(request, f"{Resource_Code_L3} - Resource Code L3 Created Successfully!")    
        return redirect('Resource_Code_L3_module')
    filter_company_Resource_Code_L1_query = Resource_Code_L1_Table.objects.filter(Company_Details = company_details_record)
    filter_company_Resource_Code_L3_query = Resource_Code_L3_Table.objects.filter(Company_Details = company_details_record)
    context = {'filter_company_Resource_Code_L1_query':filter_company_Resource_Code_L1_query, 'filter_company_Resource_Code_L3_query':filter_company_Resource_Code_L3_query}
    return render(request, "companyApp/Resource_Code_L3_module.html", context)



def get_resource_code_l2(request):
    resource_code_l1_id = request.GET.get("resource_code_l1_id")
    print(resource_code_l1_id)
    resource_code_l2_options = Resource_Code_L2_Table.objects.filter(
        Resource_Code_L1_id=resource_code_l1_id
    ).values("id", "Resource_Code_L2")
    return JsonResponse(list(resource_code_l2_options), safe=False)



def get_resource_code_l3(request):
    resource_code_l2_id = request.GET.get('resource_code_l2_id')
    data = []

    if resource_code_l2_id:
        # Fetch Resource_Code_L3 records related to the selected Resource_Code_L2
        resource_codes_l3 = Resource_Code_L3_Table.objects.filter(Resource_Code_L2_id=resource_code_l2_id).values('id', 'Resource_Code_L3')

        for resource_code in resource_codes_l3:
            data.append({
                'id': resource_code['id'],
                'Resource_Code_L3': resource_code['Resource_Code_L3'],
            })

    return JsonResponse(data, safe=False)



@login_required
def Create_Resource_Dictionary(request):
    company_details_record = request.user.company_details
    if request.method == 'POST':
        Resource_Title = request.POST.get('Resource_Title')
        Resource_Name = request.POST.get('Resource_Name')
        Resources_Category = request.POST.get('Resources_Category')
        Resource_Code_L1_id = request.POST.get('Resource_Code_L1')
        Resource_Code_L2_id = request.POST.get('Resource_Code_L2')
        Resource_Code_L3_id = request.POST.get('Resource_Code_L3')
        Unit_of_Measure = request.POST.get('Unit_of_Measure')
        Budget_Unit_Cost = request.POST.get('Budget_Unit_Cost')
        Budget_Unit_Cost = request.POST.get('Budget_Unit_Cost')

        
        Company_Resources = CompanyResourcesTable(
            Company_Details=company_details_record,
            Resource_Title=Resource_Title,
            Resource_Name=Resource_Name,
            # Resources_Category=Resources_Category,
            Resource_Code_L1=Resource_Code_L1_Table.objects.filter(id=Resource_Code_L1_id).last(),
            Resource_Code_L2=Resource_Code_L2_Table.objects.filter(id=Resource_Code_L2_id).last(),
            Resource_Code_L3=Resource_Code_L3_Table.objects.filter(id=Resource_Code_L3_id).last(),
            Unit_of_Measure=Unit_of_Measure,  
            Budget_Unit_Cost = Budget_Unit_Cost
        )
        Company_Resources.save()

        messages.success(request, "Resources successfully Created!")
        return redirect('List_Resource_Dictionary')
    filter_company_Resource_Code_L1_query = Resource_Code_L1_Table.objects.filter(Company_Details = company_details_record)
    context = {'filter_company_Resource_Code_L1_query':filter_company_Resource_Code_L1_query}
    return render(request, "companyApp/Create_Resource_Dictionary.html", context)


@login_required
def duplicate_resource(request, resource_id):
    # Fetch the existing resource record
    original_resource = get_object_or_404(CompanyResourcesTable, id=resource_id)

    # Create a new resource record with "Duplicate" appended to the name
    new_resource = CompanyResourcesTable(
        Company_Details=original_resource.Company_Details,
        Resource_Name=f"{original_resource.Resource_Name} - Duplicate",
        Resource_Code_L1=original_resource.Resource_Code_L1,
        Resource_Code_L2=original_resource.Resource_Code_L2,
        Resource_Code_L3=original_resource.Resource_Code_L3,
        Unit_of_Measure=original_resource.Unit_of_Measure,
        Budget_Unit_Cost=original_resource.Budget_Unit_Cost,
    )
    new_resource.save()

    # Notify the user and redirect
    messages.success(request, "Resource duplicated successfully!")
    return redirect('List_Resource_Dictionary')  # Replace with the name of your resource list view



@login_required
def List_Resource_Dictionary(request):
    company_details_record = request.user.company_details
    filter_resoures = CompanyResourcesTable.objects.filter(Company_Details = company_details_record)
    context = {'filter_resoures':filter_resoures}
    return render(request, "companyApp/List_Resource_Dictionary.html", context)



@login_required
def edit_resource(request, pk):
    company_details_record = request.user.company_details
    if request.method == 'POST':
        get_resource_record_id = request.POST.get('get_resource_record_id')
        get_resource_record = CompanyResourcesTable.objects.filter(id=get_resource_record_id).last()

        Resource_Title = request.POST.get('Resource_Title')
        Resource_Name = request.POST.get('Resource_Name')
        Resources_Category = request.POST.get('Resources_Category')
        Resource_Code_L1_id = request.POST.get('Resource_Code_L1')
        Resource_Code_L2_id = request.POST.get('Resource_Code_L2')
        Resource_Code_L3_id = request.POST.get('Resource_Code_L3')
        Unit_of_Measure = request.POST.get('Unit_of_Measure')
        Budget_Unit_Cost = request.POST.get('Budget_Unit_Cost')

        # Retrieve related records
        get_Resource_Code_L1_record = Resource_Code_L1_Table.objects.filter(id=Resource_Code_L1_id).last()
        get_Resource_Code_L2_record = Resource_Code_L2_Table.objects.filter(id=Resource_Code_L2_id).last()
        get_Resource_Code_L3_record = Resource_Code_L3_Table.objects.filter(id=Resource_Code_L3_id).last()

        # Update the resource record
        get_resource_record.Resource_Title = Resource_Title
        get_resource_record.Resource_Name = Resource_Name
        if Resource_Code_L1_id:
            get_resource_record.Resource_Code_L1 = get_Resource_Code_L1_record
        if Resource_Code_L2_id:
            get_resource_record.Resource_Code_L2 = get_Resource_Code_L2_record
        if Resource_Code_L3_id:
            get_resource_record.Resource_Code_L3 = get_Resource_Code_L3_record
        get_resource_record.Unit_of_Measure = Unit_of_Measure
        get_resource_record.Budget_Unit_Cost = Budget_Unit_Cost

        # Save the updated record
        get_resource_record.save()

        filter_Estimation_Assemblies_Resource_Details_under_resource = Estimation_Assemblies_Resource_Details_Table.objects.filter(
            Resource_record = get_resource_record
        )
        for assembly_row in filter_Estimation_Assemblies_Resource_Details_under_resource:
            assembly_row.Resource_Budget_Unit_Cost = Budget_Unit_Cost
            assembly_row.Unit_Cost= float(Budget_Unit_Cost) * float(assembly_row.Quantity)
            assembly_row.save()

        messages.success(request, "Resources successfully Updated!")
        return redirect('List_Resource_Dictionary')

    get_resource_record = CompanyResourcesTable.objects.filter(id=pk).last()
    filter_company_Resource_Code_L1_query = Resource_Code_L1_Table.objects.filter(Company_Details = company_details_record)
    context = {'filter_company_Resource_Code_L1_query':filter_company_Resource_Code_L1_query, 'get_resource_record':get_resource_record}
    return render(request, "companyApp/Edit_Resource_Dictionary.html", context)


def Resource_Desplay(request):
    resource_codes_level_1 = Resource_Code_L1_Table.objects.prefetch_related(
        'resource_code_l2_table_set__resource_code_l3_table_set'
    )
    return render(request, 'companyApp/Resource_Desplay.html', {'resource_codes_level_1': resource_codes_level_1})



def Resource_Delete(request, pk):
    try:
        get_resource = CompanyResourcesTable.objects.get(id=pk).delete()
        messages.success(request, "Resource Deleted Successfully!")
        return redirect('List_Resource_Dictionary')
    except Exception as exc:
        messages.success(request, f"{exc}")
        return redirect('List_Resource_Dictionary')




def Resource_Management(request):
    company_details_record = request.user.company_details
    print('company_details_record')
    print(company_details_record)
    if request.method == "POST":
        if 'add_resource' in request.POST:
            parent_type = request.POST['parent_type']
            resource_name = request.POST['resource_name']
            if parent_type == 'level1':
                Resource_Code_L1_Table.objects.create(
                    Company_Details=company_details_record,
                    Resource_Code_L1=resource_name
                )
            elif parent_type == 'level2':
                Resource_Code_L2_Table.objects.create(
                    Company_Details=company_details_record,
                    Resource_Code_L1_id=request.POST['parent_id'],
                    Resource_Code_L2=resource_name
                )
            elif parent_type == 'level3':
                Resource_Code_L3_Table.objects.create(
                    Company_Details=company_details_record,
                    Resource_Code_L2_id=request.POST['parent_id'],
                    Resource_Code_L3=resource_name
                )
        elif 'delete_resource' in request.POST:
            parent_type = request.POST['parent_type']
            parent_id = request.POST['parent_id']
            if parent_type == 'level1':
                Resource_Code_L1_Table.objects.filter(id=parent_id).delete()
            elif parent_type == 'level2':
                Resource_Code_L2_Table.objects.filter(id=parent_id).delete()
            elif parent_type == 'level3':
                Resource_Code_L3_Table.objects.filter(id=parent_id).delete()

        return redirect('Resource_Management')

    level1_resources = Resource_Code_L1_Table.objects.filter(Company_Details=company_details_record)
    data = []
    for level1 in level1_resources:
        level2_resources = Resource_Code_L2_Table.objects.filter(Company_Details=company_details_record, Resource_Code_L1=level1)
        level1_data = {
            'level1': level1,
            'level2': []
        }
        for level2 in level2_resources:
            level3_resources = Resource_Code_L3_Table.objects.filter(Company_Details=company_details_record, Resource_Code_L2=level2)
            level1_data['level2'].append({
                'level2': level2,
                'level3': [
                    {
                        'resource': level3,
                        'resources': CompanyResourcesTable.objects.filter(Company_Details=company_details_record, Resource_Code_L3=level3)
                    }
                    for level3 in level3_resources
                ]
            })
        data.append(level1_data)

    context = {
        'data': data
    }
    return render(request, 'companyApp/Resource_management.html', context)
