# ==============================================================================
# DJANGO SETTINGS FOR TESTING
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from .settings import *

# Use simple cache backend for testing instead of Redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Use simple session backend for testing
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Disable cache middleware during testing
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'config.security_middleware.SecurityMiddleware',
    'config.security_middleware.RequestLoggingMiddleware',
    'config.advanced_security.SQLInjectionProtectionMiddleware',
    'config.advanced_security.XSSProtectionMiddleware',
    'config.advanced_security.SecurityHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Use in-memory database for faster tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable throttling for tests
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {}

# Test settings
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
    },
}

# Disable email backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
