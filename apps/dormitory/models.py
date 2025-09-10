from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

User = get_user_model()


class DormitoryComplex(models.Model):
    """مجموعه خوابگاهی - هر دانشگاه چندین مجموعه خوابگاهی دارد"""
    
    GENDER_CHOICES = [
        ('MALE', 'برادران'),
        ('FEMALE', 'خواهران'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name='نام مجموعه خوابگاهی')
    name_en = models.CharField(max_length=200, blank=True, verbose_name='نام انگلیسی')
    code = models.CharField(max_length=20, unique=True, verbose_name='کد مجموعه')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='جنسیت')
    address = models.TextField(verbose_name='آدرس')
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    
    # مدیریت خوابگاه
    manager = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='managed_dormitory_complexes',
        verbose_name='مدیر مجموعه خوابگاهی'
    )
    
    # تنظیمات کلی
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    established_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تأسیس')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    # امکانات
    facilities = models.JSONField(default=list, blank=True, verbose_name='امکانات')
    rules = models.JSONField(default=list, blank=True, verbose_name='قوانین')
    
    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'مجموعه خوابگاهی'
        verbose_name_plural = 'مجموعه‌های خوابگاهی'
        ordering = ['name']
        indexes = [
            models.Index(fields=['gender']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_gender_display()})"
    
    def clean(self):
        if self.manager and hasattr(self.manager, 'profile'):
            if self.manager.profile.gender != self.gender.lower():
                raise ValidationError(
                    'مدیر خوابگاه باید هم‌جنس با خوابگاه باشد'
                )


class DormitoryBuilding(models.Model):
    """ساختمان خوابگاه - هر مجموعه خوابگاهی چندین ساختمان دارد"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    complex = models.ForeignKey(
        DormitoryComplex,
        on_delete=models.CASCADE,
        related_name='buildings',
        verbose_name='مجموعه خوابگاهی'
    )
    name = models.CharField(max_length=100, verbose_name='نام ساختمان')
    code = models.CharField(max_length=20, verbose_name='کد ساختمان')
    floor_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        verbose_name='تعداد طبقات'
    )
    
    # مشخصات فیزیکی
    construction_year = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1300), MaxValueValidator(1500)],
        verbose_name='سال ساخت'
    )
    total_area = models.PositiveIntegerField(null=True, blank=True, verbose_name='مساحت کل (متر مربع)')
    
    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    maintenance_status = models.CharField(
        max_length=20,
        choices=[
            ('GOOD', 'خوب'),
            ('FAIR', 'متوسط'),
            ('POOR', 'نیاز به تعمیر'),
            ('UNDER_MAINTENANCE', 'در حال تعمیر'),
        ],
        default='GOOD',
        verbose_name='وضعیت نگهداری'
    )
    
    # امکانات ساختمان
    has_elevator = models.BooleanField(default=False, verbose_name='آسانسور')
    has_laundry = models.BooleanField(default=False, verbose_name='رختشویخانه')
    has_kitchen = models.BooleanField(default=False, verbose_name='آشپزخانه')
    has_study_room = models.BooleanField(default=False, verbose_name='اتاق مطالعه')
    has_prayer_room = models.BooleanField(default=False, verbose_name='نمازخانه')
    
    # سرپرست ساختمان
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='supervised_buildings',
        verbose_name='سرپرست ساختمان'
    )
    
    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'ساختمان خوابگاه'
        verbose_name_plural = 'ساختمان‌های خوابگاه'
        ordering = ['complex', 'code']
        unique_together = ['complex', 'code']
        indexes = [
            models.Index(fields=['complex', 'is_active']),
            models.Index(fields=['maintenance_status']),
        ]
    
    def __str__(self):
        return f"{self.complex.name} - {self.name}"
    
    @property
    def total_rooms(self):
        """محاسبه تعداد کل اتاق‌های ساختمان"""
        return self.floors.aggregate(
            total=models.Sum('rooms__count')
        )['total'] or 0
    
    @property
    def total_capacity(self):
        """محاسبه ظرفیت کل ساختمان"""
        return sum(floor.total_capacity for floor in self.floors.all())


class DormitoryFloor(models.Model):
    """طبقه خوابگاه - هر ساختمان چندین طبقه دارد"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    building = models.ForeignKey(
        DormitoryBuilding,
        on_delete=models.CASCADE,
        related_name='floors',
        verbose_name='ساختمان'
    )
    floor_number = models.PositiveIntegerField(verbose_name='شماره طبقه')
    name = models.CharField(max_length=50, blank=True, verbose_name='نام طبقه')
    
    # سرپرست طبقه
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='supervised_floors',
        verbose_name='سرپرست طبقه'
    )
    
    # امکانات طبقه
    has_common_room = models.BooleanField(default=False, verbose_name='اتاق مشترک')
    has_kitchen = models.BooleanField(default=False, verbose_name='آشپزخانه')
    has_bathroom = models.BooleanField(default=True, verbose_name='سرویس بهداشتی')
    
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'طبقه خوابگاه'
        verbose_name_plural = 'طبقات خوابگاه'
        ordering = ['building', 'floor_number']
        unique_together = ['building', 'floor_number']
        indexes = [
            models.Index(fields=['building', 'floor_number']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.building} - طبقه {self.floor_number}"
    
    @property
    def total_capacity(self):
        """محاسبه ظرفیت کل طبقه"""
        return sum(room.capacity for room in self.rooms.all())
    
    def clean(self):
        if self.floor_number > self.building.floor_count:
            raise ValidationError(
                f'شماره طبقه نمی‌تواند بیشتر از {self.building.floor_count} باشد'
            )


class DormitoryRoom(models.Model):
    """اتاق خوابگاه - هر طبقه چندین اتاق دارد"""
    
    ROOM_TYPE_CHOICES = [
        ('SINGLE', 'یک نفره'),
        ('DOUBLE', 'دو نفره'),
        ('TRIPLE', 'سه نفره'),
        ('QUAD', 'چهار نفره'),
        ('SUITE', 'سوئیت'),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'در دسترس'),
        ('OCCUPIED', 'اشغال شده'),
        ('MAINTENANCE', 'در تعمیر'),
        ('RESERVED', 'رزرو شده'),
        ('OUT_OF_ORDER', 'خارج از سرویس'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    floor = models.ForeignKey(
        DormitoryFloor,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name='طبقه'
    )
    room_number = models.CharField(max_length=10, verbose_name='شماره اتاق')
    room_code = models.CharField(max_length=50, unique=True, verbose_name='کد اتاق')
    
    # مشخصات اتاق
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, verbose_name='نوع اتاق')
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name='ظرفیت'
    )
    area = models.PositiveIntegerField(null=True, blank=True, verbose_name='مساحت (متر مربع)')
    
    # وضعیت
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='AVAILABLE', verbose_name='وضعیت')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    # امکانات اتاق
    has_private_bathroom = models.BooleanField(default=False, verbose_name='سرویس اختصاصی')
    has_balcony = models.BooleanField(default=False, verbose_name='بالکن')
    has_air_conditioning = models.BooleanField(default=False, verbose_name='کولر')
    has_heating = models.BooleanField(default=True, verbose_name='گرمایش')
    has_internet = models.BooleanField(default=True, verbose_name='اینترنت')
    
    # محدودیت‌ها و شرایط
    academic_level_restriction = models.JSONField(
        default=list, blank=True,
        help_text='مقاطع تحصیلی مجاز (لیست)',
        verbose_name='محدودیت مقطع تحصیلی'
    )
    min_gpa = models.DecimalField(
        max_digits=4, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='حداقل معدل مورد نیاز'
    )
    special_conditions = models.JSONField(
        default=list, blank=True,
        help_text='شرایط خاص برای اسکان',
        verbose_name='شرایط خاص'
    )
    
    # قیمت‌گذاری
    monthly_rent = models.DecimalField(
        max_digits=10, decimal_places=0,
        default=0,
        verbose_name='اجاره ماهانه (تومان)'
    )
    deposit = models.DecimalField(
        max_digits=10, decimal_places=0,
        default=0,
        verbose_name='ودیعه (تومان)'
    )
    
    # یادداشت‌ها
    description = models.TextField(blank=True, verbose_name='توضیحات')
    maintenance_notes = models.TextField(blank=True, verbose_name='یادداشت‌های نگهداری')
    
    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'اتاق خوابگاه'
        verbose_name_plural = 'اتاق‌های خوابگاه'
        ordering = ['floor', 'room_number']
        unique_together = ['floor', 'room_number']
        indexes = [
            models.Index(fields=['room_code']),
            models.Index(fields=['status']),
            models.Index(fields=['room_type']),
            models.Index(fields=['floor', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.floor} - اتاق {self.room_number}"
    
    def save(self, *args, **kwargs):
        # تولید خودکار کد اتاق
        if not self.room_code:
            self.room_code = f"{self.floor.building.complex.code}-{self.floor.building.code}-{self.floor.floor_number}-{self.room_number}"
        super().save(*args, **kwargs)
    
    @property
    def current_occupancy(self):
        """تعداد ساکنان فعلی"""
        return self.accommodations.filter(
            is_active=True,
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date()
        ).count()
    
    @property
    def available_beds(self):
        """تعداد تخت‌های خالی"""
        return self.capacity - self.current_occupancy
    
    @property
    def is_full(self):
        """آیا اتاق پر است؟"""
        return self.current_occupancy >= self.capacity
    
    def clean(self):
        # بررسی ظرفیت بر اساس نوع اتاق
        type_capacity_map = {
            'SINGLE': 1,
            'DOUBLE': 2,
            'TRIPLE': 3,
            'QUAD': 4,
            'SUITE': 6,
        }
        max_capacity = type_capacity_map.get(self.room_type, 6)
        if self.capacity > max_capacity:
            raise ValidationError(
                f'ظرفیت اتاق {self.get_room_type_display()} نمی‌تواند بیشتر از {max_capacity} باشد'
            )


class DormitoryAccommodation(models.Model):
    """اسکان دانشجو در خوابگاه"""
    
    STATUS_CHOICES = [
        ('PENDING', 'در انتظار تأیید'),
        ('APPROVED', 'تأیید شده'),
        ('ACTIVE', 'فعال'),
        ('SUSPENDED', 'تعلیق'),
        ('TERMINATED', 'خاتمه یافته'),
        ('CANCELLED', 'لغو شده'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dormitory_accommodations',
        verbose_name='دانشجو'
    )
    room = models.ForeignKey(
        DormitoryRoom,
        on_delete=models.CASCADE,
        related_name='accommodations',
        verbose_name='اتاق'
    )
    
    # تاریخ‌ها
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(verbose_name='تاریخ پایان')
    actual_end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ واقعی خروج')
    
    # وضعیت
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING', verbose_name='وضعیت')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    # اطلاعات مالی
    monthly_payment = models.DecimalField(
        max_digits=10, decimal_places=0,
        verbose_name='پرداخت ماهانه'
    )
    deposit_paid = models.DecimalField(
        max_digits=10, decimal_places=0,
        default=0,
        verbose_name='ودیعه پرداخت شده'
    )
    
    # تأیید کنندگان
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='approved_accommodations',
        verbose_name='تأیید کننده'
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ تأیید')
    
    # یادداشت‌ها
    application_notes = models.TextField(blank=True, verbose_name='یادداشت درخواست')
    admin_notes = models.TextField(blank=True, verbose_name='یادداشت مدیریت')
    termination_reason = models.TextField(blank=True, verbose_name='دلیل خاتمه')
    
    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درخواست')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'اسکان خوابگاه'
        verbose_name_plural = 'اسکان‌های خوابگاه'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['room', 'is_active']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.room}"
    
    def clean(self):
        # بررسی تاریخ‌ها
        if self.start_date >= self.end_date:
            raise ValidationError('تاریخ شروع باید قبل از تاریخ پایان باشد')
        
        # بررسی جنسیت
        if hasattr(self.student, 'profile') and hasattr(self.room.floor.building.complex, 'gender'):
            student_gender = getattr(self.student.profile, 'gender', None)
            complex_gender = self.room.floor.building.complex.gender.lower()
            if student_gender and student_gender != complex_gender:
                raise ValidationError('جنسیت دانشجو با جنسیت خوابگاه مطابقت ندارد')
        
        # بررسی ظرفیت اتاق
        if self.status in ['APPROVED', 'ACTIVE']:
            conflicting_accommodations = DormitoryAccommodation.objects.filter(
                room=self.room,
                status__in=['APPROVED', 'ACTIVE'],
                start_date__lt=self.end_date,
                end_date__gt=self.start_date
            ).exclude(id=self.id)
            
            if conflicting_accommodations.count() >= self.room.capacity:
                raise ValidationError('ظرفیت اتاق تکمیل است')
    
    def save(self, *args, **kwargs):
        # تنظیم خودکار مبلغ پرداخت
        if not self.monthly_payment:
            self.monthly_payment = self.room.monthly_rent
        
        super().save(*args, **kwargs)


class DormitoryStaff(models.Model):
    """کارکنان خوابگاه"""
    
    ROLE_CHOICES = [
        ('MANAGER', 'مدیر خوابگاه'),
        ('SUPERVISOR', 'سرپرست'),
        ('GUARD', 'نگهبان'),
        ('CLEANER', 'نظافتچی'),
        ('MAINTENANCE', 'تعمیرکار'),
        ('KITCHEN_STAFF', 'کارمند آشپزخانه'),
        ('ADMIN', 'اداری'),
    ]
    
    SHIFT_CHOICES = [
        ('MORNING', 'صبح'),
        ('EVENING', 'عصر'),
        ('NIGHT', 'شب'),
        ('FULL_TIME', 'تمام وقت'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dormitory_staff_roles',
        verbose_name='کاربر'
    )
    complex = models.ForeignKey(
        DormitoryComplex,
        on_delete=models.CASCADE,
        related_name='staff_members',
        verbose_name='مجموعه خوابگاهی'
    )
    
    # اطلاعات شغلی
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, verbose_name='نقش')
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES, verbose_name='شیفت')
    building = models.ForeignKey(
        DormitoryBuilding,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_staff',
        verbose_name='ساختمان محول شده'
    )
    
    # تاریخ‌ها
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان')
    
    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    # اطلاعات تماس اضطراری
    emergency_contact = models.JSONField(
        default=dict, blank=True,
        verbose_name='تماس اضطراری'
    )
    
    # یادداشت‌ها
    notes = models.TextField(blank=True, verbose_name='یادداشت‌ها')
    
    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'کارمند خوابگاه'
        verbose_name_plural = 'کارکنان خوابگاه'
        ordering = ['complex', 'role', 'user__last_name']
        unique_together = ['user', 'complex', 'role']
        indexes = [
            models.Index(fields=['complex', 'role']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()} ({self.complex.name})"


class DormitoryMaintenance(models.Model):
    """نگهداری و تعمیرات خوابگاه"""
    
    PRIORITY_CHOICES = [
        ('LOW', 'کم'),
        ('MEDIUM', 'متوسط'),
        ('HIGH', 'زیاد'),
        ('URGENT', 'فوری'),
    ]
    
    STATUS_CHOICES = [
        ('REPORTED', 'گزارش شده'),
        ('ASSIGNED', 'محول شده'),
        ('IN_PROGRESS', 'در حال انجام'),
        ('COMPLETED', 'تکمیل شده'),
        ('CANCELLED', 'لغو شده'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(
        DormitoryRoom,
        on_delete=models.CASCADE,
        related_name='maintenance_requests',
        verbose_name='اتاق'
    )
    
    # گزارش‌دهنده
    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reported_maintenances',
        verbose_name='گزارش‌دهنده'
    )
    
    # جزئیات مشکل
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(verbose_name='شرح مشکل')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, verbose_name='اولویت')
    category = models.CharField(
        max_length=50,
        choices=[
            ('ELECTRICAL', 'برق'),
            ('PLUMBING', 'لوله‌کشی'),
            ('HEATING', 'گرمایش'),
            ('COOLING', 'سرمایش'),
            ('FURNITURE', 'مبلمان'),
            ('CLEANING', 'نظافت'),
            ('SECURITY', 'امنیت'),
            ('OTHER', 'سایر'),
        ],
        verbose_name='دسته‌بندی'
    )
    
    # وضعیت و محول شده
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='REPORTED', verbose_name='وضعیت')
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_maintenances',
        verbose_name='محول شده به'
    )
    
    # تاریخ‌ها
    reported_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ گزارش')
    assigned_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ محولی')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ شروع')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ تکمیل')
    
    # هزینه
    estimated_cost = models.DecimalField(
        max_digits=10, decimal_places=0,
        null=True, blank=True,
        verbose_name='هزینه تخمینی'
    )
    actual_cost = models.DecimalField(
        max_digits=10, decimal_places=0,
        null=True, blank=True,
        verbose_name='هزینه واقعی'
    )
    
    # یادداشت‌ها
    admin_notes = models.TextField(blank=True, verbose_name='یادداشت مدیریت')
    technician_notes = models.TextField(blank=True, verbose_name='یادداشت تکنسین')
    completion_notes = models.TextField(blank=True, verbose_name='یادداشت تکمیل')
    
    # تاریخ بروزرسانی
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'درخواست تعمیرات'
        verbose_name_plural = 'درخواست‌های تعمیرات'
        ordering = ['-reported_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['room']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['reported_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.room}"
