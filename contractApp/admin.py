from django.contrib import admin
from .models import MainContract, MainContractDetail, MainContractBudgetCostTable, SubContractTable, SubContractDetail, MainContractInvoiceTable

from .models import MainContractInvoiceTable, MainContractInvoiceDetailsTable, SubContractInvoiceTable, SubContractInvoiceDetailsTable


@admin.register(MainContractInvoiceTable)
class MainContractInvoiceTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_contract_row', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('invoice_contract_row__id',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(MainContractInvoiceDetailsTable)
class MainContractInvoiceDetailsTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'main_contract_invoice', 'main_contract_assembly', 'Invoice_Quantity', 'Invoice_Revenue', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('main_contract_invoice__id', 'main_contract_assembly__id')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'




@admin.register(SubContractInvoiceTable)
class SubContractInvoiceTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_contract_row', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('invoice_contract_row__id',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(SubContractInvoiceDetailsTable)
class SubContractInvoiceDetailsTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_contract_invoice', 'sub_contract_assembly', 'Invoice_Quantity', 'Invoice_Revenue', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('sub_contract_invoice__id', 'sub_contract_assembly__id')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'




class MainContractDetailInline(admin.TabularInline):
    model = MainContractDetail
    extra = 1
    fields = (
        'comb_assem_code',
        'assembly_name',
        'item_description',
        'unit',
        'unit_cost',
        'budget_quantity',
        'budget_costs',
        'markup',
        'markup_amount',
        'unit_price',
        'total_price',
        'target_profit',
    )
    readonly_fields = ('markup_amount', 'unit_price', 'total_price', 'target_profit')
    show_change_link = True

@admin.register(MainContract)
class MainContractAdmin(admin.ModelAdmin):
    list_display = ('contract_name', 'company_details')
    search_fields = ('contract_name', 'company_details__name')
    inlines = [MainContractDetailInline]

@admin.register(MainContractDetail)
class MainContractDetailAdmin(admin.ModelAdmin):
    list_display = (
        'main_contract',
        'comb_assem_code',
        'assembly_name',
        'unit',
        'unit_cost',
        'budget_quantity',
        'budget_costs',
        'markup',
        'markup_amount',
        'unit_price',
        'total_price',
        'target_profit',
    )
    search_fields = ('main_contract__contract_name', 'comb_assem_code', 'assembly_name')
    list_filter = ('main_contract', 'unit')
    readonly_fields = ('markup_amount', 'unit_price', 'total_price', 'target_profit')


class SubContractDetailInline(admin.TabularInline):
    model = SubContractDetail
    extra = 1

@admin.register(SubContractTable)
class SubContractTableAdmin(admin.ModelAdmin):
    list_display = ('subcontract_name', 'company_details', 'contract_value', 'contract_total_price')
    inlines = [SubContractDetailInline]

@admin.register(SubContractDetail)
class SubContractDetailAdmin(admin.ModelAdmin):
    list_display = ('sub_contract', 'comb_assem_code', 'assembly_value', 'item_description', 'unit', 'unit_cost', 'subcontract_quantity', 'subcontract_total_price')
    list_filter = ('sub_contract', 'assembly_value')
    search_fields = ('comb_assem_code', 'item_description', 'unit')

    

@admin.register(MainContractBudgetCostTable)
class MainContractBudgetCostAdmin(admin.ModelAdmin):
    list_display = ('contract_details', 'Resource_Code', 'budget_unit_rates', 'budget_cost', 'created_at', 'updated_at')
    list_filter = ('contract_details', 'Resource_Code', 'created_at', 'updated_at')
    search_fields = ('contract_details__name', 'Resource_Code__name', 'budget_unit_rates', 'budget_cost')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


