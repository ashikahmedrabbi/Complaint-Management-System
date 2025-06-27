# user/urls.py
from django.urls import path
from .views import submit_complaint

urlpatterns = [
    path('', submit_complaint, name='submit_complaint'),
]
