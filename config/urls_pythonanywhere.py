# URL Configuration for PythonAnywhere deployment
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Routes
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/courses/', include('apps.courses.urls')),
    path('api/grades/', include('apps.grades.urls')),
    path('api/attendance/', include('apps.attendance.urls')),
    path('api/schedules/', include('apps.schedules.urls')),
    path('api/exams/', include('apps.exams.urls')),
    path('api/library/', include('apps.library.urls')),
    path('api/financial/', include('apps.financial.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/data-management/', include('apps.data_management.urls')),
    path('api/mobile/', include('apps.mobile_api.urls')),
    path('api/ai-ml/', include('apps.ai_ml.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/research/', include('apps.research.urls')),
    path('api/announcements/', include('apps.announcements.urls')),
    path('api/assignments/', include('apps.assignments.urls')),
    path('api/dormitory/', include('apps.dormitory.urls')),
    path('api/', include('apps.common.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers for production
handler404 = 'config.views.custom_404'
handler500 = 'config.views.custom_500'
