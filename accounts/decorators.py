# accounts/decorators.py
from django.shortcuts import redirect
from functools import wraps

def employee_required(view_func):
    """Decorator that checks for either Django auth OR employee session"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check 1: Regular Django authentication (non-admin)
        if request.user.is_authenticated and not request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        # Check 2: Employee session (when admin is also logged in)
        if request.session.get('employee_session'):
            return view_func(request, *args, **kwargs)
        
        # Not authenticated as employee
        return redirect('login')
    
    return _wrapped_view