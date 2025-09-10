# ==============================================================================
# SECURITY MIDDLEWARE FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import logging
import time
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger(__name__)


class SecurityMiddleware(MiddlewareMixin):
    """Middleware for security logging and monitoring"""

    def __init__(self, get_response):
        self.get_response = get_response
        # IPs that have been flagged for suspicious activity
        self.suspicious_ips = set()

    def __call__(self, request):
        # Start timing
        start_time = time.time()

        # Log request details
        self.log_request(request)

        # Check for suspicious patterns
        self.check_suspicious_activity(request)

        response = self.get_response(request)

        # Log response details
        duration = time.time() - start_time
        self.log_response(request, response, duration)

        return response

    def log_request(self, request):
        """Log incoming requests"""
        user = getattr(request, 'user', None)
        user_info = f"User: {user.username if user and user.is_authenticated else 'Anonymous'}"

        logger.info(
            f"REQUEST - {request.method} {request.path} - {user_info} - "
            f"IP: {self.get_client_ip(request)} - User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
        )

    def log_response(self, request, response, duration):
        """Log response details"""
        status_code = response.status_code
        level = 'WARNING' if status_code >= 400 else 'INFO'

        logger.log(
            getattr(logging, level),
            f"RESPONSE - {request.method} {request.path} - Status: {status_code} - "
            f"Duration: {duration:.3f}s"
        )

    def check_suspicious_activity(self, request):
        """Check for suspicious patterns"""
        client_ip = self.get_client_ip(request)

        # Check for SQL injection patterns
        sql_patterns = ['union', 'select', 'drop', 'insert', 'update', 'delete', '--', '/*', '*/']
        query_string = request.META.get('QUERY_STRING', '').lower()

        for pattern in sql_patterns:
            if pattern in query_string:
                logger.warning(
                    f"SUSPICIOUS SQL PATTERN - IP: {client_ip} - "
                    f"Pattern: {pattern} - Query: {query_string}"
                )
                self.suspicious_ips.add(client_ip)
                break

        # Check for XSS patterns
        xss_patterns = ['<script', 'javascript:', 'onload=', 'onerror=']
        for pattern in xss_patterns:
            if pattern in str(request.POST) or pattern in query_string:
                logger.warning(
                    f"SUSPICIOUS XSS PATTERN - IP: {client_ip} - "
                    f"Pattern: {pattern}"
                )
                self.suspicious_ips.add(client_ip)
                break

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware for detailed request logging"""

    def __call__(self, request):
        # Add request ID for tracking
        import uuid
        request.request_id = str(uuid.uuid4())[:8]

        # Log API requests
        if request.path.startswith('/api/'):
            user = getattr(request, 'user', None)
            username = user.username if user and hasattr(user, 'is_authenticated') and user.is_authenticated else 'Anonymous'
            logger.info(
                f"API_REQUEST [{request.request_id}] - {request.method} {request.path} - "
                f"User: {username}"
            )

        response = self.get_response(request)

        # Log API responses
        if request.path.startswith('/api/'):
            logger.info(
                f"API_RESPONSE [{request.request_id}] - {request.method} {request.path} - "
                f"Status: {response.status_code}"
            )

        return response
