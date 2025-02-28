from django.db import models
from companyApp.models import CompanyDetailsTable, CompanyResourcesTable
from assembliesApp.models import Estimation_Assemblies_Table, Estimation_Assemblies_Resource_Details_Table
from django.db.models import Sum, F
from django.db.models import Sum, FloatField
from django.db.models.functions import Cast


class MainContract(models.Model):
    company_details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Company Details")
    contract_name = models.CharField(max_length=255, verbose_name="Contract Name")
    contract_total_budget_costs = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Budget Cost", null=True, blank=True, default=0)
    contract_total_markup_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Budget Cost", null=True, blank=True, default=0)
    contract_total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Budget Cost", null=True, blank=True, default=0)
    contract_total_target_profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Budget Cost", null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contract_name} - {self.company_details}"

    def main_contract_details_query(self):
        get_details_contract = MainContractDetail.objects.filter(main_contract=self)
        details = MainContractDetail.objects.filter(main_contract=self)
        # for detail in details:
        #     print(f"ID: {detail.id}, comb_assem_code: {detail.comb_assem_code}, assembly_name: {detail.assembly_name}, Assembly Row: {detail.assembly_row}, Assemblies_Code_L1: {detail.assembly_row.Assemblies_Code_L1 if detail.assembly_row else 'No assembly row'}")
        return get_details_contract
    
    def main_contract_details_query_count(self):
        get_details_contract_count = MainContractDetail.objects.filter(main_contract=self).count()
        return get_details_contract_count


    def get_contract_total_budget_quantity(self):
        related_details = MainContractDetail.objects.filter(main_contract=self)
        total = related_details.aggregate(Sum('budget_quantity'))['budget_quantity__sum'] or 0
        return round(total, 2)

    def get_contract_total_unit_cost(self):
        related_details = MainContractDetail.objects.filter(main_contract=self)
        total = related_details.aggregate(Sum('unit_cost'))['unit_cost__sum'] or 0
        return round(total, 2)

    def get_contract_total_contract_quantity(self):
        related_details = MainContractDetail.objects.filter(main_contract=self)
        total = related_details.aggregate(Sum('contract_quantity'))['contract_quantity__sum'] or 0
        return round(total, 2)

    def get_contract_total_unit_price(self):
        related_details = MainContractDetail.objects.filter(main_contract=self)
        total = related_details.aggregate(Sum('unit_price'))['unit_price__sum'] or 0
        return round(total, 2)
        
    def calculate_total_price(self):
        from django.db.models import Sum
        total = self.details.aggregate(Sum('total_price'))['total_price__sum']
        total = round(total, 2)
        return total if total is not None else 0

    def func_mainContract_total_Invoices_total_revenue(self):
        total_revenue = MainContractInvoiceDetailsTable.objects.filter(
            main_contract_invoice__invoice_contract_row=self
        ).aggregate(total_revenue=Sum('Invoice_Revenue'))['total_revenue']
        if total_revenue:
            total_revenue = round(total_revenue,  2)
        return total_revenue or 0
    
    def calculate_total_resource_budget_cost(self):
        total_sum = 0
        for detail in self.details.all():  # `related_name="details"`
            resource_budget_cost = detail.contract_resource_budget_cost_calculation()
            total_sum += resource_budget_cost.get('total_sum_budget_cost_var', 0)
        return round(total_sum, 2)
    
    def calculate_total_actual_cost(self):
        """
        Calculates the total sum of `total_sum_assembly_resource_code_amount_var` 
        for all related MainContractDetail instances.
        """
        total_sum = 0
        for detail in self.details.all():  # Access related MainContractDetail instances
            resource_cost_data = detail.actual_cost_total_resource_code_calculation()
            total_sum += resource_cost_data.get('total_sum_assembly_resource_code_amount_var', 0)
        return round(total_sum, 2)
    
    def calculate_total_subcontract_usage_cost(self):
        """
        Calculates the total sum of `total_sum_calculate_usage_amount` 
        for all related MainContractDetail instances.
        """
        total_usage_cost = 0
        for detail in self.details.all():  # Access related MainContractDetail instances
            resource_usage_data = detail.actual_cost_subcontracts_resource_list()
            total_usage_cost += resource_usage_data.get('total_sum_calculate_usage_amount', 0)
        return round(total_usage_cost, 2)

    def calculate_total_actual_expense_cost(self):
        """
        Calculates the total sum of `var_total_actual_expense_cost` 
        for all related MainContractDetail instances.
        """
        total_expense_cost = 0
        for detail in self.details.all():  # Access related MainContractDetail instances
            resource_usage_data = detail.actual_cost_expense_resource_list()
            total_expense_cost += resource_usage_data.get('var_total_actual_expense_cost', 0)
        return round(total_expense_cost, 2)

    def calculate_total_actual_store_cost(self):
        """
        Calculates the total sum of `total_actual_store_cost_var` 
        for all related MainContractDetail instances.
        """
        total_store_cost = 0
        for detail in self.details.all():  # Access related MainContractDetail instances
            resource_usage_data = detail.actual_cost_store_resource_list()
            total_store_cost += resource_usage_data.get('total_actual_store_cost_var', 0)
        return round(total_store_cost, 2)
    
    def calculate_total_earned_cost_by_resource_list(self):
        total_earned_cost = 0
        for detail in self.details.all():  
            resource_usage_data = detail.earned_cost_by_resource_list()
            total_earned_cost += resource_usage_data.get('total_actual_earned_cost_var', 0)
        return round(total_earned_cost, 2)

    def calculate_total_CPI_by_resource_list(self):
        total_cpi = 0
        for detail in self.details.all():  
            resource_usage_data = detail.calculate_assembly_cpi_value()
            total_cpi += resource_usage_data
        return round(total_cpi, 2)

    def calculate_total_TCPI_by_resource_list(self):
        total_tcpi = 0
        for detail in self.details.all():  
            resource_usage_data = detail.calculate_assembly_tcpi_value()
            total_tcpi += resource_usage_data
        return round(total_tcpi, 2)

    def calculate_total_contract_resource_variance_to_date_calculation(self):
        total_variance_to_date_cost = 0
        for detail in self.details.all():  
            resource_usage_data = detail.contract_resource_variance_to_date_calculation()
            total_variance_to_date_cost += resource_usage_data.get('contract_resource_variance_to_date_value', 0)
        return round(total_variance_to_date_cost, 2)

    def calculate_total_contract_resource_estimate_at_completion_calculation(self):
        total_eac_cost = 0
        for detail in self.details.all():  
            resource_usage_data = detail.contract_resource_estimate_at_completion_calculation()
            total_eac_cost += resource_usage_data.get('sum_total_estimate_at_completion_cost', 0)
        return round(total_eac_cost, 2)
    
    def calculate_total_contract_ETC_remaining_calculation(self):
        total_ETC_cost = 0
        for detail in self.details.all():  
            resource_usage_data = detail.contract_ETC_remaining_calculation()
            total_ETC_cost += resource_usage_data.get('contract_ETC_remaining_value', 0)
        return round(total_ETC_cost, 2)
    
    def calculate_total_contract_VAC_remaining_calculation(self):
        total_VAC_cost = 0
        for detail in self.details.all():  
            resource_usage_data = detail.contract_VAC_remaining_calculation()
            total_VAC_cost += resource_usage_data.get('contract_VAC_remaining_value', 0)
        return round(total_VAC_cost, 2)


    # def contract_assemblies_level_1_values(self):
    #     from assembliesApp.models import Assemblies_Code_L1_Table
    #     filter_assembly_level_1 = Assemblies_Code_L1_Table.objects.filter(Company_Details=self.company_details)
    #     resource_usage = {}
        
    #     for assemblies_level_1_record in filter_assembly_level_1:
    #         Assembly_Level_1_Name = assemblies_level_1_record.Assemblies_Code_L1
    #         Unit = ''
    #         total_unit_cost = 0
    #         Contract_Quantity = 0
    #         Budget_Quantity = 0
    #         Total_Budget_Costs = 0
    #         Markup = ''
    #         Total_Markup_Amount = 0
    #         Unit_Price = 0
    #         Total_Price = 0
    #         Total_Target_Profit = 0

    #         Total_Actual_Resources_Cost = 0
    #         Actual_Sub_Contract_Cost = 0
    #         Actual_Expenses_Cost = 0
    #         Actual_Store_Cost = 0
    #         EARNED_COSTS = 0
    #         VARIANCE_TO_DATE = 0
    #         ETC_REMAINING = 0
    #         Estimate_At_Completion_EAC = 0
    #         VAC_value = 0

    #         filter_contract_details = MainContractDetail.objects.filter(
    #             main_contract = self,
    #             assembly_row__Assemblies_Code_L1 = assemblies_level_1_record
    #         )
    #         print('filter_contract_details')
    #         print(filter_contract_details)
    #         if filter_contract_details:
    #             total_unit_cost = round(filter_contract_details.aggregate(total=Sum('unit_cost'))['total'], 2)
    #             Contract_Quantity = round(filter_contract_details.aggregate(total=Sum('contract_quantity'))['total'], 2)
    #             Budget_Quantity = round(filter_contract_details.aggregate(total=Sum('budget_quantity'))['total'], 2)
    #             Total_Budget_Costs = round(filter_contract_details.aggregate(total=Sum('budget_costs'))['total'], 2)
    #             Total_Markup_Amount = round(filter_contract_details.aggregate(total=Sum('markup_amount'))['total'], 2)
    #             Unit_Price = round(filter_contract_details.aggregate(total=Sum('unit_price'))['total'], 2)
    #             Total_Price = round(filter_contract_details.aggregate(total=Sum('total_price'))['total'], 2)
    #             Total_Target_Profit = round(filter_contract_details.aggregate(total=Sum('target_profit'))['total'], 2)

            
    #         for detail in filter_contract_details:  
    #             resource_cost_data = detail.actual_cost_total_resource_code_calculation()
    #             Total_Actual_Resources_Cost += resource_cost_data.get('total_sum_assembly_resource_code_amount_var', 0)
    #             Total_Actual_Resources_Cost = round(Total_Actual_Resources_Cost, 2)
            
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.actual_cost_subcontracts_resource_list()
    #             Actual_Sub_Contract_Cost += resource_usage_data.get('total_sum_calculate_usage_amount', 0)
    #             Actual_Sub_Contract_Cost = round(Actual_Sub_Contract_Cost, 2)
            
    #         for detail in filter_contract_details: 
    #             resource_usage_data = detail.actual_cost_expense_resource_list()
    #             Actual_Expenses_Cost += resource_usage_data.get('var_total_actual_expense_cost', 0)
    #             Actual_Expenses_Cost = round(Actual_Expenses_Cost, 2)
            
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.actual_cost_store_resource_list()
    #             Actual_Store_Cost += resource_usage_data.get('total_actual_store_cost_var', 0)
    #             Actual_Store_Cost = round(Actual_Store_Cost, 2)
            
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.earned_cost_by_resource_list()
    #             EARNED_COSTS += resource_usage_data.get('total_actual_earned_cost_var', 0)
    #             EARNED_COSTS = round(EARNED_COSTS, 2)

        
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.contract_resource_variance_to_date_calculation()
    #             VARIANCE_TO_DATE += resource_usage_data.get('total_cost_difference', 0)
    #             VARIANCE_TO_DATE =  round(VARIANCE_TO_DATE, 2)

       
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.contract_resource_estimate_at_completion_calculation()
    #             Estimate_At_Completion_EAC += resource_usage_data.get('sum_total_estimate_at_completion_cost', 0)
    #             Estimate_At_Completion_EAC = round(Estimate_At_Completion_EAC, 2)
        
        
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.contract_ETC_remaining_calculation()
    #             ETC_REMAINING += resource_usage_data.get('total_cost_difference', 0)
    #             ETC_REMAINING = round(ETC_REMAINING, 2)
        
        
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.contract_VAC_remaining_calculation()
    #             VAC_value += resource_usage_data.get('total_cost_difference', 0)
    #             VAC_value = round(VAC_value, 2)

    #         resource_usage[assemblies_level_1_record.Assemblies_Code_L1] = [assemblies_level_1_record.id, Assembly_Level_1_Name, Unit, total_unit_cost, Contract_Quantity, Budget_Quantity, Total_Budget_Costs, Markup, Total_Markup_Amount, Unit_Price, Total_Price, Total_Target_Profit, Total_Actual_Resources_Cost, Actual_Sub_Contract_Cost, Actual_Expenses_Cost, Actual_Store_Cost, EARNED_COSTS, VARIANCE_TO_DATE, ETC_REMAINING, Estimate_At_Completion_EAC, Estimate_At_Completion_EAC]
    #     return resource_usage


    # def contract_assemblies_level_2_values(self, assemblies_level_1_record):
    #     from assembliesApp.models import Assemblies_Code_L2_Table
    #     filter_assembly_level_2 = Assemblies_Code_L2_Table.objects.filter(Company_Details=self.company_details)
    #     resource_usage = {}
        
    #     for assemblies_level_2_record in filter_assembly_level_2:
            
    #         Assembly_Level_2_Name = assemblies_level_2_record.Assemblies_Code_L2
    #         Unit = ''
    #         total_unit_cost = 0
    #         Contract_Quantity = 0
    #         Budget_Quantity = 0
    #         Total_Budget_Costs = 0
    #         Markup = ''
    #         Total_Markup_Amount = 0
    #         Unit_Price = 0
    #         Total_Price = 0
    #         Total_Target_Profit = 0

    #         Total_Actual_Resources_Cost = 0
    #         Actual_Sub_Contract_Cost = 0
    #         Actual_Expenses_Cost = 0
    #         Actual_Store_Cost = 0
    #         EARNED_COSTS = 0
    #         VARIANCE_TO_DATE = 0
    #         ETC_REMAINING = 0
    #         Estimate_At_Completion_EAC = 0
    #         VAC_value = 0

    #         filter_contract_details = MainContractDetail.objects.filter(
    #             main_contract = self,
    #             assembly_row__Assemblies_Code_L2 = assemblies_level_2_record
    #         )
    #         # print('filter_contract_details')
    #         # print(filter_contract_details)
    #         if filter_contract_details:
    #             total_unit_cost = round(filter_contract_details.aggregate(total=Sum('unit_cost'))['total'], 2)
    #             Contract_Quantity = round(filter_contract_details.aggregate(total=Sum('contract_quantity'))['total'], 2)
    #             Budget_Quantity = round(filter_contract_details.aggregate(total=Sum('budget_quantity'))['total'], 2)
    #             Total_Budget_Costs = round(filter_contract_details.aggregate(total=Sum('budget_costs'))['total'], 2)
    #             Total_Markup_Amount = round(filter_contract_details.aggregate(total=Sum('markup_amount'))['total'], 2)
    #             Unit_Price = round(filter_contract_details.aggregate(total=Sum('unit_price'))['total'], 2)
    #             Total_Price = round(filter_contract_details.aggregate(total=Sum('total_price'))['total'], 2)
    #             Total_Target_Profit = round(filter_contract_details.aggregate(total=Sum('target_profit'))['total'], 2)

            
    #         for detail in filter_contract_details:  
    #             resource_cost_data = detail.actual_cost_total_resource_code_calculation()
    #             Total_Actual_Resources_Cost += resource_cost_data.get('total_sum_assembly_resource_code_amount_var', 0)
    #             Total_Actual_Resources_Cost = round(Total_Actual_Resources_Cost, 2)
            
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.actual_cost_subcontracts_resource_list()
    #             Actual_Sub_Contract_Cost += resource_usage_data.get('total_sum_calculate_usage_amount', 0)
    #             Actual_Sub_Contract_Cost = round(Actual_Sub_Contract_Cost, 2)
            
    #         for detail in filter_contract_details: 
    #             resource_usage_data = detail.actual_cost_expense_resource_list()
    #             Actual_Expenses_Cost += resource_usage_data.get('var_total_actual_expense_cost', 0)
    #             Actual_Expenses_Cost = round(Actual_Expenses_Cost, 2)
            
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.actual_cost_store_resource_list()
    #             Actual_Store_Cost += resource_usage_data.get('total_actual_store_cost_var', 0)
    #             Actual_Store_Cost = round(Actual_Store_Cost, 2)
            
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.earned_cost_by_resource_list()
    #             EARNED_COSTS += resource_usage_data.get('total_actual_earned_cost_var', 0)
    #             EARNED_COSTS = round(EARNED_COSTS, 2)

        
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.contract_resource_variance_to_date_calculation()
    #             VARIANCE_TO_DATE += resource_usage_data.get('contract_resource_variance_to_date_value', 0)
    #             VARIANCE_TO_DATE =  round(VARIANCE_TO_DATE, 2)

       
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.contract_resource_estimate_at_completion_calculation()
    #             Estimate_At_Completion_EAC += resource_usage_data.get('sum_total_estimate_at_completion_cost', 0)
    #             Estimate_At_Completion_EAC = round(Estimate_At_Completion_EAC, 2)
        
        
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.contract_ETC_remaining_calculation()
    #             ETC_REMAINING += resource_usage_data.get('total_cost_difference', 0)
    #             ETC_REMAINING = round(ETC_REMAINING, 2)
        
        
    #         for detail in filter_contract_details:  
    #             resource_usage_data = detail.contract_VAC_remaining_calculation()
    #             VAC_value += resource_usage_data.get('total_cost_difference', 0)
    #             VAC_value = round(VAC_value, 2)

    #         resource_usage[assemblies_level_2_record.Assemblies_Code_L1] = [assemblies_level_2_record.id, Assembly_Level_2_Name, Unit, total_unit_cost, Contract_Quantity, Budget_Quantity, Total_Budget_Costs, Markup, Total_Markup_Amount, Unit_Price, Total_Price, Total_Target_Profit, Total_Actual_Resources_Cost, Actual_Sub_Contract_Cost, Actual_Expenses_Cost, Actual_Store_Cost, EARNED_COSTS, VARIANCE_TO_DATE, ETC_REMAINING, Estimate_At_Completion_EAC, Estimate_At_Completion_EAC]
    #     return resource_usage
    

    def contract_assemblies_level_1_values(self):
        print("========================================================================================================")
        from assembliesApp.models import Assemblies_Code_L1_Table, Assemblies_Code_L2_Table
        filter_assembly_level_1 = Assemblies_Code_L1_Table.objects.filter(Company_Details=self.company_details)
        resource_usage = {}
        
        for assemblies_level_1_record in filter_assembly_level_1:
            Assembly_Level_1_Name = assemblies_level_1_record.Assemblies_Code_L1
            Unit = 'Assembly Level 1'
            total_unit_cost = 0
            Contract_Quantity = 0
            Budget_Quantity = 0
            Total_Budget_Costs = 0
            Markup = ''
            Total_Markup_Amount = 0
            Unit_Price = 0
            Total_Price = 0
            Total_Target_Profit = 0

            Total_Actual_Resources_Cost = 0
            Actual_Sub_Contract_Cost = 0
            Actual_Expenses_Cost = 0
            Actual_Store_Cost = 0
            EARNED_COSTS = 0
            VARIANCE_TO_DATE = 0
            ETC_REMAINING = 0
            Estimate_At_Completion_EAC = 0
            VAC_value = 0

            print('-=--------------------------------------------------------------------------------------------------------')
            print('Gate-1')

            filter_contract_details = MainContractDetail.objects.filter(
                main_contract=self,
                assembly_row__Assemblies_Code_L1=assemblies_level_1_record
            )
            print(filter_contract_details)
            print('Gate-2')
            
            if filter_contract_details:
                total_unit_cost = round(filter_contract_details.aggregate(total=Sum('unit_cost'))['total'], 2)
                Contract_Quantity = round(filter_contract_details.aggregate(total=Sum('contract_quantity'))['total'], 2)
                Budget_Quantity = round(filter_contract_details.aggregate(total=Sum('budget_quantity'))['total'], 2)
                Total_Budget_Costs = round(filter_contract_details.aggregate(total=Sum('budget_costs'))['total'], 2)
                Total_Markup_Amount = round(filter_contract_details.aggregate(total=Sum('markup_amount'))['total'], 2)
                Unit_Price = round(filter_contract_details.aggregate(total=Sum('unit_price'))['total'], 2)
                Total_Price = round(filter_contract_details.aggregate(total=Sum('total_price'))['total'], 2)
                Total_Target_Profit = round(filter_contract_details.aggregate(total=Sum('target_profit'))['total'], 2)
            print('Gate-3')
            for detail in filter_contract_details:  
                resource_cost_data = detail.actual_cost_total_resource_code_calculation()
                Total_Actual_Resources_Cost += resource_cost_data.get('total_sum_assembly_resource_code_amount_var', 0)
                Total_Actual_Resources_Cost = round(Total_Actual_Resources_Cost, 2)
            
            for detail in filter_contract_details:  
                resource_usage_data = detail.actual_cost_subcontracts_resource_list()
                Actual_Sub_Contract_Cost += resource_usage_data.get('total_sum_calculate_usage_amount', 0)
                Actual_Sub_Contract_Cost = round(Actual_Sub_Contract_Cost, 2)
            print('Gate-5')
            for detail in filter_contract_details: 
                resource_usage_data = detail.actual_cost_expense_resource_list()
                Actual_Expenses_Cost += resource_usage_data.get('var_total_actual_expense_cost', 0)
                Actual_Expenses_Cost = round(Actual_Expenses_Cost, 2)
            
            for detail in filter_contract_details:  
                resource_usage_data = detail.actual_cost_store_resource_list()
                Actual_Store_Cost += resource_usage_data.get('total_actual_store_cost_var', 0)
                Actual_Store_Cost = round(Actual_Store_Cost, 2)
            print('Gate-7')
            for detail in filter_contract_details:  
                resource_usage_data = detail.earned_cost_by_resource_list()
                EARNED_COSTS += resource_usage_data.get('total_actual_earned_cost_var', 0)
                EARNED_COSTS = round(EARNED_COSTS, 2)

            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_resource_variance_to_date_calculation()
                VARIANCE_TO_DATE += resource_usage_data.get('contract_resource_variance_to_date_value', 0)
                VARIANCE_TO_DATE = round(VARIANCE_TO_DATE, 2)
            print('Gate-9')
            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_resource_estimate_at_completion_calculation()
                Estimate_At_Completion_EAC += resource_usage_data.get('sum_total_estimate_at_completion_cost', 0)
                Estimate_At_Completion_EAC = round(Estimate_At_Completion_EAC, 2)

            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_ETC_remaining_calculation()
                ETC_REMAINING += resource_usage_data.get('contract_ETC_remaining_value', 0)
                ETC_REMAINING = round(ETC_REMAINING, 2)
            print('Gate-11')
            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_VAC_remaining_calculation()
                VAC_value += resource_usage_data.get('contract_VAC_remaining_value', 0)
                VAC_value = round(VAC_value, 2)
            print('Gate-12++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            resource_usage[assemblies_level_1_record.Assemblies_Code_L1] = {
                "id": assemblies_level_1_record.id,
                "name": Assembly_Level_1_Name,
                "unit": Unit,
                "total_unit_cost": total_unit_cost,
                "contract_quantity": Contract_Quantity,
                "budget_quantity": Budget_Quantity,
                "total_budget_costs": Total_Budget_Costs,
                "markup": Markup,
                "total_markup_amount": Total_Markup_Amount,
                "unit_price": Unit_Price,
                "total_price": Total_Price,
                "total_target_profit": Total_Target_Profit,
                "total_actual_resources_cost": Total_Actual_Resources_Cost,
                "actual_sub_contract_cost": Actual_Sub_Contract_Cost,
                "actual_expenses_cost": Actual_Expenses_Cost,
                "actual_store_cost": Actual_Store_Cost,
                "earned_costs": EARNED_COSTS,
                "variance_to_date": VARIANCE_TO_DATE,
                "etc_remaining": ETC_REMAINING,
                "estimate_at_completion_eac": Estimate_At_Completion_EAC,
                "vac_value": VAC_value,
                "level_2_values": self.contract_assemblies_level_2_values(assemblies_level_1_record)
            }
            print("Done -----------------------------------------------------------------------------------------")
        return resource_usage

    def contract_assemblies_level_2_values(self, assemblies_level_1_record):
        from assembliesApp.models import Assemblies_Code_L2_Table
        filter_assembly_level_2 = Assemblies_Code_L2_Table.objects.filter(Assemblies_Code_L1=assemblies_level_1_record)
        resource_usage = {}
        
        for assemblies_level_2_record in filter_assembly_level_2:
            Assembly_Level_2_Name = assemblies_level_2_record.Assemblies_Code_L2
            Unit = 'Assembly Level 2'
            total_unit_cost = 0
            Contract_Quantity = 0
            Budget_Quantity = 0
            Total_Budget_Costs = 0
            Markup = ''
            Total_Markup_Amount = 0
            Unit_Price = 0
            Total_Price = 0
            Total_Target_Profit = 0

            Total_Actual_Resources_Cost = 0
            Actual_Sub_Contract_Cost = 0
            Actual_Expenses_Cost = 0
            Actual_Store_Cost = 0
            EARNED_COSTS = 0
            VARIANCE_TO_DATE = 0
            ETC_REMAINING = 0
            Estimate_At_Completion_EAC = 0
            VAC_value = 0

            filter_contract_details = MainContractDetail.objects.filter(
                main_contract=self,
                assembly_row__Assemblies_Code_L1=assemblies_level_1_record,
                assembly_row__Assemblies_Code_L2=assemblies_level_2_record
            )
            
            if filter_contract_details:
                total_unit_cost = round(filter_contract_details.aggregate(total=Sum('unit_cost'))['total'], 2)
                Contract_Quantity = round(filter_contract_details.aggregate(total=Sum('contract_quantity'))['total'], 2)
                Budget_Quantity = round(filter_contract_details.aggregate(total=Sum('budget_quantity'))['total'], 2)
                Total_Budget_Costs = round(filter_contract_details.aggregate(total=Sum('budget_costs'))['total'], 2)
                Total_Markup_Amount = round(filter_contract_details.aggregate(total=Sum('markup_amount'))['total'], 2)
                Unit_Price = round(filter_contract_details.aggregate(total=Sum('unit_price'))['total'], 2)
                Total_Price = round(filter_contract_details.aggregate(total=Sum('total_price'))['total'], 2)
                Total_Target_Profit = round(filter_contract_details.aggregate(total=Sum('target_profit'))['total'], 2)
            
            for detail in filter_contract_details:  
                resource_cost_data = detail.actual_cost_total_resource_code_calculation()
                Total_Actual_Resources_Cost += resource_cost_data.get('total_sum_assembly_resource_code_amount_var', 0)
                Total_Actual_Resources_Cost = round(Total_Actual_Resources_Cost, 2)
            
            for detail in filter_contract_details:  
                resource_usage_data = detail.actual_cost_subcontracts_resource_list()
                Actual_Sub_Contract_Cost += resource_usage_data.get('total_sum_calculate_usage_amount', 0)
                Actual_Sub_Contract_Cost = round(Actual_Sub_Contract_Cost, 2)
            
            for detail in filter_contract_details: 
                resource_usage_data = detail.actual_cost_expense_resource_list()
                Actual_Expenses_Cost += resource_usage_data.get('var_total_actual_expense_cost', 0)
                Actual_Expenses_Cost = round(Actual_Expenses_Cost, 2)
            
            for detail in filter_contract_details:  
                resource_usage_data = detail.actual_cost_store_resource_list()
                Actual_Store_Cost += resource_usage_data.get('total_actual_store_cost_var', 0)
                Actual_Store_Cost = round(Actual_Store_Cost, 2)
            
            for detail in filter_contract_details:  
                resource_usage_data = detail.earned_cost_by_resource_list()
                EARNED_COSTS += resource_usage_data.get('total_actual_earned_cost_var', 0)
                EARNED_COSTS = round(EARNED_COSTS, 2)

            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_resource_variance_to_date_calculation()
                VARIANCE_TO_DATE += resource_usage_data.get('contract_resource_variance_to_date_value', 0)
                VARIANCE_TO_DATE = round(VARIANCE_TO_DATE, 2)

            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_resource_estimate_at_completion_calculation()
                Estimate_At_Completion_EAC += resource_usage_data.get('sum_total_estimate_at_completion_cost', 0)
                Estimate_At_Completion_EAC = round(Estimate_At_Completion_EAC, 2)
        
            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_ETC_remaining_calculation()
                ETC_REMAINING += resource_usage_data.get('contract_ETC_remaining_value', 0)
                ETC_REMAINING = round(ETC_REMAINING, 2)
        
            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_VAC_remaining_calculation()
                VAC_value += resource_usage_data.get('contract_VAC_remaining_value', 0)
                VAC_value = round(VAC_value, 2)

            resource_usage[assemblies_level_2_record.Assemblies_Code_L2] = {
                "id": assemblies_level_2_record.id,
                "name": Assembly_Level_2_Name,
                "unit": Unit,
                "total_unit_cost": total_unit_cost,
                "contract_quantity": Contract_Quantity,
                "budget_quantity": Budget_Quantity,
                "total_budget_costs": Total_Budget_Costs,
                "markup": Markup,
                "total_markup_amount": Total_Markup_Amount,
                "unit_price": Unit_Price,
                "total_price": Total_Price,
                "total_target_profit": Total_Target_Profit,
                "total_actual_resources_cost": Total_Actual_Resources_Cost,
                "actual_sub_contract_cost": Actual_Sub_Contract_Cost,
                "actual_expenses_cost": Actual_Expenses_Cost,
                "actual_store_cost": Actual_Store_Cost,
                "earned_costs": EARNED_COSTS,
                "variance_to_date": VARIANCE_TO_DATE,
                "etc_remaining": ETC_REMAINING,
                "estimate_at_completion_eac": Estimate_At_Completion_EAC,
                "vac_value": VAC_value,
                "level_3_values": self.contract_assemblies_level_3_values(assemblies_level_1_record, assemblies_level_2_record)
            }
        
        return resource_usage


    def contract_assemblies_level_3_values(self, assemblies_level_1_record, assemblies_level_2_record):
        from assembliesApp.models import Assemblies_Code_L3_Table
        filter_assembly_level_3 = Assemblies_Code_L3_Table.objects.filter(Assemblies_Code_L2=assemblies_level_2_record)
        resource_usage = {}
        
        for assemblies_level_3_record in filter_assembly_level_3:
            Assembly_Level_3_Name = assemblies_level_3_record.Assemblies_Code_L3
            Unit = 'Assembly Level 3'
            total_unit_cost = 0
            Contract_Quantity = 0
            Budget_Quantity = 0
            Total_Budget_Costs = 0
            Markup = ''
            Total_Markup_Amount = 0
            Unit_Price = 0
            Total_Price = 0
            Total_Target_Profit = 0

            Total_Actual_Resources_Cost = 0
            Actual_Sub_Contract_Cost = 0
            Actual_Expenses_Cost = 0
            Actual_Store_Cost = 0
            EARNED_COSTS = 0
            VARIANCE_TO_DATE = 0
            ETC_REMAINING = 0
            Estimate_At_Completion_EAC = 0
            VAC_value = 0

            filter_contract_details = MainContractDetail.objects.filter(
                main_contract=self,
                assembly_row__Assemblies_Code_L1=assemblies_level_1_record,
                assembly_row__Assemblies_Code_L2=assemblies_level_2_record,
                assembly_row__Assemblies_Code_L3=assemblies_level_3_record
            )
            
            if filter_contract_details:
                total_unit_cost = round(filter_contract_details.aggregate(total=Sum('unit_cost'))['total'], 2)
                Contract_Quantity = round(filter_contract_details.aggregate(total=Sum('contract_quantity'))['total'], 2)
                Budget_Quantity = round(filter_contract_details.aggregate(total=Sum('budget_quantity'))['total'], 2)
                Total_Budget_Costs = round(filter_contract_details.aggregate(total=Sum('budget_costs'))['total'], 2)
                Total_Markup_Amount = round(filter_contract_details.aggregate(total=Sum('markup_amount'))['total'], 2)
                Unit_Price = round(filter_contract_details.aggregate(total=Sum('unit_price'))['total'], 2)
                Total_Price = round(filter_contract_details.aggregate(total=Sum('total_price'))['total'], 2)
                Total_Target_Profit = round(filter_contract_details.aggregate(total=Sum('target_profit'))['total'], 2)
            
            for detail in filter_contract_details:  
                resource_cost_data = detail.actual_cost_total_resource_code_calculation()
                Total_Actual_Resources_Cost += resource_cost_data.get('total_sum_assembly_resource_code_amount_var', 0)
                Total_Actual_Resources_Cost = round(Total_Actual_Resources_Cost, 2)
            
            for detail in filter_contract_details:  
                resource_usage_data = detail.actual_cost_subcontracts_resource_list()
                Actual_Sub_Contract_Cost += resource_usage_data.get('total_sum_calculate_usage_amount', 0)
                Actual_Sub_Contract_Cost = round(Actual_Sub_Contract_Cost, 2)
            
            for detail in filter_contract_details: 
                resource_usage_data = detail.actual_cost_expense_resource_list()
                Actual_Expenses_Cost += resource_usage_data.get('var_total_actual_expense_cost', 0)
                Actual_Expenses_Cost = round(Actual_Expenses_Cost, 2)
            
            for detail in filter_contract_details:  
                resource_usage_data = detail.actual_cost_store_resource_list()
                Actual_Store_Cost += resource_usage_data.get('total_actual_store_cost_var', 0)
                Actual_Store_Cost = round(Actual_Store_Cost, 2)
            
            for detail in filter_contract_details:  
                resource_usage_data = detail.earned_cost_by_resource_list()
                EARNED_COSTS += resource_usage_data.get('total_actual_earned_cost_var', 0)
                EARNED_COSTS = round(EARNED_COSTS, 2)

            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_resource_variance_to_date_calculation()
                VARIANCE_TO_DATE += resource_usage_data.get('contract_resource_variance_to_date_value', 0)
                VARIANCE_TO_DATE = round(VARIANCE_TO_DATE, 2)

            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_resource_estimate_at_completion_calculation()
                Estimate_At_Completion_EAC += resource_usage_data.get('sum_total_estimate_at_completion_cost', 0)
                Estimate_At_Completion_EAC = round(Estimate_At_Completion_EAC, 2)
        
            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_ETC_remaining_calculation()
                ETC_REMAINING += resource_usage_data.get('contract_ETC_remaining_value', 0)
                ETC_REMAINING = round(ETC_REMAINING, 2)
        
            for detail in filter_contract_details:  
                resource_usage_data = detail.contract_VAC_remaining_calculation()
                VAC_value += resource_usage_data.get('contract_VAC_remaining_value', 0)
                VAC_value = round(VAC_value, 2)

            resource_usage[assemblies_level_3_record.Assemblies_Code_L3] = {
                "id": assemblies_level_3_record.id,
                "name": Assembly_Level_3_Name,
                "unit": Unit,
                "total_unit_cost": total_unit_cost,
                "contract_quantity": Contract_Quantity,
                "budget_quantity": Budget_Quantity,
                "total_budget_costs": Total_Budget_Costs,
                "markup": Markup,
                "total_markup_amount": Total_Markup_Amount,
                "unit_price": Unit_Price,
                "total_price": Total_Price,
                "total_target_profit": Total_Target_Profit,
                "total_actual_resources_cost": Total_Actual_Resources_Cost,
                "actual_sub_contract_cost": Actual_Sub_Contract_Cost,
                "actual_expenses_cost": Actual_Expenses_Cost,
                "actual_store_cost": Actual_Store_Cost,
                "earned_costs": EARNED_COSTS,
                "variance_to_date": VARIANCE_TO_DATE,
                "etc_remaining": ETC_REMAINING,
                "estimate_at_completion_eac": Estimate_At_Completion_EAC,
                "vac_value": VAC_value,
                "resource_level_1_values": self.contract_resource_level_1_values(assemblies_level_1_record, assemblies_level_2_record, assemblies_level_3_record),
                "filter_contract_assembly_details": filter_contract_details
            }
        
        return resource_usage

    # def contract_resource_level_1_values(self, assemblies_level_1_record, assemblies_level_2_record, assemblies_level_3_record):
    #     from assembliesApp.models import Assemblies_Code_L3_Table, Estimation_Assemblies_Table
    #     from companyApp.models import Resource_Code_L1_Table
    #     from companyApp.models import Resource_Code_L1_Table
    #     from expenseApp.models import ExpenseTable
    #     from storeApp.models import StoreTable
    #     from assembliesApp.models import Estimation_Assemblies_Resource_Details_Table

    #     filter_assembly_level_3 = Assemblies_Code_L3_Table.objects.filter(Assemblies_Code_L2=assemblies_level_2_record, Company_Details=self.company_details)
    #     filter_Estimation_Assemblies = Estimation_Assemblies_Table.objects.filter(Assemblies_Code_L3__in=filter_assembly_level_3, Company_Details=self.company_details).last()
    #     detail = MainContractDetail.objects.filter(
    #         main_contract=self,
    #         assembly_row__Assemblies_Code_L1=assemblies_level_1_record,
    #         assembly_row__Assemblies_Code_L2=assemblies_level_2_record,
    #         assembly_row__Assemblies_Code_L3=assemblies_level_3_record
    #     ).last()
    #     filter_resource_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=self.company_details)

    #     resource_usage = {}

    #     total_quantity = SubContractInvoiceDetailsTable.objects.filter(
    #         sub_contract_invoice__invoice_contract_row__contract_value=self,
    #         sub_contract_assembly__assembly_value=filter_Estimation_Assemblies
    #     ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
    #     if total_quantity:
    #         total_quantity = float(total_quantity)
    #     else:
    #         total_quantity = 0

    #     total_sum_calculate_usage_amount = 0
    #     total_sum_calculate_usage_amount_single = 0
    #     total_sum_assembly_resource_code_amount_var = 0
    #     total_actual_earned_cost_var = 0
    #     total_actual_store_cost_var = 0
    #     total_actual_expense_cost = 0
    #     total_estimate_at_completion = 0

    #     contract_remain_quantity = detail.calculate_remaining_quantity()
    #     contract_quantity = detail.contract_quantity
        
    #     for resoures_level_1_record in filter_resource_level_1:
    #         Assembly_Level_3_Name = resoures_level_1_record.Resource_Code_L1
    #         Unit = ''
    #         total_unit_cost = 0
    #         Contract_Quantity = 0
    #         Budget_Quantity = 0
    #         Total_Budget_Costs = 0
    #         Markup = ''
    #         Total_Markup_Amount = 0
    #         Unit_Price = 0
    #         Total_Price = 0
    #         Total_Target_Profit = 0

    #         Total_Actual_Resources_Cost = 0
    #         Actual_Sub_Contract_Cost = 0
    #         Actual_Expenses_Cost = 0
    #         Actual_Store_Cost = 0
    #         EARNED_COSTS = 0
    #         VARIANCE_TO_DATE = 0
    #         ETC_REMAINING = 0
    #         Estimate_At_Completion_EAC = 0
    #         VAC_value = 0



            

    #         filter_Estimation_Assemblies_Resource_Details = Estimation_Assemblies_Resource_Details_Table.objects.filter(
    #             Company_Details=self.company_details,
    #             Estimation_Assemblies=filter_Estimation_Assemblies, 
    #             Resource_record__Resource_Code_L1 = resoures_level_1_record
    #         )


    #         ultimate_usage_resource_L1_total_amount = 0
    #         ultimate_usage_resource_L1_total_single_amount = 0
    #         for assembly_detail_record in filter_Estimation_Assemblies_Resource_Details:
    #             if resoures_level_1_record == assembly_detail_record.Resource_record.Resource_Code_L1:
    #                 if assembly_detail_record.Unit_Cost:
    #                     assembly_detail_record_Unit_Cost = float(assembly_detail_record.Unit_Cost)
    #                 else:
    #                     assembly_detail_record_Unit_Cost = 0

    #                 ultimate_usage_resource_L1 = total_quantity * assembly_detail_record_Unit_Cost
    #                 ultimate_usage_resource_L1_total_amount += ultimate_usage_resource_L1
    #                 ultimate_usage_resource_L1_total_single_amount += assembly_detail_record_Unit_Cost

    #         total_expense = ExpenseTable.objects.filter(
    #             Company_Details=self.company_details,
    #             contract_value=self,
    #             assembly_value=filter_Estimation_Assemblies,
    #             resource_value__Resource_Code_L1=resoures_level_1_record
    #         ).aggregate(total_cost=Sum('total_cost'))

    #         total_store = StoreTable.objects.filter(
    #             Company_Details=self.company_details,
    #             contract_value=self,
    #             assembly_value=filter_Estimation_Assemblies,
    #             resource_value__Resource_Code_L1=resoures_level_1_record,
    #             stock_trasaction_status="Stock-Out"
    #         ).aggregate(total_cost=Sum('total_cost'))

    #         if total_expense['total_cost']:
    #             total_expense_var = float(total_expense['total_cost'])
    #         else:
    #             total_expense_var = 0

    #         if total_store['total_cost']:
    #             total_store_var = float(total_store['total_cost'])
    #         else:
    #             total_store_var = 0

    #         total_resourse_cost_var = ultimate_usage_resource_L1_total_amount + total_expense_var + total_store_var
    #         total_sum_calculate_usage_amount += ultimate_usage_resource_L1_total_amount
    #         total_sum_calculate_usage_amount_single += ultimate_usage_resource_L1_total_single_amount
    #         total_actual_store_cost_var += total_store_var
    #         total_actual_expense_cost += total_expense_var
    #         total_sum_assembly_resource_code_amount_var += total_resourse_cost_var

    #         resourse_unit_cost = Estimation_Assemblies_Resource_Details_Table.objects.filter(
    #             Company_Details=self.company_details,
    #             Estimation_Assemblies=filter_Estimation_Assemblies,
    #             Resource_record__Resource_Code_L1=resoures_level_1_record
    #         ).aggregate(total=Sum('Unit_Cost'))['total'] or 0

    #         resource_earned_amount = resourse_unit_cost * total_quantity
    #         total_actual_earned_cost_var += resource_earned_amount

    #         budget_cost = float(resourse_unit_cost) * float(contract_remain_quantity)
    #         estimate_at_completion = budget_cost + total_resourse_cost_var
    #         total_estimate_at_completion += estimate_at_completion

    #         resource_usage[resoures_level_1_record.Resource_Code_L1] = {
    #             'subcontract_cost': ultimate_usage_resource_L1_total_amount,
    #             'expense_cost': total_expense_var,
    #             'store_cost': total_store_var,
    #             'total_cost': total_resourse_cost_var,
    #             'earned_cost': resource_earned_amount,
    #             'budget_cost': budget_cost,
    #             'estimate_at_completion': estimate_at_completion
    #         }

    #         total_budget_cost = sum(resource['budget_cost'] for resource in resource_usage.values())
    #         total_cost_difference = total_budget_cost - total_sum_assembly_resource_code_amount_var

    #         resource_usage['totals'] = {
    #             'subcontract_cost': total_sum_calculate_usage_amount,
    #             'expense_cost': total_actual_expense_cost,
    #             'store_cost': total_actual_store_cost_var,
    #             'total_cost': total_sum_assembly_resource_code_amount_var,
    #             'earned_cost': total_actual_earned_cost_var,
    #             'budget_cost': total_budget_cost,
    #             'estimate_at_completion': total_estimate_at_completion,
    #             'cost_difference': total_cost_difference
    #         }
        
    #         resource_usage[resoures_level_1_record.Resource_Code_L1] = {
    #             "id": resoures_level_1_record.id,
    #             "name": resoures_level_1_record.Resource_Code_L1,
    #             "unit": "",
    #             "total_unit_cost": "",
    #             "contract_quantity": "",
    #             "budget_quantity": "",
    #             "total_budget_costs": total_budget_cost,
    #             "markup": "",
    #             "total_markup_amount": "",
    #             "unit_price": "",
    #             "total_price": "",
    #             "total_target_profit": "",
    #             "total_actual_resources_cost": total_sum_assembly_resource_code_amount_var,
    #             "actual_sub_contract_cost": total_sum_calculate_usage_amount,
    #             "actual_expenses_cost": total_actual_expense_cost,
    #             "actual_store_cost": total_actual_store_cost_var,
    #             "earned_costs": total_actual_earned_cost_var,
    #             "variance_to_date": VARIANCE_TO_DATE,
    #             "etc_remaining": ETC_REMAINING,
    #             "estimate_at_completion_eac": total_estimate_at_completion,
    #             "vac_value": VAC_value,
    #         }
        
    #     return resource_usage


    def contract_resource_level_1_values(self, assemblies_level_1_record, assemblies_level_2_record, assemblies_level_3_record):
        from assembliesApp.models import Assemblies_Code_L3_Table, Estimation_Assemblies_Table, Estimation_Assemblies_Resource_Details_Table
        from companyApp.models import Resource_Code_L1_Table
        from expenseApp.models import ExpenseTable
        from storeApp.models import StoreTable
        

        filter_assembly_level_3 = Assemblies_Code_L3_Table.objects.filter(Assemblies_Code_L2=assemblies_level_2_record, Company_Details=self.company_details)
        print("Start -----------Resource level 1 ==================================================================================================")
        filter_Estimation_Assemblies = Estimation_Assemblies_Table.objects.filter(Assemblies_Code_L3__in=filter_assembly_level_3, Company_Details=self.company_details).last()
        # filter_Estimation_Assemblies = Estimation_Assemblies_Table.objects.filter(Assemblies_Code_L3__in=filter_assembly_level_3, Company_Details=self.company_details)
        print('filter_Estimation_Assemblies')
        print(filter_Estimation_Assemblies)
        detail = MainContractDetail.objects.filter(
            main_contract=self,
            assembly_row__Assemblies_Code_L1=assemblies_level_1_record,
            assembly_row__Assemblies_Code_L2=assemblies_level_2_record,
            assembly_row__Assemblies_Code_L3=assemblies_level_3_record
        ).last()
        filter_resource_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=self.company_details)
        print("Resource level 1 ==================================================================================================")
        resource_usage = {}

        total_quantity = SubContractInvoiceDetailsTable.objects.filter(
            sub_contract_invoice__invoice_contract_row__contract_value=self,
            sub_contract_assembly__assembly_value=filter_Estimation_Assemblies
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        if total_quantity:
            total_quantity = float(total_quantity)
        else:
            total_quantity = 0

        # Calculate the total quantity from main contract invoices for earned cost
        main_contract_total_quantity = MainContractInvoiceDetailsTable.objects.filter(
            main_contract_invoice__invoice_contract_row=self,
            main_contract_assembly__assembly_row=filter_Estimation_Assemblies
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        main_contract_total_quantity = float(main_contract_total_quantity) if main_contract_total_quantity else 0

        
        print('-----------------------------------------------------------------')
        print(detail)
        if detail:
            contract_remain_quantity = detail.calculate_remaining_quantity()
            contract_quantity = detail.contract_quantity
            budget_quantity = detail.budget_quantity
        else:
            contract_remain_quantity = 0
            contract_quantity = 0
            budget_quantity = 0
        
        for resoures_level_1_record in filter_resource_level_1:
            # Calculate subcontract costs
            filter_Estimation_Assemblies_Resource_Details = Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Company_Details=self.company_details,
                Estimation_Assemblies=filter_Estimation_Assemblies
            )

            
            ultimate_usage_resource_L1_total_amount = 0
            ultimate_usage_resource_L1_total_qty = 0

            ultimate_usage_resource_L1_total_single_amount = 0
            for assembly_detail_record in filter_Estimation_Assemblies_Resource_Details:
                if resoures_level_1_record == assembly_detail_record.Resource_record.Resource_Code_L1:
                    if assembly_detail_record.Unit_Cost:
                        assembly_detail_record_Unit_Cost = float(assembly_detail_record.Unit_Cost)
                    else:
                        assembly_detail_record_Unit_Cost = 0
                    
                    ultimate_usage_resource_L1 =  total_quantity * assembly_detail_record_Unit_Cost

                    ultimate_usage_resource_L1_total_amount = ultimate_usage_resource_L1_total_amount + ultimate_usage_resource_L1

                    ultimate_usage_resource_L1_total_qty = ultimate_usage_resource_L1_total_qty + total_quantity


                    ultimate_usage_resource_L1_total_single_amount = float(ultimate_usage_resource_L1_total_single_amount) + assembly_detail_record_Unit_Cost

            subcontract_cost = round(ultimate_usage_resource_L1_total_amount, 2)
            subcontract_qty = round(ultimate_usage_resource_L1_total_qty, 2)

            

            # Calculate expense costs
            expense_cost = round(ExpenseTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record
            ).aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0, 2)

            # Calculate expense qty
            expense_qty = round(ExpenseTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record
            ).aggregate(quantity=Sum('quantity'))['quantity'] or 0, 2)


            # Calculate store costs
            store_cost = round(StoreTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                stock_trasaction_status="Stock-Out"
            ).aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0, 2)


            store_qty = round(StoreTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                stock_trasaction_status="Stock-Out"
            ).aggregate(quantity=Sum('quantity'))['quantity'] or 0, 2)

            # Calculate budget costs
            budget_unit_cost = round(Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Company_Details=self.company_details,
                Estimation_Assemblies=filter_Estimation_Assemblies,
                Resource_record__Resource_Code_L1=resoures_level_1_record
            ).aggregate(total=Sum('Unit_Cost'))['total'] or 0, 2)
            
            budget_cost = round(budget_unit_cost * float(budget_quantity), 2)


            total_actual_resources_cost = round(float(subcontract_cost) + float(expense_cost) + float(store_cost), 2)

            # Calculate earned cost
            earned_cost = round(budget_unit_cost * main_contract_total_quantity, 2)

            # Calculate variance to date
            variance_to_date = round(budget_cost - subcontract_cost, 2)

            # Calculate estimate at completion
            estimate_at_completion = round(budget_unit_cost * float(contract_remain_quantity) + total_actual_resources_cost, 2)

            print('estimate_at_completion')
            print(estimate_at_completion)

            # Calculate ETC remaining
            ETC_remaining = round(estimate_at_completion - subcontract_cost, 2)

            # Calculate VAC remaining
            VAC_remaining = round(budget_cost - estimate_at_completion, 2)

            resource_usage[resoures_level_1_record.Resource_Code_L1] = {
                "id": resoures_level_1_record.id,
                "name": resoures_level_1_record.Resource_Code_L1,
                "unit": "Resource Level 1",
                "total_unit_cost": budget_unit_cost,
                "contract_quantity": contract_quantity,
                "budget_quantity": budget_quantity,
                "total_budget_costs": budget_cost,
                "markup": "",
                "total_markup_amount": " - ",
                "unit_price": " - ",
                "total_price": " - ",
                "total_target_profit": " - ",
                "total_actual_resources_cost": total_actual_resources_cost,
                "actual_sub_contract_quantity": subcontract_qty,
                "actual_expenses_quantity": expense_qty,
                "actual_store_quantity": store_qty,
                "actual_sub_contract_cost": subcontract_cost,
                "actual_expenses_cost": expense_cost,
                "actual_store_cost": store_cost,
                "earned_costs": earned_cost,
                "variance_to_date": variance_to_date,
                "etc_remaining": ETC_remaining,
                "estimate_at_completion_eac": estimate_at_completion,
                "vac_value": VAC_remaining,
                "resource_level_2_values": self.contract_resource_level_2_values(assemblies_level_1_record, assemblies_level_2_record, assemblies_level_3_record, resoures_level_1_record)
            }
        
        return resource_usage
    

    def contract_resource_level_2_values(self, assemblies_level_1_record, assemblies_level_2_record, assemblies_level_3_record, resoures_level_1_record):
        from assembliesApp.models import Assemblies_Code_L3_Table, Estimation_Assemblies_Table, Estimation_Assemblies_Resource_Details_Table
        from companyApp.models import Resource_Code_L2_Table
        from expenseApp.models import ExpenseTable
        from storeApp.models import StoreTable
        

        filter_assembly_level_3 = assemblies_level_3_record

        filter_Estimation_Assemblies = Estimation_Assemblies_Table.objects.filter(
            Assemblies_Code_L1 = assemblies_level_1_record,
            Assemblies_Code_L2 = assemblies_level_2_record,
            Assemblies_Code_L3 = assemblies_level_3_record, 
            Company_Details = self.company_details
        ).last()
        detail = MainContractDetail.objects.filter(
            main_contract=self,
            assembly_row__Assemblies_Code_L1=assemblies_level_1_record,
            assembly_row__Assemblies_Code_L2=assemblies_level_2_record,
            assembly_row__Assemblies_Code_L3=assemblies_level_3_record
        ).last()
        filter_resource_level_2 = Resource_Code_L2_Table.objects.filter(Resource_Code_L1=resoures_level_1_record, Company_Details=self.company_details)
        print('filter_resource_level_2')
        print(filter_resource_level_2)

        resource_usage = {}

        total_quantity = SubContractInvoiceDetailsTable.objects.filter(
            sub_contract_invoice__invoice_contract_row__contract_value=self,
            sub_contract_assembly__assembly_value=filter_Estimation_Assemblies
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        if total_quantity:
            total_quantity = float(total_quantity)
        else:
            total_quantity = 0

        # Calculate the total quantity from main contract invoices for earned cost
        main_contract_total_quantity = MainContractInvoiceDetailsTable.objects.filter(
            main_contract_invoice__invoice_contract_row=self,
            main_contract_assembly__assembly_row=filter_Estimation_Assemblies
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        main_contract_total_quantity = float(main_contract_total_quantity) if main_contract_total_quantity else 0

        
        print('-----------------------------------------------------------------')
        
        if detail:
            contract_remain_quantity = detail.calculate_remaining_quantity()
            contract_quantity = detail.contract_quantity
            budget_quantity = detail.budget_quantity
        else:
            contract_remain_quantity = 0
            contract_quantity = 0
            budget_quantity = 0
        
        for resoures_level_2_record in filter_resource_level_2:
            print('resoures_level_2_record')
            print(resoures_level_2_record.Resource_Code_L2)
            # Calculate subcontract costs
            filter_Estimation_Assemblies_Resource_Details = Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Company_Details=self.company_details,
                Estimation_Assemblies=filter_Estimation_Assemblies,
                Resource_record__Resource_Code_L1 = resoures_level_1_record,
                Resource_record__Resource_Code_L2 = resoures_level_2_record,
            )

            
            ultimate_usage_resource_L2_total_amount = 0
            ultimate_usage_resource_L2_total_single_amount = 0

            ultimate_usage_resource_L2_total_qty = 0
            for assembly_detail_record in filter_Estimation_Assemblies_Resource_Details:
                if resoures_level_2_record == assembly_detail_record.Resource_record.Resource_Code_L2:
                    if assembly_detail_record.Unit_Cost:
                        assembly_detail_record_Unit_Cost = float(assembly_detail_record.Unit_Cost)
                    else:
                        assembly_detail_record_Unit_Cost = 0
                    
                    ultimate_usage_resource_L2 =  total_quantity * assembly_detail_record_Unit_Cost

                    ultimate_usage_resource_L2_total_amount = ultimate_usage_resource_L2_total_amount + ultimate_usage_resource_L2
                    ultimate_usage_resource_L2_total_qty = ultimate_usage_resource_L2_total_qty + total_quantity
                    ultimate_usage_resource_L2_total_single_amount = float(ultimate_usage_resource_L2_total_single_amount) + assembly_detail_record_Unit_Cost

            subcontract_cost = round(ultimate_usage_resource_L2_total_amount, 2)
            subcontract_qty = round(ultimate_usage_resource_L2_total_qty, 2)
            print('subcontract_cost')
            print(subcontract_cost)

            

            # Calculate expense costs
            expense_cost = round(ExpenseTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                resource_value__Resource_Code_L2=resoures_level_2_record
            ).aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0, 2)

            expense_qty = round(ExpenseTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                resource_value__Resource_Code_L2=resoures_level_2_record
            ).aggregate(quantity=Sum('quantity'))['quantity'] or 0, 2)

            # Calculate store costs
            store_cost = round(StoreTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                resource_value__Resource_Code_L2=resoures_level_2_record,
                stock_trasaction_status="Stock-Out"
            ).aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0, 2)

            store_qty = round(StoreTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                resource_value__Resource_Code_L2=resoures_level_2_record,
                stock_trasaction_status="Stock-Out"
            ).aggregate(quantity=Sum('quantity'))['quantity'] or 0, 2)

            # Calculate budget costs
            budget_unit_cost = round(Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Company_Details=self.company_details,
                Estimation_Assemblies=filter_Estimation_Assemblies,
                Resource_record__Resource_Code_L1=resoures_level_1_record,
                Resource_record__Resource_Code_L2=resoures_level_2_record
            ).aggregate(total=Sum('Unit_Cost'))['total'] or 0, 2)
            budget_cost = round(budget_unit_cost * float(budget_quantity), 2)


            total_actual_resources_cost = round(float(subcontract_cost) + float(expense_cost) + float(store_cost), 2)

            # Calculate earned cost
            earned_cost = round(budget_unit_cost * main_contract_total_quantity, 2)

            # Calculate variance to date
            variance_to_date = round(budget_cost - subcontract_cost, 2)

            # Calculate estimate at completion
            estimate_at_completion = round(budget_unit_cost * float(contract_remain_quantity) + total_actual_resources_cost, 2)

            
            # Calculate ETC remaining
            ETC_remaining = round(estimate_at_completion - subcontract_cost, 2)

            # Calculate VAC remaining
            VAC_remaining = round(budget_cost - estimate_at_completion, 2)

            resource_usage[resoures_level_2_record.Resource_Code_L2] = {
                "id": resoures_level_2_record.id,
                "name": resoures_level_2_record.Resource_Code_L2,
                "unit": "Resource Level 2",
                "total_unit_cost": budget_unit_cost,
                "contract_quantity": contract_quantity,
                "budget_quantity": budget_quantity,
                "total_budget_costs": budget_cost,
                "markup": "",
                "total_markup_amount": " - ",
                "unit_price": " - ",
                "total_price": " - ",
                "total_target_profit": " - ",
                "total_actual_resources_cost": total_actual_resources_cost,
                "actual_sub_contract_quantity": subcontract_qty,
                "actual_expenses_quantity": expense_qty,
                "actual_store_quantity": store_qty,
                "actual_sub_contract_cost": subcontract_cost,
                "actual_expenses_cost": expense_cost,
                "actual_store_cost": store_cost,
                "earned_costs": earned_cost,
                "variance_to_date": variance_to_date,
                "etc_remaining": ETC_remaining,
                "estimate_at_completion_eac": estimate_at_completion,
                "vac_value": VAC_remaining,
                "resource_level_3_values": self.contract_resource_level_3_values(assemblies_level_1_record, assemblies_level_2_record, assemblies_level_3_record, resoures_level_1_record, resoures_level_2_record)
            }

            print(resource_usage)
        
        return resource_usage

    
    def contract_resource_level_3_values(self, assemblies_level_1_record, assemblies_level_2_record, assemblies_level_3_record, resoures_level_1_record, resoures_level_2_record):
        from assembliesApp.models import Assemblies_Code_L3_Table, Estimation_Assemblies_Table, Estimation_Assemblies_Resource_Details_Table
        from companyApp.models import Resource_Code_L2_Table, Resource_Code_L3_Table
        from expenseApp.models import ExpenseTable
        from storeApp.models import StoreTable
        

        filter_assembly_level_3 = assemblies_level_3_record

        filter_Estimation_Assemblies = Estimation_Assemblies_Table.objects.filter(
            Assemblies_Code_L1 = assemblies_level_1_record,
            Assemblies_Code_L2 = assemblies_level_2_record,
            Assemblies_Code_L3 = assemblies_level_3_record, 
            Company_Details = self.company_details
        ).last()
        detail = MainContractDetail.objects.filter(
            main_contract=self,
            assembly_row__Assemblies_Code_L1=assemblies_level_1_record,
            assembly_row__Assemblies_Code_L2=assemblies_level_2_record,
            assembly_row__Assemblies_Code_L3=assemblies_level_3_record
        ).last()
        filter_resource_level_3 = Resource_Code_L3_Table.objects.filter(Resource_Code_L2=resoures_level_2_record, Company_Details=self.company_details)

        resource_usage = {}

        total_quantity = SubContractInvoiceDetailsTable.objects.filter(
            sub_contract_invoice__invoice_contract_row__contract_value=self,
            sub_contract_assembly__assembly_value=filter_Estimation_Assemblies
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        if total_quantity:
            total_quantity = float(total_quantity)
        else:
            total_quantity = 0

        # Calculate the total quantity from main contract invoices for earned cost
        main_contract_total_quantity = MainContractInvoiceDetailsTable.objects.filter(
            main_contract_invoice__invoice_contract_row=self,
            main_contract_assembly__assembly_row=filter_Estimation_Assemblies
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        main_contract_total_quantity = float(main_contract_total_quantity) if main_contract_total_quantity else 0

        
        print('-----------------------------------------------------------------')
        
        if detail:
            contract_remain_quantity = detail.calculate_remaining_quantity()
            contract_quantity = detail.contract_quantity
            budget_quantity = detail.budget_quantity
        else:
            contract_remain_quantity = 0
            contract_quantity = 0
            budget_quantity = 0
        
        for resoures_level_3_record in filter_resource_level_3:
            print('resoures_level_3_record')
            print(resoures_level_3_record.Resource_Code_L3)
            # Calculate subcontract costs
            filter_Estimation_Assemblies_Resource_Details = Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Company_Details=self.company_details,
                Estimation_Assemblies=filter_Estimation_Assemblies,
                Resource_record__Resource_Code_L1 = resoures_level_1_record,
                Resource_record__Resource_Code_L2 = resoures_level_2_record,
                Resource_record__Resource_Code_L3 = resoures_level_3_record
            )

            
            ultimate_usage_resource_L3_total_amount = 0
            ultimate_usage_resource_L3_total_qty = 0
            ultimate_usage_resource_L3_total_single_amount = 0
            for assembly_detail_record in filter_Estimation_Assemblies_Resource_Details:
                if resoures_level_3_record == assembly_detail_record.Resource_record.Resource_Code_L3:
                    if assembly_detail_record.Unit_Cost:
                        assembly_detail_record_Unit_Cost = float(assembly_detail_record.Unit_Cost)
                    else:
                        assembly_detail_record_Unit_Cost = 0
                    
                    ultimate_usage_resource_L3 =  total_quantity * assembly_detail_record_Unit_Cost

                    ultimate_usage_resource_L3_total_amount = ultimate_usage_resource_L3_total_amount + ultimate_usage_resource_L3
                    ultimate_usage_resource_L3_total_qty = ultimate_usage_resource_L3_total_qty + total_quantity
                    ultimate_usage_resource_L3_total_single_amount = float(ultimate_usage_resource_L3_total_single_amount) + assembly_detail_record_Unit_Cost

            subcontract_qty = round(ultimate_usage_resource_L3_total_qty, 2)
            subcontract_cost = round(ultimate_usage_resource_L3_total_amount, 2)
            print('subcontract_cost')
            print(subcontract_cost)

            

            # Calculate expense costs
            expense_cost = round(ExpenseTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                resource_value__Resource_Code_L2=resoures_level_2_record,
                resource_value__Resource_Code_L3=resoures_level_3_record
            ).aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0, 2)

            expense_qty = round(ExpenseTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                resource_value__Resource_Code_L2=resoures_level_2_record,
                resource_value__Resource_Code_L3=resoures_level_3_record
            ).aggregate(quantity=Sum('quantity'))['quantity'] or 0, 2)

            # Calculate store costs
            store_cost = round(StoreTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                resource_value__Resource_Code_L2=resoures_level_2_record,
                resource_value__Resource_Code_L3=resoures_level_3_record,
                stock_trasaction_status="Stock-Out"
            ).aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0, 2)


            store_qty = round(StoreTable.objects.filter(
                Company_Details=self.company_details,
                contract_value=self,
                assembly_value=filter_Estimation_Assemblies,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                resource_value__Resource_Code_L2=resoures_level_2_record,
                resource_value__Resource_Code_L3=resoures_level_3_record,
                stock_trasaction_status="Stock-Out"
            ).aggregate(quantity=Sum('quantity'))['quantity'] or 0, 2)

            # Calculate budget costs
            budget_unit_cost = round(Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Company_Details=self.company_details,
                Estimation_Assemblies=filter_Estimation_Assemblies,
                Resource_record__Resource_Code_L1=resoures_level_1_record,
                Resource_record__Resource_Code_L2=resoures_level_2_record,
                Resource_record__Resource_Code_L3=resoures_level_3_record
            ).aggregate(total=Sum('Unit_Cost'))['total'] or 0, 2)
            budget_cost = round(budget_unit_cost * float(budget_quantity), 2)


            total_actual_resources_cost = round(float(subcontract_cost) + float(expense_cost) + float(store_cost), 2)

            # Calculate earned cost
            earned_cost = round(budget_unit_cost * main_contract_total_quantity, 2)

            # Calculate variance to date
            variance_to_date = round(budget_cost - subcontract_cost, 2)

            # Calculate estimate at completion
            estimate_at_completion = round(budget_unit_cost * float(contract_remain_quantity) + total_actual_resources_cost, 2)

            
            # Calculate ETC remaining
            ETC_remaining = round(estimate_at_completion - subcontract_cost, 2)

            # Calculate VAC remaining
            VAC_remaining = round(budget_cost - estimate_at_completion, 2)

            resource_usage[resoures_level_3_record.Resource_Code_L3] = {
                "id": resoures_level_3_record.id,
                "name": resoures_level_3_record.Resource_Code_L3,
                "unit": "Resource Level 3",
                "total_unit_cost": budget_unit_cost,
                "contract_quantity": contract_quantity,
                "budget_quantity": budget_quantity,
                "total_budget_costs": budget_cost,
                "markup": "",
                "total_markup_amount": " - ",
                "unit_price": " - ",
                "total_price": " - ",
                "total_target_profit": " - ",
                "total_actual_resources_cost": total_actual_resources_cost,
                "actual_sub_contract_quantity": subcontract_qty,
                "actual_expenses_quantity": expense_qty,
                "actual_store_quantity": store_qty,
                "actual_sub_contract_cost": subcontract_cost,
                "actual_expenses_cost": expense_cost,
                "actual_store_cost": store_cost,
                "earned_costs": earned_cost,
                "variance_to_date": variance_to_date,
                "etc_remaining": ETC_remaining,
                "estimate_at_completion_eac": estimate_at_completion,
                "vac_value": VAC_remaining,
            }

            print(resource_usage)
        
        return resource_usage







class MainContractDetail(models.Model):
    main_contract = models.ForeignKey(MainContract, on_delete=models.CASCADE, related_name="details")
    comb_assem_code = models.CharField(max_length=50, verbose_name="Combination Assembly Code")
    assembly_name = models.CharField(max_length=100, verbose_name="Assembly Name")
    assembly_row = models.ForeignKey(Estimation_Assemblies_Table, on_delete=models.CASCADE, default=None, blank=True, null=True)
    item_description = models.TextField(verbose_name="Item Description")
    unit = models.CharField(max_length=50, verbose_name="Unit")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Cost")
    budget_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Budget Quantity")
    contract_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Contract Quantity", default=0, blank=True, null=True)
    budget_costs = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Budget Costs")
    markup = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Markup (%)")
    markup_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Markup Amount")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    target_profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Target Profit")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Detail for {self.main_contract.contract_name} - Unit: {self.unit}"

    def filter_assembly_resources_by_maincontract_detail(self):
        filter_Estimation_Assemblies_Resource_Details = Estimation_Assemblies_Resource_Details_Table.objects.filter(Estimation_Assemblies=self.assembly_row)
        return filter_Estimation_Assemblies_Resource_Details

    def func_Assembly_Invoices_total_quantity(self):
        total_quantity = MainContractInvoiceDetailsTable.objects.filter(
            main_contract_assembly=self
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        return total_quantity or 0

    def func_Assembly_Invoices_total_revenue(self):
        total_revenue = MainContractInvoiceDetailsTable.objects.filter(
            main_contract_assembly=self
        ).aggregate(total_revenue=Sum('Invoice_Revenue'))['total_revenue']
        if total_revenue:
            total_revenue = round(total_revenue,  2)
        return total_revenue or 0

    def func_Assembly_Invoices_remain_revenue(self):
        total_price = self.total_price
        earned_invoice_price = self.func_Assembly_Invoices_total_revenue()
        remaining_quantity = total_price - earned_invoice_price
        return remaining_quantity

    def calculate_percentage_of_contract_quantity(self):
        total_quantity = self.func_Assembly_Invoices_total_quantity()
        if total_quantity == 0 or self.contract_quantity == 0:
            return 0  # Avoid division by zero
        percentage = (total_quantity / self.contract_quantity) * 100
        rounded_percentage = round(percentage, 2)
        print(rounded_percentage)
        return rounded_percentage

    def filter_contract_assembly_invoices(self):
        filter_main_contract_invoice = MainContractInvoiceTable.objects.filter(
            invoice_contract_row=self.main_contract
        )
        return filter_main_contract_invoice

    def calculate_remaining_quantity(self):
        total_quantity = self.func_Assembly_Invoices_total_quantity()
        remaining_quantity = self.contract_quantity - total_quantity
        return remaining_quantity


    def Actual_Sub_Contract_Cost_Calculation(self):
        filter_subcontract_records = SubContractInvoiceDetailsTable.objects.filter(sub_contract_invoice__invoice_contract_row__contract_value=self.main_contract, sub_contract_assembly__assembly_value=self.assembly_row)
        total = filter_subcontract_records.aggregate(Sum('Invoice_Revenue'))['Invoice_Revenue__sum'] or 0
        return round(total, 2)
    def total_Sub_Contract_Cost_Calculation(self):
        filter_subcontract_records = SubContractDetail.objects.filter(sub_contract__contract_value=self.main_contract, assembly_value=self.assembly_row)
        total = filter_subcontract_records.aggregate(Sum('subcontract_total_price'))['subcontract_total_price__sum'] or 0
        return round(total, 2)
    def Actual_Expenses_Cost_Calculation(self):
        from expenseApp.models import ExpenseTable
        filter_expense_records = ExpenseTable.objects.filter(contract_value=self.main_contract, assembly_value=self.assembly_row)
        total = filter_expense_records.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total, 2)
    def Actual_Store_Cost_Calculation(self):
        from storeApp.models import StoreTable
        filter_store_records = StoreTable.objects.filter(contract_value=self.main_contract, assembly_value=self.assembly_row, stock_trasaction_status="Stock-Out")
        total = filter_store_records.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total, 2)

    def Total_Actual_Resources_Cost(self):
        value_Actual_Sub_Contract_Cost_Calculation = self.Actual_Sub_Contract_Cost_Calculation()
        value_Actual_Expenses_Cost_Calculation = self.Actual_Expenses_Cost_Calculation()
        value_Actual_Store_Cost_Calculation = self.Actual_Store_Cost_Calculation()
        return float(value_Actual_Sub_Contract_Cost_Calculation) + float(value_Actual_Expenses_Cost_Calculation) + float(value_Actual_Store_Cost_Calculation)

    

    def actual_cost_subcontracts_resource_list(self):
        from companyApp.models import Resource_Code_L1_Table
        filter_resoures_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=self.main_contract.company_details)
        resource_usage = {}
        
        total_quantity = SubContractInvoiceDetailsTable.objects.filter(
            sub_contract_invoice__invoice_contract_row__contract_value = self.main_contract,
            sub_contract_assembly__assembly_value = self.assembly_row
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        if total_quantity:
            total_quantity = float(total_quantity)
        else:
            total_quantity = 0
        
        print(f"total_quantity: {total_quantity}")
        print(f"total assembly amount: {self.assembly_row.Assembly_Unit_Cost}")

        total_sum_calculate_usage_amount = 0
        total_sum_calculate_usage_amount_single = 0
        for resoures_level_1_record in filter_resoures_level_1:
            filter_Estimation_Assemblies_Resource_Details = Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Company_Details=self.main_contract.company_details,
                Estimation_Assemblies=self.assembly_row
            )

            
            ultimate_usage_resource_L1_total_amount = 0
            ultimate_usage_resource_L1_total_single_amount = 0
            for assembly_detail_record in filter_Estimation_Assemblies_Resource_Details:
                if resoures_level_1_record == assembly_detail_record.Resource_record.Resource_Code_L1:
                    print(f"Show: {assembly_detail_record.Resource_record.Resource_Code_L1}: {assembly_detail_record.Unit_Cost}")
                    if assembly_detail_record.Unit_Cost:
                        assembly_detail_record_Unit_Cost = float(assembly_detail_record.Unit_Cost)
                    else:
                        assembly_detail_record_Unit_Cost = 0
                    
                    ultimate_usage_resource_L1 =  total_quantity * assembly_detail_record_Unit_Cost
                    print(f"{resoures_level_1_record.Resource_Code_L1}: {ultimate_usage_resource_L1}")

                    ultimate_usage_resource_L1_total_amount = ultimate_usage_resource_L1_total_amount + ultimate_usage_resource_L1
                    ultimate_usage_resource_L1_total_single_amount = float(ultimate_usage_resource_L1_total_single_amount) + assembly_detail_record_Unit_Cost
                
            print(f"last ultimate_usage_resource_L1_total_single_assembly_amount: {ultimate_usage_resource_L1_total_single_amount}")
            print(f"last ultimate_usage_resource_L1_total_amount: {ultimate_usage_resource_L1_total_amount}")

            resource_usage[resoures_level_1_record.Resource_Code_L1] = ultimate_usage_resource_L1_total_amount

            total_sum_calculate_usage_amount = float(total_sum_calculate_usage_amount) + ultimate_usage_resource_L1_total_amount
            total_sum_calculate_usage_amount_single  = float(total_sum_calculate_usage_amount_single) + ultimate_usage_resource_L1_total_single_amount
        resource_usage['total_sum_calculate_usage_amount'] = total_sum_calculate_usage_amount

        print(f"Single Assembly cost: {total_sum_calculate_usage_amount_single}")
        print(f"subcontract invoice revenue total: {total_sum_calculate_usage_amount}")
        return resource_usage


    def actual_cost_expense_resource_list(self):
        from expenseApp.models import ExpenseTable
        from companyApp.models import Resource_Code_L1_Table
        filter_resoures_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=self.main_contract.company_details)
        resource_usage = {}
        var_total_actual_expense_cost = 0
        for resoures_level_1_record in filter_resoures_level_1:
            total_expense = ExpenseTable.objects.filter(
                Company_Details=self.main_contract.company_details,
                contract_value=self.main_contract,
                assembly_value=self.assembly_row,
                resource_value__Resource_Code_L1=resoures_level_1_record
            ).aggregate(total_cost=Sum('total_cost'))

            if total_expense['total_cost']:
                total_expense_varr = total_expense['total_cost']
            else:
                total_expense_varr = 0
            resource_usage[resoures_level_1_record.Resource_Code_L1] = total_expense_varr
            var_total_actual_expense_cost = var_total_actual_expense_cost + total_expense_varr
        resource_usage['var_total_actual_expense_cost'] = var_total_actual_expense_cost
        return resource_usage


    def actual_cost_store_resource_list(self):
        from storeApp.models import StoreTable
        from companyApp.models import Resource_Code_L1_Table
        filter_resoures_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=self.main_contract.company_details)
        from expenseApp.models import ExpenseTable
        filter_resoures_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=self.main_contract.company_details)
        resource_usage = {}
        total_actual_store_cost_var = 0
        for resoures_level_1_record in filter_resoures_level_1:
            total_store = StoreTable.objects.filter(
                Company_Details=self.main_contract.company_details,
                contract_value=self.main_contract,
                assembly_value=self.assembly_row,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                stock_trasaction_status="Stock-Out"
            ).aggregate(total_cost=Sum('total_cost'))

            if total_store['total_cost']:
                total_store_varr = total_store['total_cost']
            else:
                total_store_varr = 0

            resource_usage[resoures_level_1_record.Resource_Code_L1] = total_store_varr
            total_actual_store_cost_var = total_actual_store_cost_var + total_store_varr
        resource_usage['total_actual_store_cost_var'] = total_actual_store_cost_var
        return resource_usage


    def actual_cost_total_resource_code_calculation(self):
        from companyApp.models import Resource_Code_L1_Table
        from expenseApp.models import ExpenseTable
        from storeApp.models import StoreTable
        filter_resoures_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=self.main_contract.company_details)
        resource_usage = {}

        total_quantity = SubContractInvoiceDetailsTable.objects.filter(
            sub_contract_invoice__invoice_contract_row__contract_value = self.main_contract,
            sub_contract_assembly__assembly_value = self.assembly_row
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        if total_quantity:
            total_quantity = float(total_quantity)
        else:
            total_quantity = 0
        
        print(f"total_quantity: {total_quantity}")
        print(f"total assembly amount: {self.assembly_row.Assembly_Unit_Cost}")

        total_sum_calculate_usage_amount = 0
        total_sum_calculate_usage_amount_single = 0
        total_sum_assembly_resource_code_amount_var = 0
        for resoures_level_1_record in filter_resoures_level_1:
            # total_invoice_revenue = SubContractInvoiceDetailsTable.objects.filter(
            #     sub_contract_assembly__assembly_value__estimation_assemblies_resourcedetailstable__Resource_record__Resource_Code_L1__id = resoures_level_1_record.id,
            #     sub_contract_invoice__invoice_contract_row__contract_value = self.main_contract,
            #     sub_contract_assembly__assembly_value = self.assembly_row,
                
            # ).aggregate(total_revenue=Sum('Invoice_Revenue'))

            filter_Estimation_Assemblies_Resource_Details = Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Company_Details=self.main_contract.company_details,
                Estimation_Assemblies=self.assembly_row
            )

            
            ultimate_usage_resource_L1_total_amount = 0
            ultimate_usage_resource_L1_total_single_amount = 0
            for assembly_detail_record in filter_Estimation_Assemblies_Resource_Details:
                if resoures_level_1_record == assembly_detail_record.Resource_record.Resource_Code_L1:
                    print(f"Show: {assembly_detail_record.Resource_record.Resource_Code_L1}: {assembly_detail_record.Unit_Cost}")
                    if assembly_detail_record.Unit_Cost:
                        assembly_detail_record_Unit_Cost = float(assembly_detail_record.Unit_Cost)
                    else:
                        assembly_detail_record_Unit_Cost = 0
                    
                    ultimate_usage_resource_L1 =  total_quantity * assembly_detail_record_Unit_Cost
                    print(f"{resoures_level_1_record.Resource_Code_L1}: {ultimate_usage_resource_L1}")

                    ultimate_usage_resource_L1_total_amount = ultimate_usage_resource_L1_total_amount + ultimate_usage_resource_L1
                    ultimate_usage_resource_L1_total_single_amount = float(ultimate_usage_resource_L1_total_single_amount) + assembly_detail_record_Unit_Cost

                    
                
            print(f"last ultimate_usage_resource_L1_total_amount: {ultimate_usage_resource_L1_total_amount}")



            total_expense = ExpenseTable.objects.filter(
                Company_Details=self.main_contract.company_details,
                contract_value=self.main_contract,
                assembly_value=self.assembly_row,
                resource_value__Resource_Code_L1=resoures_level_1_record
            ).aggregate(total_cost=Sum('total_cost'))

            total_store = StoreTable.objects.filter(
                Company_Details=self.main_contract.company_details,
                contract_value=self.main_contract,
                assembly_value=self.assembly_row,
                resource_value__Resource_Code_L1=resoures_level_1_record,
                stock_trasaction_status="Stock-Out"
            ).aggregate(total_cost=Sum('total_cost'))

            # if total_invoice_revenue['total_revenue']:
            #     total_subcontract_invoice_revenue = float(total_invoice_revenue['total_revenue'])
            # else:
            #     total_subcontract_invoice_revenue = 0
            if total_expense['total_cost']:
                total_expense_var = float(total_expense['total_cost'])
            else:
                total_expense_var = 0
            if total_store['total_cost']:
                total_store_var = float(total_store['total_cost'])
            else:
                total_store_var = 0

            total_resourse_cost_var = ultimate_usage_resource_L1_total_amount + total_expense_var + total_store_var

            resource_usage[resoures_level_1_record.Resource_Code_L1] = total_resourse_cost_var
            total_sum_assembly_resource_code_amount_var = total_sum_assembly_resource_code_amount_var + total_resourse_cost_var
        resource_usage['total_sum_assembly_resource_code_amount_var'] = total_sum_assembly_resource_code_amount_var
        return resource_usage
    




    def earned_cost_by_resource_list(self):
        from companyApp.models import Resource_Code_L1_Table
        filter_resoures_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=self.main_contract.company_details)
        resource_usage = {}
        
        total_quantity = MainContractInvoiceDetailsTable.objects.filter(
            main_contract_invoice__invoice_contract_row = self.main_contract,
            main_contract_assembly__assembly_row = self.assembly_row,
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        if total_quantity:
            total_quantity = float(total_quantity)
        else:
            total_quantity = 0
        
        print(f"total_quantity: {total_quantity}")
        print(f"total assembly amount: {self.assembly_row.Assembly_Unit_Cost}")

        total_actual_earned_cost_var = 0
        for resoures_level_1_record in filter_resoures_level_1:

            resourse_unit_cost = Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Company_Details=self.main_contract.company_details,
                Estimation_Assemblies=self.assembly_row,
                Resource_record__Resource_Code_L1=resoures_level_1_record
            ).aggregate(total=Sum('Unit_Cost'))['total'] or 0


            if resourse_unit_cost:
                resourse_unit_cost = float(resourse_unit_cost)
            else:
                resourse_unit_cost = 0

            resource_earned_amount = resourse_unit_cost * total_quantity



            resource_usage[resoures_level_1_record.Resource_Code_L1] = resource_earned_amount
            total_actual_earned_cost_var = total_actual_earned_cost_var + resource_earned_amount
            
        resource_usage['total_actual_earned_cost_var'] = total_actual_earned_cost_var

        return resource_usage


    def contract_budget_unit_rates_calculation(self):
        from companyApp.models import Resource_Code_L1_Table
        filter_resoures_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=self.main_contract.company_details)
        resource_usage = {}

        total_actual_earned_cost_var = 0
        for resoures_level_1_record in filter_resoures_level_1:

            resourse_unit_cost = Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Company_Details=self.main_contract.company_details,
                Estimation_Assemblies=self.assembly_row,
                Resource_record__Resource_Code_L1=resoures_level_1_record
            ).aggregate(total=Sum('Unit_Cost'))['total'] or 0

            resource_usage[resoures_level_1_record.Resource_Code_L1] = resourse_unit_cost
            total_actual_earned_cost_var = total_actual_earned_cost_var + resourse_unit_cost
        if total_actual_earned_cost_var:
            total_actual_earned_cost_var = round(total_actual_earned_cost_var, 2)
        resource_usage['total_budget_unit_rates_var'] = total_actual_earned_cost_var

        return resource_usage



    def contract_resource_budget_cost_calculation(self):
        from companyApp.models import Resource_Code_L1_Table
        filter_resoures_level_1 = Resource_Code_L1_Table.objects.filter(Company_Details=self.main_contract.company_details)
        resource_usage = {}

        budget_quantity = self.budget_quantity

        total_actual_earned_cost_var = 0
        for resoures_level_1_record in filter_resoures_level_1:

            resourse_unit_cost = Estimation_Assemblies_Resource_Details_Table.objects.filter(
                Company_Details=self.main_contract.company_details,
                Estimation_Assemblies=self.assembly_row,
                Resource_record__Resource_Code_L1=resoures_level_1_record
            ).aggregate(total=Sum('Unit_Cost'))['total'] or 0

            resource_budget_cost = resourse_unit_cost * float(budget_quantity)
            resource_budget_cost = round(resource_budget_cost, 2)

            resource_usage[resoures_level_1_record.Resource_Code_L1] = resource_budget_cost
            total_actual_earned_cost_var = total_actual_earned_cost_var + resource_budget_cost
            
        total_actual_earned_cost_var = round(total_actual_earned_cost_var, 2)
        resource_usage['total_sum_budget_cost_var'] = total_actual_earned_cost_var

        return resource_usage

    def contract_resource_variance_to_date_calculation(self):
        # Get resource budget cost
        resource_budget_costs = self.contract_resource_budget_cost_calculation()
        
        # Get subcontract costs
        subcontract_costs = self.actual_cost_subcontracts_resource_list()
        
        # Calculate the difference for each resource_level_1
        cost_difference = {}
        
        for resource_level_1 in resource_budget_costs.keys():
            if resource_level_1 != 'total_sum_budget_cost_var':  # Exclude the total key
                budget_cost = resource_budget_costs.get(resource_level_1, 0)
                subcontract_cost = subcontract_costs.get(resource_level_1, 0)
                cost_difference[resource_level_1] = round(budget_cost - subcontract_cost, 2)
        
        # Add total difference if needed
        total_budget_cost = resource_budget_costs.get('total_sum_budget_cost_var', 0)
        total_subcontract_cost = subcontract_costs.get('total_sum_calculate_usage_amount', 0)
        cost_difference['contract_resource_variance_to_date_value'] = round(total_budget_cost - total_subcontract_cost, 2)
        return cost_difference


    def contract_resource_estimate_at_completion_calculation(self):
        contract_remain_quantity = self.calculate_remaining_quantity()
        contract_budget_unit_rates = self.contract_budget_unit_rates_calculation()
        actual_resource_code_expense_total = self.actual_cost_total_resource_code_calculation()

        context_estimate_at_completion_EAC = {}
        estimate_at_completion_total_sum = 0
        for resource_level_1 in actual_resource_code_expense_total.keys():
            if resource_level_1 != 'total_sum_assembly_resource_code_amount_var':  
                budget_unit_rates = contract_budget_unit_rates.get(resource_level_1, 0)
                actual_resource_code_cost = actual_resource_code_expense_total.get(resource_level_1, 0)

                budget_cost = float(budget_unit_rates) * float(contract_remain_quantity)
                estimate_at_completion = budget_cost + actual_resource_code_cost

                context_estimate_at_completion_EAC[resource_level_1] = round(estimate_at_completion, 2)

            estimate_at_completion_total_sum = estimate_at_completion_total_sum + estimate_at_completion

        context_estimate_at_completion_EAC['sum_total_estimate_at_completion_cost'] = round(estimate_at_completion_total_sum, 2)

        return context_estimate_at_completion_EAC


    def contract_ETC_remaining_calculation(self):
        # Get resource budget cost
        resource_estimate_at_completion_costs = self.contract_resource_estimate_at_completion_calculation()
        
        # Get subcontract costs
        subcontract_costs = self.actual_cost_subcontracts_resource_list()
        
        # Calculate the difference for each resource_level_1
        cost_difference = {}
        
        for resource_level_1 in resource_estimate_at_completion_costs.keys():
            if resource_level_1 != 'sum_total_estimate_at_completion_cost':  # Exclude the total key
                estimate_at_completion_cost = resource_estimate_at_completion_costs.get(resource_level_1, 0)
                subcontract_cost = subcontract_costs.get(resource_level_1, 0)
                cost_difference[resource_level_1] = round(estimate_at_completion_cost - subcontract_cost, 2)
        
        # Add total difference if needed
        total_estimate_at_completion_cost = resource_estimate_at_completion_costs.get('sum_total_estimate_at_completion_cost', 0)
        total_subcontract_cost = subcontract_costs.get('total_sum_calculate_usage_amount', 0)
        cost_difference['contract_ETC_remaining_value'] = round(total_estimate_at_completion_cost - total_subcontract_cost, 2)
        return cost_difference


    def contract_VAC_remaining_calculation(self):
        # Get resource budget cost
        resource_budget_costs = self.contract_resource_budget_cost_calculation()
        
        # Get EAC_cost costs
        EAC_cost = self.contract_resource_estimate_at_completion_calculation()
        
        # Calculate the difference for each resource_level_1
        cost_difference = {}
        
        for resource_level_1 in resource_budget_costs.keys():
            if resource_level_1 != 'total_sum_budget_cost_var':  
                budget_cost = resource_budget_costs.get(resource_level_1, 0)
                get_EAC_cost = EAC_cost.get(resource_level_1, 0)
                cost_difference[resource_level_1] = round(budget_cost - get_EAC_cost, 2)
        
        # Add total difference if needed
        total_budget_cost = resource_budget_costs.get('total_sum_budget_cost_var', 0)
        total_get_EAC_cost = EAC_cost.get('sum_total_estimate_at_completion_cost', 0)
        cost_difference['contract_VAC_remaining_value'] = round(total_budget_cost - total_get_EAC_cost, 2)
        return cost_difference


    def calculate_assembly_cpi_value(self):
        earned_cost_data = self.earned_cost_by_resource_list()
        total_actual_earned_cost = earned_cost_data.get('total_actual_earned_cost_var', 0)

        print(f"Total Actual Earned Cost: {total_actual_earned_cost}")

        actual_cost_data = self.actual_cost_total_resource_code_calculation()
        total_actual_cost = actual_cost_data.get('total_sum_assembly_resource_code_amount_var', 0)

        try:
            var_cpi_value = total_actual_earned_cost / total_actual_cost
        except:
            var_cpi_value = 0

        
        return round(var_cpi_value, 2)


    def calculate_assembly_tcpi_value(self):
        budget_costs = self.budget_costs

        earned_cost_data = self.earned_cost_by_resource_list()
        total_actual_earned_cost = earned_cost_data.get('total_actual_earned_cost_var', 0)

        actual_cost_data = self.actual_cost_total_resource_code_calculation()
        total_actual_cost = actual_cost_data.get('total_sum_assembly_resource_code_amount_var', 0)

        try:
            var_tcpi_value = (budget_costs - total_actual_earned_cost) / (budget_costs - total_actual_cost)
        except:
            var_tcpi_value = 0

        
        return round(var_tcpi_value, 2)
    




    
        


class MainContractInvoiceTable(models.Model):
    invoice_contract_row = models.ForeignKey(MainContract, on_delete=models.CASCADE, related_name="contract_invoices")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def filter_MainContractInvoiceDetails(self):
        return MainContractInvoiceDetailsTable.objects.filter(main_contract_invoice=self)



class MainContractInvoiceDetailsTable(models.Model):
    main_contract_invoice = models.ForeignKey(MainContractInvoiceTable, on_delete=models.CASCADE, related_name="contract_details_invoice_details")
    main_contract_assembly = models.ForeignKey(MainContractDetail, on_delete=models.CASCADE, related_name="contract_details_invoice")
    
    Invoice_Quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Invoice Quantity")
    Invoice_Revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Invoice Revenue")
    
    Next_Remain_Quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Invoice Quantity", default=None, blank=True, null=True)
    Next_Remain_Revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Invoice Revenue", default=None, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class MainContractBudgetCostTable(models.Model):
    company_details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Company Details")
    contract_details = models.ForeignKey(MainContractDetail, on_delete=models.CASCADE)
    Resource_Code = models.ForeignKey(CompanyResourcesTable, on_delete=models.CASCADE)
    budget_unit_rates = models.CharField(max_length=255)
    budget_cost = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class SubContractTable(models.Model):
    company_details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Company Details")
    contract_value = models.ForeignKey('contractApp.MainContract', on_delete=models.CASCADE, default=None)
    subcontract_name = models.CharField(max_length=255, verbose_name="Contract Name")
    contract_total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Budget Cost", null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subcontract_name} - {self.company_details}"

    def filter_sub_contract_details(self):
        return SubContractDetail.objects.filter(sub_contract=self)

    def get_subcontract_total_price(self):
        related_details = self.filter_sub_contract_details()
        total = related_details.aggregate(Sum('subcontract_total_price'))['subcontract_total_price__sum'] or 0
        return round(total, 2)
    
    def get_subcontract_total_unit_cost(self):
        related_details = self.filter_sub_contract_details()
        total = related_details.aggregate(Sum('unit_cost'))['unit_cost__sum'] or 0
        return round(total, 2)

    def get_subcontract_total_quantity(self):
        related_details = self.filter_sub_contract_details()
        total = related_details.aggregate(Sum('subcontract_quantity'))['subcontract_quantity__sum'] or 0
        return round(total, 2)

    def main_subcontract_details_query(self):
        get_details_contract = SubContractDetail.objects.filter(sub_contract=self)
        
        return get_details_contract
    
    def main_subcontract_details_query_count(self):
        get_details_contract_count = SubContractDetail.objects.filter(sub_contract=self).count()
        return get_details_contract_count

    def calculate_total_price(self):
        total = self.details.aggregate(Sum('subcontract_total_price'))['subcontract_total_price__sum']
        if total:
            total = round(total, 2)
        else:
            total = 0.00
        return total if total is not None else 0



class SubContractDetail(models.Model):
    sub_contract = models.ForeignKey(SubContractTable, on_delete=models.CASCADE, related_name="details")
    comb_assem_code = models.CharField(max_length=50, verbose_name="Combination Assembly Code")
    assembly_value = models.ForeignKey('assembliesApp.Estimation_Assemblies_Table', on_delete=models.CASCADE)
    item_description = models.TextField(verbose_name="Item Description")
    unit = models.CharField(max_length=50, verbose_name="Unit")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Cost")
    subcontract_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="SubContract Contract Quantity")
    subcontract_total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subcontract Total Price")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Detail for {self.sub_contract.subcontract_name} - Unit: {self.unit}"

    def func_SubContract_Invoices_total_quantity(self):
        total_quantity = SubContractInvoiceDetailsTable.objects.filter(
            sub_contract_assembly=self
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        return total_quantity or 0

    def func_SubContract_Invoices_total_revenue(self):
        total_revenue = SubContractInvoiceDetailsTable.objects.filter(
            sub_contract_assembly=self
        ).aggregate(total_revenue=Sum('Invoice_Revenue'))['total_revenue']
        return total_revenue or 0

    def calculate_percentage_of_contract_quantity(self):
        total_quantity = self.func_SubContract_Invoices_total_quantity()
        if total_quantity == 0 or self.subcontract_quantity == 0:
            return 0  # Avoid division by zero
        percentage = (total_quantity / self.subcontract_quantity) * 100
        rounded_percentage = round(percentage, 2)
        print(rounded_percentage)
        return rounded_percentage

    def filter_subcontract_invoices(self):
        filter_subcontract_invoice = SubContractInvoiceTable.objects.filter(
            invoice_contract_row=self.sub_contract
        )
        return filter_subcontract_invoice

    def calculate_remaining_quantity(self):
        total_quantity = self.func_SubContract_Invoices_total_quantity()
        remaining_quantity = self.subcontract_quantity - total_quantity
        return remaining_quantity

    def func_Assembly_Invoices_total_quantity(self):
        total_quantity = SubContractInvoiceDetailsTable.objects.filter(
            sub_contract_assembly=self
        ).aggregate(total_quantity=Sum('Invoice_Quantity'))['total_quantity']
        return total_quantity or 0
    
    def func_Assembly_Invoices_total_revenue(self):
        total_revenue = SubContractInvoiceDetailsTable.objects.filter(
            sub_contract_assembly=self
        ).aggregate(total_revenue=Sum('Invoice_Revenue'))['total_revenue']
        if total_revenue:
            total_revenue = round(total_revenue,  2)
        return total_revenue or 0

    def func_Assembly_Invoices_remain_revenue(self):
        total_price = self.subcontract_total_price
        earned_invoice_price = self.func_Assembly_Invoices_total_revenue()
        remaining_quantity = total_price - earned_invoice_price
        return remaining_quantity

    





class SubContractInvoiceTable(models.Model):
    invoice_contract_row = models.ForeignKey(SubContractTable, on_delete=models.CASCADE, related_name="contract_invoices")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def filter_SubContractInvoiceDetails(self):
        return SubContractInvoiceDetailsTable.objects.filter(sub_contract_invoice=self)



class SubContractInvoiceDetailsTable(models.Model):
    sub_contract_invoice = models.ForeignKey(SubContractInvoiceTable, on_delete=models.CASCADE, related_name="contract_details_invoice_details")
    sub_contract_assembly = models.ForeignKey(SubContractDetail, on_delete=models.CASCADE, related_name="contract_details_invoice")
    Invoice_Quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Invoice Quantity")
    Invoice_Revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Invoice Revenue")

    Next_Remain_Quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Invoice Quantity", default=None, blank=True, null=True)
    Next_Remain_Revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Invoice Revenue", default=None, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)