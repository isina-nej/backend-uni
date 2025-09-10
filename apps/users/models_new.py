# ==============================================================================
# MODERN UNIVERSITY MANAGEMENT MODELS
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# معماری: Django + ابزارهای مکمل
# ==============================================================================

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import uuid
import re


# ==============================================================================
# BASE ABSTRACT MODELS
# ==============================================================================

class BaseModel(models.Model):
    """مدل پایه برای تمام مدل‌ها"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ آپدیت')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    class Meta:
        abstract = True

class PersonModel(BaseModel):
    """مدل پایه برای اشخاص"""
    national_id = models.CharField(
        max_length=10, 
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید ۱۰ رقم باشد')],
        verbose_name='کد ملی'
    )
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    first_name_en = models.CharField(max_length=100, blank=True, verbose_name='نام انگلیسی')
    last_name_en = models.CharField(max_length=100, blank=True, verbose_name='نام خانوادگی انگلیسی')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'مرد'), ('F', 'زن')],
        verbose_name='جنسیت'
    )
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^09\d{9}$', 'شماره موبایل نامعتبر')],
        verbose_name='شماره موبایل'
    )
    address = models.TextField(blank=True, verbose_name='آدرس')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='عکس')
    
    class Meta:
        abstract = True

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name_en(self):
        return f"{self.first_name_en} {self.last_name_en}"


# ==============================================================================
# ORGANIZATIONAL HIERARCHY MODELS
# ==============================================================================

class Ministry(BaseModel):
    """وزارت علوم، تحقیقات و فناوری"""
    MINISTRY_TYPES = [
        ('SCIENCE', 'وزارت علوم، تحقیقات و فناوری'),
        ('HEALTH', 'وزارت بهداشت، درمان و آموزش پزشکی'),
        ('EDUCATION', 'وزارت آموزش و پرورش'),
    ]

    name = models.CharField(max_length=255, unique=True, verbose_name='نام وزارت')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    type = models.CharField(max_length=20, choices=MINISTRY_TYPES, verbose_name='نوع وزارت')
    minister_name = models.CharField(max_length=100, verbose_name='نام وزیر')
    deputy_ministers = models.JSONField(default=list, verbose_name='معاونان')
    address = models.TextField(verbose_name='آدرس')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    website = models.URLField(verbose_name='وب‌سایت')
    established_date = models.DateField(verbose_name='تاریخ تاسیس')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    class Meta:
        verbose_name = 'وزارت'
        verbose_name_plural = 'وزارت‌ها'
        ordering = ['name']

    def __str__(self):
        return self.name


class University(BaseModel):
    """دانشگاه‌ها و مؤسسات آموزش عالی"""
    UNIVERSITY_TYPES = [
        ('STATE', 'دولتی'),
        ('AZAD', 'آزاد اسلامی'),
        ('PAYAM_NOOR', 'پیام نور'),
        ('NON_PROFIT', 'غیرانتفاعی'),
        ('MEDICAL', 'علوم پزشکی'),
        ('TECHNICAL', 'فنی و حرفه‌ای'),
        ('RESEARCH', 'پژوهشگاه'),
        ('SPECIALIZED', 'تخصصی'),
    ]

    ministry = models.ForeignKey(
        Ministry, 
        on_delete=models.CASCADE, 
        related_name='universities',
        verbose_name='وزارت متبوع'
    )
    name = models.CharField(max_length=255, verbose_name='نام دانشگاه')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, unique=True, verbose_name='کد دانشگاه')
    type = models.CharField(max_length=15, choices=UNIVERSITY_TYPES, verbose_name='نوع دانشگاه')
    
    # اطلاعات پایه
    address = models.TextField(verbose_name='آدرس')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    website = models.URLField(blank=True, verbose_name='وب‌سایت')
    email = models.EmailField(verbose_name='ایمیل')
    logo = models.ImageField(upload_to='university_logos/', null=True, blank=True, verbose_name='لوگو')
    
    # تاریخچه و اعتبار
    established_year = models.IntegerField(verbose_name='سال تاسیس')
    accreditation_status = models.CharField(max_length=50, verbose_name='وضعیت اعتبارنامه')
    
    # مدیریت
    president_name = models.CharField(max_length=100, verbose_name='رئیس دانشگاه')
    board_of_trustees = models.JSONField(default=list, verbose_name='هیأت امنا')
    
    # آمار
    student_count = models.IntegerField(default=0, verbose_name='تعداد دانشجویان')
    faculty_count = models.IntegerField(default=0, verbose_name='تعداد اعضای هیأت علمی')
    staff_count = models.IntegerField(default=0, verbose_name='تعداد کارکنان')
    
    # موقعیت جغرافیایی
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=8, 
        null=True, 
        blank=True,
        verbose_name='عرض جغرافیایی'
    )
    longitude = models.DecimalField(
        max_digits=11, 
        decimal_places=8, 
        null=True, 
        blank=True,
        verbose_name='طول جغرافیایی'
    )
    
    # رتبه‌بندی و کیفیت
    national_ranking = models.IntegerField(null=True, blank=True, verbose_name='رتبه ملی')
    international_ranking = models.IntegerField(null=True, blank=True, verbose_name='رتبه بین‌المللی')
    qs_ranking = models.IntegerField(null=True, blank=True, verbose_name='رتبه QS')
    
    # اطلاعات تکمیلی
    description = models.TextField(blank=True, verbose_name='توضیحات')
    social_media = models.JSONField(default=dict, verbose_name='شبکه‌های اجتماعی')
    
    class Meta:
        verbose_name = 'دانشگاه'
        verbose_name_plural = 'دانشگاه‌ها'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_absolute_url(self):
        return reverse('university-detail', kwargs={'pk': self.pk})


class Faculty(BaseModel):
    """دانشکده‌ها"""
    university = models.ForeignKey(
        University, 
        on_delete=models.CASCADE, 
        related_name='faculties',
        verbose_name='دانشگاه'
    )
    name = models.CharField(max_length=255, verbose_name='نام دانشکده')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, verbose_name='کد دانشکده')
    
    # اطلاعات تماس
    address = models.TextField(blank=True, verbose_name='آدرس')
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    
    # تاریخچه
    established_year = models.IntegerField(null=True, blank=True, verbose_name='سال تاسیس')
    
    # آمار
    department_count = models.IntegerField(default=0, verbose_name='تعداد گروه‌ها')
    student_count = models.IntegerField(default=0, verbose_name='تعداد دانشجویان')
    faculty_member_count = models.IntegerField(default=0, verbose_name='تعداد اعضای هیأت علمی')
    
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    class Meta:
        verbose_name = 'دانشکده'
        verbose_name_plural = 'دانشکده‌ها'
        unique_together = ['university', 'code']
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.university.name}"


class Department(BaseModel):
    """گروه‌های آموزشی"""
    faculty = models.ForeignKey(
        Faculty, 
        on_delete=models.CASCADE, 
        related_name='departments',
        verbose_name='دانشکده'
    )
    name = models.CharField(max_length=255, verbose_name='نام گروه')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, verbose_name='کد گروه')
    
    # اطلاعات تخصصی
    field_of_study = models.CharField(max_length=100, verbose_name='رشته تحصیلی')
    degree_levels = models.JSONField(default=list, verbose_name='سطوح تحصیلی')
    research_areas = models.JSONField(default=list, verbose_name='زمینه‌های پژوهشی')
    
    # اطلاعات تماس
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    
    # تاریخچه
    established_year = models.IntegerField(null=True, blank=True, verbose_name='سال تاسیس')
    
    # آمار
    student_count = models.IntegerField(default=0, verbose_name='تعداد دانشجویان')
    faculty_member_count = models.IntegerField(default=0, verbose_name='تعداد اعضای هیأت علمی')
    course_count = models.IntegerField(default=0, verbose_name='تعداد دروس')
    
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    class Meta:
        verbose_name = 'گروه آموزشی'
        verbose_name_plural = 'گروه‌های آموزشی'
        unique_together = ['faculty', 'code']
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.faculty.name}"


class ResearchCenter(BaseModel):
    """مراکز تحقیقاتی و پژوهشکده‌ها"""
    university = models.ForeignKey(
        University, 
        on_delete=models.CASCADE, 
        related_name='research_centers',
        verbose_name='دانشگاه'
    )
    name = models.CharField(max_length=255, verbose_name='نام مرکز')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, verbose_name='کد مرکز')
    
    # اطلاعات تخصصی
    research_fields = models.JSONField(default=list, verbose_name='زمینه‌های تحقیقاتی')
    research_type = models.CharField(
        max_length=50,
        choices=[
            ('BASIC', 'تحقیقات پایه'),
            ('APPLIED', 'تحقیقات کاربردی'),
            ('DEVELOPMENT', 'تحقیق و توسعه'),
            ('INNOVATION', 'نوآوری و فناوری'),
        ],
        verbose_name='نوع تحقیقات'
    )
    
    # تاریخچه
    established_year = models.IntegerField(null=True, blank=True, verbose_name='سال تاسیس')
    
    # آمار
    researcher_count = models.IntegerField(default=0, verbose_name='تعداد پژوهشگران')
    project_count = models.IntegerField(default=0, verbose_name='تعداد پروژه‌های فعال')
    publication_count = models.IntegerField(default=0, verbose_name='تعداد مقالات منتشره')
    
    # اطلاعات تماس
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    class Meta:
        verbose_name = 'مرکز تحقیقاتی'
        verbose_name_plural = 'مراکز تحقیقاتی'
        unique_together = ['university', 'code']
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.university.name}"


class AdministrativeUnit(BaseModel):
    """واحدهای اداری دانشگاه"""
    UNIT_TYPES = [
        ('EDUCATION', 'آموزشی'),
        ('RESEARCH', 'پژوهشی'), 
        ('STUDENT', 'دانشجویی'),
        ('ADMIN_FINANCE', 'اداری مالی'),
        ('CULTURAL', 'فرهنگی'),
        ('IT', 'فناوری اطلاعات'),
        ('SUPPORT', 'پشتیبانی'),
        ('MEDICAL', 'درمانی'),
        ('HEALTH', 'بهداشتی'),
        ('PLANNING', 'برنامه‌ریزی'),
        ('INTERNATIONAL', 'بین‌الملل'),
    ]

    university = models.ForeignKey(
        University, 
        on_delete=models.CASCADE, 
        related_name='administrative_units',
        verbose_name='دانشگاه'
    )
    parent_unit = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='child_units',
        verbose_name='واحد والد'
    )
    
    name = models.CharField(max_length=255, verbose_name='نام واحد')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, verbose_name='کد واحد')
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES, verbose_name='نوع واحد')
    
    # مسئولیت‌ها
    responsibilities = models.TextField(verbose_name='مسئولیت‌ها')
    services = models.JSONField(default=list, verbose_name='خدمات ارائه شده')
    
    # آمار
    employee_count = models.IntegerField(default=0, verbose_name='تعداد کارکنان')
    
    # اطلاعات تماس
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    address = models.TextField(blank=True, verbose_name='آدرس')
    
    # ساعات کاری
    working_hours = models.JSONField(default=dict, verbose_name='ساعات کاری')
    
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    class Meta:
        verbose_name = 'واحد اداری'
        verbose_name_plural = 'واحدهای اداری'
        unique_together = ['university', 'code']
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.university.name}"

    def get_hierarchy_path(self):
        """مسیر سلسله مراتبی واحد"""
        if self.parent_unit:
            return f"{self.parent_unit.get_hierarchy_path()} > {self.name}"
        return self.name


# ==============================================================================
# POSITION AND ACCESS CONTROL MODELS
# ==============================================================================

class Position(BaseModel):
    """پست‌های سازمانی"""
    POSITION_LEVELS = [
        ('EXECUTIVE', 'مدیریتی'),
        ('FACULTY', 'هیأت علمی'),
        ('ADMIN', 'اداری'),
        ('SUPPORT', 'پشتیبانی'),
        ('EDUCATION', 'آموزشی'),
        ('RESEARCH', 'پژوهشی'),
        ('MEDICAL', 'درمانی'),
        ('TECHNICAL', 'فنی'),
        ('SERVICE', 'خدماتی'),
    ]

    title = models.CharField(max_length=255, unique=True, verbose_name='عنوان پست')
    title_en = models.CharField(max_length=255, blank=True, verbose_name='عنوان انگلیسی')
    level = models.CharField(max_length=20, choices=POSITION_LEVELS, verbose_name='سطح')
    
    # شرح وظایف
    responsibilities = models.TextField(verbose_name='شرح وظایف')
    requirements = models.TextField(verbose_name='شرایط احراز')
    skills_required = models.JSONField(default=list, verbose_name='مهارت‌های مورد نیاز')
    
    # سطح دسترسی پیش‌فرض
    default_access_level = models.IntegerField(default=1, verbose_name='سطح دسترسی پیش‌فرض')
    
    # اطلاعات حقوقی
    salary_grade = models.CharField(max_length=10, blank=True, verbose_name='گروه حقوقی')
    benefits = models.JSONField(default=list, verbose_name='مزایا')
    
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    class Meta:
        verbose_name = 'پست سازمانی'
        verbose_name_plural = 'پست‌های سازمانی'
        ordering = ['title']

    def __str__(self):
        return self.title


class AccessLevel(BaseModel):
    """سطوح دسترسی"""
    name = models.CharField(max_length=100, unique=True, verbose_name='نام سطح دسترسی')
    description = models.TextField(verbose_name='توضیحات')
    level_number = models.IntegerField(unique=True, verbose_name='شماره سطح')
    
    # مجوزها
    permissions = models.JSONField(default=dict, verbose_name='مجوزها')
    
    # محدودیت‌ها
    restrictions = models.JSONField(default=dict, verbose_name='محدودیت‌ها')
    
    class Meta:
        verbose_name = 'سطح دسترسی'
        verbose_name_plural = 'سطوح دسترسی'
        ordering = ['level_number']

    def __str__(self):
        return f"{self.name} (سطح {self.level_number})"


# ==============================================================================
# EMPLOYEE MODELS
# ==============================================================================

class Employee(PersonModel):
    """کارکنان دانشگاه"""
    EMPLOYMENT_TYPES = [
        ('FULL_TIME', 'تمام وقت'),
        ('PART_TIME', 'پاره وقت'),
        ('CONTRACT', 'قراردادی'),
        ('PROJECT', 'پروژه‌ای'),
        ('VISITING', 'مهمان'),
    ]

    EMPLOYMENT_STATUS = [
        ('ACTIVE', 'فعال'),
        ('INACTIVE', 'غیرفعال'),
        ('LEAVE', 'مرخصی'),
        ('SUSPENDED', 'تعلیق'),
        ('RETIRED', 'بازنشسته'),
        ('TERMINATED', 'اخراج'),
    ]

    ACADEMIC_RANKS = [
        ('INSTRUCTOR', 'مربی'),
        ('ASSISTANT_PROF', 'استادیار'),
        ('ASSOCIATE_PROF', 'دانشیار'),
        ('FULL_PROF', 'استاد'),
        ('EMERITUS', 'استاد بازنشسته'),
        ('VISITING_PROF', 'استاد مهمان'),
        ('LECTURER', 'مدرس'),
    ]

    ADMINISTRATIVE_ROLES = [
        ('PRESIDENT', 'رئیس'),
        ('VICE_PRESIDENT', 'معاون'),
        ('DEAN', 'دکان'),
        ('VICE_DEAN', 'معاون دانشکده'),
        ('DEPARTMENT_HEAD', 'رئیس گروه'),
        ('DIRECTOR', 'مدیر'),
        ('MANAGER', 'رئیس'),
        ('SUPERVISOR', 'سرپرست'),
        ('EXPERT', 'کارشناس'),
        ('SPECIALIST', 'متخصص'),
        ('OFFICER', 'کارمند'),
        ('TECHNICIAN', 'تکنسین'),
        ('SECRETARY', 'منشی'),
        ('ASSISTANT', 'دستیار'),
    ]

    # اطلاعات استخدامی
    employee_id = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name='شماره پرسنلی'
    )
    hire_date = models.DateField(verbose_name='تاریخ استخدام')
    employment_type = models.CharField(
        max_length=20, 
        choices=EMPLOYMENT_TYPES,
        verbose_name='نوع استخدام'
    )
    employment_status = models.CharField(
        max_length=20, 
        choices=EMPLOYMENT_STATUS,
        default='ACTIVE',
        verbose_name='وضعیت استخدام'
    )
    
    # پست و سازمان
    position = models.ForeignKey(
        Position, 
        on_delete=models.CASCADE,
        verbose_name='پست سازمانی'
    )
    primary_unit = models.ForeignKey(
        AdministrativeUnit,
        on_delete=models.CASCADE,
        related_name='primary_employees',
        verbose_name='واحد اصلی'
    )
    secondary_units = models.ManyToManyField(
        AdministrativeUnit,
        blank=True,
        related_name='secondary_employees',
        verbose_name='واحدهای فرعی'
    )
    
    # رتبه‌ها و نقش‌ها
    academic_rank = models.CharField(
        max_length=20, 
        choices=ACADEMIC_RANKS,
        blank=True,
        verbose_name='رتبه دانشگاهی'
    )
    administrative_role = models.CharField(
        max_length=20, 
        choices=ADMINISTRATIVE_ROLES,
        blank=True,
        verbose_name='نقش اداری'
    )
    
    # دسترسی
    access_level = models.ForeignKey(
        AccessLevel,
        on_delete=models.CASCADE,
        verbose_name='سطح دسترسی'
    )
    
    # اطلاعات مالی
    salary_grade = models.CharField(max_length=10, blank=True, verbose_name='پایه حقوقی')
    bank_account = models.CharField(max_length=20, blank=True, verbose_name='شماره حساب')
    
    # اطلاعات تکمیلی
    education_level = models.CharField(max_length=50, blank=True, verbose_name='سطح تحصیلات')
    field_of_study = models.CharField(max_length=100, blank=True, verbose_name='رشته تحصیلی')
    
    # آمار عملکرد
    performance_score = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='امتیاز عملکرد'
    )
    
    # تاریخ‌های مهم
    contract_end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان قرارداد')
    retirement_date = models.DateField(null=True, blank=True, verbose_name='تاریخ بازنشستگی')
    
    # یادداشت‌ها
    notes = models.TextField(blank=True, verbose_name='یادداشت‌ها')
    
    class Meta:
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارکنان'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.employee_id})"

    def get_absolute_url(self):
        return reverse('employee-detail', kwargs={'pk': self.pk})

    @property
    def is_faculty_member(self):
        """آیا عضو هیأت علمی است؟"""
        return bool(self.academic_rank)

    @property
    def years_of_service(self):
        """سابقه خدمت"""
        if self.hire_date:
            return (timezone.now().date() - self.hire_date).days // 365
        return 0


class EmployeeDuty(BaseModel):
    """وظایف و مأموریت‌های کارکنان"""
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE,
        related_name='duties',
        verbose_name='کارمند'
    )
    title = models.CharField(max_length=255, verbose_name='عنوان وظیفه')
    description = models.TextField(verbose_name='شرح وظیفه')
    
    # زمان‌بندی
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان')
    
    # وضعیت
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'در انتظار'),
            ('IN_PROGRESS', 'در حال انجام'),
            ('COMPLETED', 'تکمیل شده'),
            ('CANCELLED', 'لغو شده'),
        ],
        default='PENDING',
        verbose_name='وضعیت'
    )
    
    # اولویت
    priority = models.CharField(
        max_length=10,
        choices=[
            ('LOW', 'کم'),
            ('MEDIUM', 'متوسط'),
            ('HIGH', 'بالا'),
            ('URGENT', 'فوری'),
        ],
        default='MEDIUM',
        verbose_name='اولویت'
    )
    
    # تخمین زمان
    estimated_hours = models.IntegerField(
        null=True, 
        blank=True,
        verbose_name='تخمین زمان (ساعت)'
    )
    actual_hours = models.IntegerField(
        null=True, 
        blank=True,
        verbose_name='زمان واقعی (ساعت)'
    )
    
    # نتایج
    completion_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='درصد تکمیل'
    )
    results = models.TextField(blank=True, verbose_name='نتایج')
    
    class Meta:
        verbose_name = 'وظیفه کارمند'
        verbose_name_plural = 'وظایف کارکنان'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} - {self.employee.get_full_name()}"


# ==============================================================================
# USER AUTHENTICATION MODEL
# ==============================================================================

class User(AbstractUser):
    """مدل کاربر سیستم"""
    USER_TYPES = [
        ('EMPLOYEE', 'کارمند'),
        ('STUDENT', 'دانشجو'),
        ('ADMIN', 'مدیر سیستم'),
        ('GUEST', 'مهمان'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, verbose_name='نوع کاربر')
    national_id = models.CharField(
        max_length=10, 
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید ۱۰ رقم باشد')],
        verbose_name='کد ملی'
    )
    
    # ارتباط با Employee یا Student
    employee = models.OneToOneField(
        Employee, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name='کارمند'
    )
    
    # اطلاعات اضافی
    phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^09\d{9}$', 'شماره موبایل نامعتبر')],
        verbose_name='شماره موبایل'
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='آواتار')
    
    # تنظیمات
    preferred_language = models.CharField(
        max_length=5,
        choices=[('fa', 'فارسی'), ('en', 'English')],
        default='fa',
        verbose_name='زبان ترجیحی'
    )
    timezone = models.CharField(max_length=50, default='Asia/Tehran', verbose_name='منطقه زمانی')
    
    # امنیت
    two_factor_enabled = models.BooleanField(default=False, verbose_name='تأیید دو مرحله‌ای')
    last_password_change = models.DateTimeField(auto_now_add=True, verbose_name='آخرین تغییر رمز')
    failed_login_attempts = models.IntegerField(default=0, verbose_name='تلاش‌های ناموفق ورود')
    account_locked_until = models.DateTimeField(null=True, blank=True, verbose_name='قفل تا تاریخ')
    
    # فعالیت
    last_activity = models.DateTimeField(auto_now=True, verbose_name='آخرین فعالیت')
    
    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['email', 'user_type']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.employee:
            return f"{self.employee.get_full_name()} ({self.national_id})"
        return f"{self.username} ({self.national_id})"

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'pk': self.pk})

    @property
    def is_account_locked(self):
        """آیا حساب قفل است؟"""
        if self.account_locked_until:
            return timezone.now() < self.account_locked_until
        return False

    def lock_account(self, duration_minutes=30):
        """قفل کردن حساب"""
        self.account_locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save()

    def unlock_account(self):
        """باز کردن قفل حساب"""
        self.account_locked_until = None
        self.failed_login_attempts = 0
        self.save()
