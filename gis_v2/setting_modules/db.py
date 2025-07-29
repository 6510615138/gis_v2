from pathlib import Path  # For working with file paths
import os  # For OS-level path handling
from dotenv import load_dotenv

# Project base directory (3 levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv() # Load variables from .env

DB_USER = os.getenv("DB_USER")
DB_USER_PASS = os.getenv("DB_USER_PASS")

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite database
        'NAME': BASE_DIR / 'db.sqlite3',
        "USER": DB_USER,
        "PASSWORD": DB_USER_PASS,
    }
}
