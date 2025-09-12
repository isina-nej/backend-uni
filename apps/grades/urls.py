from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .views import GradeViewSet

@api_view(['GET'])
def grades_root(request):
    """Root endpoint for Grades Management API"""
    return Response({
        'message': 'Grades Management API',
        'version': '1.0',
        'endpoints': {
            'grades': {
                'list': 'GET /grades/',
                'create': 'POST /grades/',
                'detail': 'GET /grades/{id}/',
                'update': 'PUT /grades/{id}/',
                'delete': 'DELETE /grades/{id}/',
                'by_course': 'GET /grades/by_course/{course_id}/',
                'by_student': 'GET /grades/by_student/{student_id}/',
                'statistics': 'GET /grades/statistics/',
                'bulk_create': 'POST /grades/bulk_create/',
                'bulk_update': 'PUT /grades/bulk_update/'
            }
        }
    })

router = DefaultRouter()
router.register(r'grades', GradeViewSet)

urlpatterns = [
    path('', grades_root, name='grades-root'),
    path('', include(router.urls)),
]
