from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LeaveRequestForm
from .models import LeaveRequest
from datetime import date

@login_required
def create_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('leave_list')
    else:
        form = LeaveRequestForm()
    
    return render(request, 'leaves/create.html', {'form': form})

@login_required
def leave_list(request):
    leaves = LeaveRequest.objects.filter(employee=request.user).order_by('-created_at')
    
    # Count by status
    pending_count = leaves.filter(status='pending').count()
    approved_count = leaves.filter(status='approved').count()
    rejected_count = leaves.filter(status='rejected').count()
    
    context = {
        'leaves': leaves,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    }
    
    return render(request, 'leaves/list.html', context)

@login_required
def cancel_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk, employee=request.user)
    
    if leave.status == 'pending':
        leave.delete()
        messages.success(request, 'Leave request cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel a leave request that is not pending.')
    
    return redirect('leave_list')