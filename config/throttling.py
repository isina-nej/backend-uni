# ==============================================================================
# CUSTOM THROTTLING FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle
import logging

logger = logging.getLogger(__name__)


class BurstRateThrottle(SimpleRateThrottle):
    """Throttle for burst requests (short time window)"""
    scope = 'burst'
    rate = '60/minute'  # 60 requests per minute

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return f"burst_{request.user.pk}"
        return self.get_ident(request)


class SustainedRateThrottle(SimpleRateThrottle):
    """Throttle for sustained requests (longer time window)"""
    scope = 'sustained'
    rate = '1000/hour'  # 1000 requests per hour

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return f"sustained_{request.user.pk}"
        return self.get_ident(request)


class StrictUserRateThrottle(UserRateThrottle):
    """Stricter throttle for authenticated users"""
    scope = 'strict_user'
    rate = '500/hour'  # 500 requests per hour for authenticated users


class APIEndpointThrottle(SimpleRateThrottle):
    """Specific throttle for API endpoints"""
    scope = 'api'

    def get_rate(self):
        # Different rates for different endpoints
        if self.view and hasattr(self.view, 'get_view_name'):
            view_name = self.view.get_view_name().lower()
            if 'auth' in view_name:
                return '10/minute'  # Stricter for auth endpoints
            elif 'search' in view_name:
                return '30/minute'  # Moderate for search
            else:
                return '100/minute'  # Normal for other endpoints
        return '100/minute'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return f"api_{request.user.pk}_{view.__class__.__name__}"
        return f"api_anon_{self.get_ident(request)}_{view.__class__.__name__}"

    def allow_request(self, request, view):
        allowed = super().allow_request(request, view)
        if not allowed:
            logger.warning(
                f"Rate limit exceeded for {request.method} {request.path} - "
                f"User: {getattr(request.user, 'username', 'Anonymous')} - "
                f"IP: {self.get_ident(request)}"
            )
        return allowed
