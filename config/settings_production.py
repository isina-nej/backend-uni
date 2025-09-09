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
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media')

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://sinanej2.pythonanywhere.com",
    "https://www.sinanej2.pythonanywhere.com",
]

CORS_ALLOW_ALL_ORIGINS = False

# Security settings (تنها برای HTTPS فعال کن)
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Logging for production
import logging.config
import os

# Ensure logs directory exists
LOGS_DIR = os.path.join(BASE_DIR.parent, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'django.log'),
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'error.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
