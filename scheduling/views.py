from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Schedule
from datetime import date, timedelta

@login_required
def schedule_view(request):
    today = date.today()
    
    # Calculate start of week (Monday)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Get schedule for the week
    schedule = Schedule.objects.filter(
        employee=request.user,
        date__range=[start_of_week, end_of_week]
    ).select_related('shift').order_by('date', 'shift__start_time')
    
    context = {
        'schedule': schedule,
        'week_start': start_of_week,
        'week_end': end_of_week,
        'today': today,
    }
    
    return render(request, 'scheduling/schedule.html', context)

@login_required
def upcoming_schedule(request):
    today = date.today()
    end_date = today + timedelta(days=30)
    
    schedule = Schedule.objects.filter(
        employee=request.user,
        date__range=[today, end_date]
    ).select_related('shift').order_by('date', 'shift__start_time')
    
    context = {
        'schedule': schedule,
        'today': today,
        'end_date': end_date,
    }
    
    return render(request, 'scheduling/upcoming.html', context)