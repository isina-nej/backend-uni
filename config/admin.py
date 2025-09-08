# Django Admin Panel Customization
from django.contrib import admin
from apps.users.models import User
from apps.courses.models import Course
from apps.grades.models import Grade
from apps.notifications.models import Notification
from apps.announcements.models import Announcement
from apps.assignments.models import Assignment, Submission


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'department', 'is_active']
    list_filter = ['role', 'department', 'is_active']
    search_fields = ['username', 'email', 'student_id']


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
