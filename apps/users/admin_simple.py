# ==============================================================================
# ADMIN INTERFACE FOR UNIVERSITY MANAGEMENT SYSTEM - SIMPLE VERSION
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    Ministry, University, Faculty, Department, ResearchCenter,
    AdministrativeUnit, Position, AccessLevel, Employee, EmployeeDuty,
    User, StudentCategory, AcademicProgram, Student, StudentCategoryAssignment
)

# ==============================================================================
# MINISTRY ADMIN
# ==============================================================================

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']

# ==============================================================================
# UNIVERSITY ADMIN
# ==============================================================================

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'ministry', 'university_type', 'is_active']
    list_filter = ['ministry', 'university_type', 'is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']

# ==============================================================================
# FACULTY ADMIN
# ==============================================================================

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'university', 'is_active']
    list_filter = ['university', 'is_active']
    search_fields = ['name', 'code', 'university__name']
    readonly_fields = ['created_at', 'updated_at']

# ==============================================================================
# DEPARTMENT ADMIN
# ==============================================================================

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'faculty', 'is_active']
    list_filter = ['faculty', 'is_active']
    search_fields = ['name', 'code', 'faculty__name']
    readonly_fields = ['created_at', 'updated_at']

# ==============================================================================
# RESEARCH CENTER ADMIN
# ==============================================================================

@admin.register(ResearchCenter)
class ResearchCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'university', 'is_active']
    list_filter = ['university', 'is_active']
    search_fields = ['name', 'code', 'university__name']
    readonly_fields = ['created_at', 'updated_at']

# ==============================================================================
# ADMINISTRATIVE UNIT ADMIN
# ==============================================================================

@admin.register(AdministrativeUnit)
class AdministrativeUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'university', 'unit_type', 'is_active']
    list_filter = ['university', 'unit_type', 'is_active']
    search_fields = ['name', 'code', 'university__name']
    readonly_fields = ['created_at', 'updated_at']

# ==============================================================================
# POSITION ADMIN
# ==============================================================================

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'position_type', 'level', 'is_active']
    list_filter = ['position_type', 'level', 'is_active']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at']

# ==============================================================================
# ACCESS LEVEL ADMIN
# ==============================================================================

@admin.register(AccessLevel)
class AccessLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'is_active']
    list_filter = ['level', 'is_active']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']

# ==============================================================================
# EMPLOYEE ADMIN
# ==============================================================================

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name', 'university', 'employment_status', 'is_active']
    list_filter = ['university', 'employment_status', 'education_level', 'is_active']
    search_fields = ['employee_id', 'first_name', 'last_name', 'national_id']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = _('نام کامل')

# ==============================================================================
# EMPLOYEE DUTY ADMIN
# ==============================================================================

@admin.register(EmployeeDuty)
class EmployeeDutyAdmin(admin.ModelAdmin):
    list_display = ['employee', 'position', 'unit_type', 'start_date', 'is_active']
    list_filter = ['position', 'unit_type', 'is_active']
    search_fields = ['employee__first_name', 'employee__last_name', 'position__title']
    readonly_fields = ['created_at', 'updated_at']

# ==============================================================================
# USER ADMIN
# ==============================================================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'get_full_name', 'user_type', 'is_active', 'is_staff']
    list_filter = ['user_type', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('اطلاعات شخصی'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('اطلاعات سیستم'), {'fields': ('user_type', 'employee', 'student')}),
        (_('دسترسی‌ها'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('تاریخ‌های مهم'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = _('نام کامل')

# ==============================================================================
# STUDENT CATEGORY ADMIN
# ==============================================================================

@admin.register(StudentCategory)
class StudentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'is_active']
    list_filter = ['category_type', 'is_active']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']

# ==============================================================================
# ACADEMIC PROGRAM ADMIN
# ==============================================================================

@admin.register(AcademicProgram)
class AcademicProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'degree_level', 'is_active']
    list_filter = ['department', 'degree_level', 'is_active']
    search_fields = ['name', 'code', 'department__name']
    readonly_fields = ['created_at', 'updated_at']

# ==============================================================================
# STUDENT ADMIN
# ==============================================================================

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'get_full_name', 'university', 'current_program', 'student_status']
    list_filter = ['university', 'current_program', 'student_status', 'entry_year']
    search_fields = ['student_id', 'first_name', 'last_name', 'national_id']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = _('نام کامل')

# ==============================================================================
# STUDENT CATEGORY ASSIGNMENT ADMIN
# ==============================================================================

@admin.register(StudentCategoryAssignment)
class StudentCategoryAssignmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'category', 'assigned_date', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['student__first_name', 'student__last_name', 'category__name']
    readonly_fields = ['assigned_date']
