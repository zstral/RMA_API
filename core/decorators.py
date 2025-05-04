from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(role):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if hasattr(request.user, 'profile') and request.user.profile.rol == role:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator

user_required = role_required('user')
admin_required = role_required('admin')