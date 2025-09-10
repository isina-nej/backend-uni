# ==============================================================================
# MOBILE API SERIALIZERS
# سریالایزرهای API موبایل
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import MobileDevice, MobileSession, PushNotification, OfflineSync, MobileSettings

User = get_user_model()


class MobileDeviceSerializer(serializers.ModelSerializer):
    """Serializer for mobile device management"""
    
    user_display = serializers.CharField(source='user.get_full_name', read_only=True)
    device_type_display = serializers.CharField(source='get_device_type_display', read_only=True)
    push_provider_display = serializers.CharField(source='get_push_provider_display', read_only=True)
    
    class Meta:
        model = MobileDevice
        fields = [
            'id', 'user', 'user_display', 'device_id', 'device_name',
            'device_type', 'device_type_display', 'device_model', 'os_version',
            'app_version', 'push_token', 'push_provider', 'push_provider_display',
            'push_enabled', 'timezone', 'last_location', 'is_active',
            'last_seen', 'login_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user_display', 'device_type_display', 'push_provider_display',
            'last_seen', 'login_count', 'created_at', 'updated_at'
        ]


class MobileDeviceRegistrationSerializer(serializers.Serializer):
    """Serializer for device registration"""
    
    device_id = serializers.CharField(max_length=255)
    device_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    device_type = serializers.ChoiceField(choices=MobileDevice.DEVICE_TYPES)
    device_model = serializers.CharField(max_length=100, required=False, allow_blank=True)
    os_version = serializers.CharField(max_length=50, required=False, allow_blank=True)
    app_version = serializers.CharField(max_length=20, required=False, allow_blank=True)
    timezone = serializers.CharField(max_length=50, default='UTC')
    push_token = serializers.CharField(required=False, allow_blank=True)
    push_provider = serializers.ChoiceField(choices=MobileDevice.PUSH_PROVIDERS, required=False)


class MobileSessionSerializer(serializers.ModelSerializer):
    """Serializer for mobile session tracking"""
    
    device_display = serializers.CharField(source='device.__str__', read_only=True)
    duration_display = serializers.SerializerMethodField()
    
    class Meta:
        model = MobileSession
        fields = [
            'id', 'device', 'device_display', 'session_start', 'session_end',
            'duration_seconds', 'duration_display', 'is_active', 'background_time',
            'foreground_time', 'screens_visited', 'actions_performed',
            'api_calls_made', 'network_type', 'data_usage_bytes', 'avg_response_time'
        ]
        read_only_fields = [
            'id', 'device_display', 'session_start', 'session_end',
            'duration_seconds', 'duration_display'
        ]
    
    def get_duration_display(self, obj):
        if obj.duration_seconds:
            minutes = obj.duration_seconds // 60
            seconds = obj.duration_seconds % 60
            return f"{int(minutes)}m {int(seconds)}s"
        return "Active" if obj.is_active else "Unknown"


class SessionStartSerializer(serializers.Serializer):
    """Serializer for starting a session"""
    
    device_id = serializers.CharField(max_length=255)
    network_type = serializers.CharField(max_length=20, required=False, allow_blank=True)
    location = serializers.JSONField(required=False)


class SessionUpdateSerializer(serializers.Serializer):
    """Serializer for updating session activity"""
    
    screens_visited = serializers.ListField(child=serializers.CharField(), required=False)
    actions_performed = serializers.ListField(child=serializers.JSONField(), required=False)
    api_calls_made = serializers.IntegerField(required=False)
    data_usage_bytes = serializers.IntegerField(required=False)
    foreground_time = serializers.IntegerField(required=False)
    background_time = serializers.IntegerField(required=False)


class PushNotificationSerializer(serializers.ModelSerializer):
    """Serializer for push notifications"""
    
    created_by_display = serializers.CharField(source='created_by.get_full_name', read_only=True)
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    target_users_count = serializers.SerializerMethodField()
    target_devices_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PushNotification
        fields = [
            'id', 'title', 'message', 'icon', 'image_url', 'notification_type',
            'notification_type_display', 'target_users', 'target_devices',
            'target_users_count', 'target_devices_count', 'target_user_types',
            'status', 'status_display', 'scheduled_for', 'expires_at',
            'action_url', 'action_data', 'total_recipients', 'successful_sends',
            'failed_sends', 'click_count', 'created_by', 'created_by_display',
            'created_at', 'sent_at'
        ]
        read_only_fields = [
            'id', 'notification_type_display', 'status_display', 'target_users_count',
            'target_devices_count', 'total_recipients', 'successful_sends',
            'failed_sends', 'click_count', 'created_by_display', 'created_at', 'sent_at'
        ]
    
    def get_target_users_count(self, obj):
        return obj.target_users.count()
    
    def get_target_devices_count(self, obj):
        return obj.target_devices.count()


class PushNotificationCreateSerializer(serializers.Serializer):
    """Serializer for creating push notifications"""
    
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    notification_type = serializers.ChoiceField(choices=PushNotification.NOTIFICATION_TYPES, default='general')
    icon = serializers.CharField(max_length=200, required=False, allow_blank=True)
    image_url = serializers.URLField(required=False, allow_blank=True)
    
    # Targeting options
    user_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    device_ids = serializers.ListField(child=serializers.CharField(), required=False)
    user_types = serializers.ListField(child=serializers.CharField(), required=False)
    
    # Action
    action_url = serializers.URLField(required=False, allow_blank=True)
    action_data = serializers.JSONField(required=False)
    
    # Scheduling
    schedule_for = serializers.DateTimeField(required=False)
    expires_at = serializers.DateTimeField(required=False)


class OfflineSyncSerializer(serializers.ModelSerializer):
    """Serializer for offline sync records"""
    
    device_display = serializers.CharField(source='device.__str__', read_only=True)
    sync_type_display = serializers.CharField(source='get_sync_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    progress_display = serializers.SerializerMethodField()
    duration_display = serializers.SerializerMethodField()
    
    class Meta:
        model = OfflineSync
        fields = [
            'id', 'device', 'device_display', 'sync_type', 'sync_type_display',
            'data_types', 'status', 'status_display', 'last_sync_token',
            'current_sync_token', 'total_items', 'synced_items', 'failed_items',
            'progress_percentage', 'progress_display', 'data_size_bytes',
            'compressed_size_bytes', 'started_at', 'completed_at',
            'duration_seconds', 'duration_display', 'error_message',
            'retry_count', 'max_retries', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'device_display', 'sync_type_display', 'status_display',
            'progress_display', 'duration_display', 'created_at', 'updated_at'
        ]
    
    def get_progress_display(self, obj):
        return f"{obj.progress_percentage:.1f}%"
    
    def get_duration_display(self, obj):
        if obj.duration_seconds:
            if obj.duration_seconds < 60:
                return f"{obj.duration_seconds:.1f}s"
            else:
                minutes = obj.duration_seconds // 60
                seconds = obj.duration_seconds % 60
                return f"{int(minutes)}m {int(seconds)}s"
        return "-"


class SyncInitiateSerializer(serializers.Serializer):
    """Serializer for initiating sync"""
    
    device_id = serializers.CharField(max_length=255)
    sync_type = serializers.ChoiceField(choices=OfflineSync.SYNC_TYPES, default='incremental')
    data_types = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=['courses', 'grades', 'announcements', 'notifications']
    )


class MobileSettingsSerializer(serializers.ModelSerializer):
    """Serializer for mobile app settings"""
    
    user_display = serializers.CharField(source='user.get_full_name', read_only=True)
    theme_display = serializers.CharField(source='get_theme_display', read_only=True)
    
    class Meta:
        model = MobileSettings
        fields = [
            'user', 'user_display', 'theme', 'theme_display', 'language',
            'font_size', 'push_notifications', 'email_notifications',
            'notification_sound', 'notification_vibration', 'auto_sync',
            'sync_on_wifi_only', 'offline_storage_limit_mb', 'location_tracking',
            'analytics_enabled', 'crash_reporting', 'image_quality',
            'animation_enabled', 'data_saver_mode', 'custom_settings',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'user', 'user_display', 'theme_display', 'created_at', 'updated_at'
        ]


class MobileSettingsUpdateSerializer(serializers.Serializer):
    """Serializer for updating mobile settings"""
    
    theme = serializers.ChoiceField(choices=MobileSettings.THEME_CHOICES, required=False)
    language = serializers.CharField(max_length=10, required=False)
    font_size = serializers.CharField(max_length=10, required=False)
    
    # Notifications
    push_notifications = serializers.BooleanField(required=False)
    email_notifications = serializers.BooleanField(required=False)
    notification_sound = serializers.BooleanField(required=False)
    notification_vibration = serializers.BooleanField(required=False)
    
    # Sync
    auto_sync = serializers.BooleanField(required=False)
    sync_on_wifi_only = serializers.BooleanField(required=False)
    offline_storage_limit_mb = serializers.IntegerField(required=False)
    
    # Privacy
    location_tracking = serializers.BooleanField(required=False)
    analytics_enabled = serializers.BooleanField(required=False)
    crash_reporting = serializers.BooleanField(required=False)
    
    # Performance
    image_quality = serializers.CharField(max_length=10, required=False)
    animation_enabled = serializers.BooleanField(required=False)
    data_saver_mode = serializers.BooleanField(required=False)
    
    # Custom
    custom_settings = serializers.JSONField(required=False)


class MobileUserProfileSerializer(serializers.ModelSerializer):
    """Serializer for mobile user profile"""
    
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'user_type', 'user_type_display', 'phone_number', 'avatar_url',
            'is_active', 'date_joined', 'last_login'
        ]
        read_only_fields = [
            'id', 'username', 'user_type_display', 'full_name', 'avatar_url',
            'is_active', 'date_joined', 'last_login'
        ]
    
    def get_avatar_url(self, obj):
        # Return avatar URL if available
        if hasattr(obj, 'profile') and obj.profile.avatar:
            return obj.profile.avatar.url
        return None


class MobileDashboardSerializer(serializers.Serializer):
    """Serializer for mobile dashboard data"""
    
    user_info = MobileUserProfileSerializer(read_only=True)
    stats = serializers.JSONField(read_only=True)
    recent_activities = serializers.JSONField(read_only=True)
    quick_actions = serializers.JSONField(read_only=True)
    notifications_count = serializers.IntegerField(read_only=True)
    
    def to_representation(self, instance):
        # instance would be a dictionary containing dashboard data
        return instance
