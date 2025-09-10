from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DormitoryComplexViewSet, DormitoryBuildingViewSet,
    DormitoryRoomViewSet, DormitoryAccommodationViewSet,
    DormitoryStaffViewSet, DormitoryMaintenanceViewSet
)

router = DefaultRouter()
router.register(r'complexes', DormitoryComplexViewSet, basename='dormitory-complex')
router.register(r'buildings', DormitoryBuildingViewSet, basename='dormitory-building')
router.register(r'rooms', DormitoryRoomViewSet, basename='dormitory-room')
router.register(r'accommodations', DormitoryAccommodationViewSet, basename='dormitory-accommodation')
router.register(r'staff', DormitoryStaffViewSet, basename='dormitory-staff')
router.register(r'maintenance', DormitoryMaintenanceViewSet, basename='dormitory-maintenance')

urlpatterns = [
    path('api/dormitory/', include(router.urls)),
]
