from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
import uuid
import re


class Ministry(models.Model):
    """
    وزارت علوم، تحقیقات و فناوری
    """
    MINISTRY_TYPE_CHOICES = [
        ('MOE', 'وزارت علوم، تحقیقات و فناوری'),
        ('MOH', 'وزارت بهداشت، درمان و آموزش پزشکی'),
        ('MOI', 'وزارت علوم و تحقیقات اسلامی'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='نام وزارت')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    type = models.CharField(max_length=10, choices=MINISTRY_TYPE_CHOICES, verbose_name='نوع وزارت')
    minister = models.CharField(max_length=100, verbose_name='وزیر')
    deputy_ministers = models.JSONField(default=list, verbose_name='معاونان وزیر')
    address = models.TextField(verbose_name='آدرس')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    website = models.URLField(verbose_name='وب‌سایت')
    established_date = models.DateField(verbose_name='تاریخ تاسیس')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'وزارت'
        verbose_name_plural = 'وزارت‌ها'

    def __str__(self):
        return self.name


class University(models.Model):
    """
    دانشگاه‌ها و مؤسسات آموزش عالی
    """
    UNIVERSITY_TYPE_CHOICES = [
        ('STATE', 'دولتی'),
        ('AZAD', 'آزاد اسلامی'),
        ('PAYAM_NOOR', 'پیام نور'),
        ('NON_PROFIT', 'غیرانتفاعی'),
        ('MEDICAL', 'علوم پزشکی'),
        ('TECHNICAL', 'فنی و حرفه‌ای'),
        ('RESEARCH', 'پژوهشگاه'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, verbose_name='وزارت متبوع')
    name = models.CharField(max_length=255, verbose_name='نام دانشگاه')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, unique=True, verbose_name='کد دانشگاه')
    type = models.CharField(max_length=15, choices=UNIVERSITY_TYPE_CHOICES, verbose_name='نوع دانشگاه')

    # اطلاعات پایه
    address = models.TextField(verbose_name='آدرس')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    website = models.URLField(blank=True, verbose_name='وب‌سایت')
    email = models.EmailField(verbose_name='ایمیل')

    # تاریخچه
    established_year = models.IntegerField(verbose_name='سال تاسیس')
    accreditation_status = models.CharField(max_length=50, verbose_name='وضعیت اعتبارنامه')

    # مدیریت
    president = models.CharField(max_length=100, verbose_name='رئیس دانشگاه')
    board_of_trustees = models.JSONField(default=list, verbose_name='هیأت امنا')

    # آمار و اطلاعات
    student_count = models.IntegerField(default=0, verbose_name='تعداد دانشجویان')
    faculty_count = models.IntegerField(default=0, verbose_name='تعداد اعضای هیأت علمی')
    staff_count = models.IntegerField(default=0, verbose_name='تعداد کارکنان')

    # موقعیت جغرافیایی
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)

    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    ranking = models.IntegerField(null=True, blank=True, verbose_name='رتبه دانشگاه')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'دانشگاه'
        verbose_name_plural = 'دانشگاه‌ها'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Faculty(models.Model):
    """
    دانشکده‌ها
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculties', verbose_name='دانشگاه')
    name = models.CharField(max_length=255, verbose_name='نام دانشکده')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, verbose_name='کد دانشکده')

    # مدیریت
    dean = models.CharField(max_length=100, verbose_name='دکان')
    vice_dean_education = models.CharField(max_length=100, blank=True, verbose_name='معاون آموزشی')
    vice_dean_research = models.CharField(max_length=100, blank=True, verbose_name='معاون پژوهشی')
    vice_dean_student = models.CharField(max_length=100, blank=True, verbose_name='معاون دانشجویی')

    # اطلاعات
    address = models.TextField(blank=True, verbose_name='آدرس')
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    email = models.EmailField(blank=True, verbose_name='ایمیل')

    # آمار
    department_count = models.IntegerField(default=0, verbose_name='تعداد گروه‌ها')
    student_count = models.IntegerField(default=0, verbose_name='تعداد دانشجویان')
    faculty_member_count = models.IntegerField(default=0, verbose_name='تعداد اعضای هیأت علمی')

    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    established_year = models.IntegerField(null=True, blank=True, verbose_name='سال تاسیس')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'دانشکده'
        verbose_name_plural = 'دانشکده‌ها'
        unique_together = ['university', 'code']

    def __str__(self):
        return f"{self.name} - {self.university.name}"


class Department(models.Model):
    """
    گروه‌های آموزشی
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments', verbose_name='دانشکده')
    name = models.CharField(max_length=255, verbose_name='نام گروه')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, verbose_name='کد گروه')

    # مدیریت
    head = models.CharField(max_length=100, verbose_name='رئیس گروه')
    deputy_head = models.CharField(max_length=100, blank=True, verbose_name='معاون گروه')

    # اطلاعات تخصصی
    field_of_study = models.CharField(max_length=100, verbose_name='رشته تحصیلی')
    degree_levels = models.JSONField(default=list, verbose_name='سطوح تحصیلی ارائه شده')
    research_areas = models.JSONField(default=list, verbose_name='زمینه‌های پژوهشی')

    # آمار
    student_count = models.IntegerField(default=0, verbose_name='تعداد دانشجویان')
    faculty_member_count = models.IntegerField(default=0, verbose_name='تعداد اعضای هیأت علمی')
    course_count = models.IntegerField(default=0, verbose_name='تعداد دروس')

    # اطلاعات تماس
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    email = models.EmailField(blank=True, verbose_name='ایمیل')

    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    established_year = models.IntegerField(null=True, blank=True, verbose_name='سال تاسیس')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'گروه آموزشی'
        verbose_name_plural = 'گروه‌های آموزشی'
        unique_together = ['faculty', 'code']

    def __str__(self):
        return f"{self.name} - {self.faculty.name}"


class ResearchCenter(models.Model):
    """
    مراکز تحقیقاتی
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='research_centers', verbose_name='دانشگاه')
    name = models.CharField(max_length=255, verbose_name='نام مرکز')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, verbose_name='کد مرکز')

    # مدیریت
    director = models.CharField(max_length=100, verbose_name='رئیس مرکز')
    deputy_director = models.CharField(max_length=100, blank=True, verbose_name='معاون مرکز')

    # اطلاعات تخصصی
    research_field = models.CharField(max_length=100, verbose_name='زمینه پژوهشی')
    sub_fields = models.JSONField(default=list, verbose_name='زیرزمینه‌ها')
    objectives = models.TextField(verbose_name='اهداف')

    # آمار
    researcher_count = models.IntegerField(default=0, verbose_name='تعداد پژوهشگران')
    project_count = models.IntegerField(default=0, verbose_name='تعداد پروژه‌ها')
    publication_count = models.IntegerField(default=0, verbose_name='تعداد انتشارات')

    # اطلاعات تماس
    address = models.TextField(blank=True, verbose_name='آدرس')
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    website = models.URLField(blank=True, verbose_name='وب‌سایت')

    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    established_year = models.IntegerField(null=True, blank=True, verbose_name='سال تاسیس')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'مرکز تحقیقاتی'
        verbose_name_plural = 'مرکزهای تحقیقاتی'
        unique_together = ['university', 'code']

    def __str__(self):
        return f"{self.name} - {self.university.name}"


class AdministrativeUnit(models.Model):
    """
    واحدهای اداری و پشتیبانی
    """
    UNIT_TYPE_CHOICES = [
        ('VICE_PRESIDENCY', 'معاونت'),
        ('DIRECTORATE_GENERAL', 'اداره کل'),
        ('DIRECTORATE', 'اداره'),
        ('OFFICE', 'دفتر'),
        ('SECTION', 'بخش'),
        ('UNIT', 'واحد'),
        ('CENTER', 'مرکز'),
        ('DEPARTMENT', 'بخش'),
    ]

    UNIT_CATEGORY_CHOICES = [
        ('EDUCATION', 'آموزشی'),
        ('RESEARCH', 'پژوهشی'),
        ('STUDENT', 'دانشجویی'),
        ('ADMIN_FINANCIAL', 'اداری مالی'),
        ('CULTURAL', 'فرهنگی'),
        ('TECHNOLOGY', 'فناوری اطلاعات'),
        ('SUPPORT', 'پشتیبانی'),
        ('MEDICAL', 'درمانی'),
        ('SERVICES', 'خدمات'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='administrative_units', verbose_name='دانشگاه')
    name = models.CharField(max_length=255, verbose_name='نام واحد')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, verbose_name='کد واحد')
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES, verbose_name='نوع واحد')
    category = models.CharField(max_length=20, choices=UNIT_CATEGORY_CHOICES, verbose_name='دسته‌بندی')

    # مدیریت
    manager = models.CharField(max_length=100, verbose_name='مدیر واحد')
    deputy_manager = models.CharField(max_length=100, blank=True, verbose_name='معاون مدیر')

    # اطلاعات
    responsibilities = models.TextField(verbose_name='وظایف و مسئولیت‌ها')
    sub_units = models.JSONField(default=list, verbose_name='زیرواحدها')

    # آمار
    staff_count = models.IntegerField(default=0, verbose_name='تعداد کارکنان')
    budget = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True, verbose_name='بودجه')

    # اطلاعات تماس
    address = models.TextField(blank=True, verbose_name='آدرس')
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    email = models.EmailField(blank=True, verbose_name='ایمیل')

    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    established_year = models.IntegerField(null=True, blank=True, verbose_name='سال تاسیس')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'واحد اداری'
        verbose_name_plural = 'واحدهای اداری'
        unique_together = ['university', 'code']

    def __str__(self):
        return f"{self.name} - {self.university.name}"


class Position(models.Model):
    """
    سمت‌ها و مناصب سازمانی
    """
    POSITION_LEVEL_CHOICES = [
        ('EXECUTIVE', 'مدیریت اجرایی'),
        ('SENIOR', 'ارشد'),
        ('MIDDLE', 'میانی'),
        ('JUNIOR', 'مبتدی'),
        ('SPECIALIST', 'کارشناس'),
        ('EXPERT', 'متخصص'),
        ('ADMINISTRATIVE', 'اداری'),
        ('SERVICE', 'خدماتی'),
        ('ACADEMIC', 'هیأت علمی'),
        ('RESEARCH', 'پژوهشی'),
    ]

    AUTHORITY_LEVEL_CHOICES = [
        (1, 'بدون اختیار خاص'),
        (2, 'اختیار محدود'),
        (3, 'اختیار متوسط'),
        (4, 'اختیار بالا'),
        (5, 'اختیار کامل'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('PERMANENT', 'رسمی'),
        ('CONTRACT', 'قراردادی'),
        ('PROJECT', 'پروژه‌ای'),
        ('HOURLY', 'ساعتی'),
        ('VISITING', 'مهمان'),
        ('RETIRED', 'بازنشسته'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, verbose_name='عنوان سمت')
    title_en = models.CharField(max_length=100, blank=True, verbose_name='عنوان انگلیسی')
    code = models.CharField(max_length=20, unique=True, verbose_name='کد سمت')

    # دسته‌بندی
    position_level = models.CharField(max_length=20, choices=POSITION_LEVEL_CHOICES, verbose_name='سطح سمت')
    authority_level = models.IntegerField(choices=AUTHORITY_LEVEL_CHOICES, default=1, verbose_name='سطح اختیار')
    employment_type = models.CharField(max_length=15, choices=EMPLOYMENT_TYPE_CHOICES, default='PERMANENT', verbose_name='نوع استخدام')

    # اطلاعات تخصصی
    job_description = models.TextField(verbose_name='شرح وظایف')
    required_qualifications = models.TextField(verbose_name='شرایط احراز')
    responsibilities = models.JSONField(default=list, verbose_name='مسئولیت‌ها')
    required_skills = models.JSONField(default=list, verbose_name='مهارت‌های مورد نیاز')

    # حقوق و مزایا
    base_salary = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='حقوق پایه')
    salary_grade = models.IntegerField(null=True, blank=True, verbose_name='پایه حقوقی')
    benefits = models.JSONField(default=dict, verbose_name='مزایا')

    # سازمانی
    organizational_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE, related_name='positions', verbose_name='واحد سازمانی')
    reports_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates', verbose_name='گزارش به')

    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'سمت سازمانی'
        verbose_name_plural = 'سمت‌های سازمانی'
        ordering = ['position_level', 'title']

    def __str__(self):
        return f"{self.title} ({self.code})"


class Employee(models.Model):
    """
    کارکنان دانشگاه
    """
    EMPLOYEE_TYPE_CHOICES = [
        ('ACADEMIC', 'هیأت علمی'),
        ('ADMINISTRATIVE', 'اداری'),
        ('TECHNICAL', 'فنی'),
        ('SERVICE', 'خدماتی'),
        ('RESEARCH', 'پژوهشی'),
        ('MEDICAL', 'درمانی'),
        ('SECURITY', 'امنیتی'),
        ('FINANCIAL', 'مالی'),
    ]

    ACADEMIC_RANK_CHOICES = [
        ('INSTRUCTOR', 'مربی'),
        ('ASSISTANT_PROFESSOR', 'استادیار'),
        ('ASSOCIATE_PROFESSOR', 'دانشیار'),
        ('PROFESSOR', 'استاد'),
        ('EMERITUS_PROFESSOR', 'استاد بازنشسته'),
        ('LECTURER', 'مدرس'),
        ('RESEARCHER', 'پژوهشگر'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='employees', verbose_name='دانشگاه')

    # اطلاعات شخصی
    national_id = models.CharField(max_length=10, unique=True, validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید 10 رقم باشد')], verbose_name='کد ملی')
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    first_name_en = models.CharField(max_length=50, blank=True, verbose_name='نام انگلیسی')
    last_name_en = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی انگلیسی')

    # اطلاعات تحصیلی
    academic_rank = models.CharField(max_length=25, choices=ACADEMIC_RANK_CHOICES, blank=True, verbose_name='رتبه علمی')
    education_level = models.CharField(max_length=50, blank=True, verbose_name='مقطع تحصیلی')
    field_of_study = models.CharField(max_length=100, blank=True, verbose_name='رشته تحصیلی')
    university_of_study = models.CharField(max_length=100, blank=True, verbose_name='دانشگاه محل تحصیل')

    # اطلاعات استخدامی
    employee_id = models.CharField(max_length=20, unique=True, verbose_name='شماره پرسنلی')
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPE_CHOICES, verbose_name='نوع کارمند')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='employees', verbose_name='سمت')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees', verbose_name='گروه آموزشی')
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees', verbose_name='واحد اداری')
    research_center = models.ForeignKey(ResearchCenter, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees', verbose_name='مرکز پژوهشی')

    # اطلاعات تماس
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    mobile = models.CharField(max_length=20, blank=True, verbose_name='موبایل')
    email = models.EmailField(verbose_name='ایمیل')
    address = models.TextField(blank=True, verbose_name='آدرس')

    # اطلاعات استخدامی
    hire_date = models.DateField(verbose_name='تاریخ استخدام')
    contract_end_date = models.DateField(null=True, blank=True, verbose_name='پایان قرارداد')
    base_salary = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='حقوق پایه')
    allowances = models.JSONField(default=dict, verbose_name='اضافات')

    # اطلاعات شخصی تکمیلی
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    gender = models.CharField(max_length=10, choices=[('MALE', 'مرد'), ('FEMALE', 'زن')], verbose_name='جنسیت')
    marital_status = models.CharField(max_length=15, choices=[('SINGLE', 'مجرد'), ('MARRIED', 'متأهل'), ('DIVORCED', 'طلاق گرفته'), ('WIDOWED', 'بیوه')], blank=True, verbose_name='وضعیت تأهل')
    emergency_contact = models.JSONField(default=dict, verbose_name='تماس اضطراری')

    # عملکرد و ارزیابی
    performance_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='امتیاز عملکرد')
    last_evaluation_date = models.DateField(null=True, blank=True, verbose_name='تاریخ آخرین ارزیابی')

    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    status = models.CharField(max_length=20, choices=[
        ('ACTIVE', 'فعال'),
        ('ON_LEAVE', 'مرخصی'),
        ('SUSPENDED', 'معلق'),
        ('TERMINATED', 'فوت شده'),
        ('RETIRED', 'بازنشسته'),
    ], default='ACTIVE', verbose_name='وضعیت')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارکنان'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.employee_id}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name_en(self):
        if self.first_name_en and self.last_name_en:
            return f"{self.first_name_en} {self.last_name_en}"
        return self.get_full_name()


class Student(models.Model):
    """
    دانشجویان دانشگاه
    """
    STUDENT_TYPE_CHOICES = [
        ('REGULAR', 'روزانه'),
        ('NIGHT', 'شبانه'),
        ('VIRTUAL', 'مجازی'),
        ('PAYAM_NOOR', 'پیام نور'),
        ('NON_PROFIT', 'غیرانتفاعی'),
        ('AZAD', 'آزاد اسلامی'),
        ('INTERNATIONAL', 'بین‌المللی'),
    ]

    ACADEMIC_LEVEL_CHOICES = [
        ('ASSOCIATE', 'کاردانی'),
        ('BACHELOR', 'کارشناسی'),
        ('MASTER', 'کارشناسی ارشد'),
        ('PHD', 'دکتری تخصصی'),
        ('PHD_PROFESSIONAL', 'دکتری حرفه‌ای'),
        ('POSTDOC', 'فوق دکتری'),
    ]

    ACADEMIC_STATUS_CHOICES = [
        ('ACTIVE', 'فعال'),
        ('ON_LEAVE', 'مرخصی تحصیلی'),
        ('PROBATION', 'مشروط'),
        ('GUEST', 'مهمان'),
        ('TRANSFERRED', 'انتقالی'),
        ('GRADUATED', 'فارغ‌التحصیل'),
        ('WITHDRAWN', 'انصرافی'),
        ('SUSPENDED', 'معلق'),
    ]

    FINANCIAL_STATUS_CHOICES = [
        ('REGULAR', 'عادی'),
        ('SCHOLARSHIP', 'بورسیه'),
        ('LOAN_RECIPIENT', 'دریافت‌کننده وام'),
        ('DISCOUNT', 'تخفیف شهریه'),
        ('EXEMPTION', 'معافیت شهریه'),
        ('SELF_PAYING', 'پرداخت شخصی'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='students', verbose_name='دانشگاه')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students', verbose_name='گروه آموزشی')

    # اطلاعات شخصی
    national_id = models.CharField(max_length=10, unique=True, validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید 10 رقم باشد')], verbose_name='کد ملی')
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    first_name_en = models.CharField(max_length=50, blank=True, verbose_name='نام انگلیسی')
    last_name_en = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی انگلیسی')

    # اطلاعات تحصیلی
    student_id = models.CharField(max_length=20, unique=True, verbose_name='شماره دانشجویی')
    student_type = models.CharField(max_length=15, choices=STUDENT_TYPE_CHOICES, verbose_name='نوع پذیرش')
    academic_level = models.CharField(max_length=20, choices=ACADEMIC_LEVEL_CHOICES, verbose_name='مقطع تحصیلی')
    academic_status = models.CharField(max_length=15, choices=ACADEMIC_STATUS_CHOICES, default='ACTIVE', verbose_name='وضعیت تحصیلی')
    financial_status = models.CharField(max_length=20, choices=FINANCIAL_STATUS_CHOICES, default='REGULAR', verbose_name='وضعیت مالی')

    # اطلاعات تحصیلی
    field_of_study = models.CharField(max_length=100, verbose_name='رشته تحصیلی')
    entrance_year = models.IntegerField(verbose_name='سال ورود')
    expected_graduation_year = models.IntegerField(null=True, blank=True, verbose_name='سال پیش‌بینی شده فارغ‌التحصیلی')
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name='معدل')

    # اطلاعات تماس
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    mobile = models.CharField(max_length=20, blank=True, verbose_name='موبایل')
    email = models.EmailField(verbose_name='ایمیل')
    address = models.TextField(blank=True, verbose_name='آدرس')

    # اطلاعات شخصی
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    gender = models.CharField(max_length=10, choices=[('MALE', 'مرد'), ('FEMALE', 'زن')], verbose_name='جنسیت')
    marital_status = models.CharField(max_length=15, choices=[('SINGLE', 'مجرد'), ('MARRIED', 'متأهل'), ('DIVORCED', 'طلاق گرفته'), ('WIDOWED', 'بیوه')], blank=True, verbose_name='وضعیت تأهل')
    emergency_contact = models.JSONField(default=dict, verbose_name='تماس اضطراری')

    # ویژگی‌های خاص
    special_categories = models.JSONField(default=list, verbose_name='دسته‌بندی‌های خاص')
    disabilities = models.JSONField(default=list, verbose_name='معلولیت‌ها')
    achievements = models.JSONField(default=list, verbose_name='دستاوردها')
    scholarships = models.JSONField(default=list, verbose_name='بورسیه‌ها')

    # اطلاعات خانوادگی
    father_name = models.CharField(max_length=50, blank=True, verbose_name='نام پدر')
    father_occupation = models.CharField(max_length=100, blank=True, verbose_name='شغل پدر')
    mother_name = models.CharField(max_length=50, blank=True, verbose_name='نام مادر')
    mother_occupation = models.CharField(max_length=100, blank=True, verbose_name='شغل مادر')

    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_international = models.BooleanField(default=False, verbose_name='دانشجوی بین‌المللی')
    is_veteran_child = models.BooleanField(default=False, verbose_name='فرزند شاهد/ایثارگر')
    is_athlete = models.BooleanField(default=False, verbose_name='ورزشکار')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'دانشجو'
        verbose_name_plural = 'دانشجویان'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.student_id}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name_en(self):
        if self.first_name_en and self.last_name_en:
            return f"{self.first_name_en} {self.last_name_en}"
        return self.get_full_name()

    def get_age(self):
        if self.birth_date:
            today = timezone.now().date()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None


class AccessControl(models.Model):
    """
    کنترل دسترسی پیشرفته
    """
    PERMISSION_TYPE_CHOICES = [
        ('READ', 'مشاهده'),
        ('WRITE', 'ویرایش'),
        ('DELETE', 'حذف'),
        ('APPROVE', 'تأیید'),
        ('MANAGE', 'مدیریت'),
        ('REPORT', 'گزارش‌گیری'),
        ('AUDIT', 'بازرسی'),
        ('FINANCIAL', 'مالی'),
        ('ACADEMIC', 'آکادمیک'),
        ('ADMINISTRATIVE', 'اداری'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='نام مجوز')
    codename = models.CharField(max_length=50, unique=True, verbose_name='کد مجوز')
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPE_CHOICES, verbose_name='نوع مجوز')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    module = models.CharField(max_length=50, blank=True, verbose_name='ماژول')

    # محدودیت‌ها
    resource_type = models.CharField(max_length=50, verbose_name='نوع منبع')
    scope = models.JSONField(default=dict, verbose_name='محدوده دسترسی')
    conditions = models.JSONField(default=dict, verbose_name='شرایط دسترسی')

    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'مجوز دسترسی'
        verbose_name_plural = 'مجوزهای دسترسی'

    def __str__(self):
        return f"{self.name} ({self.codename})"


class UserAccess(models.Model):
    """
    تخصیص دسترسی به کاربران
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='access_permissions', verbose_name='کاربر')
    permission = models.ForeignKey(AccessControl, on_delete=models.CASCADE, related_name='user_permissions', verbose_name='مجوز')

    # محدوده دسترسی
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True, verbose_name='دانشگاه')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True, verbose_name='دانشکده')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, verbose_name='گروه')
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE, null=True, blank=True, verbose_name='واحد اداری')

    # زمان‌بندی
    granted_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان اعطا')
    granted_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='granted_permissions', verbose_name='اعطا شده توسط')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='انقضا')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    # اطلاعات اضافی
    reason = models.TextField(blank=True, verbose_name='دلیل اعطا')
    restrictions = models.JSONField(default=dict, verbose_name='محدودیت‌ها')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'دسترسی کاربر'
        verbose_name_plural = 'دسترسی‌های کاربران'
        unique_together = ['user', 'permission', 'university', 'faculty', 'department', 'administrative_unit']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.permission.name}"

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class AuditLog(models.Model):
    """
    لاگ کامل فعالیت‌های کاربران
    """
    ACTION_CHOICES = [
        ('LOGIN', 'ورود'),
        ('LOGOUT', 'خروج'),
        ('CREATE', 'ایجاد'),
        ('READ', 'مشاهده'),
        ('UPDATE', 'ویرایش'),
        ('DELETE', 'حذف'),
        ('APPROVE', 'تأیید'),
        ('REJECT', 'رد'),
        ('EXPORT', 'خروجی'),
        ('IMPORT', 'ورودی'),
        ('SEARCH', 'جستجو'),
        ('REPORT', 'گزارش'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='audit_logs', verbose_name='کاربر')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='عملیات')
    resource_type = models.CharField(max_length=50, verbose_name='نوع منبع')
    resource_id = models.UUIDField(null=True, blank=True, verbose_name='شناسه منبع')

    # اطلاعات درخواست
    ip_address = models.GenericIPAddressField(verbose_name='آدرس IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    session_id = models.CharField(max_length=100, blank=True, verbose_name='شناسه جلسه')

    # نتیجه عملیات
    success = models.BooleanField(default=True, verbose_name='موفق')
    error_message = models.TextField(blank=True, verbose_name='پیام خطا')
    response_status = models.IntegerField(null=True, blank=True, verbose_name='کد وضعیت پاسخ')

    # اطلاعات اضافی
    details = models.JSONField(default=dict, verbose_name='جزئیات')
    old_values = models.JSONField(default=dict, verbose_name='مقادیر قدیمی')
    new_values = models.JSONField(default=dict, verbose_name='مقادیر جدید')

    # زمان
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='زمان')

    class Meta:
        verbose_name = 'لاگ فعالیت'
        verbose_name_plural = 'لاگ‌های فعالیت'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['resource_type', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.action} - {self.timestamp}"


# مدل‌های قدیمی برای سازگاری
class OrganizationalUnit(models.Model):
    """
    واحدهای سازمانی (سازگاری با مدل‌های قدیمی)
    """
    UNIT_TYPE_CHOICES = [
        ('ministry', 'وزارت'),
        ('university', 'دانشگاه'),
        ('faculty', 'دانشکده'),
        ('department', 'دانشکده'),
        ('office', 'اداره'),
        ('center', 'مرکز'),
        ('unit', 'واحد'),
    ]

    name = models.CharField(max_length=100, verbose_name='نام واحد')
    name_en = models.CharField(max_length=100, blank=True, verbose_name='نام انگلیسی')
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES, verbose_name='نوع واحد')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='واحد والد')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_units', verbose_name='مدیر')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'واحد سازمانی'
        verbose_name_plural = 'واحدهای سازمانی'

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    مدل کاربر پیشرفته با قابلیت‌های فراوان
    """
    ROLE_CHOICES = [
        ('super_admin', 'مدیر کل سیستم'),
        ('president', 'رئیس دانشگاه'),
        ('vice_president', 'معاون دانشگاه'),
        ('dean', 'دکان دانشکده'),
        ('department_head', 'رئیس گروه'),
        ('faculty', 'هیأت علمی'),
        ('researcher', 'پژوهشگر'),
        ('student', 'دانشجو'),
        ('staff', 'کارمند'),
        ('admin', 'مدیر'),
        ('guest', 'مهمان'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('permanent', 'رسمی'),
        ('contract', 'قراردادی'),
        ('project', 'پروژه‌ای'),
        ('hourly', 'ساعتی'),
        ('visiting', 'مهمان'),
        ('retired', 'بازنشسته'),
    ]

    # اطلاعات پایه
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name='نقش')
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True,
                                 validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید 10 رقم باشد')],
                                 verbose_name='کد ملی')

    # اطلاعات شخصی
    persian_first_name = models.CharField(max_length=50, blank=True, verbose_name='نام فارسی')
    persian_last_name = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی فارسی')
    father_name = models.CharField(max_length=50, blank=True, verbose_name='نام پدر')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    gender = models.CharField(max_length=10, choices=[('MALE', 'مرد'), ('FEMALE', 'زن')], verbose_name='جنسیت')

    # اطلاعات تحصیلی/استخدامی
    academic_rank = models.CharField(max_length=50, blank=True, verbose_name='رتبه علمی')
    education_level = models.CharField(max_length=50, blank=True, verbose_name='مقطع تحصیلی')
    field_of_study = models.CharField(max_length=100, blank=True, verbose_name='رشته تحصیلی')
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='شماره پرسنلی')
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='شماره دانشجویی')
    employment_type = models.CharField(max_length=15, choices=EMPLOYMENT_TYPE_CHOICES, blank=True, verbose_name='نوع استخدام')
    hire_date = models.DateField(null=True, blank=True, verbose_name='تاریخ استخدام')

    # ارتباطات سازمانی
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='واحد سازمانی')

    # اطلاعات تکمیلی
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    address = models.TextField(blank=True, verbose_name='آدرس')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='تصویر پروفایل')
    bio = models.TextField(blank=True, verbose_name='بیوگرافی')
    social_links = models.JSONField(default=dict, blank=True, verbose_name='لینک‌های شبکه‌های اجتماعی')
    achievements = models.JSONField(default=list, blank=True, verbose_name='دستاوردها')
    certifications = models.JSONField(default=list, blank=True, verbose_name='گواهینامه‌ها')
    work_experience = models.JSONField(default=list, blank=True, verbose_name='سوابق کاری')
    skills = models.JSONField(default=list, blank=True, verbose_name='مهارت‌ها')
    languages = models.JSONField(default=list, blank=True, verbose_name='زبان‌ها')
    emergency_contact = models.JSONField(default=dict, blank=True, verbose_name='تماس اضطراری')
    preferences = models.JSONField(default=dict, blank=True, verbose_name='تنظیمات شخصی')
    notes = models.TextField(blank=True, verbose_name='یادداشت‌ها')

    # فیلدهای امنیتی
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='آخرین IP ورود')
    is_verified = models.BooleanField(default=False, verbose_name='تأیید شده')

    # فیلدهای محاسباتی
    @property
    def full_persian_name(self):
        if self.persian_first_name and self.persian_last_name:
            return f"{self.persian_first_name} {self.persian_last_name}"
        return self.get_full_name()

    @property
    def is_faculty(self):
        return self.role in ['faculty', 'department_head', 'dean', 'vice_president', 'president']

    @property
    def is_student_user(self):
        return self.role == 'student'

    @property
    def is_staff_user(self):
        return self.role in ['staff', 'admin']

    @property
    def is_management_user(self):
        return self.role in ['president', 'vice_president', 'dean', 'department_head']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def get_full_name_fa(self):
        return self.full_persian_name


# مدل‌های قدیمی برای سازگاری
class UserPosition(models.Model):
    """
    تخصیص سمت‌ها به کاربران (سازگاری با مدل‌های قدیمی)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='positions', verbose_name='کاربر')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='users', verbose_name='سمت')
    is_primary = models.BooleanField(default=False, verbose_name='سمت اصلی')
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تخصیص سمت'
        verbose_name_plural = 'تخصیص سمت‌ها'
        unique_together = ['user', 'position', 'start_date']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position.title}"


class Permission(models.Model):
    """
    مجوزها و دسترسی‌های سیستم (سازگاری با مدل‌های قدیمی)
    """
    PERMISSION_TYPE_CHOICES = [
        ('read', 'مشاهده'),
        ('write', 'ویرایش'),
        ('delete', 'حذف'),
        ('approve', 'تأیید'),
        ('manage', 'مدیریت'),
        ('report', 'گزارش‌گیری'),
        ('audit', 'بازرسی'),
        ('financial', 'مالی'),
        ('academic', 'آکادمیک'),
        ('administrative', 'اداری'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name='نام مجوز')
    codename = models.CharField(max_length=50, unique=True, verbose_name='کد مجوز')
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPE_CHOICES, verbose_name='نوع مجوز')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    module = models.CharField(max_length=50, blank=True, verbose_name='ماژول')

    class Meta:
        verbose_name = 'مجوز'
        verbose_name_plural = 'مجوزها'

    def __str__(self):
        return f"{self.name} ({self.codename})"


class UserPermission(models.Model):
    """
    تخصیص مجوزها به کاربران (سازگاری با مدل‌های قدیمی)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_permissions_custom', verbose_name='کاربر')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='مجوز')
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE, null=True, blank=True, verbose_name='واحد سازمانی')
    granted_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان اعطا')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='انقضا')
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='granted_permissions', verbose_name='اعطا شده توسط')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    reason = models.TextField(blank=True, verbose_name='دلیل اعطا')
    restrictions = models.JSONField(default=dict, blank=True, verbose_name='محدودیت‌ها')

    class Meta:
        verbose_name = 'مجوز کاربر'
        verbose_name_plural = 'مجوزهای کاربران'
        unique_together = ['user', 'permission', 'organizational_unit']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.permission.name}"


class AccessLog(models.Model):
    """
    لاگ دسترسی‌های کاربران (سازگاری با مدل‌های قدیمی)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    action = models.CharField(max_length=100, verbose_name='عملیات')
    resource = models.CharField(max_length=100, verbose_name='منبع')
    ip_address = models.GenericIPAddressField(verbose_name='آدرس IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='زمان')
    success = models.BooleanField(default=True, verbose_name='موفق')
    details = models.JSONField(default=dict, blank=True, verbose_name='جزئیات')
    session_id = models.CharField(max_length=100, blank=True, verbose_name='شناسه جلسه')

    class Meta:
        verbose_name = 'لاگ دسترسی'
        verbose_name_plural = 'لاگ‌های دسترسی'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.action} - {self.timestamp}"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.action} - {self.timestamp}"


# مدل‌های قدیمی برای سازگاری
class OrganizationalUnit(models.Model):
    """
    واحدهای سازمانی (سازگاری با مدل‌های قدیمی)
    """
    UNIT_TYPE_CHOICES = [
        ('ministry', 'وزارت'),
        ('university', 'دانشگاه'),
        ('faculty', 'دانشکده'),
        ('department', 'دانشکده'),
        ('office', 'اداره'),
        ('center', 'مرکز'),
        ('unit', 'واحد'),
    ]

    name = models.CharField(max_length=100, verbose_name='نام واحد')
    name_en = models.CharField(max_length=100, blank=True, verbose_name='نام انگلیسی')
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES, verbose_name='نوع واحد')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='واحد والد')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_units', verbose_name='مدیر')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'واحد سازمانی'
        verbose_name_plural = 'واحدهای سازمانی'

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    مدل کاربر پیشرفته با قابلیت‌های فراوان
    """
    ROLE_CHOICES = [
        ('super_admin', 'مدیر کل سیستم'),
        ('president', 'رئیس دانشگاه'),
        ('vice_president', 'معاون دانشگاه'),
        ('dean', 'دکان دانشکده'),
        ('department_head', 'رئیس گروه'),
        ('faculty', 'هیأت علمی'),
        ('researcher', 'پژوهشگر'),
        ('student', 'دانشجو'),
        ('staff', 'کارمند'),
        ('admin', 'مدیر'),
        ('guest', 'مهمان'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('permanent', 'رسمی'),
        ('contract', 'قراردادی'),
        ('project', 'پروژه‌ای'),
        ('hourly', 'ساعتی'),
        ('visiting', 'مهمان'),
        ('retired', 'بازنشسته'),
    ]

    # اطلاعات پایه
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name='نقش')
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True,
                                 validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید 10 رقم باشد')],
                                 verbose_name='کد ملی')

    # اطلاعات شخصی
    persian_first_name = models.CharField(max_length=50, blank=True, verbose_name='نام فارسی')
    persian_last_name = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی فارسی')
    father_name = models.CharField(max_length=50, blank=True, verbose_name='نام پدر')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    gender = models.CharField(max_length=10, choices=[('MALE', 'مرد'), ('FEMALE', 'زن')], verbose_name='جنسیت')

    # اطلاعات تحصیلی/استخدامی
    academic_rank = models.CharField(max_length=50, blank=True, verbose_name='رتبه علمی')
    education_level = models.CharField(max_length=50, blank=True, verbose_name='مقطع تحصیلی')
    field_of_study = models.CharField(max_length=100, blank=True, verbose_name='رشته تحصیلی')
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='شماره پرسنلی')
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='شماره دانشجویی')
    employment_type = models.CharField(max_length=15, choices=EMPLOYMENT_TYPE_CHOICES, blank=True, verbose_name='نوع استخدام')
    hire_date = models.DateField(null=True, blank=True, verbose_name='تاریخ استخدام')

    # ارتباطات سازمانی
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='واحد سازمانی')

    # اطلاعات تکمیلی
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    address = models.TextField(blank=True, verbose_name='آدرس')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='تصویر پروفایل')
    bio = models.TextField(blank=True, verbose_name='بیوگرافی')
    social_links = models.JSONField(default=dict, blank=True, verbose_name='لینک‌های شبکه‌های اجتماعی')
    achievements = models.JSONField(default=list, blank=True, verbose_name='دستاوردها')
    certifications = models.JSONField(default=list, blank=True, verbose_name='گواهینامه‌ها')
    work_experience = models.JSONField(default=list, blank=True, verbose_name='سوابق کاری')
    skills = models.JSONField(default=list, blank=True, verbose_name='مهارت‌ها')
    languages = models.JSONField(default=list, blank=True, verbose_name='زبان‌ها')
    emergency_contact = models.JSONField(default=dict, blank=True, verbose_name='تماس اضطراری')
    preferences = models.JSONField(default=dict, blank=True, verbose_name='تنظیمات شخصی')
    notes = models.TextField(blank=True, verbose_name='یادداشت‌ها')

    # فیلدهای امنیتی
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='آخرین IP ورود')
    is_verified = models.BooleanField(default=False, verbose_name='تأیید شده')

    # فیلدهای محاسباتی
    @property
    def full_persian_name(self):
        if self.persian_first_name and self.persian_last_name:
            return f"{self.persian_first_name} {self.persian_last_name}"
        return self.get_full_name()

    @property
    def is_faculty(self):
        return self.role in ['faculty', 'department_head', 'dean', 'vice_president', 'president']

    @property
    def is_student_user(self):
        return self.role == 'student'

    @property
    def is_staff_user(self):
        return self.role in ['staff', 'admin']

    @property
    def is_management_user(self):
        return self.role in ['president', 'vice_president', 'dean', 'department_head']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def get_full_name_fa(self):
        return self.full_persian_name


# مدل‌های قدیمی برای سازگاری
class UserPosition(models.Model):
    """
    تخصیص سمت‌ها به کاربران (سازگاری با مدل‌های قدیمی)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='positions', verbose_name='کاربر')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='users', verbose_name='سمت')
    is_primary = models.BooleanField(default=False, verbose_name='سمت اصلی')
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تخصیص سمت'
        verbose_name_plural = 'تخصیص سمت‌ها'
        unique_together = ['user', 'position', 'start_date']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position.title}"


class Permission(models.Model):
    """
    مجوزها و دسترسی‌های سیستم (سازگاری با مدل‌های قدیمی)
    """
    PERMISSION_TYPE_CHOICES = [
        ('read', 'مشاهده'),
        ('write', 'ویرایش'),
        ('delete', 'حذف'),
        ('approve', 'تأیید'),
        ('manage', 'مدیریت'),
        ('report', 'گزارش‌گیری'),
        ('audit', 'بازرسی'),
        ('financial', 'مالی'),
        ('academic', 'آکادمیک'),
        ('administrative', 'اداری'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name='نام مجوز')
    codename = models.CharField(max_length=50, unique=True, verbose_name='کد مجوز')
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPE_CHOICES, verbose_name='نوع مجوز')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    module = models.CharField(max_length=50, blank=True, verbose_name='ماژول')

    class Meta:
        verbose_name = 'مجوز'
        verbose_name_plural = 'مجوزها'

    def __str__(self):
        return f"{self.name} ({self.codename})"


class UserPermission(models.Model):
    """
    تخصیص مجوزها به کاربران (سازگاری با مدل‌های قدیمی)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_permissions_custom', verbose_name='کاربر')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='مجوز')
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE, null=True, blank=True, verbose_name='واحد سازمانی')
    granted_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان اعطا')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='انقضا')
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='granted_permissions', verbose_name='اعطا شده توسط')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    reason = models.TextField(blank=True, verbose_name='دلیل اعطا')
    restrictions = models.JSONField(default=dict, blank=True, verbose_name='محدودیت‌ها')

    class Meta:
        verbose_name = 'مجوز کاربر'
        verbose_name_plural = 'مجوزهای کاربران'
        unique_together = ['user', 'permission', 'organizational_unit']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.permission.name}"


class AccessLog(models.Model):
    """
    لاگ دسترسی‌های کاربران (سازگاری با مدل‌های قدیمی)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    action = models.CharField(max_length=100, verbose_name='عملیات')
    resource = models.CharField(max_length=100, verbose_name='منبع')
    ip_address = models.GenericIPAddressField(verbose_name='آدرس IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='زمان')
    success = models.BooleanField(default=True, verbose_name='موفق')
    details = models.JSONField(default=dict, blank=True, verbose_name='جزئیات')
    session_id = models.CharField(max_length=100, blank=True, verbose_name='شناسه جلسه')

    class Meta:
        verbose_name = 'لاگ دسترسی'
        verbose_name_plural = 'لاگ‌های دسترسی'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.action} - {self.timestamp}"


# مدل‌های قدیمی برای سازگاری
class OrganizationalUnit(models.Model):
    """
    واحدهای سازمانی (سازگاری با مدل‌های قدیمی)
    """
    UNIT_TYPE_CHOICES = [
        ('ministry', 'وزارت'),
        ('university', 'دانشگاه'),
        ('faculty', 'دانشکده'),
        ('department', 'دانشکده'),
        ('office', 'اداره'),
        ('center', 'مرکز'),
        ('unit', 'واحد'),
    ]

    name = models.CharField(max_length=100, verbose_name='نام واحد')
    name_en = models.CharField(max_length=100, blank=True, verbose_name='نام انگلیسی')
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES, verbose_name='نوع واحد')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='واحد والد')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_units', verbose_name='مدیر')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'واحد سازمانی'
        verbose_name_plural = 'واحدهای سازمانی'

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    مدل کاربر پیشرفته با قابلیت‌های فراوان
    """
    ROLE_CHOICES = [
        ('super_admin', 'مدیر کل سیستم'),
        ('president', 'رئیس دانشگاه'),
        ('vice_president', 'معاون دانشگاه'),
        ('dean', 'دکان دانشکده'),
        ('department_head', 'رئیس گروه'),
        ('faculty', 'هیأت علمی'),
        ('researcher', 'پژوهشگر'),
        ('student', 'دانشجو'),
        ('staff', 'کارمند'),
        ('admin', 'مدیر'),
        ('guest', 'مهمان'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('permanent', 'رسمی'),
        ('contract', 'قراردادی'),
        ('project', 'پروژه‌ای'),
        ('hourly', 'ساعتی'),
        ('visiting', 'مهمان'),
        ('retired', 'بازنشسته'),
    ]

    # اطلاعات پایه
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name='نقش')
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True,
                                 validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید 10 رقم باشد')],
                                 verbose_name='کد ملی')

    # اطلاعات شخصی
    persian_first_name = models.CharField(max_length=50, blank=True, verbose_name='نام فارسی')
    persian_last_name = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی فارسی')
    father_name = models.CharField(max_length=50, blank=True, verbose_name='نام پدر')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    gender = models.CharField(max_length=10, choices=[('MALE', 'مرد'), ('FEMALE', 'زن')], verbose_name='جنسیت')

    # اطلاعات تحصیلی/استخدامی
    academic_rank = models.CharField(max_length=50, blank=True, verbose_name='رتبه علمی')
    education_level = models.CharField(max_length=50, blank=True, verbose_name='مقطع تحصیلی')
    field_of_study = models.CharField(max_length=100, blank=True, verbose_name='رشته تحصیلی')
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='شماره پرسنلی')
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='شماره دانشجویی')
    employment_type = models.CharField(max_length=15, choices=EMPLOYMENT_TYPE_CHOICES, blank=True, verbose_name='نوع استخدام')
    hire_date = models.DateField(null=True, blank=True, verbose_name='تاریخ استخدام')

    # ارتباطات سازمانی
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='واحد سازمانی')

    # اطلاعات تکمیلی
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    address = models.TextField(blank=True, verbose_name='آدرس')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='تصویر پروفایل')
    bio = models.TextField(blank=True, verbose_name='بیوگرافی')
    social_links = models.JSONField(default=dict, blank=True, verbose_name='لینک‌های شبکه‌های اجتماعی')
    achievements = models.JSONField(default=list, blank=True, verbose_name='دستاوردها')
    certifications = models.JSONField(default=list, blank=True, verbose_name='گواهینامه‌ها')
    work_experience = models.JSONField(default=list, blank=True, verbose_name='سوابق کاری')
    skills = models.JSONField(default=list, blank=True, verbose_name='مهارت‌ها')
    languages = models.JSONField(default=list, blank=True, verbose_name='زبان‌ها')
    emergency_contact = models.JSONField(default=dict, blank=True, verbose_name='تماس اضطراری')
    preferences = models.JSONField(default=dict, blank=True, verbose_name='تنظیمات شخصی')
    notes = models.TextField(blank=True, verbose_name='یادداشت‌ها')

    # فیلدهای امنیتی
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='آخرین IP ورود')
    is_verified = models.BooleanField(default=False, verbose_name='تأیید شده')

    # فیلدهای محاسباتی
    @property
    def full_persian_name(self):
        if self.persian_first_name and self.persian_last_name:
            return f"{self.persian_first_name} {self.persian_last_name}"
        return self.get_full_name()

    @property
    def is_faculty(self):
        return self.role in ['faculty', 'department_head', 'dean', 'vice_president', 'president']

    @property
    def is_student_user(self):
        return self.role == 'student'

    @property
    def is_staff_user(self):
        return self.role in ['staff', 'admin']

    @property
    def is_management_user(self):
        return self.role in ['president', 'vice_president', 'dean', 'department_head']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def get_full_name_fa(self):
        return self.full_persian_name


# مدل‌های قدیمی برای سازگاری
class UserPosition(models.Model):
    """
    تخصیص سمت‌ها به کاربران (سازگاری با مدل‌های قدیمی)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='positions', verbose_name='کاربر')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='users', verbose_name='سمت')
    is_primary = models.BooleanField(default=False, verbose_name='سمت اصلی')
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تخصیص سمت'
        verbose_name_plural = 'تخصیص سمت‌ها'
        unique_together = ['user', 'position', 'start_date']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position.title}"


class Permission(models.Model):
    """
    مجوزها و دسترسی‌های سیستم (سازگاری با مدل‌های قدیمی)
    """
    PERMISSION_TYPE_CHOICES = [
        ('read', 'مشاهده'),
        ('write', 'ویرایش'),
        ('delete', 'حذف'),
        ('approve', 'تأیید'),
        ('manage', 'مدیریت'),
        ('report', 'گزارش‌گیری'),
        ('audit', 'بازرسی'),
        ('financial', 'مالی'),
        ('academic', 'آکادمیک'),
        ('administrative', 'اداری'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name='نام مجوز')
    codename = models.CharField(max_length=50, unique=True, verbose_name='کد مجوز')
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPE_CHOICES, verbose_name='نوع مجوز')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    module = models.CharField(max_length=50, blank=True, verbose_name='ماژول')

    class Meta:
        verbose_name = 'مجوز'
        verbose_name_plural = 'مجوزها'

    def __str__(self):
        return f"{self.name} ({self.codename})"


class UserPermission(models.Model):
    """
    تخصیص مجوزها به کاربران (سازگاری با مدل‌های قدیمی)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_permissions_custom', verbose_name='کاربر')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='مجوز')
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE, null=True, blank=True, verbose_name='واحد سازمانی')
    granted_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان اعطا')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='انقضا')
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='granted_permissions', verbose_name='اعطا شده توسط')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    reason = models.TextField(blank=True, verbose_name='دلیل اعطا')
    restrictions = models.JSONField(default=dict, blank=True, verbose_name='محدودیت‌ها')

    class Meta:
        verbose_name = 'مجوز کاربر'
        verbose_name_plural = 'مجوزهای کاربران'
        unique_together = ['user', 'permission', 'organizational_unit']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.permission.name}"


class AccessLog(models.Model):
    """
    لاگ دسترسی‌های کاربران (سازگاری با مدل‌های قدیمی)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    action = models.CharField(max_length=100, verbose_name='عملیات')
    resource = models.CharField(max_length=100, verbose_name='منبع')
    ip_address = models.GenericIPAddressField(verbose_name='آدرس IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='زمان')
    success = models.BooleanField(default=True, verbose_name='موفق')
    details = models.JSONField(default=dict, blank=True, verbose_name='جزئیات')
    session_id = models.CharField(max_length=100, blank=True, verbose_name='شناسه جلسه')

    class Meta:
        verbose_name = 'لاگ دسترسی'
        verbose_name_plural = 'لاگ‌های دسترسی'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.action} - {self.timestamp}"


# مدل‌های قدیمی برای سازگاری
class OrganizationalUnit(models.Model):
    """
    واحدهای سازمانی (سازگاری با مدل‌های قدیمی)
    """
    UNIT_TYPE_CHOICES = [
        ('ministry', 'وزارت'),
        ('university', 'دانشگاه'),
        ('faculty', 'دانشکده'),
        ('department', 'دانشکده'),
        ('office', 'اداره'),
        ('center', 'مرکز'),
        ('unit', 'واحد'),
    ]

    name = models.CharField(max_length=100, verbose_name='نام واحد')
    name_en = models.CharField(max_length=100, blank=True, verbose_name='نام انگلیسی')
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES, verbose_name='نوع واحد')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='واحد والد')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_units', verbose_name='مدیر')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'واحد سازمانی'
        verbose_name_plural = 'واحدهای سازمانی'

 
 
 #   E/DG'�  B/�E�  (1'�  3'2�'1�
 c l a s s   O r g a n i z a t i o n a l U n i t ( m o d e l s . M o d e l ) : 
         " " " 
         H'-/G'�  3'2E'F�  ( 3'2�'1�  ('  E/DG'�  B/�E�) 
         " " " 
         U N I T _ T Y P E _ C H O I C E S   =   [ 
                 ( " m i n i s t r y " ,   " H2'1*" ) , 
                 ( " u n i v e r s i t y " ,   " /'F4�'G" ) , 
                 ( " f a c u l t y " ,   " /'F4�/G" ) , 
                 ( " d e p a r t m e n t " ,   " /'F4�/G" ) , 
                 ( " o f f i c e " ,   " '/'1G" ) , 
                 ( " c e n t e r " ,   " E1�2" ) , 
                 ( " u n i t " ,   " H'-/" ) , 
         ] 
 
         n a m e   =   m o d e l s . C h a r F i e l d ( m a x _ l e n g t h = 1 0 0 ,   v e r b o s e _ n a m e = " F'E  H'-/" ) 
         n a m e _ e n   =   m o d e l s . C h a r F i e l d ( m a x _ l e n g t h = 1 0 0 ,   b l a n k = T r u e ,   v e r b o s e _ n a m e = " F'E  'F�D�3�" ) 
         u n i t _ t y p e   =   m o d e l s . C h a r F i e l d ( m a x _ l e n g t h = 2 0 ,   c h o i c e s = U N I T _ T Y P E _ C H O I C E S ,   v e r b o s e _ n a m e = " FH9  H'-/" ) 
         p a r e n t   =   m o d e l s . F o r e i g n K e y ( " s e l f " ,   o n _ d e l e t e = m o d e l s . C A S C A D E ,   n u l l = T r u e ,   b l a n k = T r u e ,   r e l a t e d _ n a m e = " c h i l d r e n " ,   v e r b o s e _ n a m e = " H'-/  H'D/" ) 
         m a n a g e r   =   m o d e l s . F o r e i g n K e y ( U s e r ,   o n _ d e l e t e = m o d e l s . S E T _ N U L L ,   n u l l = T r u e ,   b l a n k = T r u e ,   r e l a t e d _ n a m e = " m a n a g e d _ u n i t s " ,   v e r b o s e _ n a m e = " E/�1" ) 
         d e s c r i p t i o n   =   m o d e l s . T e x t F i e l d ( b l a n k = T r u e ,   v e r b o s e _ n a m e = " *H6�-'*" ) 
         i s _ a c t i v e   =   m o d e l s . B o o l e a n F i e l d ( d e f a u l t = T r u e ,   v e r b o s e _ n a m e = " A9'D" ) 
         c r e a t e d _ a t   =   m o d e l s . D a t e T i m e F i e l d ( a u t o _ n o w _ a d d = T r u e ) 
         u p d a t e d _ a t   =   m o d e l s . D a t e T i m e F i e l d ( a u t o _ n o w = T r u e ) 
 
         c l a s s   M e t a : 
                 v e r b o s e _ n a m e   =   " H'-/  3'2E'F�" 
                 v e r b o s e _ n a m e _ p l u r a l   =   " H'-/G'�  3'2E'F�" 
 
         d e f   _ _ s t r _ _ ( s e l f ) : 
                 r e t u r n   s e l f . n a m e 
 
 