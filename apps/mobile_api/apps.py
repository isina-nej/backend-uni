# ==============================================================================
# MOBILE API APPLICATION
# اپلیکیشن API موبایل
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.apps import AppConfig


class MobileApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.mobile_api'
    verbose_name = 'Mobile API'
    verbose_name_plural = 'Mobile APIs'
