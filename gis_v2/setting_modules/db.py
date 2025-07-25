from pathlib import Path  # For working with file paths
import os  # For OS-level path handling

# Project base directory (3 levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Path to store geojson data files
GEOJSON_DATA_DIR = os.path.join(BASE_DIR, "data")

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite database
        'NAME': BASE_DIR / 'db.sqlite3',  # List of database paths (not valid config)
        "USER": "gis",  # User field (not used by SQLite)
    }
}