# ==============================================================================
# DATA MANAGEMENT APP CONFIGURATION
# تنظیمات اپلیکیشن مدیریت داده‌ها
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.apps import AppConfig


class DataManagementConfig(AppConfig):
    """Configuration for Data Management app"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.data_management'
    verbose_name = 'Data Management'
    verbose_name_plural = 'Data Management Systems'
    
    def ready(self):
        """Initialize the app when Django starts"""
        try:
            # Import signals to ensure they're registered
            from . import signals
        except ImportError:
            pass
