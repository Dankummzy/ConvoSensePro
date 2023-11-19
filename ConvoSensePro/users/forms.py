# users/forms.py
from django import forms
from .models import UserProfile
from users.models import User  # Import your custom User model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Use your custom User model
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class FaceImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['face_image']
        

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Include the fields you want to update


