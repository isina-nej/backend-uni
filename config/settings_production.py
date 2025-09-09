"""
Production settings for PythonAnywhere deployment
"""
import os
from .settings import *

# Production-specific settings
DEBUG = False

# Security settings
ALLOWED_HOSTS = [
    'sinanej2.pythonanywhere.com',
    'www.sinanej2.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]

# Database - keep your existing Neon PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'neondb'),
        'USER': os.getenv('DB_USER', 'neondb_owner'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'npg_gDbsPZxln7I5'),
        'HOST': os.getenv('DB_HOST', 'ep-shy-hat-a9wddu9f-pooler.gwc.azure.neon.tech'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Static files configuration for PythonAnywhere
STATIC_URL = '/static/'
STATIC_ROOT = '/home/sinanej2/backend-uni/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/sinanej2/backend-uni/media'

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://sinanej2.pythonanywhere.com",
    "https://www.sinanej2.pythonanywhere.com",
]

CORS_ALLOW_ALL_ORIGINS = False

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Logging for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/sinanej2/backend-uni/logs/django.log',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/sinanej2/backend-uni/logs/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
