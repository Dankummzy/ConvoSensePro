# users/decorators.py

from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def organizer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_organizer:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Permission denied. You must be an organizer to access this page.')
            return redirect('users:home')  # Redirect to an appropriate URL
    return _wrapped_view
