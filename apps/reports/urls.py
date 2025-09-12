from django.urls import path
from . import views
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def reports_root(request):
    return Response({'message': 'Reports API', 'endpoints': ['dashboard/', 'student/', 'course/<id>/']})

urlpatterns = [
    path('', reports_root, name='reports_root'),
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    path('student/', views.student_report, name='student_report'),
    path('course/<int:course_id>/', views.course_report, name='course_report'),
]
