# attendance/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('event_attendance/<int:event_id>/', views.event_attendance, name='event_attendance'),
]


