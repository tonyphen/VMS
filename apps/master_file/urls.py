from django.urls import path

from apps.master_file import views

urlpatterns = [
    path('', views.wood_definition, name='wood_definition'),
    path('profilemaster/', views.profile_master, name='profile_master'),
]