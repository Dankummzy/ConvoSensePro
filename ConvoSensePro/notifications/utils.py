# notifications/utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_notification_email(subject, message, recipient_list, html_message=None):
    send_mail(
        subject,
        message,
        'your_email@gmail.com',  # Sender's email address
        recipient_list,
        html_message=html_message,
    )
