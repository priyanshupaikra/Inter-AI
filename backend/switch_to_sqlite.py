# Quick Database Switch Script
# This will help you switch between SQLite and PostgreSQL easily

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def switch_to_sqlite():
    """Switch to SQLite for local development"""
    settings_file = os.path.join(os.path.dirname(__file__), 'backend', 'settings.py')
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Backup original
    with open(settings_file + '.backup', 'w') as f:
        f.write(content)
    
    # Replace database config
    new_content = content.replace(
        'DATABASES = {',
        '''# SQLite for local dev
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# PostgreSQL (commented out)
OLD_DATABASES = {'''
    ).replace(
        '"ENGINE": "django.db.backends.postgresql"',
        '"ENGINE": "django.db.backends.postgresql"  # DISABLED'
    )
    
    with open(settings_file, 'w') as f:
        f.write(new_content)
    
    print("✅ Switched to SQLite")
    print("Run: python manage.py migrate")

if __name__ == '__main__':
    print("This will switch your database to SQLite.")
    print("Your original settings.py will be backed up to settings.py.backup")
    response = input("Continue? (y/n): ")
    if response.lower() == 'y':
        switch_to_sqlite()
