# ==============================================================================
# MINIMAL ADMIN INTERFACE FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Ministry, University, Faculty, Department, ResearchCenter,
    AdministrativeUnit, Position, AccessLevel, Employee, EmployeeDuty,
    User, StudentCategory, AcademicProgram, Student, StudentCategoryAssignment
)

# Simple admin registrations
admin.site.register(Ministry)
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(ResearchCenter)
admin.site.register(AdministrativeUnit)
admin.site.register(Position)
admin.site.register(AccessLevel)
admin.site.register(Employee)
admin.site.register(EmployeeDuty)
admin.site.register(StudentCategory)
admin.site.register(AcademicProgram)
admin.site.register(Student)
admin.site.register(StudentCategoryAssignment)

# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
