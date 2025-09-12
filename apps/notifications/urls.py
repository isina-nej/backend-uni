# ==============================================================================
# NOTIFICATION URL PATTERNS WITH WEBSOCKET SUPPORT
# الگوهای URL اعلانات با پشتیبانی وب‌سوکت
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import views

@api_view(['GET'])
def notifications_root(request):
    """Root endpoint for Notifications API"""
    return Response({
        'message': 'Notifications Management API',
        'version': '1.0',
        'endpoints': {
            'notifications': {
                'list': 'GET /notifications/',
                'create': 'POST /notifications/',
                'detail': 'GET /notifications/{id}/',
                'update': 'PUT /notifications/{id}/',
                'delete': 'DELETE /notifications/{id}/',
                'mark_read': 'POST /notifications/{id}/mark_read/',
                'mark_unread': 'POST /notifications/{id}/mark_unread/',
                'bulk_mark_read': 'POST /notifications/bulk_mark_read/'
            },
            'preferences': {
                'list': 'GET /preferences/',
                'create': 'POST /preferences/',
                'detail': 'GET /preferences/{id}/',
                'update': 'PUT /preferences/{id}/',
                'delete': 'DELETE /preferences/{id}/'
            },
            'templates': {
                'list': 'GET /templates/',
                'create': 'POST /templates/',
                'detail': 'GET /templates/{id}/',
                'update': 'PUT /templates/{id}/',
                'delete': 'DELETE /templates/{id}/'
            },
            'connections': {
                'list': 'GET /connections/',
                'create': 'POST /connections/',
                'detail': 'GET /connections/{id}/',
                'update': 'PUT /connections/{id}/',
                'delete': 'DELETE /connections/{id}/'
            },
            'admin': {
                'notifications': 'GET /admin/notifications/',
                'broadcast': 'POST /admin/notifications/broadcast/',
                'statistics': 'GET /admin/notifications/statistics/'
            }
        }
    })

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'preferences', views.NotificationPreferenceViewSet, basename='notification-preference')
router.register(r'templates', views.NotificationTemplateViewSet, basename='notification-template')
router.register(r'connections', views.WebSocketConnectionViewSet, basename='websocket-connection')
router.register(r'admin/notifications', views.AdminNotificationViewSet, basename='admin-notification')

app_name = 'notifications'

urlpatterns = [
    # Root endpoint
    path('', notifications_root, name='notifications-root'),
    
    # API routes
    path('', include(router.urls)),
]
