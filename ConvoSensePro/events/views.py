# events/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from facerecognition.recognize_faces import recognize_attendance
from notifications.utils import send_notification_email
from django.conf import settings
from .forms import RegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from users.forms import FaceImageForm# Import the FaceImageForm from the users app
from django.contrib import messages
from users.models import User
from django.http import HttpResponse
from .forms import EventForm, RegistrationForm
from django.template.loader import render_to_string
from users.views import submit_face_image

from attendance.models import AttendanceRecord
from users.decorators import organizer_required


@login_required
def event_list(request):
    events = Event.objects.all()  # Fetch all events from the database
    return render(request, 'events/event_list.html', {'events': events})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Set the event organizer
            event.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user == event.organizer:
        event.delete()
    return redirect('event_list')


def register_for_event(request, event_uuid):
    event = Event.objects.get(unique_link=event_uuid)

    if request.method == 'POST':
        if event.is_full():
            messages.error(request, "Sorry, this event is already full.")
            return redirect('event_list')

        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Change 'password' to 'password1'

            # Debugging: Print the username and password
            print(f"Username: {username}, Password: {password}")

            user = User.objects.filter(username=username).first()
            if not user:
                # User doesn't exist, create a new user
                user = User.objects.create_user(username=username, password=password)
                user.email = form.cleaned_data.get('email')
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.save()

                # Debugging: Print the user's information
                print(f"New user created: {user.username}")

            user = authenticate(request, username=username, password=password)
            print(f"User after authentication: {user}")

            # Debugging: Print the authenticated user's information
            if user:
                print(f"Authenticated user: {user.username}")

            if user is not None:
                login(request, user)

            event.attendees.add(user)
            messages.success(request, f'You have successfully registered for the event: {event.name}')
            return redirect('dashboard')  # Redirect to the user's dashboard page
        else: 
            print(form.errors)
            print(form.non_field_errors)
        return redirect('event_list')  # Redirect back to the event list
    else:
        form = RegistrationForm()

    return render(request, 'events/register_event.html', {'event': event, 'form': form})




@login_required
def capture_attendance(request, event_id):
    event = Event.objects.get(pk=event_id)
    user_profile = request.user.userprofile

    # Check if the user has a face image uploaded
    if user_profile.face_image:
        # Implement face recognition and update attendance
        recognize_attendance(event, user_profile.face_image.path)
        return HttpResponse("Attendance captured successfully.")
    else:
        messages.error(request, "Please upload your face image before capturing attendance.")
        return redirect('submit_face_image')


# @organizer_required  # Use a custom decorator to restrict access to organizers
# def manage_event_attendance(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     attendance_records = AttendanceRecord.objects.filter(event=event)

#     if request.method == 'POST':
#         # Handle attendance management actions here
#         # For example, you can mark attendance or perform other actions

#         # Sample code to mark attendance for a user (modify as needed)
#         user_id = request.POST.get('user_id')
#         action = request.POST.get('action')
#         if action == 'mark_present':
#             # Add code to mark the user as present in the attendance record
#             pass
#         # Handle other actions here

#         messages.success(request, 'Attendance records updated successfully.')

#     context = {
#         'event': event,
#         'attendance_records': attendance_records,
#     }

#     return render(request, 'events/manage_event_attendance.html', context)



@login_required
def send_event_notification(request, event_id):
    event = Event.objects.get(pk=event_id)

    # Prepare email subject and message
    subject = f'Event Update: {event.name}'
    message = f'Dear {request.user.username},\n\nThe event "{event.name}" has been updated.'

    # Render the HTML message using a template (optional)
    html_message = render_to_string('notifications/event_update_email.html', {'event': event})

    # Send the email
    send_notification_email(subject, message, [request.user.email], html_message=html_message)
    messages.success(request, f'Notification sent for event: {event.name}')
    return redirect('event_list')

    
