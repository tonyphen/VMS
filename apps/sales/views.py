from django.shortcuts import render

# Create your views here.

def sales_dashboard(request):
    return render(request, 'sales/sales_dashboard.html')
