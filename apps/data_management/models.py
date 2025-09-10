# ==============================================================================
# DATA MANAGEMENT MODELS
# مدل‌های مدیریت داده‌ها
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import uuid
import json
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

User = get_user_model()


class ImportExportJob(models.Model):
    """Model for tracking import/export jobs"""
    
    JOB_TYPES = [
        ('import', 'Import'),
        ('export', 'Export'),
        ('sync', 'Synchronization'),
        ('backup', 'Backup'),
        ('restore', 'Restore'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    FORMATS = [
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('json', 'JSON'),
        ('xml', 'XML'),
        ('sql', 'SQL'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    format = models.CharField(max_length=10, choices=FORMATS, default='csv')
    
    # Job details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    model_name = models.CharField(max_length=100)  # Model to import/export
    
    # File handling
    source_file = models.FileField(upload_to='data_management/imports/', null=True, blank=True)
    result_file = models.FileField(upload_to='data_management/exports/', null=True, blank=True)
    
    # Configuration
    config = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    field_mapping = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    filters = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    
    # Statistics
    total_records = models.IntegerField(default=0)
    processed_records = models.IntegerField(default=0)
    success_records = models.IntegerField(default=0)
    error_records = models.IntegerField(default=0)
    
    # Progress tracking
    progress_percentage = models.FloatField(default=0.0)
    current_step = models.CharField(max_length=200, blank=True)
    
    # Error handling
    errors = models.JSONField(default=list, encoder=DjangoJSONEncoder)
    warnings = models.JSONField(default=list, encoder=DjangoJSONEncoder)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Scheduling
    scheduled_for = models.DateTimeField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_rule = models.CharField(max_length=200, blank=True)  # RRULE format
    
    class Meta:
        db_table = 'data_import_export_jobs'
        verbose_name = 'Import/Export Job'
        verbose_name_plural = 'Import/Export Jobs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'job_type']),
            models.Index(fields=['created_by', 'created_at']),
            models.Index(fields=['scheduled_for']),
        ]
    
    def __str__(self):
        return f"{self.get_job_type_display()}: {self.title}"
    
    @property
    def duration(self):
        """Calculate job duration"""
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        elif self.started_at:
            return timezone.now() - self.started_at
        return None
    
    @property
    def is_finished(self):
        """Check if job is finished"""
        return self.status in ['completed', 'failed', 'cancelled']
    
    def start_job(self):
        """Mark job as started"""
        self.status = 'running'
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])
    
    def complete_job(self):
        """Mark job as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.progress_percentage = 100.0
        self.save(update_fields=['status', 'completed_at', 'progress_percentage'])
    
    def fail_job(self, error_message):
        """Mark job as failed"""
        self.status = 'failed'
        self.completed_at = timezone.now()
        self.errors.append({
            'timestamp': timezone.now().isoformat(),
            'message': error_message
        })
        self.save(update_fields=['status', 'completed_at', 'errors'])


class DataSyncTask(models.Model):
    """Model for data synchronization tasks"""
    
    SYNC_TYPES = [
        ('one_way', 'One Way'),
        ('two_way', 'Two Way'),
        ('backup', 'Backup'),
        ('mirror', 'Mirror'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('disabled', 'Disabled'),
        ('error', 'Error'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Sync configuration
    sync_type = models.CharField(max_length=20, choices=SYNC_TYPES, default='one_way')
    source_model = models.CharField(max_length=100)
    target_model = models.CharField(max_length=100, blank=True)
    
    # External system integration
    external_system_name = models.CharField(max_length=100, blank=True)
    external_endpoint = models.URLField(blank=True)
    auth_config = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    
    # Scheduling
    schedule_enabled = models.BooleanField(default=False)
    schedule_cron = models.CharField(max_length=100, blank=True)  # Cron expression
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    
    # Configuration
    field_mapping = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    filters = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    transform_rules = models.JSONField(default=list, encoder=DjangoJSONEncoder)
    
    # Status and monitoring
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_sync_status = models.CharField(max_length=20, blank=True)
    last_sync_message = models.TextField(blank=True)
    total_synced_records = models.IntegerField(default=0)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'data_sync_tasks'
        verbose_name = 'Data Sync Task'
        verbose_name_plural = 'Data Sync Tasks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'schedule_enabled']),
            models.Index(fields=['next_run']),
            models.Index(fields=['source_model']),
        ]
    
    def __str__(self):
        return self.name


class BackupSchedule(models.Model):
    """Model for backup scheduling and management"""
    
    BACKUP_TYPES = [
        ('full', 'Full Backup'),
        ('incremental', 'Incremental'),
        ('differential', 'Differential'),
        ('schema_only', 'Schema Only'),
        ('data_only', 'Data Only'),
    ]
    
    FREQUENCIES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Backup configuration
    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPES, default='full')
    frequency = models.CharField(max_length=20, choices=FREQUENCIES, default='daily')
    custom_cron = models.CharField(max_length=100, blank=True)
    
    # What to backup
    include_tables = models.JSONField(default=list, encoder=DjangoJSONEncoder)
    exclude_tables = models.JSONField(default=list, encoder=DjangoJSONEncoder)
    include_media = models.BooleanField(default=True)
    include_static = models.BooleanField(default=False)
    
    # Storage configuration
    storage_path = models.CharField(max_length=500)
    max_backups_to_keep = models.IntegerField(default=10)
    compress_backup = models.BooleanField(default=True)
    encrypt_backup = models.BooleanField(default=False)
    
    # Status
    is_enabled = models.BooleanField(default=True)
    last_backup = models.DateTimeField(null=True, blank=True)
    next_backup = models.DateTimeField(null=True, blank=True)
    last_backup_status = models.CharField(max_length=20, blank=True)
    last_backup_size = models.BigIntegerField(default=0)  # Size in bytes
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'backup_schedules'
        verbose_name = 'Backup Schedule'
        verbose_name_plural = 'Backup Schedules'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_enabled', 'next_backup']),
            models.Index(fields=['backup_type', 'frequency']),
        ]
    
    def __str__(self):
        return self.name


class ExternalSystemIntegration(models.Model):
    """Model for external system integrations"""
    
    SYSTEM_TYPES = [
        ('api', 'REST API'),
        ('database', 'Database'),
        ('file_system', 'File System'),
        ('ftp', 'FTP/SFTP'),
        ('cloud_storage', 'Cloud Storage'),
        ('erp', 'ERP System'),
        ('lms', 'Learning Management System'),
        ('other', 'Other'),
    ]
    
    AUTH_TYPES = [
        ('none', 'No Authentication'),
        ('basic', 'Basic Authentication'),
        ('token', 'Token Authentication'),
        ('oauth2', 'OAuth 2.0'),
        ('api_key', 'API Key'),
        ('certificate', 'Certificate'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    system_type = models.CharField(max_length=20, choices=SYSTEM_TYPES)
    
    # Connection details
    endpoint_url = models.URLField(blank=True)
    host = models.CharField(max_length=200, blank=True)
    port = models.IntegerField(null=True, blank=True)
    database_name = models.CharField(max_length=100, blank=True)
    
    # Authentication
    auth_type = models.CharField(max_length=20, choices=AUTH_TYPES, default='none')
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=200, blank=True)  # Should be encrypted
    api_key = models.CharField(max_length=500, blank=True)
    auth_token = models.TextField(blank=True)
    
    # Configuration
    connection_config = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    timeout_seconds = models.IntegerField(default=30)
    retry_attempts = models.IntegerField(default=3)
    
    # Status monitoring
    is_active = models.BooleanField(default=True)
    last_connection_test = models.DateTimeField(null=True, blank=True)
    last_connection_status = models.BooleanField(default=False)
    last_error_message = models.TextField(blank=True)
    
    # Rate limiting
    rate_limit_per_minute = models.IntegerField(default=60)
    rate_limit_per_hour = models.IntegerField(default=1000)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'external_system_integrations'
        verbose_name = 'External System Integration'
        verbose_name_plural = 'External System Integrations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['system_type', 'is_active']),
            models.Index(fields=['last_connection_test']),
        ]
    
    def __str__(self):
        return self.name
    
    def test_connection(self):
        """Test connection to external system"""
        # This would be implemented based on system_type
        pass
