# ==============================================================================
# MOBILE API URL PATTERNS
# الگوهای URL برای API موبایل
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'devices', views.MobileDeviceViewSet, basename='mobile-device')
router.register(r'sessions', views.MobileSessionViewSet, basename='mobile-session')
router.register(r'notifications', views.PushNotificationViewSet, basename='push-notification')
router.register(r'sync', views.OfflineSyncViewSet, basename='offline-sync')
router.register(r'settings', views.MobileSettingsViewSet, basename='mobile-settings')
router.register(r'dashboard', views.MobileDashboardViewSet, basename='mobile-dashboard')

app_name = 'mobile_api'

urlpatterns = [
    # API routes
    path('', include(router.urls)),
]
