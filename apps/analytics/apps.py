# ==============================================================================
# ANALYTICS APP CONFIGURATION
# پیکربندی اپلیکیشن آنالیتیکس
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AnalyticsConfig(AppConfig):
    """Configuration for Analytics application"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.analytics'
    verbose_name = _('آنالیتیکس و گزارش‌گیری')
    
    def ready(self):
        """Initialize the app when Django starts"""
        try:
            # Import signal handlers
            from . import signals
        except ImportError:
            pass
