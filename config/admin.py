# Django Admin Panel Customization
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import (
    User, OrganizationalUnit, Position, UserPosition, 
    Permission, UserPermission, AccessLog
)
from apps.courses.models import Course
from apps.grades.models import Grade
from apps.notifications.models import Notification
from apps.announcements.models import Announcement
from apps.assignments.models import Assignment, Submission


# ===== USERS APP =====
@admin.register(OrganizationalUnit)
class OrganizationalUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'unit_type', 'parent', 'is_active', 'order']
    list_filter = ['unit_type', 'is_active', 'parent']
    search_fields = ['name', 'code', 'description']
    list_editable = ['is_active', 'order']
    ordering = ['parent', 'order', 'name']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizational_unit', 'position_level', 'authority_level', 'is_active']
    list_filter = ['position_level', 'authority_level', 'is_active']
    search_fields = ['title', 'organizational_unit__name']
    list_editable = ['is_active']


class UserPositionInline(admin.TabularInline):
    model = UserPosition
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'get_full_persian_name', 'role', 'primary_unit', 'is_active']
    list_filter = ['role', 'employment_type', 'is_active', 'primary_unit']
    search_fields = ['username', 'persian_first_name', 'persian_last_name', 'national_id']
    inlines = [UserPositionInline]
    
    def get_full_persian_name(self, obj):
        return obj.get_full_persian_name() or obj.username
    get_full_persian_name.short_description = 'نام کامل'


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename', 'permission_type', 'module']
    list_filter = ['permission_type', 'module']
    search_fields = ['name', 'codename']


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'resource', 'timestamp', 'success']
    list_filter = ['success', 'action', 'timestamp']
    readonly_fields = ['user', 'action', 'resource', 'ip_address', 'timestamp', 'success']
    
    def has_add_permission(self, request):
        return False


# ===== OTHER APPS =====


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'professor', 'created_at']
    list_filter = ['professor', 'created_at']
    search_fields = ['title', 'code']
    filter_horizontal = ['students']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'score', 'grade_letter', 'date_assigned']
    list_filter = ['course', 'grade_letter', 'date_assigned']
    search_fields = ['student__username', 'course__title']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'target_audience', 'priority', 'is_published', 'created_at']
    list_filter = ['target_audience', 'priority', 'is_published', 'created_at']
    search_fields = ['title', 'content']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'professor', 'due_date', 'max_score']
    list_filter = ['course', 'professor', 'due_date']
    search_fields = ['title', 'course__title']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'score']
    list_filter = ['assignment', 'submitted_at', 'graded_at']
    search_fields = ['student__username', 'assignment__title']
