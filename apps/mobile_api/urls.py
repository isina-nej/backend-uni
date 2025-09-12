# ==============================================================================
# MOBILE API URL PATTERNS
# الگوهای URL برای API موبایل
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import views

@api_view(['GET'])
def mobile_api_root(request):
    """Root endpoint for Mobile API"""
    return Response({
        'message': 'Mobile API',
        'version': '1.0',
        'endpoints': {
            'devices': {
                'list': 'GET /devices/',
                'create': 'POST /devices/',
                'detail': 'GET /devices/{id}/',
                'update': 'PUT /devices/{id}/',
                'delete': 'DELETE /devices/{id}/',
                'register': 'POST /devices/register/',
                'unregister': 'POST /devices/{id}/unregister/'
            },
            'sessions': {
                'list': 'GET /sessions/',
                'create': 'POST /sessions/',
                'detail': 'GET /sessions/{id}/',
                'update': 'PUT /sessions/{id}/',
                'delete': 'DELETE /sessions/{id}/',
                'start': 'POST /sessions/start/',
                'end': 'POST /sessions/{id}/end/',
                'update_activity': 'POST /sessions/{id}/update_activity/'
            },
            'notifications': {
                'list': 'GET /notifications/',
                'create': 'POST /notifications/',
                'detail': 'GET /notifications/{id}/',
                'update': 'PUT /notifications/{id}/',
                'delete': 'DELETE /notifications/{id}/',
                'send': 'POST /notifications/send/'
            },
            'sync': {
                'list': 'GET /sync/',
                'create': 'POST /sync/',
                'detail': 'GET /sync/{id}/',
                'update': 'PUT /sync/{id}/',
                'delete': 'DELETE /sync/{id}/',
                'sync_data': 'POST /sync/sync_data/',
                'get_changes': 'GET /sync/get_changes/'
            },
            'settings': {
                'list': 'GET /settings/',
                'create': 'POST /settings/',
                'detail': 'GET /settings/{id}/',
                'update': 'PUT /settings/{id}/',
                'delete': 'DELETE /settings/{id}/'
            },
            'dashboard': {
                'list': 'GET /dashboard/',
                'stats': 'GET /dashboard/stats/',
                'notifications': 'GET /dashboard/notifications/',
                'schedule': 'GET /dashboard/schedule/'
            }
        }
    })

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
    # Root endpoint
    path('', mobile_api_root, name='mobile-api-root'),
    
    # API routes
    path('', include(router.urls)),
]
