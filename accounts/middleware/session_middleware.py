# accounts/middleware/session_middleware.py
class SeparateSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Don't modify settings directly - it's shared across requests!
        # Instead, set a flag in the request
        
        # Set different session cookie names based on path
        if request.path.startswith('/admin/'):
            request._session_cookie_name = 'admin_sessionid'
        elif any(request.path.startswith(path) for path in ['/accounts/', '/dashboard', '/profile']):
            request._session_cookie_name = 'employee_sessionid'
        else:
            request._session_cookie_name = 'sessionid'
        
        response = self.get_response(request)
        
        # You can't easily change session cookie name per request in Django
        # This approach needs a different solution
        
        return response