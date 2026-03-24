"""
AEGISAI – accounts/decorators.py
Role guards that work with the session-based USER/POLICE auth
and Django's built-in auth for ADMIN.
"""

from functools import wraps
from django.shortcuts import redirect


def _get_role(request):
    """Return the role string from the session, or 'ADMIN' for Django superusers."""
    role = request.session.get('auth_user_role')
    if role:
        return role
    if request.user.is_authenticated and getattr(request.user, 'role', None) == 'ADMIN':
        return 'ADMIN'
    return None


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            role = _get_role(request)
            if role not in allowed_roles:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def user_required(view_func):
    return role_required(['USER'])(view_func)


def admin_required(view_func):
    return role_required(['ADMIN'])(view_func)


def police_required(view_func):
    return role_required(['POLICE'])(view_func)
