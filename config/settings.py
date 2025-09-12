# ==============================================================================
# SIMPLE DJANGO SETTINGS FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here-change-this-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    'drf_spectacular',
    'channels',  # For WebSocket support
]
# The `LOCAL_APPS` list in the Django settings file is defining the names of the local Django
# applications that are part of the University Management System project. Each string in the list
# represents the name of a Django app within the project.

LOCAL_APPS = [
    'apps.users',
    'apps.common',
    'apps.courses',
    'apps.grades',
    'apps.attendance',
    'apps.schedules',
    'apps.exams',
    'apps.library',
    'apps.financial',
    'apps.notifications',
    'apps.analytics',
    'apps.data_management',
    'apps.mobile_api',
    'apps.ai_ml',
    'apps.reports',
    'apps.research',
    'apps.announcements',
    'apps.assignments',
    'apps.authentication',
    'apps.dormitory',  # اضافه شده: مدیریت خوابگاه
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'config.monitoring.MonitoringMiddleware',  # Performance monitoring
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',  # Cache middleware
    'config.security_middleware.SecurityMiddleware',
    'config.security_middleware.RequestLoggingMiddleware',
    'config.advanced_security.SQLInjectionProtectionMiddleware',
    'config.advanced_security.XSSProtectionMiddleware',
    'config.advanced_security.SecurityHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # For internationalization
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',  # Cache middleware
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database (SQLite for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',  # Temporarily disabled for testing
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'config.pagination.CustomPagination',
    'PAGE_SIZE': 20,
    'PAGE_SIZE_QUERY_PARAM': 'page_size',
    'MAX_PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'config.throttling.BurstRateThrottle',
        'config.throttling.SustainedRateThrottle',
        'config.throttling.APIEndpointThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'burst': '60/minute',
        'sustained': '1000/hour',
        'api': '100/minute',
        'strict_user': '500/hour',
    },
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'config.error_handling.custom_exception_handler',
    'DEFAULT_VERSIONING_CLASS': 'config.versioning.CustomAcceptHeaderVersioning',
    'DEFAULT_VERSION': '1.0',
    'ALLOWED_VERSIONS': ['1.0', '1.1'],
}

# JWT Configuration
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "https://university-management.com",
    "https://www.university-management.com",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOWED_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Logging Configuration
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
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = False  # Set to True in production with HTTPS
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Cache Configuration (simplified for development)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    },
    'session': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'session-cache',
        'TIMEOUT': 1800,
    }
}

# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'session'

# Cache Timeouts
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600  # 10 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'university_api'

# API Documentation with drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'University Management System API',
    'DESCRIPTION': '''
    سیستم مدیریت دانشگاهی - University Management System API
    
    این API برای مدیریت کامل سیستم دانشگاهی طراحی شده است.
    
    ## ویژگی‌های کلیدی:
    - 🎓 مدیریت کاربران و نقش‌ها
    - 📚 مدیریت دوره‌های آموزشی
    - 📊 سیستم نمرات و ارزیابی
    - 📅 برنامه‌ریزی زمانی
    - 🏛️ ساختار سازمانی
    
    ## احراز هویت:
    از Token، JWT، یا Session authentication استفاده کنید.
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'DISABLE_ERRORS_AND_WARNINGS': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'displayRequestDuration': True,
        'filter': True,
        'tryItOutEnabled': True,
        'supportedSubmitMethods': ['get', 'post', 'put', 'patch', 'delete'],
        'docExpansion': 'none',
        'defaultModelsExpandDepth': 2,
        'defaultModelExpandDepth': 2,
    },
    'REDOC_SETTINGS': {
        'nativeScrollbars': True,
        'theme': {
            'colors': {
                'primary': {
                    'main': '#1976d2'
                }
            }
        }
    },
    'EXTENSIONS': {
        'drf_spectacular.contrib.django_filters': {
            'SKIP_FILTERS_WITH_ERRORS': True,
        }
    }
}

# Internationalization
LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# Additional i18n settings
LANGUAGES = [
    ('en', 'English'),
    ('fa', 'Persian'),
    ('ar', 'Arabic'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ==============================================================================
# CHANNELS & WEBSOCKET CONFIGURATION
# ==============================================================================

# Channel layers for WebSocket support
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
            'capacity': 1500,  # Maximum messages to store
            'expiry': 60,      # Message expiry time in seconds
        },
    },
}

# WebSocket settings
WEBSOCKET_ACCEPT_ALL = False  # Set to True to accept all WebSocket connections
WEBSOCKET_TIMEOUT = 300  # WebSocket timeout in seconds
