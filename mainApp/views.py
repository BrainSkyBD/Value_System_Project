from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
import plotly.graph_objs as go
from contractApp.models import MainContract


@login_required
def index(request):
    return redirect('dashboard')

@login_required
def dashboard(request):
    # Calculate total company revenue and total actual costs
    total_revenue = 0
    total_actual_costs = 0

    contracts = MainContract.objects.filter(company_details = request.user.company_details)
    for contract in contracts:
        total_revenue += contract.func_mainContract_total_Invoices_total_revenue()
        total_actual_costs += contract.calculate_total_actual_cost()

    # Create a bar chart
    labels = ['Total Company Revenue', 'Total Actual Costs']
    values = [total_revenue, total_actual_costs]
    bar_chart = go.Figure(data=[
        go.Bar(x=labels, y=values, marker=dict(color=['#1f77b4', '#ff7f0e']))
    ])
    bar_chart.update_layout(
        title='Total Company Revenue vs Total Actual Costs',
        xaxis_title='Metrics',
        yaxis_title='Amount',
        template='plotly_white'
    )

    # Convert plotly graph to HTML
    graph_html = bar_chart.to_html(full_html=False)

    print(f"Total Revenue: {total_revenue}, Total Actual Costs: {total_actual_costs}")
    # print(graph_html)
    
    context = {
        'graph_html': graph_html
    }
    return render(request, "dashboard.html", context)

@login_required
def account_settings(request):
    return render(request, "account_settings.html")
    
@login_required
def account_settings_notification(request):
    return render(request, "account_settings_notification.html")
    
@login_required
def account_settings_connections(request):
    return render(request, "account_settings_connections.html")