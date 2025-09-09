"""
Simple production settings for PythonAnywhere deployment
This version uses basic environment variables without django-environ
"""
import os
from .settings import *

# Production-specific settings
DEBUG = False

# Override debug setting from environment if needed
if os.environ.get('DEBUG') == 'True':
    DEBUG = True

# Database configuration for PythonAnywhere MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'sinanej2$backend_uni_db'),
        'USER': os.environ.get('DB_USER', 'sinanej2'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'sinanej2.mysql.pythonanywhere-services.com'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-production-secret-key-here')

# Allow PythonAnywhere hosts
ALLOWED_HOSTS = [
    'sinanej2.pythonanywhere.com',
    'www.sinanej2.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]

# Static files settings for production
STATIC_ROOT = '/home/sinanej2/backend-uni/static'
STATIC_URL = '/static/'

# Media files settings
MEDIA_ROOT = '/home/sinanej2/backend-uni/media'
MEDIA_URL = '/media/'

# Logging configuration
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
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/sinanej2/backend-uni/logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://sinanej2.pythonanywhere.com",
    "http://localhost:3000",  # For Flutter web development
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
