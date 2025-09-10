# ==============================================================================
# API DOCUMENTATION CONFIGURATION WITH SWAGGER/OPENAPI
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path, include
from rest_framework import permissions
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


class CustomAutoSchema(AutoSchema):
    """Custom schema generator for better API documentation"""
    
    def get_operation_id(self):
        """Generate operation ID for API endpoints"""
        operation_id = super().get_operation_id()
        
        # Add version prefix if versioned
        if hasattr(self.view, 'versioning_class') and self.view.request:
            version = self.view.request.version
            if version:
                operation_id = f"v{version}_{operation_id}"
        
        return operation_id

    def get_tags(self):
        """Generate tags for API grouping"""
        tags = super().get_tags()
        
        # Add app-based tags
        if hasattr(self.view, 'queryset') and self.view.queryset is not None:
            app_label = self.view.queryset.model._meta.app_label
            tags = [app_label.title()]
        
        # Add custom tags based on view class
        if hasattr(self.view, 'swagger_tags'):
            tags.extend(self.view.swagger_tags)
            
        return tags

    def get_description(self):
        """Generate description for API endpoints"""
        description = super().get_description()
        
        # Add role-based access information
        if hasattr(self.view, 'permission_classes'):
            permissions_info = []
            for perm_class in self.view.permission_classes:
                permissions_info.append(perm_class.__name__)
            
            if permissions_info:
                description += f"\n\n**Required Permissions:** {', '.join(permissions_info)}"
        
        # Add caching information
        if hasattr(self.view, 'get_queryset') and 'cache' in str(self.view.get_queryset):
            description += "\n\n**Note:** This endpoint uses caching for better performance."
            
        return description


# Swagger configuration
SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'config.swagger_config.CustomAutoSchema',
    'TITLE': 'University Management System API',
    'DESCRIPTION': '''
    # University Management System API

    این API برای مدیریت سیستم دانشگاهی طراحی شده است و شامل عملکردهای زیر می‌باشد:
    
    ## ویژگی‌های کلیدی:
    - 🎓 مدیریت کاربران (دانشجویان، اساتید، کارمندان)
    - 📚 مدیریت دوره‌های آموزشی
    - 📊 سیستم نمرات و ارزیابی
    - 📅 مدیریت برنامه زمانی کلاس‌ها
    - 📋 سیستم حضور و غیاب
    - 🏛️ مدیریت ساختار سازمانی دانشگاه
    
    ## احراز هویت:
    این API از سه روش احراز هویت پشتیبانی می‌کند:
    - **Token Authentication**: استفاده از Token در header
    - **JWT Authentication**: استفاده از JSON Web Token
    - **Session Authentication**: برای استفاده در browser
    
    ## نسخه‌بندی:
    API از نسخه‌بندی پشتیبانی می‌کند. نسخه فعلی: v1
    
    ## محدودیت‌های نرخ:
    - کاربران عادی: 100 درخواست در دقیقه
    - کاربران پیشرفته: 500 درخواست در ساعت
    
    ## پشتیبانی:
    برای پشتیبانی با تیم توسعه تماس بگیرید.
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
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
            },
            'typography': {
                'fontSize': '14px',
                'lineHeight': '1.5em',
                'code': {
                    'fontSize': '13px'
                },
                'headings': {
                    'fontFamily': 'Montserrat, sans-serif'
                }
            }
        }
    }
}


# Custom examples for API documentation
API_EXAMPLES = {
    'user_registration': OpenApiExample(
        'User Registration Example',
        description='نمونه ثبت‌نام کاربر جدید',
        value={
            'national_id': '1234567890',
            'username': 'student123',
            'email': 'student@university.ac.ir',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'user_type': 'STUDENT',
            'phone': '09123456789',
            'first_name': 'علی',
            'last_name': 'احمدی',
            'birth_date': '2000-01-01',
            'preferred_language': 'fa',
            'timezone': 'Asia/Tehran'
        }
    ),
    'course_creation': OpenApiExample(
        'Course Creation Example',
        description='نمونه ایجاد دوره آموزشی',
        value={
            'title': 'مبانی برنامه‌نویسی',
            'code': 'CS101',
            'description': 'این دوره مبانی برنامه‌نویسی را آموزش می‌دهد',
            'professor': 1
        }
    ),
    'enrollment': OpenApiExample(
        'Student Enrollment Example',
        description='نمونه ثبت‌نام دانشجو در دوره',
        value={
            'student_id': 5
        }
    ),
    'grade_submission': OpenApiExample(
        'Grade Submission Example',
        description='نمونه ثبت نمره',
        value={
            'student': 5,
            'course': 1,
            'score': 18.5,
            'exam_type': 'FINAL',
            'exam_date': '2024-01-15',
            'description': 'امتحان پایان ترم'
        }
    )
}


# API versioning configuration
API_VERSIONING = {
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1'],
    'VERSION_PARAM': 'version',
    'HEADER_NAME': 'Accept-Version',
}


# Error response schemas
ERROR_RESPONSES = {
    400: {
        'description': 'Bad Request - درخواست نامعتبر',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'},
                        'details': {'type': 'object'},
                        'code': {'type': 'string'}
                    }
                },
                'example': {
                    'error': 'Validation failed',
                    'details': {
                        'email': ['این فیلد الزامی است']
                    },
                    'code': 'VALIDATION_ERROR'
                }
            }
        }
    },
    401: {
        'description': 'Unauthorized - غیر مجاز',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'},
                        'code': {'type': 'string'}
                    }
                },
                'example': {
                    'error': 'Authentication credentials were not provided',
                    'code': 'AUTHENTICATION_FAILED'
                }
            }
        }
    },
    403: {
        'description': 'Forbidden - ممنوع',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'},
                        'code': {'type': 'string'}
                    }
                },
                'example': {
                    'error': 'You do not have permission to perform this action',
                    'code': 'PERMISSION_DENIED'
                }
            }
        }
    },
    404: {
        'description': 'Not Found - یافت نشد',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'},
                        'code': {'type': 'string'}
                    }
                },
                'example': {
                    'error': 'Resource not found',
                    'code': 'NOT_FOUND'
                }
            }
        }
    },
    429: {
        'description': 'Too Many Requests - تعداد درخواست‌های زیاد',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'},
                        'code': {'type': 'string'},
                        'retry_after': {'type': 'integer'}
                    }
                },
                'example': {
                    'error': 'Rate limit exceeded',
                    'code': 'THROTTLED',
                    'retry_after': 60
                }
            }
        }
    },
    500: {
        'description': 'Internal Server Error - خطای داخلی سرور',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'},
                        'code': {'type': 'string'}
                    }
                },
                'example': {
                    'error': 'Internal server error',
                    'code': 'INTERNAL_ERROR'
                }
            }
        }
    }
}
