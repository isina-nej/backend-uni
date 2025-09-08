from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    path('student/', views.student_report, name='student_report'),
    path('course/<int:course_id>/', views.course_report, name='course_report'),
]
