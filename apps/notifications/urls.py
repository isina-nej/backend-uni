# ==============================================================================
# NOTIFICATION URL PATTERNS WITH WEBSOCKET SUPPORT
# الگوهای URL اعلانات با پشتیبانی وب‌سوکت
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'preferences', views.NotificationPreferenceViewSet, basename='notification-preference')
router.register(r'templates', views.NotificationTemplateViewSet, basename='notification-template')
router.register(r'connections', views.WebSocketConnectionViewSet, basename='websocket-connection')
router.register(r'admin/notifications', views.AdminNotificationViewSet, basename='admin-notification')

app_name = 'notifications'

urlpatterns = [
    # API routes
    path('', include(router.urls)),
]
