# ==============================================================================
# DATA MANAGEMENT URL PATTERNS
# الگوهای URL مدیریت داده‌ها
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'jobs', views.ImportExportJobViewSet, basename='import-export-job')
router.register(r'sync-tasks', views.DataSyncTaskViewSet, basename='data-sync-task')
router.register(r'backup-schedules', views.BackupScheduleViewSet, basename='backup-schedule')
router.register(r'integrations', views.ExternalSystemIntegrationViewSet, basename='external-integration')

app_name = 'data_management'

urlpatterns = [
    # API routes
    path('', include(router.urls)),
]
