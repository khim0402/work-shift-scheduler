from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmployeeRegistrationForm, EmployeeUpdateForm
from scheduling.models import Schedule, Shift
from leaves.models import LeaveRequest
from datetime import date, timedelta
from .decorators import employee_required  # Add this import
from django.views.decorators.csrf import csrf_exempt  # ADD THIS IMPORT


# Add this function to accounts/views.py
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'Registration successful! Welcome {user.username}.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Registration error: {str(e)}')
                return render(request, 'accounts/register.html', {'form': form})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EmployeeRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@csrf_exempt  # ADD THIS DECORATOR
def login_view(request):
    # Don't check if user is authenticated - allow both!
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is superuser
            if user.is_superuser:
                messages.error(request, 'Admin users must login via /admin/')
                return render(request, 'accounts/login.html')
            
            # Check if ADMIN is already logged in
            if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_superuser:
                # ADMIN is logged in - DON'T logout!
                # Instead, create SEPARATE employee session
                request.session['employee_session'] = True
                request.session['employee_id'] = user.id
                request.session['employee_username'] = user.username
                request.session['employee_role'] = user.role
                request.session['employee_name'] = user.get_full_name() or user.username
                
                messages.success(request, f'Employee session started for {user.username}')
                return redirect('dashboard')
            else:
                # No admin logged in, proceed normally
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    # Clear employee session if exists
    if 'employee_session' in request.session:
        keys_to_remove = ['employee_session', 'employee_id', 'employee_username', 
                         'employee_role', 'employee_name']
        for key in keys_to_remove:
            if key in request.session:
                del request.session[key]
    
    # Only logout from Django auth if not an admin session
    if not (request.user.is_authenticated and request.user.is_superuser):
        logout(request)
    
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@employee_required  # Replace @login_required with this
def dashboard(request):
    # Get the actual user (could be from request.user OR session)
    if request.session.get('employee_session'):
        # Using employee session (admin is also logged in)
        employee_id = request.session.get('employee_id')
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            current_user = User.objects.get(id=employee_id)
        except User.DoesNotExist:
            # Clear invalid session
            request.session.flush()
            return redirect('login')
    else:
        # Regular Django authentication
        current_user = request.user
    
    # Get today's date
    today = date.today()
    
    # Calculate start of week (Monday)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Get this week's schedule
    schedule = Schedule.objects.filter(
        employee=current_user,  # Use current_user instead of request.user
        date__range=[start_of_week, end_of_week]
    ).select_related('shift').order_by('date', 'shift__start_time')
    
    # Get recent leave requests
    leave_requests = LeaveRequest.objects.filter(
        employee=current_user  # Use current_user instead of request.user
    ).order_by('-created_at')[:5]
    
    # Get today's shift
    todays_shift = Schedule.objects.filter(
        employee=current_user,  # Use current_user instead of request.user
        date=today
    ).select_related('shift').first()
    
    # Count pending leaves
    pending_leaves = LeaveRequest.objects.filter(
        employee=current_user,  # Use current_user instead of request.user
        status='pending'
    ).count()
    
    context = {
        'user': current_user,  # Use current_user instead of request.user
        'schedule': schedule,
        'leave_requests': leave_requests,
        'todays_shift': todays_shift,
        'week_start': start_of_week,
        'week_end': end_of_week,
        'today': today,
        'pending_leaves': pending_leaves,
        'is_employee_session': request.session.get('employee_session', False),
    }
    
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = EmployeeUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})