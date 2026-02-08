import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.apps import apps

print("Checking database schema...")

# Check all tables
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"\nTables in database: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")

# Check accounts_employee table structure
print("\nChecking accounts_employee table structure...")
with connection.cursor() as cursor:
    cursor.execute("PRAGMA table_info(accounts_employee);")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  Column: {col[1]} (Type: {col[2]}, Nullable: {col[3]==0})")

# Check if there are any users
from accounts.models import Employee
user_count = Employee.objects.count()
print(f"\nTotal users in database: {user_count}")

# Check constraints
print("\nChecking constraints...")
with connection.cursor() as cursor:
    cursor.execute("PRAGMA foreign_key_list(accounts_employee);")
    fks = cursor.fetchall()
    if fks:
        print("Foreign keys found:")
        for fk in fks:
            print(f"  - {fk}")
    else:
        print("No foreign key constraints")