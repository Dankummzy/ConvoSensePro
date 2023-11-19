from django.shortcuts import render
from django.conf import settings
# Import the render_to_string function at the top of your views.py
from django.template.loader import render_to_string


User = settings.AUTH_USER_MODEL


# # Inside a view or signal handler where you want to send an email
# subject = "Attendance Confirmation"  # Or "Event Update" based on the type of notification
# message = "Your attendance has been confirmed."  # Your email message content

# # Render the HTML content of the desired template
# html_message = render_to_string('notifications/attendance_confirmation_email.html', {'context_variable': value})

# # Send the email with the HTML content
# send_notification_email(subject, message, [recipient_email], html_message=html_message)
