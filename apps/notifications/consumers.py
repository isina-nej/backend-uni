# ==============================================================================
# WEBSOCKET CONSUMERS FOR REAL-TIME NOTIFICATIONS
# مصرف‌کننده‌های وب‌سوکت برای اعلانات بلادرنگ
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from asgiref.sync import sync_to_async
from .models import WebSocketConnection, Notification, NotificationPreference

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time notifications"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        # Get user from scope (requires AuthMiddleware)
        self.user = self.scope.get('user', AnonymousUser())
        
        if self.user.is_anonymous:
            # Reject anonymous users
            await self.close(code=4001)
            return
        
        # Create user-specific group
        self.user_group_name = f"user_{self.user.id}"
        self.room_group_name = f"notifications_{self.user.id}"
        
        # Join user's notification group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Accept WebSocket connection
        await self.accept()
        
        # Store connection in database
        await self.store_connection()
        
        # Send initial data
        await self.send_initial_data()
        
        logger.info(f"WebSocket connected for user {self.user.username}")
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Remove from group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        
        # Mark connection as disconnected in database
        await self.remove_connection()
        
        logger.info(f"WebSocket disconnected for user {self.user.username if not self.user.is_anonymous else 'Anonymous'}")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'mark_read':
                await self.handle_mark_read(data)
            elif message_type == 'mark_all_read':
                await self.handle_mark_all_read()
            elif message_type == 'get_unread_count':
                await self.handle_get_unread_count()
            elif message_type == 'get_notifications':
                await self.handle_get_notifications(data)
            elif message_type == 'ping':
                await self.handle_ping()
            else:
                await self.send_error('نوع پیام نامعتبر است')
                
        except json.JSONDecodeError:
            await self.send_error('فرمت JSON نامعتبر است')
        except Exception as e:
            logger.error(f"Error in WebSocket receive: {e}")
            await self.send_error('خطا در پردازش پیام')
    
    async def notification_message(self, event):
        """Handle notification broadcast to this consumer"""
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': event['notification']
        }))
    
    async def unread_count_update(self, event):
        """Handle unread count update"""
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': event['count']
        }))
    
    async def system_message(self, event):
        """Handle system-wide messages"""
        await self.send(text_data=json.dumps({
            'type': 'system_message',
            'data': event['message']
        }))
    
    # Helper methods
    
    async def handle_mark_read(self, data):
        """Mark notification as read"""
        notification_id = data.get('notification_id')
        if notification_id:
            success = await self.mark_notification_read(notification_id)
            if success:
                # Send updated unread count
                count = await self.get_unread_count()
                await self.send(text_data=json.dumps({
                    'type': 'mark_read_response',
                    'success': True,
                    'notification_id': notification_id,
                    'unread_count': count
                }))
            else:
                await self.send_error('خطا در علامت‌گذاری به عنوان خوانده شده')
    
    async def handle_mark_all_read(self):
        """Mark all notifications as read"""
        success = await self.mark_all_notifications_read()
        if success:
            await self.send(text_data=json.dumps({
                'type': 'mark_all_read_response',
                'success': True,
                'unread_count': 0
            }))
    
    async def handle_get_unread_count(self):
        """Get unread notifications count"""
        count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': count
        }))
    
    async def handle_get_notifications(self, data):
        """Get paginated notifications"""
        page = data.get('page', 1)
        page_size = data.get('page_size', 20)
        
        notifications = await self.get_user_notifications(page, page_size)
        await self.send(text_data=json.dumps({
            'type': 'notifications_list',
            'data': notifications
        }))
    
    async def handle_ping(self):
        """Handle ping for connection keep-alive"""
        await self.send(text_data=json.dumps({
            'type': 'pong',
            'timestamp': timezone.now().isoformat()
        }))
    
    async def send_initial_data(self):
        """Send initial data when connection is established"""
        # Send unread count
        count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'unread_count': count,
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'full_name': self.user.get_full_name()
            }
        }))
        
        # Send recent notifications
        recent_notifications = await self.get_user_notifications(1, 5)
        await self.send(text_data=json.dumps({
            'type': 'recent_notifications',
            'data': recent_notifications
        }))
    
    async def send_error(self, message):
        """Send error message to client"""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message
        }))
    
    # Database operations
    
    @database_sync_to_async
    def store_connection(self):
        """Store WebSocket connection in database"""
        try:
            # Get client info
            headers = dict(self.scope.get('headers', []))
            user_agent = headers.get(b'user-agent', b'').decode('utf-8')
            
            # Create or update connection
            connection, created = WebSocketConnection.objects.get_or_create(
                user=self.user,
                connection_id=self.channel_name,
                defaults={
                    'channel_name': self.channel_name,
                    'user_agent': user_agent,
                    'platform': 'web'  # Can be enhanced to detect platform
                }
            )
            
            if not created:
                connection.is_active = True
                connection.last_activity = timezone.now()
                connection.save()
                
            return connection
        except Exception as e:
            logger.error(f"Error storing WebSocket connection: {e}")
            return None
    
    @database_sync_to_async
    def remove_connection(self):
        """Remove WebSocket connection from database"""
        try:
            WebSocketConnection.objects.filter(
                connection_id=self.channel_name
            ).update(
                is_active=False,
                disconnected_at=timezone.now()
            )
        except Exception as e:
            logger.error(f"Error removing WebSocket connection: {e}")
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark specific notification as read"""
        try:
            notification = Notification.objects.get(
                id=notification_id,
                user=self.user
            )
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            return False
    
    @database_sync_to_async
    def mark_all_notifications_read(self):
        """Mark all user notifications as read"""
        try:
            Notification.objects.filter(
                user=self.user,
                is_read=False
            ).update(
                is_read=True,
                read_at=timezone.now()
            )
            return True
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {e}")
            return False
    
    @database_sync_to_async
    def get_unread_count(self):
        """Get unread notifications count"""
        try:
            return Notification.objects.filter(
                user=self.user,
                is_read=False
            ).count()
        except Exception as e:
            logger.error(f"Error getting unread count: {e}")
            return 0
    
    @database_sync_to_async
    def get_user_notifications(self, page=1, page_size=20):
        """Get paginated user notifications"""
        try:
            offset = (page - 1) * page_size
            notifications = Notification.objects.filter(
                user=self.user
            ).order_by('-created_at')[offset:offset + page_size]
            
            return [notification.to_websocket_dict() for notification in notifications]
        except Exception as e:
            logger.error(f"Error getting user notifications: {e}")
            return []


class NotificationBroadcastConsumer(AsyncWebsocketConsumer):
    """Consumer for system-wide notification broadcasts"""
    
    async def connect(self):
        """Handle connection for broadcast notifications"""
        self.user = self.scope.get('user', AnonymousUser())
        
        if self.user.is_anonymous:
            await self.close(code=4001)
            return
        
        # Join global notification group
        self.broadcast_group_name = "global_notifications"
        
        await self.channel_layer.group_add(
            self.broadcast_group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"Broadcast WebSocket connected for user {self.user.username}")
    
    async def disconnect(self, close_code):
        """Handle disconnection"""
        if hasattr(self, 'broadcast_group_name'):
            await self.channel_layer.group_discard(
                self.broadcast_group_name,
                self.channel_name
            )
        
        logger.info(f"Broadcast WebSocket disconnected for user {self.user.username if not self.user.is_anonymous else 'Anonymous'}")
    
    async def receive(self, text_data):
        """Handle incoming messages"""
        # This consumer is mainly for receiving broadcasts
        pass
    
    async def broadcast_message(self, event):
        """Handle broadcast messages"""
        await self.send(text_data=json.dumps({
            'type': 'broadcast',
            'data': event['message']
        }))
    
    async def system_announcement(self, event):
        """Handle system announcements"""
        await self.send(text_data=json.dumps({
            'type': 'system_announcement',
            'data': event['announcement']
        }))


class AdminNotificationConsumer(AsyncWebsocketConsumer):
    """Special consumer for admin real-time monitoring"""
    
    async def connect(self):
        """Handle admin connection"""
        self.user = self.scope.get('user', AnonymousUser())
        
        # Only allow admin users
        if self.user.is_anonymous or not self.user.is_staff:
            await self.close(code=4003)
            return
        
        # Join admin monitoring group
        self.admin_group_name = "admin_monitoring"
        
        await self.channel_layer.group_add(
            self.admin_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send admin dashboard data
        await self.send_admin_stats()
        
        logger.info(f"Admin WebSocket connected for user {self.user.username}")
    
    async def disconnect(self, close_code):
        """Handle admin disconnection"""
        if hasattr(self, 'admin_group_name'):
            await self.channel_layer.group_discard(
                self.admin_group_name,
                self.channel_name
            )
        
        logger.info(f"Admin WebSocket disconnected for user {self.user.username if not self.user.is_anonymous else 'Anonymous'}")
    
    async def receive(self, text_data):
        """Handle admin commands"""
        try:
            data = json.loads(text_data)
            command = data.get('command')
            
            if command == 'get_stats':
                await self.send_admin_stats()
            elif command == 'get_active_connections':
                await self.send_active_connections()
            elif command == 'send_broadcast':
                await self.handle_broadcast(data)
                
        except json.JSONDecodeError:
            await self.send_error('فرمت JSON نامعتبر است')
        except Exception as e:
            logger.error(f"Error in admin WebSocket receive: {e}")
            await self.send_error('خطا در پردازش دستور')
    
    async def admin_stats_update(self, event):
        """Handle admin stats updates"""
        await self.send(text_data=json.dumps({
            'type': 'stats_update',
            'data': event['stats']
        }))
    
    async def new_user_activity(self, event):
        """Handle new user activity notifications"""
        await self.send(text_data=json.dumps({
            'type': 'user_activity',
            'data': event['activity']
        }))
    
    async def send_admin_stats(self):
        """Send admin dashboard statistics"""
        stats = await self.get_admin_stats()
        await self.send(text_data=json.dumps({
            'type': 'admin_stats',
            'data': stats
        }))
    
    async def send_active_connections(self):
        """Send active WebSocket connections"""
        connections = await self.get_active_connections()
        await self.send(text_data=json.dumps({
            'type': 'active_connections',
            'data': connections
        }))
    
    async def handle_broadcast(self, data):
        """Handle admin broadcast message"""
        message = data.get('message')
        if message:
            # Broadcast to all users
            await self.channel_layer.group_send(
                "global_notifications",
                {
                    'type': 'broadcast_message',
                    'message': message
                }
            )
            
            await self.send(text_data=json.dumps({
                'type': 'broadcast_sent',
                'success': True
            }))
    
    async def send_error(self, message):
        """Send error message to admin"""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message
        }))
    
    @database_sync_to_async
    def get_admin_stats(self):
        """Get admin dashboard statistics"""
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            # Get various statistics
            total_users = User.objects.count()
            active_connections = WebSocketConnection.objects.filter(is_active=True).count()
            total_notifications = Notification.objects.count()
            unread_notifications = Notification.objects.filter(is_read=False).count()
            
            return {
                'total_users': total_users,
                'active_connections': active_connections,
                'total_notifications': total_notifications,
                'unread_notifications': unread_notifications,
                'timestamp': timezone.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting admin stats: {e}")
            return {}
    
    @database_sync_to_async
    def get_active_connections(self):
        """Get active WebSocket connections"""
        try:
            connections = WebSocketConnection.objects.filter(
                is_active=True
            ).select_related('user').values(
                'user__username',
                'user__first_name',
                'user__last_name',
                'platform',
                'connected_at',
                'last_activity'
            )
            
            return list(connections)
        except Exception as e:
            logger.error(f"Error getting active connections: {e}")
            return []
