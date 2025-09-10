# ==============================================================================
# SECURITY SETTINGS FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
import re
import logging

logger = logging.getLogger(__name__)


class SQLInjectionProtectionMiddleware(MiddlewareMixin):
    """Middleware to protect against SQL injection"""

    SQL_PATTERNS = [
        r'union\s+select',
        r';\s*drop',
        r';\s*delete',
        r';\s*update',
        r';\s*insert',
        r'--',
        r'/\*.*\*/',
        r'xp_cmdshell',
        r'exec\s*\(',
        r'cast\s*\(',
        r'convert\s*\(',
    ]

    def __call__(self, request):
        # Check query parameters
        for key, value in request.GET.items():
            if self._contains_sql_injection(str(value)):
                logger.warning(
                    f"SQL Injection attempt detected in query parameter - "
                    f"IP: {self._get_client_ip(request)} - Param: {key} - Value: {value}"
                )
                return HttpResponseForbidden("Invalid request")

        # Check POST data
        if request.method == 'POST':
            for key, value in request.POST.items():
                if self._contains_sql_injection(str(value)):
                    logger.warning(
                        f"SQL Injection attempt detected in POST data - "
                        f"IP: {self._get_client_ip(request)} - Param: {key}"
                    )
                    return HttpResponseForbidden("Invalid request")

        return self.get_response(request)

    def _contains_sql_injection(self, value):
        """Check if value contains SQL injection patterns"""
        value_lower = value.lower()
        for pattern in self.SQL_PATTERNS:
            if re.search(pattern, value_lower, re.IGNORECASE):
                return True
        return False

    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class XSSProtectionMiddleware(MiddlewareMixin):
    """Middleware to protect against XSS attacks"""

    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'vbscript:',
        r'onload\s*=',
        r'onerror\s*=',
        r'onclick\s*=',
        r'<iframe[^>]*>',
        r'<object[^>]*>',
        r'<embed[^>]*>',
        r'eval\s*\(',
        r'document\.cookie',
        r'document\.location',
    ]

    def __call__(self, request):
        # Check query parameters
        for key, value in request.GET.items():
            if self._contains_xss(str(value)):
                logger.warning(
                    f"XSS attempt detected in query parameter - "
                    f"IP: {self._get_client_ip(request)} - Param: {key} - Value: {value}"
                )
                return HttpResponseForbidden("Invalid request")

        # Check POST data
        if request.method == 'POST':
            for key, value in request.POST.items():
                if self._contains_xss(str(value)):
                    logger.warning(
                        f"XSS attempt detected in POST data - "
                        f"IP: {self._get_client_ip(request)} - Param: {key}"
                    )
                    return HttpResponseForbidden("Invalid request")

        return self.get_response(request)

    def _contains_xss(self, value):
        """Check if value contains XSS patterns"""
        for pattern in self.XSS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE | re.DOTALL):
                return True
        return False

    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Middleware to add security headers"""

    def __call__(self, request):
        response = self.get_response(request)

        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

        # Content Security Policy (basic)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response['Content-Security-Policy'] = csp

        return response


# Security utility functions
def sanitize_input(value):
    """Sanitize user input"""
    if not value:
        return value

    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", ';', '--', '/*', '*/']
    for char in dangerous_chars:
        value = value.replace(char, '')

    return value.strip()


def validate_file_upload(file):
    """Validate uploaded file"""
    if not file:
        return False

    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024
    if file.size > max_size:
        return False

    # Check file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
    file_name = file.name.lower()
    if not any(file_name.endswith(ext) for ext in allowed_extensions):
        return False

    return True
