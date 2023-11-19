from facerecognition.recognize_faces import recognize_attendance  # Import the face recognition function
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import AttendanceRecord
from django.conf import settings
from events.models import Event
from users.models import User

from .signals import attendance_updated


def capture_attendance(request, event_id):
    event = Event.objects.get(pk=event_id)
    user_profile = request.user.userprofile

    if user_profile.face_image:
    # Implement face recognition and update attendance
        recognize_attendance(event, user_profile.face_image.path)
        attendance_updated.send(sender=event, event=event, user_id=request.user.id, present=True)
        return HttpResponse("Attendance captured successfully.")

    else:
        messages.error(request, "Please upload your face image before capturing attendance.")
        return redirect('submit_face_image')



def event_attendance(request, event_id):
    event = Event.objects.get(pk=event_id)
    attendance_records = AttendanceRecord.objects.filter(event=event)

    context = {
        'event': event,
        'attendance_records': attendance_records,
    }

    return render(request, 'attendance/event_attendance.html', context)



