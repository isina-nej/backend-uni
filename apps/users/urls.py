# ==============================================================================
# URL CONFIGURATION FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    # Authentication
    AuthViewSet,
    # User Management
    UserViewSet,
    # Organizational
    MinistryViewSet, UniversityViewSet, FacultyViewSet, DepartmentViewSet,
    ResearchCenterViewSet, AdministrativeUnitViewSet,
    # Position & Access
    PositionViewSet, AccessLevelViewSet,
    # Employee
    EmployeeViewSet, EmployeeDutyViewSet,
    # Student
    StudentCategoryViewSet, AcademicProgramViewSet, StudentViewSet,
    StudentCategoryAssignmentViewSet,
    # Dashboard
    DashboardViewSet
)

# ==============================================================================
# ROUTER CONFIGURATION
# ==============================================================================

router = DefaultRouter()

# Authentication (بدون prefix برای راحتی)
router.register(r'auth', AuthViewSet, basename='auth')

# User Management
router.register(r'', UserViewSet, basename='user')

# Organizational Hierarchy
router.register(r'ministries', MinistryViewSet, basename='ministry')
router.register(r'universities', UniversityViewSet, basename='university')
router.register(r'faculties', FacultyViewSet, basename='faculty')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'research-centers', ResearchCenterViewSet, basename='research-center')
router.register(r'administrative-units', AdministrativeUnitViewSet, basename='administrative-unit')

# Position and Access Control
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'access-levels', AccessLevelViewSet, basename='access-level')

# Employee Management
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'employee-duties', EmployeeDutyViewSet, basename='employee-duty')

# Student Management
router.register(r'student-categories', StudentCategoryViewSet, basename='student-category')
router.register(r'academic-programs', AcademicProgramViewSet, basename='academic-program')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'student-category-assignments', StudentCategoryAssignmentViewSet, basename='student-category-assignment')
# router.register(r'academic-records', AcademicRecordViewSet, basename='academic-record')  # Removed temporarily

# Dashboard and Statistics
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

# ==============================================================================
# URL PATTERNS
# ==============================================================================

urlpatterns = [
    # API Router URLs
    path('api/', include(router.urls)),
    
    # JWT Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # DRF Browsable API Authentication
    path('api-auth/', include('rest_framework.urls')),
]

# ==============================================================================
# CUSTOM URL PATTERNS (اختیاری)
# ==============================================================================

# URL patterns اضافی برای endpoint های خاص
extra_patterns = [
    # Authentication shortcuts
    path('api/register/', AuthViewSet.as_view({'post': 'register'}), name='user-register'),
    path('api/login/', AuthViewSet.as_view({'post': 'login'}), name='user-login'),
    path('api/logout/', AuthViewSet.as_view({'post': 'logout'}), name='user-logout'),
    path('api/profile/', AuthViewSet.as_view({'get': 'profile', 'put': 'update_profile'}), name='user-profile'),
    
    # Quick access to statistics
    path('api/stats/', DashboardViewSet.as_view({'get': 'stats'}), name='dashboard-stats'),
    path('api/recent-activities/', DashboardViewSet.as_view({'get': 'recent_activities'}), name='recent-activities'),
    path('api/system-health/', DashboardViewSet.as_view({'get': 'system_health'}), name='system-health'),
]

urlpatterns += extra_patterns

# ==============================================================================
# API DOCUMENTATION
# ==============================================================================

"""
API Endpoints Documentation:

## Authentication
- POST /api/register/ - ثبت‌نام کاربر جدید
- POST /api/login/ - ورود کاربر
- POST /api/logout/ - خروج کاربر
- GET /api/profile/ - دریافت پروفایل کاربر
- PUT /api/profile/ - به‌روزرسانی پروفایل

## Universities and Organizational Structure
- GET /api/universities/ - لیست دانشگاه‌ها
- POST /api/universities/ - ایجاد دانشگاه جدید
- GET /api/universities/{id}/ - جزئیات دانشگاه
- PUT /api/universities/{id}/ - ویرایش دانشگاه
- DELETE /api/universities/{id}/ - حذف دانشگاه
- GET /api/universities/{id}/statistics/ - آمار دانشگاه
- GET /api/universities/{id}/faculties/ - دانشکده‌های دانشگاه

- GET /api/faculties/ - لیست دانشکده‌ها
- GET /api/faculties/{id}/departments/ - گروه‌های دانشکده

- GET /api/departments/ - لیست گروه‌های آموزشی

## Employee Management
- GET /api/employees/ - لیست کارکنان
- POST /api/employees/ - ایجاد کارمند جدید
- GET /api/employees/{id}/ - جزئیات کارمند
- GET /api/employees/{id}/duties/ - وظایف کارمند
- POST /api/employees/{id}/assign_duty/ - تخصیص وظیفه
- PUT /api/employees/{id}/change_status/ - تغییر وضعیت استخدام

## Student Management
- GET /api/students/ - لیست دانشجویان
- POST /api/students/ - ایجاد دانشجوی جدید
- GET /api/students/{id}/ - جزئیات دانشجو
- GET /api/students/{id}/academic_record/ - پرونده تحصیلی
- GET /api/students/{id}/categories/ - دسته‌های دانشجو
- POST /api/students/{id}/assign_category/ - تخصیص به دسته
- PUT /api/students/{id}/change_status/ - تغییر وضعیت تحصیلی
- GET /api/students/{id}/enrollment_eligibility/ - بررسی واجد شرایط بودن

## Academic Programs
- GET /api/academic-programs/ - لیست برنامه‌های تحصیلی
- GET /api/academic-programs/{id}/students/ - دانشجویان برنامه
- GET /api/academic-programs/{id}/capacity_status/ - وضعیت ظرفیت

## Dashboard and Statistics
- GET /api/stats/ - آمار کلی سیستم
- GET /api/recent-activities/ - فعالیت‌های اخیر
- GET /api/system-health/ - سلامت سیستم

## Filtering and Search
تمام endpoint ها از فیلترینگ، جستجو و مرتب‌سازی پشتیبانی می‌کنند:
- ?search=term - جستجو در فیلدهای مشخص شده
- ?ordering=field - مرتب‌سازی بر اساس فیلد
- ?field=value - فیلتر بر اساس فیلد خاص
- ?page=1 - صفحه‌بندی

مثال:
GET /api/students/?search=احمد&academic_status=ACTIVE&ordering=-entrance_year&page=1
"""
