# ==============================================================================
# STUDENT MODELS
# مدل‌های دانشجویان بر اساس ساختار کامل دانشگاه‌های ایران
# ==============================================================================

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.urls import reverse
from .models_new import BaseModel, PersonModel, University, Faculty, Department, User
import uuid


# ==============================================================================
# STUDENT CATEGORY AND CLASSIFICATION MODELS
# ==============================================================================

class StudentCategory(BaseModel):
    """دسته‌های ویژه دانشجویان"""
    CATEGORY_TYPES = [
        ('TALENT', 'استعداد درخشان'),
        ('MARTYR_FAMILY', 'خانواده شهدا'),
        ('VETERAN_FAMILY', 'خانواده ایثارگران'),
        ('DISABLED', 'معلول'),
        ('ATHLETE', 'ورزشکار'),
        ('INTERNATIONAL', 'بین‌المللی'),
        ('MARRIED', 'متأهل'),
        ('WORKING', 'شاغل'),
        ('MINORITY', 'اقلیت'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name='نام دسته')
    name_en = models.CharField(max_length=100, blank=True, verbose_name='نام انگلیسی')
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES, verbose_name='نوع دسته')
    description = models.TextField(verbose_name='توضیحات')
    
    # مزایا و تسهیلات
    benefits = models.JSONField(default=list, verbose_name='مزایا')
    special_services = models.JSONField(default=list, verbose_name='خدمات ویژه')
    
    # شرایط عضویت
    eligibility_criteria = models.TextField(verbose_name='شرایط واجد شرایط بودن')
    required_documents = models.JSONField(default=list, verbose_name='مدارک مورد نیاز')
    
    # محدودیت‌ها
    max_members = models.IntegerField(null=True, blank=True, verbose_name='حداکثر اعضا')
    validity_period_months = models.IntegerField(null=True, blank=True, verbose_name='مدت اعتبار (ماه)')
    
    class Meta:
        verbose_name = 'دسته دانشجویی'
        verbose_name_plural = 'دسته‌های دانشجویی'
        ordering = ['name']

    def __str__(self):
        return self.name


class AcademicProgram(BaseModel):
    """برنامه‌های تحصیلی"""
    PROGRAM_TYPES = [
        ('BACHELOR', 'کارشناسی'),
        ('MASTER', 'کارشناسی ارشد'),
        ('PHD', 'دکتری تخصصی'),
        ('PROFESSIONAL_DOCTORATE', 'دکتری حرفه‌ای'),
        ('POST_DOCTORATE', 'فوق دکتری'),
        ('DIPLOMA', 'دیپلم'),
        ('ASSOCIATE', 'کاردانی'),
    ]

    PROGRAM_MODES = [
        ('FULL_TIME', 'تمام وقت'),
        ('PART_TIME', 'پاره وقت'),
        ('EVENING', 'شبانه'),
        ('WEEKEND', 'آخر هفته'),
        ('DISTANCE', 'مجازی'),
        ('HYBRID', 'ترکیبی'),
    ]

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='academic_programs',
        verbose_name='گروه آموزشی'
    )
    name = models.CharField(max_length=255, verbose_name='نام برنامه')
    name_en = models.CharField(max_length=255, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, verbose_name='کد برنامه')
    
    # نوع و حالت برنامه
    program_type = models.CharField(max_length=30, choices=PROGRAM_TYPES, verbose_name='نوع برنامه')
    program_mode = models.CharField(max_length=20, choices=PROGRAM_MODES, verbose_name='حالت ارائه')
    
    # مشخصات آموزشی
    total_credits = models.IntegerField(verbose_name='مجموع واحدها')
    duration_semesters = models.IntegerField(verbose_name='مدت تحصیل (ترم)')
    minimum_gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='حداقل معدل'
    )
    
    # پیش‌نیازها
    prerequisites = models.JSONField(default=list, verbose_name='پیش‌نیازهای ورود')
    entrance_requirements = models.TextField(verbose_name='شرایط پذیرش')
    
    # اطلاعات مالی
    tuition_per_semester = models.DecimalField(
        max_digits=12, 
        decimal_places=0,
        verbose_name='شهریه هر ترم'
    )
    additional_fees = models.JSONField(default=dict, verbose_name='هزینه‌های اضافی')
    
    # ظرفیت
    max_capacity = models.IntegerField(verbose_name='حداکثر ظرفیت')
    current_enrollment = models.IntegerField(default=0, verbose_name='تعداد فعلی ثبت‌نام')
    
    # وضعیت
    is_accepting_students = models.BooleanField(default=True, verbose_name='پذیرای دانشجو')
    accreditation_status = models.CharField(max_length=50, verbose_name='وضعیت اعتبار')
    
    # اطلاعات تکمیلی
    objectives = models.TextField(verbose_name='اهداف برنامه')
    career_prospects = models.TextField(verbose_name='چشم‌انداز شغلی')
    curriculum = models.JSONField(default=dict, verbose_name='برنامه درسی')
    
    class Meta:
        verbose_name = 'برنامه تحصیلی'
        verbose_name_plural = 'برنامه‌های تحصیلی'
        unique_together = ['department', 'code']
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.department.name}"

    @property
    def remaining_capacity(self):
        """ظرفیت باقی‌مانده"""
        return self.max_capacity - self.current_enrollment

    @property
    def is_full(self):
        """آیا ظرفیت تکمیل است؟"""
        return self.current_enrollment >= self.max_capacity


# ==============================================================================
# MAIN STUDENT MODEL
# ==============================================================================

class Student(PersonModel):
    """مدل اصلی دانشجویان"""
    STUDENT_TYPES = [
        ('REGULAR', 'روزانه'),
        ('EVENING', 'شبانه'),
        ('SELF_SUPPORTING', 'پردیس خودگردان'),
        ('DISTANCE', 'مجازی'),
        ('PAYAM_NOOR', 'پیام نور'),
        ('NON_PROFIT', 'غیرانتفاعی'),
        ('AZAD', 'آزاد اسلامی'),
    ]

    ACADEMIC_STATUS = [
        ('ACTIVE', 'فعال'),
        ('ACADEMIC_LEAVE', 'مرخصی تحصیلی'),
        ('CONDITIONAL', 'مشروط'),
        ('GUEST', 'مهمان'),
        ('TRANSFER', 'انتقالی'),
        ('GRADUATED', 'فارغ‌التحصیل'),
        ('DROPPED', 'انصرافی'),
        ('EXPELLED', 'اخراج'),
        ('SUSPENDED', 'تعلیق'),
    ]

    FINANCIAL_STATUS = [
        ('REGULAR', 'عادی'),
        ('SCHOLARSHIP', 'بورسیه'),
        ('LOAN', 'وام‌گیرنده'),
        ('DISCOUNT', 'تخفیف شهریه'),
        ('EXEMPTION', 'معافیت شهریه'),
        ('SPONSORED', 'تحت حمایت'),
    ]

    MARITAL_STATUS = [
        ('SINGLE', 'مجرد'),
        ('MARRIED', 'متأهل'),
        ('DIVORCED', 'مطلقه'),
        ('WIDOWED', 'بیوه'),
    ]

    # شناسه‌ها
    student_id = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name='شماره دانشجویی'
    )
    university_student_id = models.CharField(
        max_length=30,
        verbose_name='شماره دانشجویی دانشگاه'
    )
    
    # برنامه تحصیلی
    academic_program = models.ForeignKey(
        AcademicProgram,
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name='برنامه تحصیلی'
    )
    
    # نوع دانشجو
    student_type = models.CharField(max_length=20, choices=STUDENT_TYPES, verbose_name='نوع دانشجو')
    academic_status = models.CharField(
        max_length=20, 
        choices=ACADEMIC_STATUS, 
        default='ACTIVE',
        verbose_name='وضعیت تحصیلی'
    )
    financial_status = models.CharField(
        max_length=20, 
        choices=FINANCIAL_STATUS, 
        default='REGULAR',
        verbose_name='وضعیت مالی'
    )
    
    # اطلاعات شخصی تکمیلی
    marital_status = models.CharField(
        max_length=10, 
        choices=MARITAL_STATUS, 
        default='SINGLE',
        verbose_name='وضعیت تأهل'
    )
    military_service_status = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='وضعیت خدمت نظام وظیفه'
    )
    
    # اطلاعات تحصیلی
    entrance_year = models.IntegerField(verbose_name='سال ورود')
    entrance_semester = models.CharField(
        max_length=10,
        choices=[('FALL', 'پاییز'), ('SPRING', 'بهار'), ('SUMMER', 'تابستان')],
        verbose_name='ترم ورود'
    )
    current_semester = models.IntegerField(default=1, verbose_name='ترم جاری')
    
    # عملکرد تحصیلی
    current_gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='معدل فعلی'
    )
    cumulative_gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='معدل کل'
    )
    total_credits_earned = models.IntegerField(default=0, verbose_name='واحدهای گذرانده شده')
    total_credits_attempted = models.IntegerField(default=0, verbose_name='واحدهای اخذ شده')
    
    # اطلاعات مالی
    total_tuition_paid = models.DecimalField(
        max_digits=12, 
        decimal_places=0,
        default=0,
        verbose_name='کل شهریه پرداخت شده'
    )
    outstanding_balance = models.DecimalField(
        max_digits=12, 
        decimal_places=0,
        default=0,
        verbose_name='بدهی باقی‌مانده'
    )
    scholarship_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=0,
        default=0,
        verbose_name='مبلغ بورسیه'
    )
    
    # اطلاعات خوابگاه
    dormitory_resident = models.BooleanField(default=False, verbose_name='ساکن خوابگاه')
    dormitory_room = models.CharField(max_length=20, blank=True, verbose_name='شماره اتاق')
    meal_plan = models.CharField(
        max_length=20,
        choices=[
            ('NONE', 'بدون طرح غذایی'),
            ('BASIC', 'طرح پایه'),
            ('FULL', 'طرح کامل'),
            ('CUSTOM', 'طرح اختصاصی'),
        ],
        default='NONE',
        verbose_name='طرح غذایی'
    )
    
    # اطلاعات والدین/سرپرست
    father_name = models.CharField(max_length=100, verbose_name='نام پدر')
    father_job = models.CharField(max_length=100, blank=True, verbose_name='شغل پدر')
    mother_name = models.CharField(max_length=100, verbose_name='نام مادر')
    mother_job = models.CharField(max_length=100, blank=True, verbose_name='شغل مادر')
    guardian_phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^09\d{9}$', 'شماره موبایل نامعتبر')],
        verbose_name='تلفن سرپرست'
    )
    
    # آدرس‌ها
    permanent_address = models.TextField(verbose_name='آدرس دائمی')
    current_address = models.TextField(blank=True, verbose_name='آدرس فعلی')
    
    # اطلاعات اضطراری
    emergency_contact_name = models.CharField(max_length=100, verbose_name='نام تماس اضطراری')
    emergency_contact_phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^09\d{9}$', 'شماره موبایل نامعتبر')],
        verbose_name='تلفن تماس اضطراری'
    )
    emergency_contact_relation = models.CharField(max_length=50, verbose_name='نسبت تماس اضطراری')
    
    # اطلاعات پزشکی
    blood_type = models.CharField(
        max_length=5,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-'),
        ],
        blank=True,
        verbose_name='گروه خونی'
    )
    medical_conditions = models.TextField(blank=True, verbose_name='شرایط پزشکی')
    medications = models.TextField(blank=True, verbose_name='داروهای مصرفی')
    allergies = models.TextField(blank=True, verbose_name='آلرژی‌ها')
    
    # تاریخ‌های مهم
    expected_graduation_date = models.DateField(null=True, blank=True, verbose_name='تاریخ فارغ‌التحصیلی انتظاری')
    actual_graduation_date = models.DateField(null=True, blank=True, verbose_name='تاریخ فارغ‌التحصیلی واقعی')
    last_enrollment_date = models.DateField(null=True, blank=True, verbose_name='آخرین تاریخ ثبت‌نام')
    
    # یادداشت‌ها
    advisor_notes = models.TextField(blank=True, verbose_name='یادداشت‌های مشاور')
    admin_notes = models.TextField(blank=True, verbose_name='یادداشت‌های اداری')
    
    class Meta:
        verbose_name = 'دانشجو'
        verbose_name_plural = 'دانشجویان'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.student_id})"

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk': self.pk})

    @property
    def university(self):
        """دانشگاه دانشجو"""
        return self.academic_program.department.faculty.university

    @property
    def faculty(self):
        """دانشکده دانشجو"""
        return self.academic_program.department.faculty

    @property
    def department(self):
        """گروه آموزشی دانشجو"""
        return self.academic_program.department

    @property
    def academic_year(self):
        """سال تحصیلی فعلی"""
        return (self.current_semester + 1) // 2

    @property
    def is_on_probation(self):
        """آیا مشروط است؟"""
        return self.academic_status == 'CONDITIONAL'

    @property
    def is_graduating_soon(self):
        """آیا نزدیک فارغ‌التحصیلی است؟"""
        if self.expected_graduation_date:
            days_to_graduation = (self.expected_graduation_date - timezone.now().date()).days
            return 0 <= days_to_graduation <= 365
        return False

    @property
    def academic_standing(self):
        """وضعیت تحصیلی بر اساس معدل"""
        if self.cumulative_gpa >= 17:
            return 'ممتاز'
        elif self.cumulative_gpa >= 14:
            return 'خوب'
        elif self.cumulative_gpa >= 12:
            return 'قابل قبول'
        else:
            return 'نیاز به بهبود'

    def calculate_remaining_credits(self):
        """محاسبه واحدهای باقی‌مانده"""
        return self.academic_program.total_credits - self.total_credits_earned

    def can_register_for_semester(self):
        """آیا می‌تواند برای ترم ثبت‌نام کند؟"""
        return (
            self.academic_status == 'ACTIVE' and
            self.outstanding_balance <= 0 and
            self.is_active
        )


# ==============================================================================
# STUDENT CATEGORY ASSIGNMENT
# ==============================================================================

class StudentCategoryAssignment(BaseModel):
    """تخصیص دانشجو به دسته‌های ویژه"""
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='category_assignments',
        verbose_name='دانشجو'
    )
    category = models.ForeignKey(
        StudentCategory,
        on_delete=models.CASCADE,
        related_name='student_assignments',
        verbose_name='دسته'
    )
    
    # تاریخ‌ها
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان')
    
    # وضعیت
    status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'فعال'),
            ('INACTIVE', 'غیرفعال'),
            ('SUSPENDED', 'تعلیق'),
            ('EXPIRED', 'منقضی'),
        ],
        default='ACTIVE',
        verbose_name='وضعیت'
    )
    
    # مدارک و تأییدات
    supporting_documents = models.JSONField(default=list, verbose_name='مدارک پشتیبان')
    approval_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تأیید')
    approved_by = models.CharField(max_length=100, blank=True, verbose_name='تأیید کننده')
    
    # یادداشت‌ها
    notes = models.TextField(blank=True, verbose_name='یادداشت‌ها')
    
    class Meta:
        verbose_name = 'تخصیص دسته دانشجویی'
        verbose_name_plural = 'تخصیص‌های دسته دانشجویی'
        unique_together = ['student', 'category']
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.category.name}"

    @property
    def is_active(self):
        """آیا تخصیص فعال است؟"""
        today = timezone.now().date()
        return (
            self.status == 'ACTIVE' and
            self.start_date <= today and
            (self.end_date is None or self.end_date >= today)
        )

    @property
    def is_expired(self):
        """آیا تخصیص منقضی شده؟"""
        if self.end_date:
            return timezone.now().date() > self.end_date
        return False


# ==============================================================================
# STUDENT USER MODEL
# ==============================================================================

# Extend the User model to include Student relationship
User.add_to_class(
    'student', 
    models.OneToOneField(
        Student, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name='دانشجو'
    )
)


# ==============================================================================
# STUDENT ACADEMIC RECORDS
# ==============================================================================

class AcademicRecord(BaseModel):
    """پرونده تحصیلی دانشجو"""
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='academic_record',
        verbose_name='دانشجو'
    )
    
    # نمرات ورودی
    entrance_exam_score = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='نمره کنکور'
    )
    entrance_rank = models.IntegerField(null=True, blank=True, verbose_name='رتبه کنکور')
    high_school_gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='معدل دیپلم'
    )
    
    # آمار تحصیلی
    total_semesters_enrolled = models.IntegerField(default=0, verbose_name='تعداد ترم‌های ثبت‌نام')
    semesters_on_probation = models.IntegerField(default=0, verbose_name='ترم‌های مشروطی')
    academic_leaves_taken = models.IntegerField(default=0, verbose_name='مرخصی‌های تحصیلی')
    
    # رکوردهای عملکرد
    highest_semester_gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='بالاترین معدل ترم'
    )
    lowest_semester_gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='پایین‌ترین معدل ترم'
    )
    
    # اطلاعات فارغ‌التحصیلی
    thesis_title = models.CharField(max_length=500, blank=True, verbose_name='عنوان پایان‌نامه')
    thesis_supervisor = models.CharField(max_length=100, blank=True, verbose_name='استاد راهنما')
    thesis_grade = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='نمره پایان‌نامه'
    )
    graduation_gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='معدل فارغ‌التحصیلی'
    )
    graduation_rank = models.IntegerField(null=True, blank=True, verbose_name='رتبه فارغ‌التحصیلی')
    
    # افتخارات و جوایز
    honors = models.JSONField(default=list, verbose_name='افتخارات')
    awards = models.JSONField(default=list, verbose_name='جوایز')
    scholarships_received = models.JSONField(default=list, verbose_name='بورسیه‌های دریافتی')
    
    # فعالیت‌های فوق برنامه
    extracurricular_activities = models.JSONField(default=list, verbose_name='فعالیت‌های فوق برنامه')
    research_projects = models.JSONField(default=list, verbose_name='پروژه‌های تحقیقاتی')
    publications = models.JSONField(default=list, verbose_name='انتشارات')
    
    class Meta:
        verbose_name = 'پرونده تحصیلی'
        verbose_name_plural = 'پرونده‌های تحصیلی'

    def __str__(self):
        return f"پرونده تحصیلی {self.student.get_full_name()}"
