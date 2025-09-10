from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # New hierarchical models
    MinistryViewSet, UniversityViewSet, FacultyViewSet, DepartmentViewSet,
    ResearchCenterViewSet, AdministrativeUnitViewSet, PositionViewSet,
    EmployeeViewSet, StudentViewSet, AccessControlViewSet,
    UserAccessViewSet, AuditLogViewSet,
    # Legacy models for compatibility
    UserViewSet, OrganizationalUnitViewSet, UserPositionViewSet,
    PermissionViewSet, UserPermissionViewSet, AccessLogOldViewSet
)

router = DefaultRouter()

# New hierarchical university structure
router.register(r'ministries', MinistryViewSet, basename='ministry')
router.register(r'universities', UniversityViewSet, basename='university')
router.register(r'faculties', FacultyViewSet, basename='faculty')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'research-centers', ResearchCenterViewSet, basename='research-center')
router.register(r'administrative-units', AdministrativeUnitViewSet, basename='administrative-unit')
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'access-controls', AccessControlViewSet, basename='access-control')
router.register(r'user-access', UserAccessViewSet, basename='user-access')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

# Legacy models for compatibility
router.register(r'users', UserViewSet, basename='user')
router.register(r'organizational-units', OrganizationalUnitViewSet, basename='organizational-unit')
router.register(r'user-positions', UserPositionViewSet, basename='user-position')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'user-permissions', UserPermissionViewSet, basename='user-permission')
router.register(r'access-logs-old', AccessLogOldViewSet, basename='access-log-old')

urlpatterns = [
    path('', include(router.urls)),
]
