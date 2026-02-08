from django.db import models
from accounts.models import Employee

class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='schedules')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['date', 'shift__start_time']
    
    def __str__(self):
        return f"{self.employee.username} - {self.shift.name} - {self.date}"