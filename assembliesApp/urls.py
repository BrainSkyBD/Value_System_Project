from django.urls import path, include
from . import views


urlpatterns = [
    path('estimate-assemblies/', views.estimate_assemblies, name="estimate_assemblies"),
    path('company_assembly_record', views.company_assembly_record, name="company_assembly_record"),
    path('assemblies_list', views.assemblies_list, name="assemblies_list"),
    path('edit_assembly/<int:pk>/', views.edit_assembly, name="edit_assembly"),
    path('assemblies_Delete/<int:pk>/', views.assemblies_Delete, name="assemblies_Delete"),

# wewe
    path('Assemblies_Code_L1_module/', views.Assemblies_Code_L1_module, name="Assemblies_Code_L1_module"),
    path('Assemblies_Code_L2_module/', views.Assemblies_Code_L2_module, name="Assemblies_Code_L2_module"),
    path('Assemblies_Code_L3_module/', views.Assemblies_Code_L3_module, name="Assemblies_Code_L3_module"),

    path('get-Assemblies-code-l2/', views.get_Assemblies_code_l2, name='get_Assemblies_code_l2'),
    path('get-Assemblies-code-l3/', views.get_Assemblies_code_l3, name='get_Assemblies_code_l3'),

    
    path('Assemblies_Desplay/', views.Assemblies_Desplay, name="Assemblies_Desplay"),
    path('Assemblies_Management/', views.Assemblies_Management, name="Assemblies_Management"),
    
]