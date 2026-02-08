from django.contrib import admin
from django.utils.html import format_html
from .models import Shift, Schedule

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_time', 'description_short')
    search_fields = ('name', 'description')
    list_per_page = 20
    
    def display_time(self, obj):
        return f"{obj.start_time.strftime('%I:%M %p')} - {obj.end_time.strftime('%I:%M %p')}"
    display_time.short_description = 'Time'
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'shift', 'notes_short')
    list_filter = ('date', 'shift')
    search_fields = ('employee__username', 'employee__email', 'notes')
    date_hierarchy = 'date'
    list_per_page = 20
    
    def notes_short(self, obj):
        return obj.notes[:50] + '...' if len(obj.notes) > 50 else obj.notes or '-'
    notes_short.short_description = 'Notes'