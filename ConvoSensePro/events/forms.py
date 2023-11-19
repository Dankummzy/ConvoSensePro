# events/forms.py
from django import forms
from .models import Event 
from django.contrib.auth.forms import UserCreationForm
from users.models import User 


class EventForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'}),
        input_formats=['%d/%m/%Y'],  # Specify the desired date format (day/month/year)
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'placeholder': 'HH:MM'}),
        input_formats=['%H:%M'],  # Specify the desired time format (hour:minute)
    )

    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'description', 'location', 'capacity']  # Include all fields from the Event model
    


class RegistrationForm(UserCreationForm):
    event = forms.ModelChoiceField(queryset=Event.objects.all())  # Event selection field

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    



