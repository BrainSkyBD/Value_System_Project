from django.urls import path, include
from . import views


urlpatterns = [
    path('calculate-stores/', views.calculate_stores, name="calculate_stores"),
    path('fetch_assemblies_by_contract/<int:contract_id>/', views.fetch_assemblies_by_contract, name='fetch_assemblies_by_contract'),
    path('store_fetch_resorce_by_assemblies/<int:assembly_id>/', views.fetch_resorce_by_assemblies, name='fetch_resorce_by_assemblies'),
    path('save-store/', views.save_store, name='save_store'),

    path("stores/", views.store_list, name="store_list"),
    path("stores/delete/<int:pk>/", views.delete_store, name="delete_store"),
    
    path("stock_in_list/", views.stock_in_list, name="stock_in_list"),
    path("stock_out_list/", views.stock_out_list, name="stock_out_list"),

    path('store_management', views.store_management, name="store_management"),
]