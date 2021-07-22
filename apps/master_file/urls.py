from django.urls import path

from apps.master_file import views

urlpatterns = [
    path('profilemaster/', views.profile_master, name='profile_master'),
]