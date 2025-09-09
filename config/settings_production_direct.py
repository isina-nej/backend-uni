"""
Direct production settings for PythonAnywhere deployment
No environment variables needed - all settings are hardcoded
"""
import os
from .settings import *

# Production-specific settings
DEBUG = False

# Database configuration for PythonAnywhere MySQL
# توجه: باید پسورد دیتابیس رو از تب Databases بگیری
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sinanej2$backend_uni_db',  # نام دیتابیس از تب Databases
        'USER': 'sinanej2',
        'PASSWORD': '',  # اینجا پسورد دیتابیست رو بنویس
        'HOST': 'sinanej2.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Security settings
SECRET_KEY = 'django-insecure-production-key-change-this-123456789'

# Allow PythonAnywhere hosts
ALLOWED_HOSTS = [
    'sinanej2.pythonanywhere.com',
    'www.sinanej2.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
    '*',  # برای تست - بعداً حذفش کن
]

# Static files settings for production
STATIC_ROOT = '/home/sinanej2/backend-uni/staticfiles'
STATIC_URL = '/static/'

# Additional static files directories
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files settings
MEDIA_ROOT = '/home/sinanej2/backend-uni/media'
MEDIA_URL = '/media/'

# Ensure logs directory exists
LOGS_DIR = BASE_DIR / 'logs'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
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

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://sinanej2.pythonanywhere.com",
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True

# Disable migrations for problematic apps if needed
# MIGRATION_MODULES = {
#     'problematic_app': None,
# }
