from django.urls import path, include
from . import views

urlpatterns = [
    # adding users
    path('create_contract/', views.create_contract, name="create_contract"),
    path('save-contract/', views.save_contract, name='save_contract'),
    path('contract-list/', views.contract_list, name='contract_list'),
    path('contract/<int:contract_id>/', views.view_contract, name='view_contract'),
    path('contract/delete/<int:contract_id>/', views.delete_contract, name='delete_contract'),

    path('Contract_Management/', views.Contract_Management, name="Contract_Management"),

    # subcontracts
    path('create_subcontract/', views.create_subcontract, name="create_subcontract"),
    path('save_subcontract/', views.save_subcontract, name="save_subcontract"),
    path('subcontract_list/', views.subcontract_list, name='subcontract_list'),

    path('SubContract_Management/', views.SubContract_Management, name="SubContract_Management"),
]