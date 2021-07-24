from django.urls import path

from apps.sales import views

urlpatterns = [
    path('', views.sales_dashboard, name='sales_dashboard')
]