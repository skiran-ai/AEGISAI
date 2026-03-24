from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # User auth
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    # User modules
    path('update-profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('feedback/', views.my_feedback, name='my_feedback'),
    path('feedback/delete/<int:pk>/', views.delete_feedback, name='delete_feedback'),
    path('reports/', views.user_reports, name='user_reports'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),

    # File share
    path('fileshare/', views.file_share, name='file_share'),
    path('file-inbox/', views.file_inbox, name='file_inbox'),
    path('download/<int:pk>/', views.download_file, name='download_file'),

    # Admin auth
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-police/', views.admin_police, name='admin_police'),
    path('admin-incidents/', views.admin_incidents, name='admin_incidents'),
    path('admin-incidents/<int:pk>/', views.admin_incident_detail, name='admin_incident_detail'),
    path('admin-feedback/', views.admin_feedback, name='admin_feedback'),
    path('admin-threats/', views.admin_threats, name='admin_threats'),
    path('admin-dashboard/toggle-suspend/<int:user_id>/', views.toggle_suspend_user, name='toggle_suspend_user'),

    # Police auth
    path('police-register/', views.police_register, name='police_register'),
    path('police-login/', views.police_login, name='police_login'),
    path('police-dashboard/', views.police_dashboard, name='police_dashboard'),
    path('police-reports/', views.police_reports, name='police_reports'),
    path('police-reports/<int:pk>/', views.police_report_detail, name='police_report_detail'),
    path('police-threats/', views.police_threats, name='police_threats'),

    # Logout
    path('logout/', views.user_logout, name='logout'),
]
