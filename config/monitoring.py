# ==============================================================================
# API HEALTH CHECK AND MONITORING
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from drf_spectacular.utils import extend_schema
import time
import psutil
import os
from datetime import datetime
from apps.users.models import User
from apps.courses.models import Course


class HealthCheckView(APIView):
    """API Health Check endpoint"""
    permission_classes = []  # Public endpoint
    
    @extend_schema(
        summary='سلامت سیستم',
        description='بررسی سلامت کلی سیستم و سرویس‌ها',
        responses={200: 'System is healthy'}
    )
    def get(self, request):
        """Check system health"""
        start_time = time.time()
        
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'environment': 'development' if settings.DEBUG else 'production',
            'checks': {}
        }
        
        # Database check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                health_data['checks']['database'] = {
                    'status': 'healthy',
                    'response_time_ms': round((time.time() - start_time) * 1000, 2)
                }
        except Exception as e:
            health_data['checks']['database'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_data['status'] = 'unhealthy'
        
        # Cache check
        cache_start = time.time()
        try:
            cache.set('health_check', 'test', 10)
            cache_result = cache.get('health_check')
            if cache_result == 'test':
                health_data['checks']['cache'] = {
                    'status': 'healthy',
                    'response_time_ms': round((time.time() - cache_start) * 1000, 2)
                }
            else:
                health_data['checks']['cache'] = {
                    'status': 'unhealthy',
                    'error': 'Cache test failed'
                }
                health_data['status'] = 'degraded'
        except Exception as e:
            health_data['checks']['cache'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_data['status'] = 'degraded'
        
        # Overall response time
        health_data['response_time_ms'] = round((time.time() - start_time) * 1000, 2)
        
        # Return appropriate status code
        status_code = status.HTTP_200_OK
        if health_data['status'] == 'unhealthy':
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        elif health_data['status'] == 'degraded':
            status_code = status.HTTP_206_PARTIAL_CONTENT
            
        return Response(health_data, status=status_code)


class SystemInfoView(APIView):
    """System information endpoint"""
    permission_classes = []  # Public endpoint
    
    @extend_schema(
        summary='اطلاعات سیستم',
        description='دریافت اطلاعات کلی سیستم و آمار',
        responses={200: 'System information'}
    )
    def get(self, request):
        """Get system information and statistics"""
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Database statistics
        try:
            total_users = User.objects.count()
            total_courses = Course.objects.count()
            active_users = User.objects.filter(is_active=True).count()
        except Exception:
            total_users = total_courses = active_users = 0
        
        system_info = {
            'api_version': '1.0.0',
            'django_version': '4.2.7',
            'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            'environment': 'development' if settings.DEBUG else 'production',
            'timezone': settings.TIME_ZONE,
            'language': settings.LANGUAGE_CODE,
            'features': {
                'authentication': ['Token', 'JWT', 'Session'],
                'filtering': True,
                'pagination': True,
                'caching': True,
                'api_documentation': True,
                'versioning': True,
                'internationalization': True,
                'error_handling': True,
                'monitoring': True,
            },
            'system_metrics': {
                'cpu_usage_percent': cpu_percent,
                'memory_usage_percent': memory.percent,
                'disk_usage_percent': disk.percent,
                'memory_total_gb': round(memory.total / (1024**3), 2),
                'memory_available_gb': round(memory.available / (1024**3), 2),
                'disk_total_gb': round(disk.total / (1024**3), 2),
                'disk_free_gb': round(disk.free / (1024**3), 2),
            },
            'database_statistics': {
                'total_users': total_users,
                'active_users': active_users,
                'total_courses': total_courses,
            },
            'endpoints': {
                'api_root': '/api/',
                'documentation': {
                    'swagger': '/api/docs/',
                    'redoc': '/api/redoc/',
                    'schema': '/api/schema/'
                },
                'health_check': '/api/health/',
                'system_info': '/api/info/',
            }
        }
        
        return Response(system_info)


class APIVersionView(APIView):
    """API version information"""
    permission_classes = []
    
    @extend_schema(
        summary='اطلاعات نسخه API',
        description='دریافت اطلاعات نسخه‌های مختلف API',
        responses={200: 'Version information'}
    )
    def get(self, request):
        """Get API version information"""
        from config.versioning import get_api_version_info
        return Response(get_api_version_info())


class StatusView(APIView):
    """Simple status endpoint"""
    permission_classes = []
    
    @extend_schema(
        summary='وضعیت سرویس',
        description='بررسی ساده وضعیت سرویس',
        responses={200: 'Service status'}
    )
    def get(self, request):
        """Get simple service status"""
        return Response({
            'status': 'online',
            'message': 'University Management System API is running',
            'timestamp': datetime.now().isoformat(),
            'uptime': 'Available since startup'
        })


# Middleware for request monitoring
class MonitoringMiddleware:
    """Middleware to monitor API requests"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_time = time.time()
    
    def __call__(self, request):
        # Record request start time
        request_start = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Calculate response time
        response_time = (time.time() - request_start) * 1000
        
        # Add response time header
        response['X-Response-Time'] = f"{response_time:.2f}ms"
        
        # Add version header
        response['X-API-Version'] = getattr(request, 'version', '1.0')
        
        # Log slow requests (> 1000ms)
        if response_time > 1000:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Slow request: {request.method} {request.path} took {response_time:.2f}ms")
        
        return response
    
    def process_exception(self, request, exception):
        """Log exceptions"""
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Exception in {request.method} {request.path}: {exception}", exc_info=True)
        return None


# Custom 404 handler
def custom_404_handler(request, exception=None):
    """Custom 404 error handler"""
    from rest_framework.response import Response
    from rest_framework import status
    
    error_data = {
        'error': True,
        'message': 'منبع مورد نظر یافت نشد',
        'error_code': 'NOT_FOUND',
        'path': request.path,
        'method': request.method,
        'suggestions': [
            'بررسی کنید که URL صحیح باشد',
            'مستندات API را مطالعه کنید',
            'از endpoint های موجود استفاده کنید'
        ],
        'available_endpoints': {
            'api_docs': '/api/docs/',
            'health_check': '/api/health/',
            'users': '/api/users/',
            'courses': '/api/courses/',
        }
    }
    
    return Response(error_data, status=status.HTTP_404_NOT_FOUND)


# Performance monitoring utilities
class PerformanceMonitor:
    """Monitor API performance"""
    
    @staticmethod
    def log_performance_metrics():
        """Log performance metrics"""
        import logging
        logger = logging.getLogger('performance')
        
        # System metrics
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        
        logger.info(f"System Performance - CPU: {cpu_percent}%, Memory: {memory.percent}%")
    
    @staticmethod
    def check_database_performance():
        """Check database query performance"""
        from django.db import connection
        
        # Get database queries info
        queries = connection.queries
        if queries:
            total_time = sum(float(query['time']) for query in queries)
            slow_queries = [q for q in queries if float(q['time']) > 0.1]
            
            if slow_queries:
                import logging
                logger = logging.getLogger('performance')
                logger.warning(f"Found {len(slow_queries)} slow database queries")
    
    @staticmethod
    def get_cache_stats():
        """Get cache performance statistics"""
        try:
            # This would depend on your cache backend
            # For Redis, you could get stats like hit rate, memory usage, etc.
            from django.core.cache import cache
            
            # Test cache performance
            start_time = time.time()
            cache.set('perf_test', 'test_value', 1)
            cache.get('perf_test')
            cache_time = (time.time() - start_time) * 1000
            
            return {
                'cache_response_time_ms': round(cache_time, 2),
                'status': 'healthy' if cache_time < 10 else 'slow'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
