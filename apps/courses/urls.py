from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .views import CourseViewSet

@api_view(['GET'])
def courses_root(request):
    """Root endpoint for Courses API"""
    return Response({
        'message': 'Courses Management API',
        'version': '1.0',
        'endpoints': {
            'courses': {
                'list': 'GET /courses/',
                'create': 'POST /courses/',
                'detail': 'GET /courses/{id}/',
                'update': 'PUT /courses/{id}/',
                'delete': 'DELETE /courses/{id}/',
                'enroll': 'POST /courses/{id}/enroll/',
                'unenroll': 'POST /courses/{id}/unenroll/',
                'students': 'GET /courses/{id}/students/',
                'grades': 'GET /courses/{id}/grades/',
                'statistics': 'GET /courses/{id}/statistics/'
            }
        }
    })

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', courses_root, name='courses-root'),
    path('', include(router.urls)),
]
