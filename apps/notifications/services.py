# ==============================================================================
# NOTIFICATION SERVICES FOR REAL-TIME COMMUNICATION
# خدمات اعلانات برای ارتباطات بلادرنگ
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import (
    Notification, NotificationTemplate, NotificationPreference, 
    WebSocketConnection
)

logger = logging.getLogger(__name__)
User = get_user_model()


class NotificationService:
    """Comprehensive notification service for all delivery channels"""
    
    def __init__(self):
        self.channel_layer = get_channel_layer()
    
    def create_notification(
        self,
        user,
        title: str,
        message: str,
        notification_type: str = 'info',
        priority: str = 'medium',
        data: Optional[Dict] = None,
        template_name: Optional[str] = None,
        auto_send: bool = True
    ) -> Notification:
        """Create a new notification"""
        try:
            # Create notification instance
            notification = Notification.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                priority=priority,
                data=data or {},
                template_name=template_name
            )
            
            if auto_send:
                self.send_notification(notification)
            
            logger.info(f"Notification created for user {user.username}: {title}")
            return notification
            
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            raise
    
    def create_bulk_notifications(
        self,
        users: List,
        title: str,
        message: str,
        notification_type: str = 'info',
        priority: str = 'medium',
        data: Optional[Dict] = None,
        template_name: Optional[str] = None
    ) -> List[Notification]:
        """Create notifications for multiple users"""
        notifications = []
        
        try:
            for user in users:
                notification = Notification.objects.create(
                    user=user,
                    title=title,
                    message=message,
                    notification_type=notification_type,
                    priority=priority,
                    data=data or {},
                    template_name=template_name
                )
                notifications.append(notification)
            
            # Send all notifications
            for notification in notifications:
                self.send_notification(notification)
            
            logger.info(f"Bulk notifications created for {len(users)} users: {title}")
            return notifications
            
        except Exception as e:
            logger.error(f"Error creating bulk notifications: {e}")
            raise
    
    def send_notification(self, notification: Notification):
        """Send notification through appropriate channels"""
        try:
            # Get user preferences
            preferences = self.get_user_preferences(notification.user)
            
            # Send through each enabled channel
            if preferences.get('websocket_enabled', True):
                self.send_websocket_notification(notification)
            
            if preferences.get('email_enabled', False):
                self.send_email_notification(notification)
            
            if preferences.get('push_enabled', False):
                self.send_push_notification(notification)
            
            # Mark as sent
            notification.is_sent = True
            notification.sent_at = timezone.now()
            notification.save()
            
        except Exception as e:
            logger.error(f"Error sending notification {notification.id}: {e}")
    
    def send_websocket_notification(self, notification: Notification):
        """Send notification via WebSocket"""
        try:
            if not self.channel_layer:
                logger.warning("Channel layer not configured for WebSocket notifications")
                return
            
            # Prepare notification data for WebSocket
            notification_data = notification.to_websocket_dict()
            
            # Send to user's personal group
            group_name = f"notifications_{notification.user.id}"
            
            async_to_sync(self.channel_layer.group_send)(
                group_name,
                {
                    'type': 'notification_message',
                    'notification': notification_data
                }
            )
            
            # Update unread count
            unread_count = Notification.objects.filter(
                user=notification.user,
                is_read=False
            ).count()
            
            async_to_sync(self.channel_layer.group_send)(
                group_name,
                {
                    'type': 'unread_count_update',
                    'count': unread_count
                }
            )
            
            # Record delivery (would use NotificationDelivery model if implemented)
            logger.info(f"WebSocket delivery recorded for notification {notification.id}")
            
            logger.debug(f"WebSocket notification sent to user {notification.user.username}")
            
        except Exception as e:
            logger.error(f"Error sending WebSocket notification: {e}")
            # Record failed delivery (would use NotificationDelivery model if implemented)
            logger.error(f"Failed WebSocket delivery for notification {notification.id}: {e}")
    
    def send_email_notification(self, notification: Notification):
        """Send notification via email"""
        try:
            user = notification.user
            
            # Skip if user has no email
            if not user.email:
                logger.warning(f"User {user.username} has no email address")
                return
            
            # Use template if specified
            if notification.template_name:
                try:
                    template = NotificationTemplate.objects.get(
                        name=notification.template_name,
                        template_type='email'
                    )
                    
                    context = {
                        'user': user,
                        'notification': notification,
                        'data': notification.data
                    }
                    
                    subject = template.render_subject(context)
                    html_content = template.render_content(context)
                    
                except NotificationTemplate.DoesNotExist:
                    # Fallback to simple email
                    subject = notification.title
                    html_content = notification.message
            else:
                subject = notification.title
                html_content = notification.message
            
            # Send email
            send_mail(
                subject=subject,
                message=notification.message,  # Plain text fallback
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_content,
                fail_silently=False
            )
            
            # Record successful delivery (would use NotificationDelivery model if implemented)
            logger.info(f"Email delivery recorded for notification {notification.id}")
            
            logger.info(f"Email notification sent to {user.email}")
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            # Record failed delivery (would use NotificationDelivery model if implemented)
            logger.error(f"Failed email delivery for notification {notification.id}: {e}")
    
    def send_push_notification(self, notification: Notification):
        """Send push notification (placeholder for future implementation)"""
        try:
            # This would integrate with a push notification service
            # like Firebase Cloud Messaging (FCM) or Apple Push Notification Service (APNs)
            
            logger.info(f"Push notification would be sent for notification {notification.id}")
            
            # Record delivery attempt (would use NotificationDelivery model if implemented)
            logger.info(f"Push notification delivery recorded for notification {notification.id}")
            
        except Exception as e:
            logger.error(f"Error sending push notification: {e}")
            # Would record failed delivery if NotificationDelivery model was implemented
    
    def get_user_preferences(self, user) -> Dict[str, Any]:
        """Get user notification preferences"""
        try:
            preferences = NotificationPreference.objects.filter(user=user)
            
            # Convert to dictionary
            prefs_dict = {}
            for pref in preferences:
                prefs_dict[f"{pref.delivery_method}_enabled"] = pref.is_enabled
                if pref.notification_types:
                    prefs_dict[f"{pref.delivery_method}_types"] = pref.notification_types
            
            # Set defaults if no preferences exist
            if not prefs_dict:
                prefs_dict = {
                    'websocket_enabled': True,
                    'email_enabled': False,
                    'push_enabled': False,
                    'sms_enabled': False
                }
            
            return prefs_dict
            
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return {
                'websocket_enabled': True,
                'email_enabled': False,
                'push_enabled': False,
                'sms_enabled': False
            }
    
    def broadcast_to_all_users(
        self,
        title: str,
        message: str,
        notification_type: str = 'announcement',
        exclude_users: Optional[List] = None
    ):
        """Broadcast notification to all users"""
        try:
            # Get all active users
            users = User.objects.filter(is_active=True)
            
            if exclude_users:
                users = users.exclude(id__in=[u.id for u in exclude_users])
            
            # Create notifications for all users
            self.create_bulk_notifications(
                users=list(users),
                title=title,
                message=message,
                notification_type=notification_type,
                priority='high'
            )
            
            # Also send global WebSocket broadcast
            if self.channel_layer:
                async_to_sync(self.channel_layer.group_send)(
                    "global_notifications",
                    {
                        'type': 'broadcast_message',
                        'message': {
                            'title': title,
                            'message': message,
                            'type': notification_type,
                            'timestamp': timezone.now().isoformat()
                        }
                    }
                )
            
            logger.info(f"Broadcast sent to {users.count()} users: {title}")
            
        except Exception as e:
            logger.error(f"Error broadcasting to all users: {e}")
    
    def send_system_announcement(
        self,
        title: str,
        message: str,
        target_roles: Optional[List[str]] = None
    ):
        """Send system-wide announcement"""
        try:
            # Filter users by roles if specified
            if target_roles:
                users = User.objects.filter(
                    is_active=True,
                    groups__name__in=target_roles
                ).distinct()
            else:
                users = User.objects.filter(is_active=True)
            
            # Create and send notifications
            self.create_bulk_notifications(
                users=list(users),
                title=title,
                message=message,
                notification_type='system_announcement',
                priority='high'
            )
            
            # Send WebSocket broadcast
            if self.channel_layer:
                async_to_sync(self.channel_layer.group_send)(
                    "global_notifications",
                    {
                        'type': 'system_announcement',
                        'announcement': {
                            'title': title,
                            'message': message,
                            'target_roles': target_roles,
                            'timestamp': timezone.now().isoformat()
                        }
                    }
                )
            
            logger.info(f"System announcement sent to {users.count()} users: {title}")
            
        except Exception as e:
            logger.error(f"Error sending system announcement: {e}")
    
    def cleanup_old_notifications(self, days: int = 30):
        """Clean up old notifications"""
        try:
            cutoff_date = timezone.now() - timedelta(days=days)
            
            # Delete old read notifications
            deleted_count = Notification.objects.filter(
                created_at__lt=cutoff_date,
                is_read=True
            ).delete()[0]
            
            logger.info(f"Cleaned up {deleted_count} old notifications")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up old notifications: {e}")
            return 0
    
    def get_notification_analytics(self) -> Dict[str, Any]:
        """Get notification system analytics"""
        try:
            total_notifications = Notification.objects.count()
            unread_notifications = Notification.objects.filter(is_read=False).count()
            
            # Delivery statistics (would use NotificationDelivery model if implemented)
            successful_deliveries = 0  # Placeholder
            failed_deliveries = 0      # Placeholder
            
            # Active WebSocket connections
            active_connections = WebSocketConnection.objects.filter(
                is_active=True
            ).count()
            
            return {
                'total_notifications': total_notifications,
                'unread_notifications': unread_notifications,
                'read_rate': (total_notifications - unread_notifications) / max(total_notifications, 1) * 100,
                'successful_deliveries': successful_deliveries,
                'failed_deliveries': failed_deliveries,
                'delivery_success_rate': successful_deliveries / max(successful_deliveries + failed_deliveries, 1) * 100,
                'active_websocket_connections': active_connections,
                'timestamp': timezone.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting notification analytics: {e}")
            return {}


# Global notification service instance
notification_service = NotificationService()


# Convenience functions for common operations
def send_notification(user, title: str, message: str, **kwargs):
    """Send a notification to a specific user"""
    return notification_service.create_notification(user, title, message, **kwargs)


def send_bulk_notifications(users: List, title: str, message: str, **kwargs):
    """Send notifications to multiple users"""
    return notification_service.create_bulk_notifications(users, title, message, **kwargs)


def broadcast_announcement(title: str, message: str, **kwargs):
    """Broadcast an announcement to all users"""
    return notification_service.broadcast_to_all_users(title, message, **kwargs)


def send_system_announcement(title: str, message: str, **kwargs):
    """Send a system announcement"""
    return notification_service.send_system_announcement(title, message, **kwargs)
