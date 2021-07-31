from django.urls import path

from apps.master_file import views

urlpatterns = [
    path('wd/', views.wood_definition, name='wood_definition'),
    path('size/', views.size, name='size'),
    path('mf_upload/', views.master_file_upload, name='master_file_upload'),

    path('profilemaster/create/', views.profile_master_create, name='profile_master_create'),
    path('profilemaster/update/<str:id>/', views.profile_master_update, name='profile_master_update'),
    path('profilemaster/delete/<str:id>/', views.profile_master_delete, name='profile_master_delete'),

    path('profile/create/', views.profile_create, name='profile_create'),
    path('profile/update/<str:id>/', views.profile_update, name='profile_update'),
    path('profile/delete/<str:id>/', views.profile_delete, name='profile_delete'),

    path('wt/create/', views.wood_type_create, name='wood_type_create'),
    path('wt/update/<str:id>/', views.wood_type_update, name='wood_type_update'),
    path('wt/delete/<str:id>/', views.wood_type_delete, name='wood_type_delete'),

    path('sg/create/', views.sort_group_create, name='sort_group_create'),
    path('sg/update/<str:id>/', views.sort_group_update, name='sort_group_update'),
    path('sg/delete/<str:id>/', views.sort_group_delete, name='sort_group_delete'),

    path('length/create/', views.length_create, name='length_create'),
    path('length/update/<int:id>/', views.length_update, name='length_update'),
    path('length/delete/<int:id>/', views.length_delete, name='length_delete'),

    path('thick/create/', views.thick_create, name='thick_create'),
    path('thick/update/<int:id>/', views.thick_update, name='thick_update'),
    path('thick/delete/<int:id>/', views.thick_delete, name='thick_delete'),

    path('ls/create/', views.log_scale_create, name='log_scale_create'),
    path('ls/update/<int:id>/', views.log_scale_update, name='log_scale_update'),
    path('ls/delete/<int:id>/', views.log_scale_delete, name='log_scale_delete'),



]
