from django.db import models
from authenticationApp.models import User
import uuid
from ckeditor.fields import RichTextField
# Create your models here.


    
class CompanyDetailsTable(models.Model):
    class Meta:
        verbose_name_plural = "Company Table"
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Subscription_Option = (
        ('Starter', 'Starter'),
        ('Company', 'Company'),
        ('Enterprise', 'Enterprise'),
    )
    Subscription = models.CharField(max_length=255, choices=Subscription_Option, default='Starter')
    Company_Id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    Company_Legal_Name = models.CharField(max_length=255)
    Company_Type_Option = (
        ('Owner', 'Owner'),
        ('Construction Management', 'Construction Management'),
        ('Main Contractor', 'Main Contractor'),
        ('Subcontractor', 'Subcontractor'),
    )
    Company_Type = models.CharField(max_length=255, choices=Company_Type_Option, default='Owner')
    Email = models.CharField(max_length=255, null=True, blank=True)
    Telephone = models.CharField(max_length=255, null=True, blank=True)
    Country = models.CharField(max_length=255, null=True, blank=True)
    Address = models.CharField(max_length=255, null=True, blank=True)
    Company_Website = models.CharField(max_length=255, null=True, blank=True)
    Tax_Identification_Number = models.CharField(max_length=255, null=True, blank=True)
    Primary_Contact_Person = models.CharField(max_length=255, null=True, blank=True)
    Company_Logo = models.ImageField(upload_to='Company_Logo/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





class ProjectTable(models.Model):
    class Meta:
        verbose_name_plural = "Project Table"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Project_Id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    Project_Name = models.CharField(max_length=255)
    Project_Start_Date = models.DateField(null=True)
    Short_Description = RichTextField(null=True, blank=True)
    Default_Workflow = models.CharField(max_length=255, null=True, blank=True)
    Note_book = models.CharField(max_length=255, null=True, blank=True)
    Assigned_User = models.ManyToManyField(User, related_name="project_assigned_user", default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Resource_Code_L1_Table(models.Model):
    class Meta:
        verbose_name = "Resource Code Level 1"
        verbose_name_plural = "Resource Codes Level 1"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L1 = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Resource_Code_L2_Table(models.Model):
    class Meta:
        verbose_name = "Resource Code Level 2"
        verbose_name_plural = "Resource Codes Level 2"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L1 = models.ForeignKey(Resource_Code_L1_Table, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L2 = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Resource_Code_L3_Table(models.Model):
    class Meta:
        verbose_name = "Resource Code Level 3"
        verbose_name_plural = "Resource Codes Level 3"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L1 = models.ForeignKey(Resource_Code_L1_Table, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L2 = models.ForeignKey(Resource_Code_L2_Table, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L3 = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CompanyResourcesTable(models.Model):
    class Meta:
        verbose_name_plural = "Company Resources Table"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Name = models.CharField(max_length=255, null=True, blank=True)
    Resource_Code_L1 = models.ForeignKey(Resource_Code_L1_Table, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L2 = models.ForeignKey(Resource_Code_L2_Table, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L3 = models.ForeignKey(Resource_Code_L3_Table, on_delete=models.CASCADE, null=True, blank=True)
    Unit_of_Measure = models.CharField(max_length=255, null=True, blank=True)
    Budget_Unit_Cost = models.CharField(max_length=255, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)