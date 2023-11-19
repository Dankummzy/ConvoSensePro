# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_event, name='create_event'),
    path('events/list/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('events/register/<uuid:event_uuid>/', views.register_for_event, name='register_for_event'),
    # path('manage_event_attendance/<int:event_id>/', views.manage_event_attendance, name='manage_event_attendance'),
]


