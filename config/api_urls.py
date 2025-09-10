from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('', include('apps.common.urls')),  # Health check and API info - temporarily disabled
    path('users/', include('apps.users.urls')),
    # path('courses/', include('apps.courses.urls')),  # temporarily disabled
    # path('notifications/', include('apps.notifications.urls')),  # temporarily disabled
    # path('grades/', include('apps.grades.urls')),  # temporarily disabled
    # path('schedules/', include('apps.schedules.urls')),  # temporarily disabled
    # path('exams/', include('apps.exams.urls')),  # temporarily disabled
    # path('library/', include('apps.library.urls')),  # temporarily disabled
    # path('financial/', include('apps.financial.urls')),  # temporarily disabled
    # path('attendance/', include('apps.attendance.urls')),  # temporarily disabled
    # path('research/', include('apps.research.urls')),  # temporarily disabled
    # path('announcements/', include('apps.announcements.urls')),  # temporarily disabled
    # path('assignments/', include('apps.assignments.urls')),  # temporarily disabled
    # path('auth/', include('apps.authentication.urls')),  # temporarily disabled
    # path('auth/token/', obtain_auth_token, name='api_token_auth'),  # temporarily disabled
    # path('reports/', include('apps.reports.urls')),  # temporarily disabled
]
