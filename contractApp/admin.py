from django.contrib import admin
from .models import MainContract, MainContractDetail
from .models import SubContractTable, SubContractDetail


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