from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('account-settings/', views.account_settings, name="account_settings"),
    path('account_settings_notification/', views.account_settings_notification, name="account_settings_notification"),
    path('account_settings_connections/', views.account_settings_connections, name="account_settings_connections"),
]