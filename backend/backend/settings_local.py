"""
Local development settings - uses SQLite instead of PostgreSQL
Usage: python manage.py runserver --settings=backend.settings_local
"""
from .settings import *

# Override database to use SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

print("🔧 Using SQLite database for local development")
