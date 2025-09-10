# ==============================================================================
# NOTIFICATION SERIALIZERS WITH WEBSOCKET SUPPORT
# سریالایزرهای اعلانات با پشتیبانی وب‌سوکت
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Notification, NotificationTemplate, NotificationPreference,
    WebSocketConnection
)

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    time_since_created = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_username', 'user_full_name',
            'title', 'message', 'notification_type', 'priority',
            'data', 'template_name', 'is_read', 'is_sent',
            'created_at', 'updated_at', 'read_at', 'sent_at',
            'scheduled_for', 'expires_at', 'time_since_created'
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'updated_at', 'read_at', 'sent_at'
        ]
    
    def get_time_since_created(self, obj):
        """Get human-readable time since creation"""
        from django.utils import timezone
        from django.utils.timesince import timesince
        
        return timesince(obj.created_at, timezone.now())


class NotificationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notifications"""
    
    class Meta:
        model = Notification
        fields = [
            'title', 'message', 'notification_type', 'priority',
            'data', 'template_name', 'scheduled_for', 'expires_at'
        ]


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """Serializer for NotificationTemplate model"""
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'template_type', 'subject_template',
            'content_template', 'variables', 'is_active',
            'created_at', 'updated_at'
        ]


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for NotificationPreference model"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'user', 'user_username', 'delivery_method',
            'is_enabled', 'notification_types', 'quiet_hours_start',
            'quiet_hours_end', 'frequency', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class WebSocketConnectionSerializer(serializers.ModelSerializer):
    """Serializer for WebSocketConnection model"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = WebSocketConnection
        fields = [
            'id', 'user', 'user_username', 'connection_id',
            'channel_name', 'platform', 'user_agent', 'is_active',
            'connected_at', 'disconnected_at', 'last_activity'
        ]
        read_only_fields = [
            'id', 'user', 'connection_id', 'channel_name',
            'connected_at', 'disconnected_at', 'last_activity'
        ]


class BulkNotificationSerializer(serializers.Serializer):
    """Serializer for bulk notification creation"""
    
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text="List of user IDs to send notifications to"
    )
    title = serializers.CharField(max_length=255)
    message = serializers.CharField()
    notification_type = serializers.CharField(max_length=50, default='info')
    priority = serializers.CharField(max_length=20, default='medium')
