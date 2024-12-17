from django.urls import path, include
from . import views


urlpatterns = [
    # adding users
    path('create-user/', views.create_user, name="create_user"),
    path('user_list', views.user_list, name="user_list"),
    # company
    path('company-settings/', views.company_settings, name="company_settings"),
    path('company-subscription/', views.company_subscription, name="company_subscription"),

    # project
    path('create-project/', views.create_project, name="create_project"),
    path('list-project/', views.list_project, name="list_project"),

    path('Resource_Code_L1_module/', views.Resource_Code_L1_module, name="Resource_Code_L1_module"),
    path('Resource_Code_L2_module/', views.Resource_Code_L2_module, name="Resource_Code_L2_module"),
    path('Resource_Code_L3_module/', views.Resource_Code_L3_module, name="Resource_Code_L3_module"),

    path('get-resource-code-l2/', views.get_resource_code_l2, name='get_resource_code_l2'),
    path('get-resource-code-l3/', views.get_resource_code_l3, name='get_resource_code_l3'),

    # resource dictionary
    path('Create-Resource-Dictionary/', views.Create_Resource_Dictionary, name="Create_Resource_Dictionary"),
    path('List-Resource-Dictionary/', views.List_Resource_Dictionary, name="List_Resource_Dictionary"),
    path('Resource_Desplay/', views.Resource_Desplay, name="Resource_Desplay"),
    path('Resource_Management/', views.Resource_Management, name="Resource_Management"),
]