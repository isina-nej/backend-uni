from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from config.monitoring import (
    HealthCheckView,
    SystemInfoView,
    APIVersionView,
    StatusView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Health and Monitoring
    path('api/health/', HealthCheckView.as_view(), name='health-check'),
    path('api/info/', SystemInfoView.as_view(), name='system-info'),
    path('api/version/', APIVersionView.as_view(), name='api-version'),
    path('api/status/', StatusView.as_view(), name='status'),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API routes
    path('api/', include('config.api_urls')),
]
