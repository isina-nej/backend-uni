# ==============================================================================
# NOTIFICATION SERVICES FOR REAL-TIME COMMUNICATION (PythonAnywhere Compatible)
# خدمات اعلانات سازگار با PythonAnywhere (بدون channels)
# ==============================================================================

import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

# Import models with error handling
try:
    from .models import (
        Notification, NotificationTemplate, NotificationPreference
    )
except ImportError:
    # Fallback for models that might not exist
    Notification = None
    NotificationTemplate = None
    NotificationPreference = None

logger = logging.getLogger(__name__)
User = get_user_model()


class NotificationService:
    """Simplified notification service for PythonAnywhere deployment"""
    
    def __init__(self):
        self.channel_layer = None  # Disabled for PythonAnywhere
        
    def send_notification(self, user_id: int, message: str, notification_type: str = 'info'):
        """Send a basic notification"""
        try:
            if Notification:
                notification = Notification.objects.create(
                    user_id=user_id,
                    message=message,
                    notification_type=notification_type,
                    created_at=timezone.now()
                )
                logger.info(f"Notification created: {notification.id}")
                return notification
            else:
                logger.warning("Notification model not available")
                return None
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            return None
    
    def send_email_notification(self, user_email: str, subject: str, message: str):
        """Send email notification"""
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
            logger.info(f"Email sent to {user_email}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def send_bulk_notification(self, user_ids: List[int], message: str, notification_type: str = 'info'):
        """Send notification to multiple users"""
        results = []
        for user_id in user_ids:
            result = self.send_notification(user_id, message, notification_type)
            results.append(result)
        return results
    
    def get_user_notifications(self, user_id: int, limit: int = 20):
        """Get notifications for a user"""
        try:
            if Notification:
                notifications = Notification.objects.filter(
                    user_id=user_id
                ).order_by('-created_at')[:limit]
                return list(notifications.values())
            else:
                return []
        except Exception as e:
            logger.error(f"Error fetching notifications: {e}")
            return []
    
    def mark_as_read(self, notification_id: int):
        """Mark notification as read"""
        try:
            if Notification:
                notification = Notification.objects.get(id=notification_id)
                notification.is_read = True
                notification.read_at = timezone.now()
                notification.save()
                return True
            return False
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            return False


# Create a singleton instance
notification_service = NotificationService()
