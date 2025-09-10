# ==============================================================================
# REAL-TIME NOTIFICATION MANAGEMENT COMMANDS
# دستورات مدیریت اعلانات بلادرنگ
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.notifications.services import notification_service
from apps.notifications.models import Notification, WebSocketConnection
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    """Management command for testing notification system"""
    
    help = 'Test and manage the real-time notification system'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['test', 'broadcast', 'cleanup', 'stats', 'connections'],
            default='test',
            help='Action to perform'
        )
        
        parser.add_argument(
            '--user',
            type=str,
            help='Username for single user test'
        )
        
        parser.add_argument(
            '--title',
            type=str,
            default='Test Notification',
            help='Notification title'
        )
        
        parser.add_argument(
            '--message',
            type=str,
            default='This is a test notification from the management command.',
            help='Notification message'
        )
        
        parser.add_argument(
            '--type',
            type=str,
            default='info',
            help='Notification type'
        )
        
        parser.add_argument(
            '--priority',
            type=str,
            default='medium',
            help='Notification priority'
        )
        
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Days for cleanup operation'
        )
    
    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'test':
            self.test_notifications(options)
        elif action == 'broadcast':
            self.test_broadcast(options)
        elif action == 'cleanup':
            self.cleanup_notifications(options)
        elif action == 'stats':
            self.show_stats()
        elif action == 'connections':
            self.show_connections()
    
    def test_notifications(self, options):
        """Test sending notifications to specific user or all users"""
        title = options['title']
        message = options['message']
        notification_type = options['type']
        priority = options['priority']
        username = options.get('user')
        
        try:
            if username:
                # Send to specific user
                try:
                    user = User.objects.get(username=username)
                    notification = notification_service.create_notification(
                        user=user,
                        title=title,
                        message=message,
                        notification_type=notification_type,
                        priority=priority
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully sent notification to {username}: {notification.id}'
                        )
                    )
                
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'User {username} not found')
                    )
            else:
                # Broadcast to all users
                notification_service.broadcast_to_all_users(
                    title=title,
                    message=message,
                    notification_type=notification_type
                )
                
                user_count = User.objects.filter(is_active=True).count()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully broadcast notification to {user_count} users'
                    )
                )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending notification: {e}')
            )
    
    def test_broadcast(self, options):
        """Test system-wide broadcast"""
        title = options['title']
        message = options['message']
        
        try:
            notification_service.send_system_announcement(
                title=title,
                message=message
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully sent system announcement: {title}'
                )
            )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending system announcement: {e}')
            )
    
    def cleanup_notifications(self, options):
        """Clean up old notifications"""
        days = options['days']
        
        try:
            deleted_count = notification_service.cleanup_old_notifications(days)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully cleaned up {deleted_count} old notifications'
                )
            )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error cleaning up notifications: {e}')
            )
    
    def show_stats(self):
        """Show notification system statistics"""
        try:
            analytics = notification_service.get_notification_analytics()
            
            self.stdout.write(self.style.SUCCESS('=== Notification System Statistics ==='))
            self.stdout.write(f"Total notifications: {analytics.get('total_notifications', 0)}")
            self.stdout.write(f"Unread notifications: {analytics.get('unread_notifications', 0)}")
            self.stdout.write(f"Read rate: {analytics.get('read_rate', 0):.2f}%")
            self.stdout.write(f"Active WebSocket connections: {analytics.get('active_websocket_connections', 0)}")
            self.stdout.write(f"Successful deliveries: {analytics.get('successful_deliveries', 0)}")
            self.stdout.write(f"Failed deliveries: {analytics.get('failed_deliveries', 0)}")
            self.stdout.write(f"Delivery success rate: {analytics.get('delivery_success_rate', 0):.2f}%")
            
            # Additional statistics
            total_users = User.objects.filter(is_active=True).count()
            recent_notifications = Notification.objects.filter(
                created_at__gte=timezone.now() - timezone.timedelta(days=7)
            ).count()
            
            self.stdout.write(f"Total active users: {total_users}")
            self.stdout.write(f"Notifications in last 7 days: {recent_notifications}")
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error getting statistics: {e}')
            )
    
    def show_connections(self):
        """Show active WebSocket connections"""
        try:
            connections = WebSocketConnection.objects.filter(
                is_active=True
            ).select_related('user')
            
            self.stdout.write(self.style.SUCCESS('=== Active WebSocket Connections ==='))
            
            if not connections:
                self.stdout.write('No active connections found.')
                return
            
            for conn in connections:
                duration = timezone.now() - conn.connected_at
                self.stdout.write(
                    f"User: {conn.user.username} | "
                    f"Platform: {conn.platform} | "
                    f"Connected: {duration.total_seconds():.0f}s ago | "
                    f"Channel: {conn.channel_name[:20]}..."
                )
            
            self.stdout.write(f"\nTotal active connections: {connections.count()}")
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error getting connections: {e}')
            )
