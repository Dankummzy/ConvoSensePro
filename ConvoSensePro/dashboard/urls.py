# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    # Add more URL patterns for other dashboard sections if needed
]
