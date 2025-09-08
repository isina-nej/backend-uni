from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('courses/', include('apps.courses.urls')),
    path('notifications/', include('apps.notifications.urls')),
]
