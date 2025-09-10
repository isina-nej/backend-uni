# ==============================================================================
# MOBILE API SERVICES
# سرویس‌های API موبایل
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import json
import logging
from typing import Dict, List, Optional, Any
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q, Count, Avg
from django.contrib.auth import get_user_model

from .models import MobileDevice, MobileSession, PushNotification, OfflineSync, MobileSettings
from apps.notifications.models import Notification
from apps.courses.models import Course
from apps.grades.models import Grade
from apps.announcements.models import Announcement

User = get_user_model()
logger = logging.getLogger(__name__)


class MobileDeviceService:
    """Service for managing mobile devices"""
    
    @staticmethod
    def register_device(user, device_data: Dict) -> MobileDevice:
        """Register or update a mobile device"""
        device_id = device_data.get('device_id')
        
        # Check if device already exists
        device, created = MobileDevice.objects.get_or_create(
            device_id=device_id,
            defaults={
                'user': user,
                'device_name': device_data.get('device_name', ''),
                'device_type': device_data.get('device_type', 'android'),
                'device_model': device_data.get('device_model', ''),
                'os_version': device_data.get('os_version', ''),
                'app_version': device_data.get('app_version', ''),
                'timezone': device_data.get('timezone', 'UTC'),
            }
        )
        
        if not created:
            # Update existing device
            device.user = user
            device.device_name = device_data.get('device_name', device.device_name)
            device.device_type = device_data.get('device_type', device.device_type)
            device.device_model = device_data.get('device_model', device.device_model)
            device.os_version = device_data.get('os_version', device.os_version)
            device.app_version = device_data.get('app_version', device.app_version)
            device.timezone = device_data.get('timezone', device.timezone)
            device.is_active = True
            device.save()
        
        return device
    
    @staticmethod
    def update_push_token(device: MobileDevice, push_token: str, provider: str = 'fcm'):
        """Update push notification token for device"""
        device.push_token = push_token
        device.push_provider = provider
        device.push_enabled = True
        device.save(update_fields=['push_token', 'push_provider', 'push_enabled'])
    
    @staticmethod
    def get_user_devices(user) -> List[MobileDevice]:
        """Get all active devices for a user"""
        return MobileDevice.objects.filter(user=user, is_active=True).order_by('-last_seen')
    
    @staticmethod
    def deactivate_old_devices(user, keep_count: int = 5):
        """Deactivate old devices, keep only the most recent ones"""
        devices = MobileDevice.objects.filter(user=user, is_active=True).order_by('-last_seen')
        
        if devices.count() > keep_count:
            old_devices = devices[keep_count:]
            for device in old_devices:
                device.is_active = False
                device.save(update_fields=['is_active'])


class MobileSessionService:
    """Service for managing mobile app sessions"""
    
    @staticmethod
    def start_session(device: MobileDevice, session_data: Dict) -> MobileSession:
        """Start a new mobile session"""
        # End any existing active sessions for this device
        MobileSession.objects.filter(device=device, is_active=True).update(
            is_active=False,
            session_end=timezone.now()
        )
        
        # Create new session
        session = MobileSession.objects.create(
            device=device,
            network_type=session_data.get('network_type', ''),
            is_active=True
        )
        
        # Update device activity
        device.update_activity()
        
        return session
    
    @staticmethod
    def end_session(session_id: str):
        """End a mobile session"""
        try:
            session = MobileSession.objects.get(id=session_id, is_active=True)
            session.end_session()
            return session
        except MobileSession.DoesNotExist:
            logger.warning(f"Session {session_id} not found or already ended")
            return None
    
    @staticmethod
    def update_session_activity(session_id: str, activity_data: Dict):
        """Update session activity metrics"""
        try:
            session = MobileSession.objects.get(id=session_id, is_active=True)
            
            # Update activity data
            if 'screens_visited' in activity_data:
                session.screens_visited = activity_data['screens_visited']
            
            if 'actions_performed' in activity_data:
                session.actions_performed = activity_data['actions_performed']
            
            if 'api_calls_made' in activity_data:
                session.api_calls_made = activity_data['api_calls_made']
            
            if 'data_usage_bytes' in activity_data:
                session.data_usage_bytes = activity_data['data_usage_bytes']
            
            session.save()
            return session
            
        except MobileSession.DoesNotExist:
            logger.warning(f"Session {session_id} not found")
            return None


class PushNotificationService:
    """Service for managing push notifications"""
    
    @staticmethod
    def send_notification(
        title: str,
        message: str,
        user_ids: List[int] = None,
        device_ids: List[str] = None,
        notification_type: str = 'general',
        action_data: Dict = None
    ) -> PushNotification:
        """Send push notification to specified users/devices"""
        
        notification = PushNotification.objects.create(
            title=title,
            message=message,
            notification_type=notification_type,
            action_data=action_data or {},
            status='scheduled',
            scheduled_for=timezone.now()
        )
        
        # Add target users
        if user_ids:
            notification.target_users.set(User.objects.filter(id__in=user_ids))
        
        # Add target devices
        if device_ids:
            notification.target_devices.set(MobileDevice.objects.filter(id__in=device_ids))
        
        # Queue for sending (this would integrate with actual push service)
        PushNotificationService._queue_notification(notification)
        
        return notification
    
    @staticmethod
    def _queue_notification(notification: PushNotification):
        """Queue notification for sending (placeholder for actual implementation)"""
        # This would integrate with Firebase Cloud Messaging, Apple Push Notification, etc.
        logger.info(f"Queued notification {notification.id} for sending")
        
        # For now, just mark as sent
        notification.status = 'sent'
        notification.sent_at = timezone.now()
        notification.save()
    
    @staticmethod
    def get_user_notifications(user, limit: int = 50) -> List[Dict]:
        """Get recent notifications for a user"""
        notifications = PushNotification.objects.filter(
            Q(target_users=user) | Q(target_devices__user=user)
        ).distinct().order_by('-created_at')[:limit]
        
        return [
            {
                'id': str(notif.id),
                'title': notif.title,
                'message': notif.message,
                'type': notif.notification_type,
                'action_data': notif.action_data,
                'created_at': notif.created_at.isoformat(),
                'read': False  # This would come from a separate read status model
            }
            for notif in notifications
        ]


class OfflineSyncService:
    """Service for managing offline data synchronization"""
    
    @staticmethod
    def initiate_sync(device: MobileDevice, sync_type: str = 'incremental', data_types: List[str] = None) -> OfflineSync:
        """Initiate offline sync for a device"""
        
        if data_types is None:
            data_types = ['courses', 'grades', 'announcements', 'notifications']
        
        sync_record = OfflineSync.objects.create(
            device=device,
            sync_type=sync_type,
            data_types=data_types,
            status='pending'
        )
        
        # Start sync process
        OfflineSyncService._execute_sync(sync_record)
        
        return sync_record
    
    @staticmethod
    def _execute_sync(sync_record: OfflineSync):
        """Execute the actual sync process"""
        sync_record.start_sync()
        
        try:
            user = sync_record.device.user
            sync_data = {}
            
            # Sync courses
            if 'courses' in sync_record.data_types:
                sync_data['courses'] = OfflineSyncService._get_user_courses(user)
            
            # Sync grades
            if 'grades' in sync_record.data_types:
                sync_data['grades'] = OfflineSyncService._get_user_grades(user)
            
            # Sync announcements
            if 'announcements' in sync_record.data_types:
                sync_data['announcements'] = OfflineSyncService._get_recent_announcements()
            
            # Sync notifications
            if 'notifications' in sync_record.data_types:
                sync_data['notifications'] = PushNotificationService.get_user_notifications(user)
            
            # Calculate data size
            sync_record.data_size_bytes = len(json.dumps(sync_data).encode('utf-8'))
            sync_record.total_items = sum(len(data) if isinstance(data, list) else 1 for data in sync_data.values())
            sync_record.synced_items = sync_record.total_items
            
            # Complete sync
            sync_record.complete_sync()
            
            # Cache sync data for the device
            cache_key = f"sync_data_{sync_record.device.id}"
            cache.set(cache_key, sync_data, timeout=3600)  # 1 hour
            
        except Exception as e:
            sync_record.fail_sync(str(e))
            logger.error(f"Sync failed for device {sync_record.device.id}: {e}")
    
    @staticmethod
    def _get_user_courses(user) -> List[Dict]:
        """Get courses for user"""
        if user.user_type == 'student':
            courses = user.enrolled_courses.all()
            return [
                {
                    'id': course.id,
                    'name': course.title,
                    'code': course.code,
                    'description': course.description,
                    'instructor': course.professor.get_full_name() if course.professor else None
                }
                for course in courses
            ]
        elif user.user_type == 'faculty':
            courses = Course.objects.filter(professor=user)
            return [
                {
                    'id': course.id,
                    'name': course.title,
                    'code': course.code,
                    'description': course.description,
                    'enrolled_count': course.students.count()
                }
                for course in courses
            ]
        return []
    
    @staticmethod
    def _get_user_grades(user) -> List[Dict]:
        """Get grades for user"""
        if user.user_type == 'student':
            grades = Grade.objects.filter(student=user).select_related('course')
            return [
                {
                    'id': grade.id,
                    'course_name': grade.course.title,
                    'grade': grade.grade,
                    'points': grade.points,
                    'date_recorded': grade.date_recorded.isoformat() if grade.date_recorded else None
                }
                for grade in grades
            ]
        return []
    
    @staticmethod
    def _get_recent_announcements() -> List[Dict]:
        """Get recent announcements"""
        announcements = Announcement.objects.filter(
            is_active=True,
            published_date__lte=timezone.now()
        ).order_by('-published_date')[:20]
        
        return [
            {
                'id': announcement.id,
                'title': announcement.title,
                'content': announcement.content,
                'published_date': announcement.published_date.isoformat(),
                'priority': announcement.priority
            }
            for announcement in announcements
        ]
    
    @staticmethod
    def get_sync_data(device: MobileDevice) -> Optional[Dict]:
        """Get cached sync data for device"""
        cache_key = f"sync_data_{device.id}"
        return cache.get(cache_key)


class MobileSettingsService:
    """Service for managing mobile app settings"""
    
    @staticmethod
    def get_or_create_settings(user) -> MobileSettings:
        """Get or create mobile settings for user"""
        settings, created = MobileSettings.objects.get_or_create(user=user)
        return settings
    
    @staticmethod
    def update_settings(user, settings_data: Dict) -> MobileSettings:
        """Update mobile settings for user"""
        settings = MobileSettingsService.get_or_create_settings(user)
        
        # Update fields from settings_data
        for field, value in settings_data.items():
            if hasattr(settings, field):
                setattr(settings, field, value)
        
        settings.save()
        return settings
    
    @staticmethod
    def get_settings_dict(user) -> Dict:
        """Get mobile settings as dictionary"""
        settings = MobileSettingsService.get_or_create_settings(user)
        
        return {
            'theme': settings.theme,
            'language': settings.language,
            'font_size': settings.font_size,
            'push_notifications': settings.push_notifications,
            'email_notifications': settings.email_notifications,
            'notification_sound': settings.notification_sound,
            'notification_vibration': settings.notification_vibration,
            'auto_sync': settings.auto_sync,
            'sync_on_wifi_only': settings.sync_on_wifi_only,
            'offline_storage_limit_mb': settings.offline_storage_limit_mb,
            'location_tracking': settings.location_tracking,
            'analytics_enabled': settings.analytics_enabled,
            'crash_reporting': settings.crash_reporting,
            'image_quality': settings.image_quality,
            'animation_enabled': settings.animation_enabled,
            'data_saver_mode': settings.data_saver_mode,
            'custom_settings': settings.custom_settings
        }


# Service instances
mobile_device_service = MobileDeviceService()
mobile_session_service = MobileSessionService()
push_notification_service = PushNotificationService()
offline_sync_service = OfflineSyncService()
mobile_settings_service = MobileSettingsService()
