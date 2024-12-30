from django.urls import path, include
from . import views


urlpatterns = [
    path('calculate-expenses/', views.calculate_expenses, name="calculate_expenses"),
    path('fetch_assemblies_by_contract/<int:contract_id>/', views.fetch_assemblies_by_contract, name='fetch_assemblies_by_contract'),
    path('fetch_resorce_by_assemblies/<int:assembly_id>/', views.fetch_resorce_by_assemblies, name='fetch_resorce_by_assemblies'),
    path('save-expense/', views.save_expense, name='save_expense'),

    path("expenses/", views.expense_list, name="expense_list"),
    path("expenses/delete/<int:pk>/", views.delete_expense, name="delete_expense"),

    path('expenses_management/', views.expenses_management, name="expenses_management"),
]