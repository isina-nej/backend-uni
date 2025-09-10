# ==============================================================================
# ENHANCED ERROR HANDLING FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler for better error messages"""
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': '',
            'details': None,
            'error_code': '',
            'timestamp': context['request'].META.get('HTTP_X_TIMESTAMP', ''),
            'path': context['request'].path,
            'method': context['request'].method
        }
        
        # Handle different types of errors
        if response.status_code == 400:  # Bad Request
            custom_response_data['message'] = _('درخواست نامعتبر است')
            custom_response_data['error_code'] = 'VALIDATION_ERROR'
            custom_response_data['details'] = response.data
            
        elif response.status_code == 401:  # Unauthorized
            custom_response_data['message'] = _('احراز هویت مورد نیاز است')
            custom_response_data['error_code'] = 'AUTHENTICATION_REQUIRED'
            
        elif response.status_code == 403:  # Forbidden
            custom_response_data['message'] = _('دسترسی ممنوع است')
            custom_response_data['error_code'] = 'ACCESS_FORBIDDEN'
            
        elif response.status_code == 404:  # Not Found
            custom_response_data['message'] = _('منبع مورد نظر یافت نشد')
            custom_response_data['error_code'] = 'RESOURCE_NOT_FOUND'
            
        elif response.status_code == 405:  # Method Not Allowed
            custom_response_data['message'] = _('روش درخواست مجاز نیست')
            custom_response_data['error_code'] = 'METHOD_NOT_ALLOWED'
            
        elif response.status_code == 406:  # Not Acceptable
            custom_response_data['message'] = _('فرمت درخواست قابل قبول نیست')
            custom_response_data['error_code'] = 'NOT_ACCEPTABLE'
            
        elif response.status_code == 409:  # Conflict
            custom_response_data['message'] = _('تضاد در داده‌ها')
            custom_response_data['error_code'] = 'DATA_CONFLICT'
            
        elif response.status_code == 429:  # Too Many Requests
            custom_response_data['message'] = _('تعداد درخواست‌ها بیش از حد مجاز است')
            custom_response_data['error_code'] = 'RATE_LIMIT_EXCEEDED'
            retry_after = response.get('Retry-After')
            if retry_after:
                custom_response_data['retry_after'] = retry_after
                
        elif response.status_code >= 500:  # Server Error
            custom_response_data['message'] = _('خطای داخلی سرور')
            custom_response_data['error_code'] = 'INTERNAL_SERVER_ERROR'
            
            # Log server errors
            logger.error(f"Server error: {exc}", exc_info=True, extra={
                'request_path': context['request'].path,
                'request_method': context['request'].method,
                'user': context['request'].user.id if context['request'].user.is_authenticated else None
            })
        
        else:
            custom_response_data['message'] = _('خطای نامشخص')
            custom_response_data['error_code'] = 'UNKNOWN_ERROR'
        
        response.data = custom_response_data
    
    # Handle specific Django exceptions
    elif isinstance(exc, ValidationError):
        custom_response_data = {
            'error': True,
            'message': _('خطای اعتبارسنجی'),
            'details': exc.message_dict if hasattr(exc, 'message_dict') else str(exc),
            'error_code': 'VALIDATION_ERROR',
            'timestamp': context['request'].META.get('HTTP_X_TIMESTAMP', ''),
            'path': context['request'].path,
            'method': context['request'].method
        }
        response = Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)
        
    elif isinstance(exc, IntegrityError):
        custom_response_data = {
            'error': True,
            'message': _('نقض یکپارچگی داده‌ها'),
            'details': str(exc),
            'error_code': 'INTEGRITY_ERROR',
            'timestamp': context['request'].META.get('HTTP_X_TIMESTAMP', ''),
            'path': context['request'].path,
            'method': context['request'].method
        }
        response = Response(custom_response_data, status=status.HTTP_409_CONFLICT)
    
    return response


class ErrorMessages:
    """Centralized error messages in both Persian and English"""
    
    # Authentication Errors
    AUTHENTICATION_FAILED = {
        'fa': 'احراز هویت ناموفق',
        'en': 'Authentication failed'
    }
    
    INVALID_CREDENTIALS = {
        'fa': 'اطلاعات ورود نامعتبر است',
        'en': 'Invalid credentials'
    }
    
    ACCOUNT_LOCKED = {
        'fa': 'حساب کاربری قفل شده است',
        'en': 'Account is locked'
    }
    
    ACCOUNT_INACTIVE = {
        'fa': 'حساب کاربری غیرفعال است',
        'en': 'Account is inactive'
    }
    
    # Validation Errors
    REQUIRED_FIELD = {
        'fa': 'این فیلد الزامی است',
        'en': 'This field is required'
    }
    
    INVALID_FORMAT = {
        'fa': 'فرمت نامعتبر است',
        'en': 'Invalid format'
    }
    
    INVALID_EMAIL = {
        'fa': 'آدرس ایمیل نامعتبر است',
        'en': 'Invalid email address'
    }
    
    INVALID_PHONE = {
        'fa': 'شماره تلفن نامعتبر است',
        'en': 'Invalid phone number'
    }
    
    INVALID_NATIONAL_ID = {
        'fa': 'کد ملی نامعتبر است',
        'en': 'Invalid national ID'
    }
    
    # Business Logic Errors
    ALREADY_ENROLLED = {
        'fa': 'دانشجو قبلاً در این دوره ثبت‌نام کرده است',
        'en': 'Student is already enrolled in this course'
    }
    
    COURSE_FULL = {
        'fa': 'ظرفیت دوره تکمیل شده است',
        'en': 'Course capacity is full'
    }
    
    ENROLLMENT_CLOSED = {
        'fa': 'زمان ثبت‌نام به پایان رسیده است',
        'en': 'Enrollment period has ended'
    }
    
    GRADE_ALREADY_EXISTS = {
        'fa': 'نمره برای این دانشجو قبلاً ثبت شده است',
        'en': 'Grade already exists for this student'
    }
    
    SCHEDULE_CONFLICT = {
        'fa': 'تداخل در برنامه زمانی',
        'en': 'Schedule conflict detected'
    }
    
    # Permission Errors
    PERMISSION_DENIED = {
        'fa': 'دسترسی ممنوع',
        'en': 'Permission denied'
    }
    
    ADMIN_REQUIRED = {
        'fa': 'دسترسی مدیر مورد نیاز است',
        'en': 'Admin access required'
    }
    
    PROFESSOR_REQUIRED = {
        'fa': 'دسترسی استاد مورد نیاز است',
        'en': 'Professor access required'
    }
    
    # Resource Errors
    USER_NOT_FOUND = {
        'fa': 'کاربر یافت نشد',
        'en': 'User not found'
    }
    
    COURSE_NOT_FOUND = {
        'fa': 'دوره یافت نشد',
        'en': 'Course not found'
    }
    
    STUDENT_NOT_FOUND = {
        'fa': 'دانشجو یافت نشد',
        'en': 'Student not found'
    }
    
    STUDENT_NOT_ENROLLED = {
        'fa': 'دانشجو در این دوره ثبت‌نام نکرده است',
        'en': 'Student is not enrolled in this course'
    }
    
    PROFESSOR_NOT_FOUND = {
        'fa': 'استاد یافت نشد',
        'en': 'Professor not found'
    }
    
    @classmethod
    def get_message(cls, error_key, language='fa'):
        """Get error message in specified language"""
        error_dict = getattr(cls, error_key, None)
        if error_dict and language in error_dict:
            return error_dict[language]
        return error_dict.get('en', 'Unknown error') if error_dict else 'Unknown error'


def get_error_response(error_key, language='fa', details=None, status_code=400):
    """Helper function to create standardized error responses"""
    message = ErrorMessages.get_message(error_key, language)
    
    error_response = {
        'error': True,
        'message': message,
        'error_code': error_key,
        'details': details
    }
    
    return Response(error_response, status=status_code)


# Custom exceptions
class BusinessLogicError(Exception):
    """Custom exception for business logic errors"""
    def __init__(self, message, error_code=None, details=None):
        self.message = message
        self.error_code = error_code or 'BUSINESS_LOGIC_ERROR'
        self.details = details
        super().__init__(self.message)


class ValidationError(Exception):
    """Custom validation error"""
    def __init__(self, message, error_code=None, field=None):
        self.message = message
        self.error_code = error_code or 'VALIDATION_ERROR'
        self.field = field
        super().__init__(self.message)


class PermissionError(Exception):
    """Custom permission error"""
    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code or 'PERMISSION_ERROR'
        super().__init__(self.message)
