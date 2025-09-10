# ==============================================================================
# DATA MANAGEMENT SERIALIZERS
# سریالایزرهای مدیریت داده‌ها
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ImportExportJob, DataSyncTask, BackupSchedule, ExternalSystemIntegration

User = get_user_model()


class ImportExportJobSerializer(serializers.ModelSerializer):
    """Serializer for Import/Export Jobs"""
    
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    duration_display = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    job_type_display = serializers.CharField(source='get_job_type_display', read_only=True)
    format_display = serializers.CharField(source='get_format_display', read_only=True)
    
    class Meta:
        model = ImportExportJob
        fields = [
            'id', 'job_type', 'job_type_display', 'status', 'status_display',
            'format', 'format_display', 'title', 'description', 'model_name',
            'source_file', 'result_file', 'config', 'field_mapping', 'filters',
            'total_records', 'processed_records', 'success_records', 'error_records',
            'progress_percentage', 'current_step', 'errors', 'warnings',
            'created_by', 'created_by_name', 'created_at', 'updated_at',
            'started_at', 'completed_at', 'duration_display',
            'scheduled_for', 'is_recurring', 'recurrence_rule'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at', 'started_at',
            'completed_at', 'progress_percentage', 'processed_records',
            'success_records', 'error_records', 'current_step', 'errors', 'warnings'
        ]
    
    def get_duration_display(self, obj):
        """Get formatted duration"""
        duration = obj.duration
        if duration:
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours > 0:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        return None


class ExportJobCreateSerializer(serializers.Serializer):
    """Serializer for creating export jobs"""
    
    model_name = serializers.CharField(max_length=100)
    format = serializers.ChoiceField(
        choices=[('csv', 'CSV'), ('json', 'JSON'), ('excel', 'Excel')],
        default='csv'
    )
    filters = serializers.JSONField(required=False, default=dict)
    config = serializers.JSONField(required=False, default=dict)
    execute_immediately = serializers.BooleanField(default=False)


class ImportJobCreateSerializer(serializers.Serializer):
    """Serializer for creating import jobs"""
    
    model_name = serializers.CharField(max_length=100)
    source_file = serializers.FileField()
    format = serializers.ChoiceField(
        choices=[('csv', 'CSV'), ('json', 'JSON'), ('excel', 'Excel')],
        default='csv'
    )
    field_mapping = serializers.JSONField(required=False, default=dict)
    config = serializers.JSONField(required=False, default=dict)
    execute_immediately = serializers.BooleanField(default=False)


class DataSyncTaskSerializer(serializers.ModelSerializer):
    """Serializer for Data Sync Tasks"""
    
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    sync_type_display = serializers.CharField(source='get_sync_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    next_run_display = serializers.SerializerMethodField()
    
    class Meta:
        model = DataSyncTask
        fields = [
            'id', 'name', 'description', 'sync_type', 'sync_type_display',
            'source_model', 'target_model', 'external_system_name',
            'external_endpoint', 'auth_config', 'schedule_enabled',
            'schedule_cron', 'last_run', 'next_run', 'next_run_display',
            'field_mapping', 'filters', 'transform_rules',
            'status', 'status_display', 'last_sync_status',
            'last_sync_message', 'total_synced_records',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at',
            'last_run', 'next_run', 'last_sync_status',
            'last_sync_message', 'total_synced_records'
        ]
    
    def get_next_run_display(self, obj):
        """Get formatted next run time"""
        if obj.next_run:
            return obj.next_run.strftime('%Y-%m-%d %H:%M')
        return None


class BackupScheduleSerializer(serializers.ModelSerializer):
    """Serializer for Backup Schedules"""
    
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    backup_type_display = serializers.CharField(source='get_backup_type_display', read_only=True)
    frequency_display = serializers.CharField(source='get_frequency_display', read_only=True)
    backup_size_display = serializers.SerializerMethodField()
    next_backup_display = serializers.SerializerMethodField()
    
    class Meta:
        model = BackupSchedule
        fields = [
            'id', 'name', 'description', 'backup_type', 'backup_type_display',
            'frequency', 'frequency_display', 'custom_cron',
            'include_tables', 'exclude_tables', 'include_media', 'include_static',
            'storage_path', 'max_backups_to_keep', 'compress_backup', 'encrypt_backup',
            'is_enabled', 'last_backup', 'next_backup', 'next_backup_display',
            'last_backup_status', 'last_backup_size', 'backup_size_display',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at',
            'last_backup', 'next_backup', 'last_backup_status', 'last_backup_size'
        ]
    
    def get_backup_size_display(self, obj):
        """Get formatted backup size"""
        if obj.last_backup_size > 0:
            size = obj.last_backup_size
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} PB"
        return None
    
    def get_next_backup_display(self, obj):
        """Get formatted next backup time"""
        if obj.next_backup:
            return obj.next_backup.strftime('%Y-%m-%d %H:%M')
        return None


class ExternalSystemIntegrationSerializer(serializers.ModelSerializer):
    """Serializer for External System Integrations"""
    
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    system_type_display = serializers.CharField(source='get_system_type_display', read_only=True)
    auth_type_display = serializers.CharField(source='get_auth_type_display', read_only=True)
    connection_status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ExternalSystemIntegration
        fields = [
            'id', 'name', 'description', 'system_type', 'system_type_display',
            'endpoint_url', 'host', 'port', 'database_name',
            'auth_type', 'auth_type_display', 'username', 'password',
            'api_key', 'auth_token', 'connection_config',
            'timeout_seconds', 'retry_attempts', 'is_active',
            'last_connection_test', 'last_connection_status',
            'connection_status_display', 'last_error_message',
            'rate_limit_per_minute', 'rate_limit_per_hour',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at',
            'last_connection_test', 'last_connection_status', 'last_error_message'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'api_key': {'write_only': True},
            'auth_token': {'write_only': True},
        }
    
    def get_connection_status_display(self, obj):
        """Get connection status display"""
        if obj.last_connection_status:
            return "Connected"
        elif obj.last_connection_test:
            return "Failed"
        else:
            return "Not Tested"


class DataModelSerializer(serializers.Serializer):
    """Serializer for available data models"""
    
    app_label = serializers.CharField()
    model_name = serializers.CharField()
    verbose_name = serializers.CharField()
    verbose_name_plural = serializers.CharField()
    field_count = serializers.IntegerField()
    record_count = serializers.IntegerField()


class FieldMappingSerializer(serializers.Serializer):
    """Serializer for field mapping configuration"""
    
    source_field = serializers.CharField()
    target_field = serializers.CharField()
    data_type = serializers.CharField()
    required = serializers.BooleanField(default=False)
    default_value = serializers.CharField(required=False, allow_blank=True)


class SystemStatisticsSerializer(serializers.Serializer):
    """Serializer for system statistics"""
    
    total_import_jobs = serializers.IntegerField()
    total_export_jobs = serializers.IntegerField()
    active_sync_tasks = serializers.IntegerField()
    backup_schedules = serializers.IntegerField()
    external_integrations = serializers.IntegerField()
    
    recent_jobs = serializers.ListField(child=serializers.DictField())
    storage_usage = serializers.DictField()
    system_health = serializers.DictField()
