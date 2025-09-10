from django.apps import AppConfig


class DormitoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dormitory'
    verbose_name = 'مدیریت خوابگاه'
    verbose_name_plural = 'مدیریت خوابگاه‌ها'

    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.dormitory.signals  # noqa
        except ImportError:
            pass
