from django.urls import path

from apps.master_file import views

urlpatterns = [
    path('', views.wood_definition, name='wood_definition'),
    path('wd_upload/', views.wdefinition_upload, name='wdefinition_upload'),
    path('profilemaster/', views.profile_master, name='profile_master'),
]
