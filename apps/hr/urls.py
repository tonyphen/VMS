from django.urls import path
from apps.hr.models import HealthCheck, HealthCheckItem, Department
from apps.hr import views


urlpatterns = [
    path('', views.hc_list, name='hc_list'),
    path('add/', views.hc_create, name='hc_create'),
    path('<int:id>/update/', views.hc_update, name='hc_update'),
    path('<int:id>/delete/', views.hc_delete, name='hc_delete'),
    path('detail/<int:hc_id>/', views.hc_items, name='hc_items'),
    path('detail/<int:hc_id>/create/', views.hc_item_create, name='hc_item_create'),
    path('detail/<int:hc_id>/update/<int:id>/', views.hc_item_update, name='hc_item_update'),
]