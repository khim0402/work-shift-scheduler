from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from accounts.models import Employee
from scheduling.models import Schedule, Shift
from leaves.models import LeaveRequest
from datetime import date

@staff_member_required
def custom_admin_index(request, extra_context=None):
    # Get statistics for the dashboard
    today = date.today()
    
    stats = {
        'total_employees': Employee.objects.count(),
        'pending_leaves': LeaveRequest.objects.filter(status='pending').count(),
        'today_schedules': Schedule.objects.filter(date=today).count(),
        'active_shifts': Shift.objects.count(),
    }
    
    # Get the default admin index context
    from django.contrib.admin.sites import site
    context = {
        **site.each_context(request),
        'title': 'Dashboard',
        'subtitle': None,
        'app_list': site.get_app_list(request),
        **stats,
    }
    
    if extra_context is not None:
        context.update(extra_context)
    
    request.current_app = site.name
    
    return TemplateResponse(request, 'admin/index.html', context)

# Override the default admin index
admin.site.index = custom_admin_index