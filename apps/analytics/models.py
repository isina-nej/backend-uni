# ==============================================================================
# ADVANCED ANALYTICS & REPORTING MODELS
# مدل‌های آنالیتیکس و گزارش‌گیری پیشرفته
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import json
import uuid

User = get_user_model()


class DashboardType(models.TextChoices):
    """Types of dashboards available in the system"""
    ADMIN = 'admin', _('مدیریتی')
    STUDENT = 'student', _('دانشجویی')
    FACULTY = 'faculty', _('هیئت علمی')
    DEPARTMENT = 'department', _('دپارتمان')
    FINANCIAL = 'financial', _('مالی')
    ACADEMIC = 'academic', _('آکادمیک')
    RESEARCH = 'research', _('پژوهشی')
    LIBRARY = 'library', _('کتابخانه')
    CUSTOM = 'custom', _('سفارشی')


class ChartType(models.TextChoices):
    """Chart types for data visualization"""
    LINE = 'line', _('خطی')
    BAR = 'bar', _('ستونی')
    PIE = 'pie', _('دایره‌ای')
    DOUGHNUT = 'doughnut', _('حلقه‌ای')
    AREA = 'area', _('ناحیه‌ای')
    SCATTER = 'scatter', _('پراکندگی')
    RADAR = 'radar', _('رادار')
    HEATMAP = 'heatmap', _('نقشه حرارتی')
    GAUGE = 'gauge', _('عقربه‌ای')
    TABLE = 'table', _('جدولی')
    KPI = 'kpi', _('شاخص کلیدی')


class ReportFrequency(models.TextChoices):
    """Report generation frequency"""
    REAL_TIME = 'real_time', _('بلادرنگ')
    DAILY = 'daily', _('روزانه')
    WEEKLY = 'weekly', _('هفتگی')
    MONTHLY = 'monthly', _('ماهانه')
    QUARTERLY = 'quarterly', _('فصلی')
    YEARLY = 'yearly', _('سالانه')
    ON_DEMAND = 'on_demand', _('درخواستی')


class Dashboard(models.Model):
    """Dynamic dashboard configuration"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    description = models.TextField(blank=True, verbose_name=_('توضیحات'))
    dashboard_type = models.CharField(
        max_length=20,
        choices=DashboardType.choices,
        default=DashboardType.CUSTOM,
        verbose_name=_('نوع داشبورد')
    )
    
    # Access Control
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_dashboards',
        verbose_name=_('ایجادکننده')
    )
    is_public = models.BooleanField(default=False, verbose_name=_('عمومی'))
    allowed_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='accessible_dashboards',
        verbose_name=_('کاربران مجاز')
    )
    allowed_roles = models.JSONField(default=list, blank=True, verbose_name=_('نقش‌های مجاز'))
    
    # Layout and Configuration
    layout_config = models.JSONField(
        default=dict,
        help_text=_('تنظیمات چیدمان داشبورد'),
        verbose_name=_('پیکربندی چیدمان')
    )
    refresh_interval = models.PositiveIntegerField(
        default=300,  # 5 minutes
        help_text=_('بازه به‌روزرسانی به ثانیه'),
        verbose_name=_('بازه به‌روزرسانی')
    )
    
    # Metadata
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    is_default = models.BooleanField(default=False, verbose_name=_('پیش‌فرض'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ به‌روزرسانی'))
    last_accessed = models.DateTimeField(null=True, blank=True, verbose_name=_('آخرین دسترسی'))
    access_count = models.PositiveIntegerField(default=0, verbose_name=_('تعداد دسترسی'))
    
    class Meta:
        db_table = 'analytics_dashboards'
        verbose_name = _('داشبورد')
        verbose_name_plural = _('داشبوردها')
        indexes = [
            models.Index(fields=['dashboard_type', 'is_active']),
            models.Index(fields=['created_by', 'is_public']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_dashboard_type_display()})"
    
    def update_access(self):
        """Update access statistics"""
        self.last_accessed = timezone.now()
        self.access_count += 1
        self.save(update_fields=['last_accessed', 'access_count'])
    
    def can_access(self, user):
        """Check if user can access this dashboard"""
        if not user.is_authenticated:
            return False
        
        if self.created_by == user or user.is_superuser:
            return True
        
        if self.is_public:
            return True
        
        if self.allowed_users.filter(id=user.id).exists():
            return True
        
        # Check roles
        if self.allowed_roles and hasattr(user, 'groups'):
            user_roles = list(user.groups.values_list('name', flat=True))
            if any(role in self.allowed_roles for role in user_roles):
                return True
        
        return False


class Widget(models.Model):
    """Dashboard widget for data visualization"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dashboard = models.ForeignKey(
        Dashboard,
        on_delete=models.CASCADE,
        related_name='widgets',
        verbose_name=_('داشبورد')
    )
    
    # Widget Configuration
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    description = models.TextField(blank=True, verbose_name=_('توضیحات'))
    chart_type = models.CharField(
        max_length=20,
        choices=ChartType.choices,
        default=ChartType.BAR,
        verbose_name=_('نوع نمودار')
    )
    
    # Data Source
    data_source = models.CharField(
        max_length=100,
        help_text=_('منبع داده (مدل یا API)'),
        verbose_name=_('منبع داده')
    )
    query_config = models.JSONField(
        default=dict,
        help_text=_('تنظیمات کوئری داده'),
        verbose_name=_('پیکربندی کوئری')
    )
    aggregation_config = models.JSONField(
        default=dict,
        help_text=_('تنظیمات تجمیع داده'),
        verbose_name=_('پیکربندی تجمیع')
    )
    
    # Layout and Display
    position_x = models.PositiveIntegerField(default=0, verbose_name=_('موقعیت X'))
    position_y = models.PositiveIntegerField(default=0, verbose_name=_('موقعیت Y'))
    width = models.PositiveIntegerField(default=4, verbose_name=_('عرض'))
    height = models.PositiveIntegerField(default=3, verbose_name=_('ارتفاع'))
    
    # Chart Configuration
    chart_config = models.JSONField(
        default=dict,
        help_text=_('تنظیمات نمودار (رنگ، فونت، و...)'),
        verbose_name=_('پیکربندی نمودار')
    )
    
    # Refresh and Caching
    refresh_interval = models.PositiveIntegerField(
        default=300,  # 5 minutes
        verbose_name=_('بازه به‌روزرسانی')
    )
    cache_duration = models.PositiveIntegerField(
        default=600,  # 10 minutes
        verbose_name=_('مدت کش')
    )
    
    # Metadata
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('ترتیب'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ به‌روزرسانی'))
    
    class Meta:
        db_table = 'analytics_widgets'
        verbose_name = _('ویجت')
        verbose_name_plural = _('ویجت‌ها')
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['dashboard', 'is_active']),
            models.Index(fields=['chart_type']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_chart_type_display()})"


class Report(models.Model):
    """Custom report configuration"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name=_('عنوان گزارش'))
    description = models.TextField(blank=True, verbose_name=_('توضیحات'))
    
    # Report Configuration
    report_type = models.CharField(
        max_length=50,
        help_text=_('نوع گزارش (student, faculty, financial, etc.)'),
        verbose_name=_('نوع گزارش')
    )
    data_sources = models.JSONField(
        default=list,
        help_text=_('لیست منابع داده'),
        verbose_name=_('منابع داده')
    )
    filters = models.JSONField(
        default=dict,
        help_text=_('فیلترهای گزارش'),
        verbose_name=_('فیلترها')
    )
    grouping = models.JSONField(
        default=list,
        help_text=_('گروه‌بندی داده‌ها'),
        verbose_name=_('گروه‌بندی')
    )
    sorting = models.JSONField(
        default=list,
        help_text=_('مرتب‌سازی داده‌ها'),
        verbose_name=_('مرتب‌سازی')
    )
    
    # Schedule Configuration
    frequency = models.CharField(
        max_length=20,
        choices=ReportFrequency.choices,
        default=ReportFrequency.ON_DEMAND,
        verbose_name=_('دوره تکرار')
    )
    schedule_config = models.JSONField(
        default=dict,
        help_text=_('تنظیمات زمان‌بندی'),
        verbose_name=_('پیکربندی زمان‌بندی')
    )
    
    # Access Control
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_reports',
        verbose_name=_('ایجادکننده')
    )
    is_public = models.BooleanField(default=False, verbose_name=_('عمومی'))
    allowed_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='accessible_reports',
        verbose_name=_('کاربران مجاز')
    )
    allowed_roles = models.JSONField(default=list, blank=True, verbose_name=_('نقش‌های مجاز'))
    
    # Export Configuration
    export_formats = models.JSONField(
        default=list,
        help_text=_('فرمت‌های خروجی مجاز'),
        verbose_name=_('فرمت‌های خروجی')
    )
    
    # Metadata
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    last_generated = models.DateTimeField(null=True, blank=True, verbose_name=_('آخرین تولید'))
    generation_count = models.PositiveIntegerField(default=0, verbose_name=_('تعداد تولید'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ به‌روزرسانی'))
    
    class Meta:
        db_table = 'analytics_reports'
        verbose_name = _('گزارش')
        verbose_name_plural = _('گزارش‌ها')
        indexes = [
            models.Index(fields=['report_type', 'is_active']),
            models.Index(fields=['created_by', 'frequency']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def can_access(self, user):
        """Check if user can access this report"""
        if not user.is_authenticated:
            return False
        
        if self.created_by == user or user.is_superuser:
            return True
        
        if self.is_public:
            return True
        
        if self.allowed_users.filter(id=user.id).exists():
            return True
        
        # Check roles
        if self.allowed_roles and hasattr(user, 'groups'):
            user_roles = list(user.groups.values_list('name', flat=True))
            if any(role in self.allowed_roles for role in user_roles):
                return True
        
        return False


class ReportExecution(models.Model):
    """Track report execution history"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='executions',
        verbose_name=_('گزارش')
    )
    executed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='report_executions',
        verbose_name=_('اجراکننده')
    )
    
    # Execution Details
    executed_at = models.DateTimeField(auto_now_add=True, verbose_name=_('زمان اجرا'))
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('در انتظار')),
            ('running', _('در حال اجرا')),
            ('completed', _('تکمیل شده')),
            ('failed', _('شکست خورده')),
            ('cancelled', _('لغو شده')),
        ],
        default='pending',
        verbose_name=_('وضعیت')
    )
    
    # Results
    result_data = models.JSONField(
        null=True,
        blank=True,
        help_text=_('داده‌های نتیجه گزارش'),
        verbose_name=_('داده‌های نتیجه')
    )
    row_count = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('تعداد ردیف'))
    file_path = models.CharField(
        max_length=500,
        blank=True,
        help_text=_('مسیر فایل خروجی'),
        verbose_name=_('مسیر فایل')
    )
    file_size = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('اندازه فایل'))
    
    # Performance Metrics
    execution_time = models.FloatField(
        null=True,
        blank=True,
        help_text=_('زمان اجرا به ثانیه'),
        verbose_name=_('زمان اجرا')
    )
    memory_usage = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_('استفاده از حافظه به بایت'),
        verbose_name=_('استفاده از حافظه')
    )
    
    # Error Handling
    error_message = models.TextField(blank=True, verbose_name=_('پیام خطا'))
    error_traceback = models.TextField(blank=True, verbose_name=_('ردیابی خطا'))
    
    class Meta:
        db_table = 'analytics_report_executions'
        verbose_name = _('اجرای گزارش')
        verbose_name_plural = _('اجراهای گزارش')
        ordering = ['-executed_at']
        indexes = [
            models.Index(fields=['report', 'status']),
            models.Index(fields=['executed_by', 'executed_at']),
            models.Index(fields=['status', 'executed_at']),
        ]
    
    def __str__(self):
        return f"{self.report.title} - {self.executed_at.strftime('%Y-%m-%d %H:%M')}"


class AnalyticsMetric(models.Model):
    """Store calculated analytics metrics"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric_name = models.CharField(max_length=100, verbose_name=_('نام معیار'))
    metric_type = models.CharField(
        max_length=50,
        choices=[
            ('student_performance', _('عملکرد دانشجویی')),
            ('faculty_performance', _('عملکرد هیئت علمی')),
            ('course_analytics', _('آنالیتیکس درس')),
            ('financial_metrics', _('معیارهای مالی')),
            ('system_performance', _('عملکرد سیستم')),
            ('custom', _('سفارشی')),
        ],
        verbose_name=_('نوع معیار')
    )
    
    # Value and Context
    value = models.JSONField(verbose_name=_('مقدار'))
    context = models.JSONField(
        default=dict,
        help_text=_('زمینه و فیلترهای محاسبه'),
        verbose_name=_('زمینه')
    )
    
    # Time Range
    period_start = models.DateTimeField(verbose_name=_('شروع دوره'))
    period_end = models.DateTimeField(verbose_name=_('پایان دوره'))
    
    # Metadata
    calculated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('زمان محاسبه'))
    calculated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('محاسبه‌کننده')
    )
    
    # Caching
    cache_key = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('کلید کش برای بازیابی سریع'),
        verbose_name=_('کلید کش')
    )
    expires_at = models.DateTimeField(verbose_name=_('زمان انقضا'))
    
    class Meta:
        db_table = 'analytics_metrics'
        verbose_name = _('معیار آنالیتیکس')
        verbose_name_plural = _('معیارهای آنالیتیکس')
        indexes = [
            models.Index(fields=['metric_type', 'metric_name']),
            models.Index(fields=['period_start', 'period_end']),
            models.Index(fields=['calculated_at']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['cache_key']),
        ]
    
    def __str__(self):
        return f"{self.metric_name} ({self.period_start.date()} - {self.period_end.date()})"
    
    def is_expired(self):
        """Check if the metric cache has expired"""
        return timezone.now() > self.expires_at
