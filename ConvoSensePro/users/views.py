# users/views.py
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm  # Import your custom registration form
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import FaceImageForm
from django.conf import settings
from django.contrib import messages
from .models import User
import cv2
import os
import time

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64 


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if a user with the same username already exists
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
            else:
                form.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('dashboard')  # Redirect to the user dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')  # Redirect to the user dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('users:login')


@login_required
def profile(request):
    # Implement user profile management views (e.g., updating profile picture)
    return render(request, 'registration/profile.html')


@login_required
def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=user_profile)
        face_image_form = FaceImageForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and face_image_form.is_valid():
            user_form.save()
            face_image_form.save()
            return redirect('dashboard')  # Redirect to the dashboard after editing
            
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        face_image_form = FaceImageForm(instance=user_profile)

    return render(request, 'users/edit_profile.html', {'user_form': user_form, 'face_image_form': face_image_form})


@login_required
def submit_face_image(request):
    if request.method == 'POST':
        try:
            for capture_count in range(3):
                image_data_uri = request.POST.get('image_data')

                # Call the capture_face_images function to save the images
                capture_face_images(request, capture_count, image_data_uri)

            return JsonResponse({'success': True, 'message': 'Images saved successfully.'})
        except Exception as e:
            # Handle the error and return an error response
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return render(request, 'users/submit_face_image.html')


def capture_face_images(request, capture_count, image_data_uri):
    try:
        # Decode the base64 image data
        image_data = base64.b64decode(image_data_uri.split(',')[1])

        # Get the username from the request
        username = request.user.username

        # Create a directory to store user's face images if it doesn't exist
        image_dir = os.path.join(settings.MEDIA_ROOT, 'user_faces', username)
        os.makedirs(image_dir, exist_ok=True)

        # Save the captured image with a unique filename
        image_filename = os.path.join(image_dir, f'{username}_{capture_count}.jpg')
        with open(image_filename, 'wb') as image_file:
            image_file.write(image_data)

    except Exception as e:
        # Handle the error gracefully, log it, and notify the user if necessary
        print(f"An error occurred while capturing images: {str(e)}")
        # You can add further error handling or user notifications here.



