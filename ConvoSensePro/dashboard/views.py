# dashboard/views.py
from django.shortcuts import render
from users.models import UserProfile
from django.conf import settings
from django.contrib.auth.decorators import login_required
from events.models import Event



@login_required
def dashboard(request):
    # Retrieve user-specific data (event registrations, attendance history, etc.)
    user = request.user
    user_profile = request.user.userprofile 
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    
    created_events = Event.objects.filter(organizer=request.user)

    # Retrieve events the user has registered for
    registered_events = Event.objects.filter(attendees=user)
    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'user_profile': user_profile,  # You can pass the entire user profile as well
        'created_events': created_events,
        'registered_events': registered_events
    } 
    
     
    return render(request, 'dashboard/dashboard.html', user_data)

