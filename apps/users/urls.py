from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, OrganizationalUnitViewSet, PositionViewSet,
    UserPositionViewSet, PermissionViewSet, UserPermissionViewSet,
    AccessLogViewSet
)

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'organizational-units', OrganizationalUnitViewSet, basename='organizational-unit')
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'user-positions', UserPositionViewSet, basename='user-position')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'user-permissions', UserPermissionViewSet, basename='user-permission')
router.register(r'access-logs', AccessLogViewSet, basename='access-log')

urlpatterns = [
    path('', include(router.urls)),
]
