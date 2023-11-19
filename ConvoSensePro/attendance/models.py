from django.db import models
from users.models import User  # Import User model from the Users App
from events.models import Event  # Import Event model from the Events App

class AttendanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)  # Add a field to track attendance status

    def __str__(self):
        return f'{self.user.username} at {self.event.name}'

