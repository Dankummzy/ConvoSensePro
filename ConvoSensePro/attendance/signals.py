from django.db.models.signals import Signal
from django.dispatch import receiver
from .models import AttendanceRecord
from events.models import Event

# Signal to update attendance count
attendance_updated = Signal()

@receiver(attendance_updated)
def update_attendance_count(sender, event=None, user_id=None, present=False, **kwargs):
    if event and user_id:
        # Check if the user is already marked as present for this event
        attendance_record, created = AttendanceRecord.objects.get_or_create(
            event=event, user_id=user_id,
            defaults={'user': User.objects.get(id=user_id), 'present': present}
        )

        if created:
            # If not present, increment the attendance count for the event and user
            event.attendance_count += 1
            event.save()
            user = User.objects.get(id=user_id)
            user.attendance_count += 1
            user.save()


