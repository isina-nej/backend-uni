from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .views import ScheduleViewSet

@api_view(['GET'])
def schedules_root(request):
    """Root endpoint for Schedules Management API"""
    return Response({
        'message': 'Schedules Management API',
        'version': '1.0',
        'endpoints': {
            'schedules': {
                'list': 'GET /schedules/',
                'create': 'POST /schedules/',
                'detail': 'GET /schedules/{id}/',
                'update': 'PUT /schedules/{id}/',
                'delete': 'DELETE /schedules/{id}/',
                'by_course': 'GET /schedules/by_course/{course_id}/',
                'by_instructor': 'GET /schedules/by_instructor/{instructor_id}/',
                'by_room': 'GET /schedules/by_room/{room_id}/',
                'conflicts': 'GET /schedules/conflicts/',
                'calendar': 'GET /schedules/calendar/',
                'weekly': 'GET /schedules/weekly/',
                'today': 'GET /schedules/today/'
            }
        }
    })

router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet)

urlpatterns = [
    path('', schedules_root, name='schedules-root'),
    path('', include(router.urls)),
]
