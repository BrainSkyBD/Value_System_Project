from django.urls import path, include
from . import views

urlpatterns = [
    # adding users
    path('create_contract/', views.create_contract, name="create_contract"),
    path('save-contract/', views.save_contract, name='save_contract'),
    path('contract-list/', views.contract_list, name='contract_list'),
    path('contract/<int:contract_id>/', views.view_contract, name='view_contract'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('contract/delete/<int:contract_id>/', views.delete_contract, name='delete_contract'),

    path('contract-edit/<int:contract_id>/', views.edit_contract, name='edit_contract'),
    path('save-edit-contract/', views.save_edit_contract, name='save_edit_contract'),
    path('delete-contract-row/<int:row_id>/', views.delete_contract_row, name='delete_contract_row'),


    path('Contract_Management/', views.Contract_Management_main, name="Contract_Management"),
    path('contract_assembly_resource_details_management/', views.contract_assembly_resource_details_management, name="contract_assembly_resource_details_management"),

    # subcontracts
    path('create_subcontract/', views.create_subcontract, name="create_subcontract"),
    path('save_subcontract/', views.save_subcontract, name="save_subcontract"),
    path('subcontract_list/', views.subcontract_list, name='subcontract_list'),
    
    path('subcontract/<int:subcontract_id>/', views.view_subcontract, name='view_subcontract'),
    path('subcontract_create_invoice/', views.subcontract_create_invoice, name='subcontract_create_invoice'),
    path('subcontract/delete/<int:subcontract_id>/', views.delete_subcontract, name='delete_subcontract'),

    path('SubContract_Management/', views.SubContract_Management_main, name="SubContract_Management"),
]