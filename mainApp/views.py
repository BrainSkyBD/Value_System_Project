from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index(request):
    return redirect('dashboard')

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def account_settings(request):
    return render(request, "account_settings.html")
    
@login_required
def account_settings_notification(request):
    return render(request, "account_settings_notification.html")
    
@login_required
def account_settings_connections(request):
    return render(request, "account_settings_connections.html")