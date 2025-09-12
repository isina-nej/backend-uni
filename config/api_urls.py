from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

@api_view(['GET'])
def api_root(request):
    """Root endpoint for University Management API"""
    return Response({
        'name': 'University Management System API',
        'version': '1.0',
        'description': 'API for managing university operations including users, courses, grades, schedules, and more.',
        'endpoints': {
            'health': '/api/health/',
            'documentation': {
                'swagger': '/api/docs/',
                'redoc': '/api/redoc/',
                'schema': '/api/schema/'
            },
            'modules': {
                'users': '/api/users/',
                'courses': '/api/courses/',
                'grades': '/api/grades/',
                'schedules': '/api/schedules/',
                'exams': '/api/exams/',
                'library': '/api/library/',
                'financial': '/api/financial/',
                'attendance': '/api/attendance/',
                'research': '/api/research/',
                'announcements': '/api/announcements/',
                'assignments': '/api/assignments/',
                'notifications': '/api/notifications/',
                'analytics': '/api/analytics/',
                'data_management': '/api/data-management/',
                'mobile': '/api/mobile/',
                'ai_ml': '/api/ai-ml/',
                'dormitory': '/api/dormitory/',
                'reports': '/api/reports/'
            },
            'authentication': {
                'auth': '/api/auth/',
                'token': '/api/token/',
                'token_refresh': '/api/token/refresh/',
                'auth_token': '/api/auth/token/'
            }
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include('apps.common.urls')),  # Health check and API info
    path('users/', include('apps.users.urls')),
    path('courses/', include('apps.courses.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('data-management/', include('apps.data_management.urls')),
    path('mobile/', include('apps.mobile_api.urls')),
    path('ai-ml/', include('apps.ai_ml.urls')),
    path('grades/', include('apps.grades.urls')),
    path('schedules/', include('apps.schedules.urls')),
    path('exams/', include('apps.exams.urls')),
    path('library/', include('apps.library.urls')),
    path('financial/', include('apps.financial.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('research/', include('apps.research.urls')),
    path('announcements/', include('apps.announcements.urls')),
    path('assignments/', include('apps.assignments.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('dormitory/', include('apps.dormitory.urls')),  # اضافه شده: مدیریت خوابگاه
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reports/', include('apps.reports.urls')),
]
