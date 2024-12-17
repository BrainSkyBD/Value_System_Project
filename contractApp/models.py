from django.db import models
from companyApp.models import CompanyDetailsTable
from assembliesApp.models import Estimation_Assemblies_Table

class MainContract(models.Model):
    company_details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Company Details")
    contract_name = models.CharField(max_length=255, verbose_name="Contract Name")
    contract_total_budget_costs = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Budget Cost", null=True, blank=True, default=0)
    contract_total_markup_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Budget Cost", null=True, blank=True, default=0)
    contract_total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Budget Cost", null=True, blank=True, default=0)
    contract_total_target_profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Budget Cost", null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.contract_name} - {self.company_details}"

class MainContractDetail(models.Model):
    main_contract = models.ForeignKey(MainContract, on_delete=models.CASCADE, related_name="details")
    comb_assem_code = models.CharField(max_length=50, verbose_name="Combination Assembly Code")
    assembly_name = models.CharField(max_length=100, verbose_name="Assembly Name")
    assembly_row = models.ForeignKey(Estimation_Assemblies_Table, on_delete=models.CASCADE, default=None, blank=True, null=True)
    item_description = models.TextField(verbose_name="Item Description")
    unit = models.CharField(max_length=50, verbose_name="Unit")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Cost")
    budget_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Budget Quantity")
    budget_costs = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Budget Costs")
    markup = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Markup (%)")
    markup_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Markup Amount")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    target_profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Target Profit")

    def __str__(self):
        return f"Detail for {self.main_contract.contract_name} - Unit: {self.unit}"





class SubContractTable(models.Model):
    company_details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Company Details")
    contract_value = models.ForeignKey('contractApp.MainContract', on_delete=models.CASCADE, default=None)
    subcontract_name = models.CharField(max_length=255, verbose_name="Contract Name")
    contract_total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Budget Cost", null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.subcontract_name} - {self.company_details}"

    def filter_sub_contract_details(self):
        return SubContractDetail.objects.filter(sub_contract=self)


class SubContractDetail(models.Model):
    sub_contract = models.ForeignKey(SubContractTable, on_delete=models.CASCADE, related_name="details")
    comb_assem_code = models.CharField(max_length=50, verbose_name="Combination Assembly Code")
    assembly_value = models.ForeignKey('assembliesApp.Estimation_Assemblies_Table', on_delete=models.CASCADE)
    item_description = models.TextField(verbose_name="Item Description")
    unit = models.CharField(max_length=50, verbose_name="Unit")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Cost")
    subcontract_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Budget Quantity")
    subcontract_total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")

    def __str__(self):
        return f"Detail for {self.main_contract.contract_name} - Unit: {self.unit}"
