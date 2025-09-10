# ==============================================================================
# MOBILE API ADMIN
# پنل ادمین API موبایل
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import MobileDevice, MobileSession, PushNotification, OfflineSync, MobileSettings


@admin.register(MobileDevice)
class MobileDeviceAdmin(admin.ModelAdmin):
    list_display = [
        'device_name', 'user', 'device_type', 'app_version', 
        'is_active', 'last_seen', 'login_count'
    ]
    list_filter = [
        'device_type', 'is_active', 'push_enabled', 'push_provider',
        'created_at', 'last_seen'
    ]
    search_fields = ['device_name', 'device_id', 'user__username', 'device_model']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_seen', 'login_count']
    
    fieldsets = (
        ('Device Information', {
            'fields': ('user', 'device_id', 'device_name', 'device_type', 'device_model', 'os_version', 'app_version')
        }),
        ('Push Notifications', {
            'fields': ('push_token', 'push_provider', 'push_enabled')
        }),
        ('Location & Timezone', {
            'fields': ('timezone', 'last_location'),
            'classes': ('collapse',)
        }),
        ('Activity', {
            'fields': ('is_active', 'last_seen', 'login_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['deactivate_devices', 'clear_push_tokens']
    
    def deactivate_devices(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} devices deactivated.')
    deactivate_devices.short_description = "Deactivate selected devices"
    
    def clear_push_tokens(self, request, queryset):
        updated = queryset.update(push_token='', push_enabled=False)
        self.message_user(request, f'Push tokens cleared for {updated} devices.')
    clear_push_tokens.short_description = "Clear push tokens for selected devices"


@admin.register(MobileSession)
class MobileSessionAdmin(admin.ModelAdmin):
    list_display = [
        'device', 'session_start', 'duration_display', 'is_active',
        'api_calls_made', 'network_type'
    ]
    list_filter = [
        'is_active', 'network_type', 'session_start',
        'device__device_type'
    ]
    search_fields = ['device__user__username', 'device__device_name']
    readonly_fields = [
        'id', 'session_start', 'session_end', 'duration_seconds',
        'background_time', 'foreground_time'
    ]
    
    fieldsets = (
        ('Session Info', {
            'fields': ('device', 'session_start', 'session_end', 'duration_seconds', 'is_active')
        }),
        ('Activity Tracking', {
            'fields': ('background_time', 'foreground_time', 'screens_visited', 'actions_performed', 'api_calls_made')
        }),
        ('Network & Performance', {
            'fields': ('network_type', 'data_usage_bytes', 'avg_response_time'),
            'classes': ('collapse',)
        })
    )
    
    def duration_display(self, obj):
        if obj.duration_seconds:
            minutes = obj.duration_seconds // 60
            seconds = obj.duration_seconds % 60
            return f"{int(minutes)}m {int(seconds)}s"
        return "Active" if obj.is_active else "Unknown"
    duration_display.short_description = "Duration"


@admin.register(PushNotification)
class PushNotificationAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'notification_type', 'status', 'total_recipients',
        'successful_sends', 'click_count', 'created_at'
    ]
    list_filter = [
        'status', 'notification_type', 'created_at', 'sent_at'
    ]
    search_fields = ['title', 'message', 'created_by__username']
    readonly_fields = [
        'id', 'total_recipients', 'successful_sends', 'failed_sends',
        'click_count', 'created_at', 'sent_at'
    ]
    filter_horizontal = ['target_users', 'target_devices']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'message', 'notification_type', 'icon', 'image_url')
        }),
        ('Targeting', {
            'fields': ('target_users', 'target_devices', 'target_user_types')
        }),
        ('Delivery', {
            'fields': ('status', 'scheduled_for', 'expires_at')
        }),
        ('Action', {
            'fields': ('action_url', 'action_data'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('total_recipients', 'successful_sends', 'failed_sends', 'click_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'sent_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['send_notifications', 'cancel_notifications']
    
    def send_notifications(self, request, queryset):
        sent_count = 0
        for notification in queryset.filter(status='draft'):
            notification.status = 'scheduled'
            notification.scheduled_for = timezone.now()
            notification.save()
            sent_count += 1
        
        self.message_user(request, f'{sent_count} notifications scheduled for sending.')
    send_notifications.short_description = "Send selected notifications"
    
    def cancel_notifications(self, request, queryset):
        cancelled_count = queryset.filter(status__in=['draft', 'scheduled']).update(status='cancelled')
        self.message_user(request, f'{cancelled_count} notifications cancelled.')
    cancel_notifications.short_description = "Cancel selected notifications"


@admin.register(OfflineSync)
class OfflineSyncAdmin(admin.ModelAdmin):
    list_display = [
        'device', 'sync_type', 'status', 'progress_display',
        'synced_items', 'total_items', 'duration_display', 'created_at'
    ]
    list_filter = [
        'status', 'sync_type', 'created_at', 'device__device_type'
    ]
    search_fields = ['device__user__username', 'device__device_name']
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'started_at', 'completed_at',
        'duration_seconds', 'progress_percentage', 'retry_count'
    ]
    
    fieldsets = (
        ('Sync Configuration', {
            'fields': ('device', 'sync_type', 'data_types', 'status')
        }),
        ('Progress', {
            'fields': ('total_items', 'synced_items', 'failed_items', 'progress_percentage')
        }),
        ('Tokens', {
            'fields': ('last_sync_token', 'current_sync_token'),
            'classes': ('collapse',)
        }),
        ('Data Metrics', {
            'fields': ('data_size_bytes', 'compressed_size_bytes'),
            'classes': ('collapse',)
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'duration_seconds'),
            'classes': ('collapse',)
        }),
        ('Error Handling', {
            'fields': ('error_message', 'retry_count', 'max_retries'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def progress_display(self, obj):
        if obj.progress_percentage:
            return f"{obj.progress_percentage:.1f}%"
        return "0%"
    progress_display.short_description = "Progress"
    
    def duration_display(self, obj):
        if obj.duration_seconds:
            if obj.duration_seconds < 60:
                return f"{obj.duration_seconds:.1f}s"
            else:
                minutes = obj.duration_seconds // 60
                seconds = obj.duration_seconds % 60
                return f"{int(minutes)}m {int(seconds)}s"
        return "-"
    duration_display.short_description = "Duration"


@admin.register(MobileSettings)
class MobileSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'theme', 'language', 'push_notifications',
        'auto_sync', 'data_saver_mode', 'updated_at'
    ]
    list_filter = [
        'theme', 'language', 'push_notifications', 'auto_sync',
        'data_saver_mode', 'location_tracking'
    ]
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('UI Preferences', {
            'fields': ('theme', 'language', 'font_size')
        }),
        ('Notifications', {
            'fields': ('push_notifications', 'email_notifications', 'notification_sound', 'notification_vibration')
        }),
        ('Sync Preferences', {
            'fields': ('auto_sync', 'sync_on_wifi_only', 'offline_storage_limit_mb')
        }),
        ('Privacy Settings', {
            'fields': ('location_tracking', 'analytics_enabled', 'crash_reporting'),
            'classes': ('collapse',)
        }),
        ('Performance', {
            'fields': ('image_quality', 'animation_enabled', 'data_saver_mode'),
            'classes': ('collapse',)
        }),
        ('Custom Settings', {
            'fields': ('custom_settings',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['reset_to_defaults']
    
    def reset_to_defaults(self, request, queryset):
        reset_count = 0
        for settings in queryset:
            settings.theme = 'auto'
            settings.language = 'fa'
            settings.font_size = 'medium'
            settings.push_notifications = True
            settings.auto_sync = True
            settings.save()
            reset_count += 1
        
        self.message_user(request, f'{reset_count} settings reset to defaults.')
    reset_to_defaults.short_description = "Reset selected settings to defaults"
