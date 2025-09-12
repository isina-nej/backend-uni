from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .views import (
    DormitoryComplexViewSet, DormitoryBuildingViewSet,
    DormitoryRoomViewSet, DormitoryAccommodationViewSet,
    DormitoryStaffViewSet, DormitoryMaintenanceViewSet
)

@api_view(['GET'])
def dormitory_root(request):
    """Root endpoint for Dormitory Management API"""
    return Response({
        'message': 'Dormitory Management API',
        'version': '1.0',
        'endpoints': {
            'complexes': {
                'list': 'GET /complexes/',
                'create': 'POST /complexes/',
                'detail': 'GET /complexes/{id}/',
                'update': 'PUT /complexes/{id}/',
                'delete': 'DELETE /complexes/{id}/',
                'statistics': 'GET /complexes/{id}/statistics/',
                'available_rooms': 'GET /complexes/{id}/available_rooms/'
            },
            'buildings': {
                'list': 'GET /buildings/',
                'create': 'POST /buildings/',
                'detail': 'GET /buildings/{id}/',
                'update': 'PUT /buildings/{id}/',
                'delete': 'DELETE /buildings/{id}/'
            },
            'rooms': {
                'list': 'GET /rooms/',
                'create': 'POST /rooms/',
                'detail': 'GET /rooms/{id}/',
                'update': 'PUT /rooms/{id}/',
                'delete': 'DELETE /rooms/{id}/',
                'available': 'GET /rooms/available/',
                'maintenance_history': 'GET /rooms/{id}/maintenance_history/'
            },
            'accommodations': {
                'list': 'GET /accommodations/',
                'create': 'POST /accommodations/',
                'detail': 'GET /accommodations/{id}/',
                'update': 'PUT /accommodations/{id}/',
                'delete': 'DELETE /accommodations/{id}/',
                'my_accommodations': 'GET /accommodations/my_accommodations/',
                'approve': 'POST /accommodations/{id}/approve/'
            },
            'staff': {
                'list': 'GET /staff/',
                'create': 'POST /staff/',
                'detail': 'GET /staff/{id}/',
                'update': 'PUT /staff/{id}/',
                'delete': 'DELETE /staff/{id}/'
            },
            'maintenance': {
                'list': 'GET /maintenance/',
                'create': 'POST /maintenance/',
                'detail': 'GET /maintenance/{id}/',
                'update': 'PUT /maintenance/{id}/',
                'delete': 'DELETE /maintenance/{id}/'
            }
        }
    })

router = DefaultRouter()
router.register(r'complexes', DormitoryComplexViewSet, basename='dormitory-complex')
router.register(r'buildings', DormitoryBuildingViewSet, basename='dormitory-building')
router.register(r'rooms', DormitoryRoomViewSet, basename='dormitory-room')
router.register(r'accommodations', DormitoryAccommodationViewSet, basename='dormitory-accommodation')
router.register(r'staff', DormitoryStaffViewSet, basename='dormitory-staff')
router.register(r'maintenance', DormitoryMaintenanceViewSet, basename='dormitory-maintenance')

urlpatterns = [
    path('', dormitory_root, name='dormitory-root'),
    path('', include(router.urls)),
]
