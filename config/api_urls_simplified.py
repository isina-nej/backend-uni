# ==============================================================================
# SIMPLIFIED API URLS FOR PYTHONANYWHERE DEPLOYMENT
# URL های ساده‌شده برای استقرار PythonAnywhere
# ==============================================================================

from django.urls import path, include

app_name = 'api'

# Only include URLs for apps that are installed and working
urlpatterns = [
    # Authentication
    path('auth/', include('apps.authentication.urls')),
    
    # Core apps
    path('users/', include('apps.users.urls')),
    path('courses/', include('apps.courses.urls')),
    path('grades/', include('apps.grades.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('schedules/', include('apps.schedules.urls')),
    path('exams/', include('apps.exams.urls')),
    path('library/', include('apps.library.urls')),
    path('financial/', include('apps.financial.urls')),
    
    # Additional apps (if they work without complex dependencies)
    path('analytics/', include('apps.analytics.urls')),
    path('data-management/', include('apps.data_management.urls')),
    path('mobile/', include('apps.mobile_api.urls')),
    path('reports/', include('apps.reports.urls')),
    path('research/', include('apps.research.urls')),
    path('announcements/', include('apps.announcements.urls')),
    path('assignments/', include('apps.assignments.urls')),
    path('dormitory/', include('apps.dormitory.urls')),
    
    # Common utilities
    path('', include('apps.common.urls')),
]

# Note: Disabled problematic apps:
# - notifications (requires channels)
# - ai_ml (may have heavy dependencies)
