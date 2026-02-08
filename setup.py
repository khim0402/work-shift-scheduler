import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from scheduling.models import Shift
from datetime import time

def setup_database():
    print("Setting up database...")
    
    User = get_user_model()
    
    # Create default shifts
    shifts = [
        ('Morning Shift', time(6, 0), time(14, 0), '6:00 AM - 2:00 PM'),
        ('Afternoon Shift', time(14, 0), time(22, 0), '2:00 PM - 10:00 PM'),
        ('Night Shift', time(22, 0), time(6, 0), '10:00 PM - 6:00 AM'),
    ]
    
    for name, start, end, desc in shifts:
        shift, created = Shift.objects.get_or_create(
            name=name,
            defaults={'start_time': start, 'end_time': end, 'description': desc}
        )
        if created:
            print(f"✓ Created shift: {name}")
    
    print("✓ Database setup complete!")
    print("\nTo create a superuser (Django admin), run:")
    print("python manage.py createsuperuser")
    print("\nTo start the server, run:")
    print("python manage.py runserver")

if __name__ == '__main__':
    setup_database()