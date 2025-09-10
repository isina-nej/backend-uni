# ==============================================================================
# ADMIN CONFIGURATION FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from .models import (
    Ministry, University, Faculty, Department, ResearchCenter, 
    AdministrativeUnit, Position, AccessLevel, Employee, EmployeeDuty, User,
    StudentCategory, AcademicProgram, Student, StudentCategoryAssignment
)


# ==============================================================================
# ADMIN CONFIGURATIONS
# ==============================================================================

@admin.register(Ministry)
class MinistryAdmin(ImportExportModelAdmin):
    list_display = ['name', 'type', 'minister_name', 'universities_count', 'is_active']
    list_filter = ['type', 'is_active', 'established_date']
    search_fields = ['name', 'name_en', 'minister_name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('name', 'name_en', 'type', 'minister_name')
        }),
        ('جزئیات', {
            'fields': ('deputy_ministers', 'address', 'phone', 'website', 'established_date', 'description')
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
        ('متا داده', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def universities_count(self, obj):
        return obj.universities.filter(is_active=True).count()
    universities_count.short_description = 'تعداد دانشگاه‌ها'


@admin.register(University)
class UniversityAdmin(ImportExportModelAdmin):
    list_display = ['name', 'code', 'type', 'ministry', 'president_name', 'student_count', 'faculty_count', 'is_active']
    list_filter = ['type', 'ministry', 'is_active', 'established_year']
    search_fields = ['name', 'name_en', 'code', 'president_name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'view_logo']
    filter_horizontal = []
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('ministry', 'name', 'name_en', 'code', 'type')
        }),
        ('اطلاعات تماس', {
            'fields': ('address', 'phone', 'website', 'email', 'logo', 'view_logo')
        }),
        ('مدیریت', {
            'fields': ('president_name', 'board_of_trustees')
        }),
        ('تاریخچه و اعتبار', {
            'fields': ('established_year', 'accreditation_status')
        }),
        ('آمار', {
            'fields': ('student_count', 'faculty_count', 'staff_count')
        }),
        ('موقعیت جغرافیایی', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('رتبه‌بندی', {
            'fields': ('national_ranking', 'international_ranking', 'qs_ranking'),
            'classes': ('collapse',)
        }),
        ('اطلاعات تکمیلی', {
            'fields': ('description', 'social_media'),
            'classes': ('collapse',)
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
        ('متا داده', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def view_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100" height="100" />', obj.logo.url)
        return "بدون لوگو"
    view_logo.short_description = 'نمایش لوگو'


@admin.register(Faculty)
class FacultyAdmin(ImportExportModelAdmin):
    list_display = ['name', 'code', 'university', 'department_count', 'student_count', 'faculty_member_count', 'is_active']
    list_filter = ['university', 'is_active', 'established_year']
    search_fields = ['name', 'name_en', 'code']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('university', 'name', 'name_en', 'code')
        }),
        ('اطلاعات تماس', {
            'fields': ('address', 'phone', 'email')
        }),
        ('تاریخچه', {
            'fields': ('established_year',)
        }),
        ('آمار', {
            'fields': ('department_count', 'student_count', 'faculty_member_count')
        }),
        ('اطلاعات تکمیلی', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
        ('متا داده', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ['name', 'code', 'faculty', 'field_of_study', 'student_count', 'faculty_member_count', 'is_active']
    list_filter = ['faculty__university', 'faculty', 'is_active', 'established_year']
    search_fields = ['name', 'name_en', 'code', 'field_of_study']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(ResearchCenter)
class ResearchCenterAdmin(ImportExportModelAdmin):
    list_display = ['name', 'code', 'university', 'research_type', 'researcher_count', 'project_count', 'is_active']
    list_filter = ['university', 'research_type', 'is_active', 'established_year']
    search_fields = ['name', 'name_en', 'code']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(AdministrativeUnit)
class AdministrativeUnitAdmin(ImportExportModelAdmin):
    list_display = ['name', 'code', 'university', 'unit_type', 'parent_unit', 'employee_count', 'is_active']
    list_filter = ['university', 'unit_type', 'parent_unit', 'is_active']
    search_fields = ['name', 'name_en', 'code']
    readonly_fields = ['id', 'created_at', 'updated_at', 'hierarchy_path']
    
    def hierarchy_path(self, obj):
        return obj.get_hierarchy_path()
    hierarchy_path.short_description = 'مسیر سلسله مراتبی'


@admin.register(Position)
class PositionAdmin(ImportExportModelAdmin):
    list_display = ['title', 'level', 'default_access_level', 'salary_grade', 'employees_count', 'is_active']
    list_filter = ['level', 'is_active']
    search_fields = ['title', 'title_en']
    readonly_fields = ['id', 'created_at', 'updated_at']

    def employees_count(self, obj):
        return obj.employee_set.filter(is_active=True).count()
    employees_count.short_description = 'تعداد کارکنان'


@admin.register(AccessLevel)
class AccessLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'level_number', 'description', 'is_active']
    list_filter = ['level_number', 'is_active']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['level_number']


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ['get_full_name', 'employee_id', 'position', 'primary_unit', 'academic_rank', 'employment_status', 'hire_date', 'is_active']
    list_filter = ['employment_type', 'employment_status', 'academic_rank', 'administrative_role', 'primary_unit__university', 'is_active']
    search_fields = ['first_name', 'last_name', 'national_id', 'employee_id', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at', 'years_of_service', 'view_photo']
    filter_horizontal = ['secondary_units']
    
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('national_id', 'first_name', 'last_name', 'first_name_en', 'last_name_en', 
                      'birth_date', 'gender', 'photo', 'view_photo')
        }),
        ('اطلاعات تماس', {
            'fields': ('email', 'phone', 'address')
        }),
        ('اطلاعات استخدامی', {
            'fields': ('employee_id', 'hire_date', 'employment_type', 'employment_status', 
                      'contract_end_date', 'retirement_date')
        }),
        ('پست و سازمان', {
            'fields': ('position', 'primary_unit', 'secondary_units')
        }),
        ('رتبه‌ها و نقش‌ها', {
            'fields': ('academic_rank', 'administrative_role')
        }),
        ('دسترسی', {
            'fields': ('access_level',)
        }),
        ('اطلاعات مالی', {
            'fields': ('salary_grade', 'bank_account'),
            'classes': ('collapse',)
        }),
        ('اطلاعات تحصیلی', {
            'fields': ('education_level', 'field_of_study'),
            'classes': ('collapse',)
        }),
        ('عملکرد', {
            'fields': ('performance_score', 'years_of_service'),
            'classes': ('collapse',)
        }),
        ('یادداشت‌ها', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
        ('متا داده', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def view_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" height="100" />', obj.photo.url)
        return "بدون عکس"
    view_photo.short_description = 'نمایش عکس'


@admin.register(EmployeeDuty)
class EmployeeDutyAdmin(admin.ModelAdmin):
    list_display = ['title', 'employee', 'status', 'priority', 'start_date', 'completion_percentage', 'is_active']
    list_filter = ['status', 'priority', 'employee__primary_unit', 'is_active']
    search_fields = ['title', 'description', 'employee__first_name', 'employee__last_name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['national_id', 'username', 'get_full_name', 'user_type', 'email', 'is_active', 'last_login']
    list_filter = ['user_type', 'is_active', 'is_staff', 'two_factor_enabled']
    search_fields = ['national_id', 'username', 'first_name', 'last_name', 'email']
    readonly_fields = ['id', 'last_login', 'date_joined', 'last_activity', 'is_account_locked']
    
    fieldsets = (
        ('اطلاعات ورود', {
            'fields': ('national_id', 'username', 'password')
        }),
        ('اطلاعات شخصی', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('نوع کاربر', {
            'fields': ('user_type', 'employee', 'student')
        }),
        ('اطلاعات تماس', {
            'fields': ('phone', 'avatar')
        }),
        ('تنظیمات', {
            'fields': ('preferred_language', 'timezone')
        }),
        ('امنیت', {
            'fields': ('two_factor_enabled', 'last_password_change', 'failed_login_attempts', 
                      'account_locked_until', 'is_account_locked')
        }),
        ('مجوزها', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('فعالیت', {
            'fields': ('last_login', 'date_joined', 'last_activity'),
            'classes': ('collapse',)
        })
    )
    
    add_fieldsets = (
        ('اطلاعات اصلی', {
            'classes': ('wide',),
            'fields': ('national_id', 'username', 'email', 'user_type', 'password1', 'password2'),
        }),
    )

    def get_full_name(self, obj):
        return obj.get_full_name() if hasattr(obj, 'get_full_name') else f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'نام کامل'


# ==============================================================================
# STUDENT ADMIN CONFIGURATIONS
# ==============================================================================

@admin.register(StudentCategory)
class StudentCategoryAdmin(ImportExportModelAdmin):
    list_display = ['name', 'category_type', 'max_members', 'students_count', 'is_active']
    list_filter = ['category_type', 'is_active']
    search_fields = ['name', 'name_en']
    readonly_fields = ['id', 'created_at', 'updated_at']

    def students_count(self, obj):
        return obj.student_assignments.filter(status='ACTIVE').count()
    students_count.short_description = 'تعداد دانشجویان'


@admin.register(AcademicProgram)
class AcademicProgramAdmin(ImportExportModelAdmin):
    list_display = ['name', 'code', 'department', 'program_type', 'program_mode', 'max_capacity', 'current_enrollment', 'remaining_capacity', 'is_active']
    list_filter = ['program_type', 'program_mode', 'department__faculty__university', 'is_accepting_students', 'is_active']
    search_fields = ['name', 'name_en', 'code']
    readonly_fields = ['id', 'created_at', 'updated_at', 'remaining_capacity', 'is_full']

    def remaining_capacity(self, obj):
        return obj.remaining_capacity
    remaining_capacity.short_description = 'ظرفیت باقی‌مانده'


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ['get_full_name', 'student_id', 'academic_program', 'student_type', 'academic_status', 'current_semester', 'cumulative_gpa', 'is_active']
    list_filter = ['student_type', 'academic_status', 'financial_status', 'entrance_year', 'academic_program__department__faculty__university', 'is_active']
    search_fields = ['first_name', 'last_name', 'national_id', 'student_id', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at', 'university', 'faculty', 'department', 'academic_year', 'academic_standing', 'view_photo']
    
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('national_id', 'first_name', 'last_name', 'first_name_en', 'last_name_en',
                      'birth_date', 'gender', 'photo', 'view_photo')
        }),
        ('اطلاعات تماس', {
            'fields': ('email', 'phone', 'address', 'permanent_address')
        }),
        ('اطلاعات تحصیلی', {
            'fields': ('student_id', 'university_student_id', 'academic_program', 
                      'university', 'faculty', 'department')
        }),
        ('نوع و وضعیت', {
            'fields': ('student_type', 'academic_status', 'financial_status', 'marital_status')
        }),
        ('ورود و ترم', {
            'fields': ('entrance_year', 'entrance_semester', 'current_semester', 'academic_year')
        }),
        ('عملکرد تحصیلی', {
            'fields': ('current_gpa', 'cumulative_gpa', 'academic_standing', 
                      'total_credits_earned', 'total_credits_attempted')
        }),
        ('اطلاعات مالی', {
            'fields': ('total_tuition_paid', 'outstanding_balance', 'scholarship_amount'),
            'classes': ('collapse',)
        }),
        ('خانواده', {
            'fields': ('father_name', 'guardian_phone'),
            'classes': ('collapse',)
        }),
        ('اضطراری', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone'),
            'classes': ('collapse',)
        }),
        ('تاریخ‌های مهم', {
            'fields': ('expected_graduation_date',),
            'classes': ('collapse',)
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
        ('متا داده', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def view_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" height="100" />', obj.photo.url)
        return "بدون عکس"
    view_photo.short_description = 'نمایش عکس'


@admin.register(StudentCategoryAssignment)
class StudentCategoryAssignmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'category', 'status', 'start_date', 'end_date', 'is_active']
    list_filter = ['category', 'status', 'is_active', 'start_date']
    search_fields = ['student__first_name', 'student__last_name', 'student__student_id', 'category__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'


# ==============================================================================
# ADMIN SITE CUSTOMIZATION
# ==============================================================================

admin.site.site_header = 'سیستم مدیریت دانشگاه'
admin.site.site_title = 'مدیریت دانشگاه'
admin.site.index_title = 'پنل مدیریت سیستم یکپارچه دانشگاه'

# Add custom CSS and JavaScript
admin.site.enable_nav_sidebar = True
