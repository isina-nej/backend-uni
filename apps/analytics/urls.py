# ==============================================================================
# ANALYTICS URL PATTERNS
# الگوهای URL آنالیتیکس
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'dashboards', views.DashboardViewSet, basename='dashboard')
router.register(r'widgets', views.WidgetViewSet, basename='widget')
router.register(r'reports', views.ReportViewSet, basename='report')
router.register(r'executions', views.ReportExecutionViewSet, basename='report-execution')
router.register(r'analytics', views.AnalyticsViewSet, basename='analytics')

app_name = 'analytics'

urlpatterns = [
    # API routes
    path('', include(router.urls)),
    
    # Custom endpoints
    path('data-sources/', views.DataSourceListView.as_view(), name='data-sources'),
    path('data-sources/<str:source_name>/data/', views.DataSourceDataView.as_view(), name='data-source-data'),
]
