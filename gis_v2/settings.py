from pathlib import Path
import os 


# Project base directory (2 levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ROOT_URLCONF = 'gis_v2.urls'

WSGI_APPLICATION = 'gis_v2.wsgi.application'

# Static files (CSS, JavaScript, Images)     https://docs.djangoproject.com/en/5.2/howto/static-files
STATIC_URL = 'static/'

# Default primary key field type # https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True

from .setting_modules.db import *
from .setting_modules.drf import *
from .setting_modules.installed_app import *
from .setting_modules.internationalization import *
from .setting_modules.middleware import *
from .setting_modules.password_validation import *
from .setting_modules.secrets import *
from .setting_modules.template_setting import *
from .setting_modules.db import *
