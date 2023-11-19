from django.urls import path
from . import views  # Import your views module


urlpatterns = [
    # Define the URL pattern for start_face_recognition
    path('start_face_recognition/<int:event_id>/', views.start_face_recognition, name='start_face_recognition'),
]

