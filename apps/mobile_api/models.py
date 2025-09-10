# ==============================================================================
# MOBILE API MODELS
# مدل‌های API موبایل
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

User = get_user_model()


class MobileDevice(models.Model):
    """Model for managing mobile devices"""
    
    DEVICE_TYPES = [
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('web', 'Web Browser'),
        ('desktop', 'Desktop App'),
    ]
    
    PUSH_PROVIDERS = [
        ('fcm', 'Firebase Cloud Messaging'),
        ('apn', 'Apple Push Notification'),
        ('web', 'Web Push'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mobile_devices')
    
    # Device information
    device_id = models.CharField(max_length=255, unique=True)
    device_name = models.CharField(max_length=200, blank=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    device_model = models.CharField(max_length=100, blank=True)
    os_version = models.CharField(max_length=50, blank=True)
    app_version = models.CharField(max_length=20, blank=True)
    
    # Push notification settings
    push_token = models.TextField(blank=True)
    push_provider = models.CharField(max_length=20, choices=PUSH_PROVIDERS, blank=True)
    push_enabled = models.BooleanField(default=True)
    
    # Location and timezone
    timezone = models.CharField(max_length=50, default='UTC')
    last_location = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    
    # Activity tracking
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)
    login_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'mobile_devices'
        verbose_name = 'Mobile Device'
        verbose_name_plural = 'Mobile Devices'
        ordering = ['-last_seen']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['device_type', 'is_active']),
            models.Index(fields=['last_seen']),
        ]
    
    def __str__(self):
        return f"{self.device_name or self.device_model} ({self.user.username})"
    
    def update_activity(self):
        """Update device activity"""
        self.last_seen = timezone.now()
        self.login_count += 1
        self.save(update_fields=['last_seen', 'login_count'])


class MobileSession(models.Model):
    """Model for tracking mobile app sessions"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(MobileDevice, on_delete=models.CASCADE, related_name='sessions')
    
    # Session information
    session_start = models.DateTimeField(auto_now_add=True)
    session_end = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=0)
    
    # App state tracking
    is_active = models.BooleanField(default=True)
    background_time = models.IntegerField(default=0)  # Seconds in background
    foreground_time = models.IntegerField(default=0)  # Seconds in foreground
    
    # Activity metrics
    screens_visited = models.JSONField(default=list, encoder=DjangoJSONEncoder)
    actions_performed = models.JSONField(default=list, encoder=DjangoJSONEncoder)
    api_calls_made = models.IntegerField(default=0)
    
    # Network and performance
    network_type = models.CharField(max_length=20, blank=True)  # wifi, cellular, offline
    data_usage_bytes = models.BigIntegerField(default=0)
    avg_response_time = models.FloatField(default=0.0)
    
    class Meta:
        db_table = 'mobile_sessions'
        verbose_name = 'Mobile Session'
        verbose_name_plural = 'Mobile Sessions'
        ordering = ['-session_start']
        indexes = [
            models.Index(fields=['device', 'session_start']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"Session {self.device.user.username} - {self.session_start.strftime('%Y-%m-%d %H:%M')}"
    
    def end_session(self):
        """End the current session"""
        if self.is_active:
            self.session_end = timezone.now()
            self.duration_seconds = (self.session_end - self.session_start).total_seconds()
            self.is_active = False
            self.save(update_fields=['session_end', 'duration_seconds', 'is_active'])


class PushNotification(models.Model):
    """Model for managing push notifications"""
    
    NOTIFICATION_TYPES = [
        ('general', 'General'),
        ('announcement', 'Announcement'),
        ('grade', 'Grade Update'),
        ('assignment', 'Assignment'),
        ('exam', 'Exam'),
        ('schedule', 'Schedule Change'),
        ('message', 'Message'),
        ('reminder', 'Reminder'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Content
    title = models.CharField(max_length=200)
    message = models.TextField()
    icon = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True)
    
    # Targeting
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    target_users = models.ManyToManyField(User, blank=True, related_name='push_notifications')
    target_devices = models.ManyToManyField(MobileDevice, blank=True)
    target_user_types = models.JSONField(default=list, encoder=DjangoJSONEncoder)  # ['student', 'faculty', 'admin']
    
    # Delivery settings
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_for = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Action
    action_url = models.URLField(blank=True)
    action_data = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    
    # Statistics
    total_recipients = models.IntegerField(default=0)
    successful_sends = models.IntegerField(default=0)
    failed_sends = models.IntegerField(default=0)
    click_count = models.IntegerField(default=0)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'push_notifications'
        verbose_name = 'Push Notification'
        verbose_name_plural = 'Push Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'scheduled_for']),
            models.Index(fields=['notification_type', 'created_at']),
            models.Index(fields=['created_by']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class OfflineSync(models.Model):
    """Model for managing offline data synchronization"""
    
    SYNC_TYPES = [
        ('full', 'Full Sync'),
        ('incremental', 'Incremental'),
        ('delta', 'Delta Sync'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(MobileDevice, on_delete=models.CASCADE, related_name='sync_records')
    
    # Sync configuration
    sync_type = models.CharField(max_length=20, choices=SYNC_TYPES)
    data_types = models.JSONField(default=list, encoder=DjangoJSONEncoder)  # ['courses', 'grades', 'announcements']
    
    # Sync state
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    last_sync_token = models.CharField(max_length=255, blank=True)
    current_sync_token = models.CharField(max_length=255, blank=True)
    
    # Progress tracking
    total_items = models.IntegerField(default=0)
    synced_items = models.IntegerField(default=0)
    failed_items = models.IntegerField(default=0)
    progress_percentage = models.FloatField(default=0.0)
    
    # Data metrics
    data_size_bytes = models.BigIntegerField(default=0)
    compressed_size_bytes = models.BigIntegerField(default=0)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.FloatField(default=0.0)
    
    # Error handling
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'offline_sync'
        verbose_name = 'Offline Sync'
        verbose_name_plural = 'Offline Syncs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['device', 'status']),
            models.Index(fields=['sync_type', 'created_at']),
            models.Index(fields=['status', 'started_at']),
        ]
    
    def __str__(self):
        return f"Sync {self.device.user.username} - {self.get_status_display()}"
    
    def start_sync(self):
        """Start the sync process"""
        self.status = 'in_progress'
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])
    
    def complete_sync(self):
        """Complete the sync process"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        if self.started_at:
            self.duration_seconds = (self.completed_at - self.started_at).total_seconds()
        self.progress_percentage = 100.0
        self.save(update_fields=['status', 'completed_at', 'duration_seconds', 'progress_percentage'])
    
    def fail_sync(self, error_message):
        """Mark sync as failed"""
        self.status = 'failed'
        self.error_message = error_message
        self.retry_count += 1
        self.save(update_fields=['status', 'error_message', 'retry_count'])


class MobileSettings(models.Model):
    """Model for user-specific mobile app settings"""
    
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto (System)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mobile_settings')
    
    # UI preferences
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='auto')
    language = models.CharField(max_length=10, default='fa')
    font_size = models.CharField(max_length=10, default='medium')  # small, medium, large
    
    # Notification preferences
    push_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    notification_sound = models.BooleanField(default=True)
    notification_vibration = models.BooleanField(default=True)
    
    # Sync preferences
    auto_sync = models.BooleanField(default=True)
    sync_on_wifi_only = models.BooleanField(default=False)
    offline_storage_limit_mb = models.IntegerField(default=100)
    
    # Privacy settings
    location_tracking = models.BooleanField(default=False)
    analytics_enabled = models.BooleanField(default=True)
    crash_reporting = models.BooleanField(default=True)
    
    # Performance settings
    image_quality = models.CharField(max_length=10, default='medium')  # low, medium, high
    animation_enabled = models.BooleanField(default=True)
    data_saver_mode = models.BooleanField(default=False)
    
    # Custom settings
    custom_settings = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'mobile_settings'
        verbose_name = 'Mobile Settings'
        verbose_name_plural = 'Mobile Settings'
    
    def __str__(self):
        return f"Mobile Settings for {self.user.username}"
