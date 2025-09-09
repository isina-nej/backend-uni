from django.urls import path, include

urlpatterns = [
    path('', include('apps.common.urls')),  # Health check and API info
    path('users/', include('apps.users.urls')),
    path('courses/', include('apps.courses.urls')),
    path('notifications/', include('apps.notifications.urls')),
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
    path('reports/', include('apps.reports.urls')),
]
