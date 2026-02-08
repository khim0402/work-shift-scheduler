# accounts/middleware/admin_protect.py
from django.shortcuts import redirect

class AdminSessionProtectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Now request.user exists (comes after AuthenticationMiddleware)
        
        # Prevent employee session users from accessing admin
        if request.path.startswith('/admin/'):
            if request.session.get('session_type') == 'employee':
                return redirect('dashboard')
        
        # Optional: Prevent admin from using employee routes
        if any(request.path.startswith(path) for path in ['/accounts/', '/dashboard', '/profile']):
            if request.user.is_authenticated and request.user.is_superuser:
                # Admin accessing employee area - allow but maybe show message
                pass
        
        return self.get_response(request)