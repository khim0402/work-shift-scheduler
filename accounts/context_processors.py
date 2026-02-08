def session_info(request):
    return {
        'session_type': request.session.get('session_type', 'unknown'),
        'is_employee_session': request.session.get('session_type') == 'employee',
        'is_admin_session': request.user.is_authenticated and request.user.is_superuser,
    }