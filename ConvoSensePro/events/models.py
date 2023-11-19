from django.db import models
from django.conf import settings
import uuid
from users.models import User



class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(
        help_text='Enter date in DD/MM/YYYY format'  # Add a help text
    )
    time = models.TimeField(
        help_text='Enter time in HH:MM format'  # Add a help text
    )
    description = models.TextField()
    location = models.CharField(
        max_length=100,
        default='Your Event Location'  # Set a default location
    )
    unique_link = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    organizer = models.ForeignKey(User, on_delete=models.CASCADE)  # Organizer of the event

    capacity = models.PositiveIntegerField(
        default=100,  # Set a default capacity or adjust as needed
        help_text='Maximum number of attendees allowed for this event'
    )
    attendees = models.ManyToManyField(User, related_name='events_attending', blank=True)
    is_attendance_capture_ready = models.BooleanField(default=False)
    
    def is_full(self):
        return self.attendees.count() >= self.capacity
        
    def __str__(self):
        return self.name



