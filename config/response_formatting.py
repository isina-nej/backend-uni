# ==============================================================================
# API RESPONSE ENHANCEMENT AND FORMATTING
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.utils.translation import gettext as _
from datetime import datetime
import time


class StandardAPIResponse:
    """Standard API response formatter"""
    
    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK, meta=None):
        """Format successful response"""
        response_data = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'status_code': status_code,
        }
        
        if message:
            response_data['message'] = message
        
        if data is not None:
            response_data['data'] = data
        
        if meta:
            response_data['meta'] = meta
            
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(message, status_code=status.HTTP_400_BAD_REQUEST, errors=None, error_code=None):
        """Format error response"""
        response_data = {
            'success': False,
            'timestamp': datetime.now().isoformat(),
            'status_code': status_code,
            'message': message,
        }
        
        if error_code:
            response_data['error_code'] = error_code
            
        if errors:
            response_data['errors'] = errors
            
        return Response(response_data, status=status_code)
    
    @staticmethod
    def paginated_response(queryset, request, serializer_class, page_size=20):
        """Format paginated response"""
        paginator = StandardPagination()
        paginator.page_size = page_size
        
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = serializer_class(paginated_queryset, many=True, context={'request': request})
        
        return paginator.get_paginated_response(serializer.data)


class StandardPagination(PageNumberPagination):
    """Enhanced pagination with metadata"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """Return paginated response with enhanced metadata"""
        return Response({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'pagination': {
                'count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'page_size': self.get_page_size(self.request),
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
                'next_page': self.page.next_page_number() if self.page.has_next() else None,
                'previous_page': self.page.previous_page_number() if self.page.has_previous() else None,
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                }
            },
            'data': data,
        })


class ResponseTimeMiddleware:
    """Add response time to API responses"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        
        # Add response time for API endpoints
        if request.path.startswith('/api/'):
            response_time = round((time.time() - start_time) * 1000, 2)
            response['X-Response-Time'] = f"{response_time}ms"
            
            # If it's a JSON response, add response time to the data
            if hasattr(response, 'data') and isinstance(response.data, dict):
                response.data['response_time_ms'] = response_time
        
        return response


# Enhanced filters for better API experience
class EnhancedFilterMixin:
    """Enhanced filtering capabilities"""
    
    def get_queryset(self):
        """Enhanced queryset with advanced filtering"""
        queryset = super().get_queryset()
        
        # Date range filtering
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        # Ordering
        ordering = self.request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        # Search across multiple fields
        search = self.request.query_params.get('search')
        if search and hasattr(self, 'search_fields'):
            from django.db.models import Q
            search_query = Q()
            for field in self.search_fields:
                search_query |= Q(**{f"{field}__icontains": search})
            queryset = queryset.filter(search_query)
        
        return queryset


# API versioning response helpers
class VersionedResponseMixin:
    """Add version information to responses"""
    
    def finalize_response(self, request, response, *args, **kwargs):
        """Add version info to response headers"""
        response = super().finalize_response(request, response, *args, **kwargs)
        
        # Add API version to headers
        response['X-API-Version'] = getattr(request, 'version', '1.0')
        
        # Add version info to response data for JSON responses
        if (hasattr(response, 'data') and 
            isinstance(response.data, dict) and 
            response.get('content-type', '').startswith('application/json')):
            response.data['api_version'] = getattr(request, 'version', '1.0')
        
        return response


# Internationalization response helpers
class InternationalizedResponseMixin:
    """Add internationalization support to responses"""
    
    def get_success_message(self, action='retrieved'):
        """Get localized success message"""
        messages = {
            'retrieved': _('اطلاعات با موفقیت دریافت شد'),
            'created': _('رکورد جدید با موفقیت ایجاد شد'),
            'updated': _('اطلاعات با موفقیت به‌روزرسانی شد'),
            'deleted': _('رکورد با موفقیت حذف شد'),
        }
        return messages.get(action, _('عملیات با موفقیت انجام شد'))
    
    def get_error_message(self, error_type='general'):
        """Get localized error message"""
        messages = {
            'validation': _('اطلاعات ارسالی معتبر نیست'),
            'not_found': _('منبع مورد نظر یافت نشد'),
            'permission': _('شما اجازه دسترسی به این منبع را ندارید'),
            'authentication': _('برای دسترسی باید وارد شوید'),
            'general': _('خطایی در پردازش درخواست رخ داد'),
        }
        return messages.get(error_type, messages['general'])


# Enhanced API view base class
class EnhancedAPIView:
    """Base class for enhanced API views"""
    
    def dispatch(self, request, *args, **kwargs):
        """Enhanced dispatch with timing and logging"""
        start_time = time.time()
        
        # Add request timing
        request.start_time = start_time
        
        # Process request
        response = super().dispatch(request, *args, **kwargs)
        
        # Add performance headers
        if hasattr(response, 'data'):
            processing_time = round((time.time() - start_time) * 1000, 2)
            response['X-Processing-Time'] = f"{processing_time}ms"
        
        return response
    
    def handle_exception(self, exc):
        """Enhanced exception handling"""
        from rest_framework.views import exception_handler
        
        # Call DRF's default exception handler first
        response = exception_handler(exc, self.get_view_context())
        
        if response is not None:
            # Enhance error response format
            custom_response_data = {
                'success': False,
                'timestamp': datetime.now().isoformat(),
                'status_code': response.status_code,
                'message': self.get_error_message_for_exception(exc),
                'errors': response.data,
            }
            response.data = custom_response_data
        
        return response
    
    def get_error_message_for_exception(self, exc):
        """Get appropriate error message for exception type"""
        from rest_framework.exceptions import (
            ValidationError, NotFound, PermissionDenied, 
            AuthenticationFailed, NotAuthenticated
        )
        
        if isinstance(exc, ValidationError):
            return _('اطلاعات ارسالی معتبر نیست')
        elif isinstance(exc, NotFound):
            return _('منبع مورد نظر یافت نشد')
        elif isinstance(exc, (PermissionDenied,)):
            return _('شما اجازه دسترسی به این منبع را ندارید')
        elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
            return _('برای دسترسی باید وارد شوید')
        else:
            return _('خطایی در پردازش درخواست رخ داد')


# Response formatting utilities
class ResponseFormatter:
    """Utility class for response formatting"""
    
    @staticmethod
    def format_model_data(instance, serializer_class, request=None):
        """Format model instance data"""
        serializer = serializer_class(instance, context={'request': request} if request else {})
        return serializer.data
    
    @staticmethod
    def format_validation_errors(errors):
        """Format Django/DRF validation errors"""
        if isinstance(errors, dict):
            formatted_errors = {}
            for field, field_errors in errors.items():
                if isinstance(field_errors, list):
                    formatted_errors[field] = [str(error) for error in field_errors]
                else:
                    formatted_errors[field] = str(field_errors)
            return formatted_errors
        elif isinstance(errors, list):
            return [str(error) for error in errors]
        else:
            return str(errors)
    
    @staticmethod
    def add_request_metadata(response_data, request):
        """Add request metadata to response"""
        if isinstance(response_data, dict):
            response_data['request_info'] = {
                'method': request.method,
                'path': request.path,
                'user': str(request.user) if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
                'ip_address': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:100],  # Truncate for security
            }
        return response_data
