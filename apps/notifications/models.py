# ==============================================================================
# REAL-TIME NOTIFICATIONS SYSTEM
# سیستم اعلانات بلادرنگ
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import json
import uuid

User = get_user_model()


class NotificationType(models.TextChoices):
    """Types of notifications in the system"""
    INFO = 'info', _('اطلاعات')
    SUCCESS = 'success', _('موفقیت')
    WARNING = 'warning', _('هشدار')
    ERROR = 'error', _('خطا')
    URGENT = 'urgent', _('فوری')
    ANNOUNCEMENT = 'announcement', _('اعلان')
    ASSIGNMENT = 'assignment', _('تکلیف')
    GRADE = 'grade', _('نمره')
    SCHEDULE = 'schedule', _('برنامه زمانی')
    EXAM = 'exam', _('امتحان')
    ATTENDANCE = 'attendance', _('حضور و غیاب')
    PAYMENT = 'payment', _('پرداخت')
    LIBRARY = 'library', _('کتابخانه')
    MESSAGE = 'message', _('پیام')


class NotificationChannel(models.TextChoices):
    """Notification delivery channels"""
    IN_APP = 'in_app', _('درون برنامه')
    EMAIL = 'email', _('ایمیل')
    SMS = 'sms', _('پیامک')
    PUSH = 'push', _('اعلان پوش')
    WEBSOCKET = 'websocket', _('وب‌سوکت')
    WEB = 'web', _('وب')
    FLUTTER = 'flutter', _('اپلیکیشن موبایل')
    TELEGRAM = 'telegram', _('تلگرام')
    DISCORD = 'discord', _('دیسکورد')
    SLACK = 'slack', _('اسلک')


class NotificationPriority(models.TextChoices):
    """Notification priority levels"""
    LOW = 'low', _('پایین')
    NORMAL = 'normal', _('عادی')
    HIGH = 'high', _('بالا')
    CRITICAL = 'critical', _('بحرانی')


class Notification(models.Model):
    """Enhanced notification model with real-time capabilities"""
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    message = models.TextField(verbose_name=_('پیام'))
    type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO,
        verbose_name=_('نوع اعلان')
    )
    priority = models.CharField(
        max_length=20,
        choices=NotificationPriority.choices,
        default=NotificationPriority.NORMAL,
        verbose_name=_('اولویت')
    )
    
    # Recipients and Sender
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        verbose_name=_('کاربر')
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sent_notifications',
        verbose_name=_('فرستنده')
    )
    
    # Platform and Channel Support (backward compatibility)
    platform = models.CharField(
        max_length=20, 
        choices=NotificationChannel.choices,
        default=NotificationChannel.WEB,
        verbose_name=_('پلتفرم')
    )
    
    # Delivery Channels (new enhanced system)
    channels = models.JSONField(
        default=list,
        help_text=_('کانال‌های ارسال اعلان')
    )
    
    # Related Object (Generic Foreign Key)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    
    # Status and Tracking
    is_read = models.BooleanField(default=False, verbose_name=_('خوانده شده'))
    read_at = models.DateTimeField(null=True, blank=True, verbose_name=_('زمان خواندن'))
    is_sent = models.BooleanField(default=False, verbose_name=_('ارسال شده'))
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_('زمان ارسال'))
    
    # Real-time features
    is_real_time = models.BooleanField(default=True, verbose_name=_('بلادرنگ'))
    websocket_sent = models.BooleanField(default=False, verbose_name=_('ارسال وب‌سوکت'))
    
    # Scheduling
    scheduled_for = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('زمان‌بندی شده برای')
    )
    expires_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('منقضی می‌شود در')
    )
    
    # Additional Data
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('داده‌های اضافی اعلان')
    )
    
    # Action buttons and URL
    action_url = models.URLField(blank=True, verbose_name=_('لینک عمل'))
    action_text = models.CharField(max_length=100, blank=True, verbose_name=_('متن دکمه'))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ به‌روزرسانی'))
    
    class Meta:
        db_table = 'notifications'
        verbose_name = _('اعلان')
        verbose_name_plural = _('اعلانات')
        ordering = ['-created_at', '-priority']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['type', 'priority']),
            models.Index(fields=['created_at']),
            models.Index(fields=['scheduled_for']),
            models.Index(fields=['is_real_time', 'websocket_sent']),
        ]
    
    def __str__(self):
        return f"{self.platform} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def mark_as_sent(self):
        """Mark notification as sent"""
        if not self.is_sent:
            self.is_sent = True
            self.sent_at = timezone.now()
            self.save(update_fields=['is_sent', 'sent_at'])
    
    def mark_websocket_sent(self):
        """Mark as sent via WebSocket"""
        if not self.websocket_sent:
            self.websocket_sent = True
            self.save(update_fields=['websocket_sent'])
    
    @property
    def is_expired(self):
        """Check if notification is expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    @property
    def is_scheduled(self):
        """Check if notification is scheduled for future"""
        if self.scheduled_for:
            return timezone.now() < self.scheduled_for
        return False
    
    def to_websocket_dict(self):
        """Convert to dictionary for WebSocket transmission"""
        return {
            'id': str(self.id),
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'priority': self.priority,
            'platform': self.platform,
            'is_read': self.is_read,
            'action_url': self.action_url,
            'action_text': self.action_text,
            'created_at': self.created_at.isoformat(),
            'extra_data': self.extra_data,
        }


class NotificationTemplate(models.Model):
    """Template for notification messages"""
    
    name = models.CharField(max_length=100, unique=True, verbose_name=_('نام قالب'))
    type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        verbose_name=_('نوع اعلان')
    )
    title_template = models.CharField(max_length=200, verbose_name=_('قالب عنوان'))
    message_template = models.TextField(verbose_name=_('قالب پیام'))
    default_channels = models.JSONField(
        default=list,
        help_text=_('کانال‌های پیش‌فرض')
    )
    priority = models.CharField(
        max_length=20,
        choices=NotificationPriority.choices,
        default=NotificationPriority.NORMAL,
        verbose_name=_('اولویت پیش‌فرض')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    is_real_time = models.BooleanField(default=True, verbose_name=_('بلادرنگ'))
    
    # Multilingual support
    title_template_en = models.CharField(max_length=200, blank=True, verbose_name=_('قالب عنوان انگلیسی'))
    message_template_en = models.TextField(blank=True, verbose_name=_('قالب پیام انگلیسی'))
    title_template_ar = models.CharField(max_length=200, blank=True, verbose_name=_('قالب عنوان عربی'))
    message_template_ar = models.TextField(blank=True, verbose_name=_('قالب پیام عربی'))
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ به‌روزرسانی'))
    
    class Meta:
        db_table = 'notification_templates'
        verbose_name = _('قالب اعلان')
        verbose_name_plural = _('قالب‌های اعلان')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class NotificationPreference(models.Model):
    """User notification preferences"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    
    # Channel preferences
    email_enabled = models.BooleanField(default=True, verbose_name=_('ایمیل فعال'))
    sms_enabled = models.BooleanField(default=False, verbose_name=_('پیامک فعال'))
    push_enabled = models.BooleanField(default=True, verbose_name=_('اعلان پوش فعال'))
    in_app_enabled = models.BooleanField(default=True, verbose_name=_('اعلان درون برنامه فعال'))
    websocket_enabled = models.BooleanField(default=True, verbose_name=_('اعلان بلادرنگ فعال'))
    
    # Platform preferences (backward compatibility)
    web_enabled = models.BooleanField(default=True, verbose_name=_('وب فعال'))
    flutter_enabled = models.BooleanField(default=True, verbose_name=_('موبایل فعال'))
    telegram_enabled = models.BooleanField(default=False, verbose_name=_('تلگرام فعال'))
    
    # Type-specific preferences
    preferences = models.JSONField(
        default=dict,
        help_text=_('تنظیمات تفصیلی برای هر نوع اعلان')
    )
    
    # Quiet hours
    quiet_hours_enabled = models.BooleanField(default=False, verbose_name=_('ساعات سکوت فعال'))
    quiet_start_time = models.TimeField(null=True, blank=True, verbose_name=_('شروع ساعات سکوت'))
    quiet_end_time = models.TimeField(null=True, blank=True, verbose_name=_('پایان ساعات سکوت'))
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ به‌روزرسانی'))
    
    class Meta:
        db_table = 'notification_preferences'
        verbose_name = _('تنظیمات اعلان')
        verbose_name_plural = _('تنظیمات اعلانات')
    
    def __str__(self):
        return f"تنظیمات اعلان {self.user.get_full_name()}"


class WebSocketConnection(models.Model):
    """Track active WebSocket connections"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='websocket_connections')
    connection_id = models.CharField(max_length=100, unique=True, verbose_name=_('شناسه اتصال'))
    channel_name = models.CharField(max_length=100, verbose_name=_('نام کانال'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    
    # Connection metadata
    user_agent = models.TextField(blank=True, verbose_name=_('مرورگر کاربر'))
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('آدرس IP'))
    platform = models.CharField(max_length=50, blank=True, verbose_name=_('پلتفرم'))
    
    connected_at = models.DateTimeField(auto_now_add=True, verbose_name=_('زمان اتصال'))
    last_activity = models.DateTimeField(auto_now=True, verbose_name=_('آخرین فعالیت'))
    disconnected_at = models.DateTimeField(null=True, blank=True, verbose_name=_('زمان قطع اتصال'))
    
    class Meta:
        db_table = 'websocket_connections'
        verbose_name = _('اتصال وب‌سوکت')
        verbose_name_plural = _('اتصالات وب‌سوکت')
        ordering = ['-connected_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['connection_id']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.connection_id}"
    
    def disconnect(self):
        """Mark connection as disconnected"""
        self.is_active = False
        self.disconnected_at = timezone.now()
        self.save(update_fields=['is_active', 'disconnected_at'])
