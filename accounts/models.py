from django.contrib.auth.models import AbstractUser
from django.db import models

class Employee(AbstractUser):
    ROLE_CHOICES = [
        ('cashier', 'Cashier'),
        ('kitchen_staff', 'Kitchen Staff'),
        ('server', 'Server'),
        ('manager', 'Manager'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='server')
    phone = models.CharField(max_length=20, blank=True, default='')  # Make blank allowed
    address = models.TextField(blank=True, default='')  # Make blank allowed
    hire_date = models.DateField(auto_now_add=True)
    
    # Add these fields to avoid integrity errors
    email = models.EmailField(blank=True, default='')  # Ensure email field exists
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    class Meta:
        # Ensure unique email is not required to avoid conflicts
        swappable = 'AUTH_USER_MODEL'