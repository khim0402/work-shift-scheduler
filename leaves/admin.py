from django.contrib import admin
from django.utils.html import format_html
from .models import LeaveRequest

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'date_range', 'duration', 'status_badge', 'created_at', 'status')
    list_filter = ('status', 'leave_type', 'created_at')
    search_fields = ('employee__username', 'employee__email', 'reason')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    actions = ['approve_selected', 'reject_selected']
    list_per_page = 20
    
    def date_range(self, obj):
        return f"{obj.start_date.strftime('%b %d')} - {obj.end_date.strftime('%b %d, %Y')}"
    date_range.short_description = 'Dates'
    
    def duration(self, obj):
        days = (obj.end_date - obj.start_date).days + 1
        return f"{days} day{'s' if days > 1 else ''}"
    duration.short_description = 'Duration'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'warning',
            'approved': 'success',
            'rejected': 'danger'
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def approve_selected(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} leave requests approved.')
    approve_selected.short_description = "Approve selected leaves"
    
    def reject_selected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} leave requests rejected.')
    reject_selected.short_description = "Reject selected leaves"