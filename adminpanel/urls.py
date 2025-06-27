# adminpanel/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('assign/<int:complaint_id>/', views.assign_worker, name='assign_worker'),
    path('add-worker/', views.add_worker, name='add_worker'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
]
