from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', include('apps.common.urls')),  # Health check and API info
    path('users/', include('apps.users.urls')),
    path('courses/', include('apps.courses.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('data-management/', include('apps.data_management.urls')),
    path('mobile/', include('apps.mobile_api.urls')),
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
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reports/', include('apps.reports.urls')),
]
