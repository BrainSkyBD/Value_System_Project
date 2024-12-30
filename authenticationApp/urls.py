from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.login_func, name="login_func"),
    path('signup/', views.signup_func, name="signup_func"),
    path("logout_func/", views.logout_func, name="logout_func"),
]