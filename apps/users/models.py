from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class OrganizationalUnit(models.Model):
    """
    واحدهای سازمانی دانشگاه - ساختار سلسله مراتبی
    """
    UNIT_TYPE_CHOICES = [
        # سطح دانشگاه
        ('university', 'دانشگاه'),
        ('presidency', 'حوزه ریاست'),
        
        # معاونت‌های اصلی
        ('vice_presidency', 'معاونت'),
        ('vice_education', 'معاونت آموزشی'),
        ('vice_research', 'معاونت پژوهش و فناوری'),
        ('vice_student', 'معاونت دانشجویی'),
        ('vice_planning', 'معاونت برنامه‌ریزی و توسعه منابع'),
        ('vice_admin', 'معاونت اداری و مالی'),
        ('vice_construction', 'معاونت عمرانی'),
        ('vice_cultural', 'معاونت فرهنگی و اجتماعی'),
        ('vice_international', 'معاونت بین‌الملل'),
        ('vice_technology', 'معاونت فناوری‌های دیجیتال'),
        
        # دانشکده‌ها و گروه‌ها
        ('faculty', 'دانشکده'),
        ('department', 'گروه آموزشی'),
        ('research_center', 'مرکز تحقیقاتی'),
        
        # ادارات و بخش‌ها
        ('directorate_general', 'اداره کل'),
        ('directorate', 'اداره'),
        ('office', 'دفتر'),
        ('section', 'بخش'),
        ('unit', 'واحد'),
        
        # سازمان‌های وابسته
        ('organization', 'سازمان'),
        ('student_org', 'سازمان امور دانشجویی'),
        ('development_org', 'سازمان توسعه و سرمایه‌گذاری'),
        
        # شوراها
        ('council', 'شورا'),
        ('board', 'هیأت'),
        ('committee', 'کمیته'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='نام واحد')
    code = models.CharField(max_length=20, unique=True, verbose_name='کد واحد')
    unit_type = models.CharField(max_length=30, choices=UNIT_TYPE_CHOICES, verbose_name='نوع واحد')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name='واحد والد')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'واحد سازمانی'
        verbose_name_plural = 'واحدهای سازمانی'
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.get_unit_type_display()} - {self.name}"
    
    def get_full_path(self):
        """مسیر کامل واحد سازمانی"""
        path = [self.name]
        parent = self.parent
        while parent:
            path.insert(0, parent.name)
            parent = parent.parent
        return ' / '.join(path)


class Position(models.Model):
    """
    سمت‌ها و مناصب سازمانی
    """
    POSITION_LEVEL_CHOICES = [
        ('executive', 'مدیریت اجرایی'),
        ('senior', 'ارشد'),
        ('middle', 'میانی'),
        ('junior', 'مبتدی'),
        ('specialist', 'کارشناس'),
        ('expert', 'متخصص'),
        ('administrative', 'اداری'),
        ('service', 'خدماتی'),
        ('academic', 'هیأت علمی'),
        ('research', 'پژوهشی'),
    ]
    
    AUTHORITY_LEVEL_CHOICES = [
        (1, 'بدون اختیار خاص'),
        (2, 'اختیار محدود'),
        (3, 'اختیار متوسط'),
        (4, 'اختیار بالا'),
        (5, 'اختیار کامل'),
    ]
    
    title = models.CharField(max_length=100, verbose_name='عنوان سمت')
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE, 
                                          related_name='positions', verbose_name='واحد سازمانی')
    position_level = models.CharField(max_length=20, choices=POSITION_LEVEL_CHOICES, verbose_name='سطح سمت')
    authority_level = models.IntegerField(choices=AUTHORITY_LEVEL_CHOICES, default=1, verbose_name='سطح اختیار')
    job_description = models.TextField(blank=True, verbose_name='شرح وظایف')
    required_qualifications = models.TextField(blank=True, verbose_name='شرایط احراز')
    salary_grade = models.PositiveIntegerField(null=True, blank=True, verbose_name='پایه حقوقی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'سمت سازمانی'
        verbose_name_plural = 'سمت‌های سازمانی'
        unique_together = ['title', 'organizational_unit']
    
    def __str__(self):
        return f"{self.title} - {self.organizational_unit.name}"


class User(AbstractUser):
    ROLE_CHOICES = [
        # نقش‌های اصلی
        ('student', 'دانشجو'),
        ('faculty', 'عضو هیأت علمی'),
        ('staff', 'کارمند'),
        ('manager', 'مدیر'),
        ('president', 'رئیس دانشگاه'),
        ('vice_president', 'معاون'),
        ('dean', 'دکان دانشکده'),
        ('head_of_department', 'رئیس گروه'),
        
        # نقش‌های تخصصی
        ('researcher', 'پژوهشگر'),
        ('administrative', 'اداری'),
        ('financial', 'مالی'),
        ('technical', 'فنی'),
        ('security', 'امنیتی'),
        ('service', 'خدماتی'),
        
        # نقش‌های دانشجویی
        ('undergraduate', 'کارشناسی'),
        ('graduate', 'کارشناسی ارشد'),
        ('phd', 'دکتری'),
        ('postdoc', 'فوق دکتری'),
        
        # نقش‌های سیستمی
        ('super_admin', 'مدیر کل سیستم'),
        ('system_admin', 'مدیر سیستم'),
        ('auditor', 'بازرس'),
        ('guest', 'مهمان'),
    ]
    
    ACADEMIC_RANK_CHOICES = [
        ('instructor', 'مربی'),
        ('assistant_professor', 'استادیار'),
        ('associate_professor', 'دانشیار'),
        ('professor', 'استاد'),
        ('emeritus_professor', 'استاد بازنشسته'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('permanent', 'رسمی'),
        ('contract', 'قراردادی'),
        ('project', 'پروژه‌ای'),
        ('hourly', 'ساعتی'),
        ('visiting', 'مهمان'),
        ('retired', 'بازنشسته'),
    ]
    
    # اطلاعات شخصی
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True,
                                 validators=[RegexValidator(r'^\d{10}$', 'کد ملی باید 10 رقم باشد')],
                                 verbose_name='کد ملی')
    persian_first_name = models.CharField(max_length=50, blank=True, verbose_name='نام فارسی')
    persian_last_name = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی فارسی')
    father_name = models.CharField(max_length=50, blank=True, verbose_name='نام پدر')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    gender = models.CharField(max_length=10, choices=[('male', 'مرد'), ('female', 'زن')], 
                            blank=True, verbose_name='جنسیت')
    
    # اطلاعات تماس
    phone = models.CharField(max_length=15, blank=True, verbose_name='تلفن')
    mobile = models.CharField(max_length=15, blank=True, verbose_name='موبایل')
    address = models.TextField(blank=True, verbose_name='آدرس')
    
    # اطلاعات سازمانی
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='student', verbose_name='نقش')
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='شماره پرسنلی')
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='شماره دانشجویی')
    
    # رابطه با واحد سازمانی
    primary_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='primary_members',
                                   verbose_name='واحد سازمانی اصلی')
    
    # اطلاعات آکادمیک
    academic_rank = models.CharField(max_length=30, choices=ACADEMIC_RANK_CHOICES, 
                                   blank=True, verbose_name='مرتبه علمی')
    field_of_study = models.CharField(max_length=100, blank=True, verbose_name='رشته تحصیلی')
    degree = models.CharField(max_length=50, blank=True, verbose_name='مدرک تحصیلی')
    
    # اطلاعات استخدامی
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, 
                                     blank=True, verbose_name='نوع استخدام')
    hire_date = models.DateField(null=True, blank=True, verbose_name='تاریخ استخدام')
    salary_grade = models.PositiveIntegerField(null=True, blank=True, verbose_name='پایه حقوقی')
    
    # وضعیت
    is_verified = models.BooleanField(default=False, verbose_name='تأیید شده')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
    
    def __str__(self):
        name = f"{self.persian_first_name} {self.persian_last_name}".strip()
        if not name:
            name = f"{self.first_name} {self.last_name}".strip()
        if not name:
            name = self.username
        return f"{name} ({self.get_role_display()})"
    
    def get_full_persian_name(self):
        return f"{self.persian_first_name} {self.persian_last_name}".strip()
    
    def is_faculty_member(self):
        return self.role in ['faculty', 'dean', 'head_of_department'] or self.academic_rank
    
    def is_student(self):
        return self.role in ['student', 'undergraduate', 'graduate', 'phd', 'postdoc']
    
    def is_staff_member(self):
        return self.role in ['staff', 'manager', 'administrative', 'financial', 'technical', 'service']
    
    def is_management(self):
        return self.role in ['president', 'vice_president', 'dean', 'head_of_department', 'manager']


class UserPosition(models.Model):
    """
    تخصیص کاربران به سمت‌ها - امکان چند سمت برای یک کاربر
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='positions', verbose_name='کاربر')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='assignments', verbose_name='سمت')
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_primary = models.BooleanField(default=False, verbose_name='سمت اصلی')
    appointment_letter = models.CharField(max_length=100, blank=True, verbose_name='شماره حکم')
    notes = models.TextField(blank=True, verbose_name='یادداشت‌ها')
    
    class Meta:
        verbose_name = 'تخصیص سمت'
        verbose_name_plural = 'تخصیص‌های سمت'
        unique_together = ['user', 'position', 'start_date']
    
    def __str__(self):
        return f"{self.user} - {self.position} ({'فعال' if self.is_active else 'غیرفعال'})"


class Permission(models.Model):
    """
    مجوزها و دسترسی‌های سیستم
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
        return f"{self.name} ({self.get_permission_type_display()})"


class UserPermission(models.Model):
    """
    تخصیص مجوزها به کاربران
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_permissions_custom', verbose_name='کاربر')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='مجوز')
    organizational_unit = models.ForeignKey(OrganizationalUnit, on_delete=models.CASCADE, 
                                          null=True, blank=True, verbose_name='محدود به واحد')
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                 related_name='granted_permissions', verbose_name='اعطا شده توسط')
    granted_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ اعطا')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ انقضا')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    class Meta:
        verbose_name = 'مجوز کاربر'
        verbose_name_plural = 'مجوزهای کاربران'
        unique_together = ['user', 'permission', 'organizational_unit']
    
    def __str__(self):
        unit_str = f" - {self.organizational_unit}" if self.organizational_unit else ""
        return f"{self.user} - {self.permission}{unit_str}"


class AccessLog(models.Model):
    """
    لاگ دسترسی‌های کاربران برای بازرسی
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    action = models.CharField(max_length=100, verbose_name='عمل انجام شده')
    resource = models.CharField(max_length=100, verbose_name='منبع')
    ip_address = models.GenericIPAddressField(verbose_name='آدرس IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='زمان')
    success = models.BooleanField(default=True, verbose_name='موفق')
    
    class Meta:
        verbose_name = 'لاگ دسترسی'
        verbose_name_plural = 'لاگ‌های دسترسی'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
