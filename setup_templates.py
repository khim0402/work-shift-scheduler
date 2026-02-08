import os
import sys

# Create all template directories
directories = [
    'templates',
    'templates/accounts',
    'templates/core',
    'templates/leaves',
    'templates/scheduling',
    'templates/admin',
    'static/css',
    'static/js',
    'static/images',
    'media/profiles'
]

print("Creating directories...")
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"✓ Created: {directory}")

# Create empty __init__.py files for apps
apps = ['accounts', 'scheduling', 'leaves', 'core']
for app in apps:
    init_file = f"{app}/__init__.py"
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('')
        print(f"✓ Created: {init_file}")

print("\n✓ All directories created successfully!")
print("\nNext steps:")
print("1. Run: python manage.py makemigrations")
print("2. Run: python manage.py migrate")
print("3. Run: python manage.py collectstatic --noinput")
print("4. Run: python manage.py createsuperuser")
print("5. Run: python manage.py runserver")