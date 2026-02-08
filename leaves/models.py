from django.db import models
from accounts.models import Employee

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('vacation', 'Vacation'),
        ('sick', 'Sick Leave'),
        ('personal', 'Personal Leave'),
        ('emergency', 'Emergency'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.username} - {self.get_leave_type_display()} - {self.get_status_display()}"
    
    def duration(self):
        return (self.end_date - self.start_date).days + 1