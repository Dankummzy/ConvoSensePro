# users/urls.py
from django.urls import path
from . import views


app_name = 'users'


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Add this line for login
    path('logout/', views.logout_view, name='logout'),  # Add this line for login
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('submit_face_image/', views.submit_face_image, name='submit_face_image'),
]

