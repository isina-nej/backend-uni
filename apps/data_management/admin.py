# ==============================================================================
# DATA MANAGEMENT ADMIN INTERFACE
# رابط مدیریتی مدیریت داده‌ها
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import ImportExportJob, DataSyncTask, BackupSchedule, ExternalSystemIntegration


@admin.register(ImportExportJob)
class ImportExportJobAdmin(admin.ModelAdmin):
    """Admin interface for Import/Export Jobs"""
    
    list_display = [
        'title', 'job_type', 'status', 'model_name', 
        'progress_display', 'created_by', 'created_at', 'duration_display'
    ]
    list_filter = [
        'job_type', 'status', 'format', 'created_at', 
        'is_recurring', 'model_name'
    ]
    search_fields = ['title', 'description', 'model_name', 'created_by__username']
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'started_at', 'completed_at',
        'progress_percentage', 'duration_display', 'statistics_display'
    ]
    
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'description', 'job_type', 'model_name', 'format')
        }),
        ('Files', {
            'fields': ('source_file', 'result_file')
        }),
        ('Configuration', {
            'fields': ('config', 'field_mapping', 'filters'),
            'classes': ('collapse',)
        }),
        ('Progress & Statistics', {
            'fields': (
                'status', 'progress_percentage', 'current_step',
                'statistics_display', 'duration_display'
            ),
            'classes': ('collapse',)
        }),
        ('Scheduling', {
            'fields': ('scheduled_for', 'is_recurring', 'recurrence_rule'),
            'classes': ('collapse',)
        }),
        ('Errors & Warnings', {
            'fields': ('errors', 'warnings'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def progress_display(self, obj):
        """Display progress as a progress bar"""
        if obj.progress_percentage > 0:
            color = 'green' if obj.status == 'completed' else 'blue'
            if obj.status == 'failed':
                color = 'red'
            return format_html(
                '<div style="width:100px; background:#f0f0f0; border-radius:3px;">'
                '<div style="width:{}px; background:{}; height:20px; border-radius:3px; text-align:center; color:white; font-size:12px; line-height:20px;">'
                '{}%'
                '</div></div>',
                obj.progress_percentage, color, round(obj.progress_percentage)
            )
        return "Not started"
    progress_display.short_description = "Progress"
    
    def duration_display(self, obj):
        """Display job duration"""
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
        return "Not completed"
    duration_display.short_description = "Duration"
    
    def statistics_display(self, obj):
        """Display job statistics"""
        if obj.total_records > 0:
            return format_html(
                '<strong>Total:</strong> {} | <strong>Success:</strong> {} | <strong>Errors:</strong> {}',
                obj.total_records, obj.success_records, obj.error_records
            )
        return "No data processed"
    statistics_display.short_description = "Statistics"


@admin.register(DataSyncTask)
class DataSyncTaskAdmin(admin.ModelAdmin):
    """Admin interface for Data Sync Tasks"""
    
    list_display = [
        'name', 'sync_type', 'source_model', 'status',
        'schedule_enabled', 'last_run', 'next_run_display'
    ]
    list_filter = [
        'sync_type', 'status', 'schedule_enabled', 
        'last_run', 'created_at'
    ]
    search_fields = ['name', 'description', 'source_model', 'target_model']
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'last_run', 
        'next_run', 'total_synced_records'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'sync_type')
        }),
        ('Sync Configuration', {
            'fields': ('source_model', 'target_model', 'field_mapping', 'filters')
        }),
        ('External System', {
            'fields': (
                'external_system_name', 'external_endpoint', 'auth_config'
            ),
            'classes': ('collapse',)
        }),
        ('Scheduling', {
            'fields': (
                'schedule_enabled', 'schedule_cron', 'last_run', 'next_run'
            )
        }),
        ('Advanced Configuration', {
            'fields': ('transform_rules',),
            'classes': ('collapse',)
        }),
        ('Status & Monitoring', {
            'fields': (
                'status', 'last_sync_status', 'last_sync_message', 
                'total_synced_records'
            )
        }),
        ('Metadata', {
            'fields': ('id', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def next_run_display(self, obj):
        """Display next run time"""
        if obj.next_run:
            return obj.next_run.strftime('%Y-%m-%d %H:%M')
        return "Not scheduled"
    next_run_display.short_description = "Next Run"


@admin.register(BackupSchedule)
class BackupScheduleAdmin(admin.ModelAdmin):
    """Admin interface for Backup Schedules"""
    
    list_display = [
        'name', 'backup_type', 'frequency', 'is_enabled',
        'last_backup', 'next_backup_display', 'backup_size_display'
    ]
    list_filter = [
        'backup_type', 'frequency', 'is_enabled', 
        'last_backup', 'created_at'
    ]
    search_fields = ['name', 'description', 'storage_path']
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'last_backup', 
        'next_backup', 'last_backup_status', 'backup_size_display'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'is_enabled')
        }),
        ('Backup Configuration', {
            'fields': (
                'backup_type', 'frequency', 'custom_cron',
                'include_tables', 'exclude_tables'
            )
        }),
        ('Storage Options', {
            'fields': (
                'storage_path', 'max_backups_to_keep',
                'compress_backup', 'encrypt_backup'
            )
        }),
        ('Media & Static Files', {
            'fields': ('include_media', 'include_static'),
            'classes': ('collapse',)
        }),
        ('Status & Statistics', {
            'fields': (
                'last_backup', 'next_backup', 'last_backup_status',
                'backup_size_display'
            )
        }),
        ('Metadata', {
            'fields': ('id', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def next_backup_display(self, obj):
        """Display next backup time"""
        if obj.next_backup:
            return obj.next_backup.strftime('%Y-%m-%d %H:%M')
        return "Not scheduled"
    next_backup_display.short_description = "Next Backup"
    
    def backup_size_display(self, obj):
        """Display backup size in human readable format"""
        if obj.last_backup_size > 0:
            size = obj.last_backup_size
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} PB"
        return "No backup"
    backup_size_display.short_description = "Last Backup Size"


@admin.register(ExternalSystemIntegration)
class ExternalSystemIntegrationAdmin(admin.ModelAdmin):
    """Admin interface for External System Integrations"""
    
    list_display = [
        'name', 'system_type', 'connection_status_display',
        'last_connection_test', 'is_active'
    ]
    list_filter = [
        'system_type', 'auth_type', 'is_active',
        'last_connection_test', 'created_at'
    ]
    search_fields = ['name', 'description', 'endpoint_url', 'host']
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'last_connection_test',
        'last_connection_status', 'last_error_message'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'system_type', 'is_active')
        }),
        ('Connection Details', {
            'fields': (
                'endpoint_url', 'host', 'port', 'database_name'
            )
        }),
        ('Authentication', {
            'fields': (
                'auth_type', 'username', 'password', 'api_key', 'auth_token'
            )
        }),
        ('Configuration', {
            'fields': (
                'connection_config', 'timeout_seconds', 'retry_attempts'
            ),
            'classes': ('collapse',)
        }),
        ('Rate Limiting', {
            'fields': ('rate_limit_per_minute', 'rate_limit_per_hour'),
            'classes': ('collapse',)
        }),
        ('Status & Monitoring', {
            'fields': (
                'last_connection_test', 'last_connection_status',
                'last_error_message'
            )
        }),
        ('Metadata', {
            'fields': ('id', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def connection_status_display(self, obj):
        """Display connection status with color"""
        if obj.last_connection_status:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Connected</span>'
            )
        elif obj.last_connection_test:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Failed</span>'
            )
        else:
            return format_html(
                '<span style="color: orange; font-weight: bold;">? Not Tested</span>'
            )
    connection_status_display.short_description = "Connection Status"
    
    actions = ['test_connections']
    
    def test_connections(self, request, queryset):
        """Test connections for selected integrations"""
        tested = 0
        for integration in queryset:
            integration.test_connection()
            tested += 1
        
        self.message_user(
            request,
            f"Tested {tested} integration(s). Check status in the list."
        )
    test_connections.short_description = "Test selected connections"
