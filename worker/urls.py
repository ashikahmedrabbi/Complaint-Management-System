# worker/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('complaint/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
]
