from django.db import models
from companyApp.models import CompanyDetailsTable, CompanyResourcesTable
import uuid
from django.db.models import Sum
from datetime import datetime
# Create your models here.
class Assemblies_Code_L1_Table(models.Model):
    class Meta:
        verbose_name = "Assemblies Code Level 1"
        verbose_name_plural = "Assemblies Codes Level 1"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Assemblies_Code_L1 = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def filter_assemblies_level_2_list(self):
        return Assemblies_Code_L2_Table.objects.filter(Assemblies_Code_L1=self)


class Assemblies_Code_L2_Table(models.Model):
    class Meta:
        verbose_name = "Assemblies Code Level 2"
        verbose_name_plural = "Assemblies Codes Level 2"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Assemblies_Code_L1 = models.ForeignKey(Assemblies_Code_L1_Table, on_delete=models.CASCADE, null=True, blank=True)
    Assemblies_Code_L2 = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def filter_assemblies_level_3_list(self):
        return Assemblies_Code_L3_Table.objects.filter(Assemblies_Code_L2=self)


class Assemblies_Code_L3_Table(models.Model):
    class Meta:
        verbose_name = "Assemblies Code Level 3"
        verbose_name_plural = "Assemblies Codes Level 3"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Assemblies_Code_L1 = models.ForeignKey(Assemblies_Code_L1_Table, on_delete=models.CASCADE, null=True, blank=True)
    Assemblies_Code_L2 = models.ForeignKey(Assemblies_Code_L2_Table, on_delete=models.CASCADE, null=True, blank=True)
    Assemblies_Code_L3 = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





class Estimation_Assemblies_Table(models.Model):
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Assembly_Code = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    Assembly_Name = models.CharField(max_length=255, null=True, blank=True)
    Assemblies_Code_L1 = models.ForeignKey(Assemblies_Code_L1_Table, on_delete=models.CASCADE, null=True, blank=True)
    Assemblies_Code_L2 = models.ForeignKey(Assemblies_Code_L2_Table, on_delete=models.CASCADE, null=True, blank=True)
    Assemblies_Code_L3 = models.ForeignKey(Assemblies_Code_L3_Table, on_delete=models.CASCADE, null=True, blank=True)
    Unit_of_Measure = models.CharField(max_length=255, null=True, blank=True)
    # Quantity = models.CharField(max_length=255, null=True, blank=True)
    Assembly_Unit_Cost = models.CharField(max_length=255, null=True, blank=True)
    # Total_Cost = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.Assembly_Code

    def get_resource_code_totals(self):
        resource_code_totals = {}

        # Fetch all Resource_Code_L1 entries related to this assembly
        resource_details = Estimation_Assemblies_Resource_Details_Table.objects.filter(
            Estimation_Assemblies=self
        ).values('Resource_record__Resource_Code_L1', 'Resource_record__Resource_Code_L1__Resource_Code_L1')

        # Calculate the total for each Resource_Code_L1
        for resource in resource_details.distinct():
            print(resource)
            resource_code_l1 = resource['Resource_record__Resource_Code_L1']
            resource_code_l1_name = resource['Resource_record__Resource_Code_L1__Resource_Code_L1']
            total_cost = Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Estimation_Assemblies=self,
                Resource_record__Resource_Code_L1=resource_code_l1
            ).aggregate(total=Sum('Unit_Cost'))['total'] or 0

            # Store in dictionary
            resource_code_totals[resource_code_l1_name] = total_cost

        return resource_code_totals

    

        
class Estimation_Assemblies_Resource_Details_Table(models.Model):
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Estimation_Assemblies = models.ForeignKey(Estimation_Assemblies_Table, on_delete=models.CASCADE, null=True, blank=True, related_name="estimation_assemblies_resourcedetailstable")
    Resource_record = models.ForeignKey(CompanyResourcesTable, on_delete=models.CASCADE, max_length=255, null=True, blank=True)
    Resource_Budget_Unit_Cost = models.CharField(max_length=255, null=True, blank=True, default="")
    Quantity = models.CharField(max_length=255, null=True, blank=True, default="")
    Unit_of_Measure = models.CharField(max_length=255, null=True, blank=True)
    Unit_Cost = models.CharField(max_length=255, null=True, blank=True)
    