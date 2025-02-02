from django.db import models
from companyApp.models import CompanyDetailsTable



class ExpenseTable(models.Model):
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    comb_assem_code = models.CharField(max_length=255)
    contract_value = models.ForeignKey('contractApp.MainContract', on_delete=models.CASCADE)
    assembly_value = models.ForeignKey('assembliesApp.Estimation_Assemblies_Table', on_delete=models.CASCADE)
    resource_value = models.ForeignKey('companyApp.CompanyResourcesTable', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    Calculate_Manual_Unit_Cost = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Expense: {self.comb_assem_code} - {self.total_cost}"
