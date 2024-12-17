from django.contrib import admin
from .models import CompanyDetailsTable, ProjectTable, CompanyResourcesTable, Resource_Code_L1_Table, Resource_Code_L2_Table, Resource_Code_L3_Table


@admin.register(CompanyDetailsTable)
class CompanyDetailsTableAdmin(admin.ModelAdmin):
    list_display = ('User', 'Company_Legal_Name', 'Subscription', 'Company_Type', 'Email', 'Telephone', 'Country', 'created_at', 'updated_at')
    search_fields = ('Company_Legal_Name', 'Email', 'Telephone', 'Country', 'Subscription')
    list_filter = ('Subscription', 'Company_Type', 'Country', 'created_at')
    readonly_fields = ('Company_Id', 'created_at', 'updated_at')


@admin.register(ProjectTable)
class ProjectTableAdmin(admin.ModelAdmin):
    list_display = ('Company_Details', 'Project_Name', 'Project_Start_Date', 'Default_Workflow', 'created_at', 'updated_at')
    search_fields = ('Project_Name', 'Default_Workflow')
    list_filter = ('Project_Start_Date', 'Company_Details')
    readonly_fields = ('Project_Id', 'created_at', 'updated_at')


@admin.register(CompanyResourcesTable)
class CompanyResourcesTableAdmin(admin.ModelAdmin):
    list_display = ('Resource_Name', 'Resource_Code_L1', 'Resource_Code_L2', 'Resource_Code_L3', 'created_at', 'updated_at')
    search_fields = ('Resource_Name', 'Resource_Code_L1')
    # list_filter = ('created_at')
    readonly_fields = ('created_at', 'updated_at')




@admin.register(Resource_Code_L1_Table)
class ResourceCodeL1Admin(admin.ModelAdmin):
    list_display = ('Company_Details', 'Resource_Code_L1', 'created_at', 'updated_at')
    search_fields = ('Resource_Code_L1',)
    list_filter = ('Company_Details', 'created_at')
    ordering = ('-created_at',)


@admin.register(Resource_Code_L2_Table)
class ResourceCodeL2Admin(admin.ModelAdmin):
    list_display = ('Company_Details', 'Resource_Code_L1', 'Resource_Code_L2', 'created_at', 'updated_at')
    search_fields = ('Resource_Code_L2',)
    list_filter = ('Company_Details', 'Resource_Code_L1', 'created_at')
    ordering = ('-created_at',)


@admin.register(Resource_Code_L3_Table)
class ResourceCodeL3Admin(admin.ModelAdmin):
    list_display = ('Company_Details', 'Resource_Code_L1', 'Resource_Code_L2', 'Resource_Code_L3', 'created_at', 'updated_at')
    search_fields = ('Resource_Code_L3',)
    list_filter = ('Company_Details', 'Resource_Code_L1', 'Resource_Code_L2', 'created_at')
    ordering = ('-created_at',)
