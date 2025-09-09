"""
Local development settings
"""
import os
from .settings import *

# Load environment variables from .env.local file
from pathlib import Path
import environ

env = environ.Env(
    DEBUG=(bool, True)
)

# Take environment variables from .env.local file
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env.local'))

# Development-specific settings
DEBUG = env('DEBUG')

# Database - SQLite for local development (easier to test)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_local.sqlite3',
    }
}

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Static files configuration for local development
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'static_local')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media_local')

# Disable some production-only middleware for easier debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
