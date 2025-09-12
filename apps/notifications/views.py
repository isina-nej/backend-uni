# ==============================================================================
# NOTIFICATION API VIEWS WITH WEBSOCKET INTEGRATION
# نماهای API اعلانات با یکپارچگی وب‌سوکت
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import (
    Notification, NotificationTemplate, NotificationPreference, 
    WebSocketConnection
)
from .serializers import (
    NotificationSerializer, NotificationTemplateSerializer,
    NotificationPreferenceSerializer, WebSocketConnectionSerializer,
    NotificationCreateSerializer, BulkNotificationSerializer
)
from .services import notification_service
import logging

logger = logging.getLogger(__name__)


class NotificationPagination(PageNumberPagination):
    """Custom pagination for notifications"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user notifications"""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NotificationPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'priority', 'is_read', 'is_sent']
    
    def get_queryset(self):
        """Get notifications for the authenticated user"""
        return Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return NotificationCreateSerializer
        elif self.action == 'bulk_create':
            return BulkNotificationSerializer
        return NotificationSerializer
    
    def perform_create(self, serializer):
        """Set user when creating notification"""
        serializer.save(user=self.request.user)
    
    @extend_schema(
        summary="Mark notification as read",
        description="Mark a specific notification as read and update unread count"
    )
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a notification as read"""
        try:
            notification = self.get_object()
            notification.mark_as_read()
            
            # Get updated unread count
            unread_count = Notification.objects.filter(
                user=request.user,
                is_read=False
            ).count()
            
            return Response({
                'success': True,
                'message': 'Notification marked as read',
                'unread_count': unread_count
            })
            
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            return Response({
                'success': False,
                'error': 'Failed to mark notification as read'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Mark all notifications as read",
        description="Mark all user notifications as read"
    )
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read for the user"""
        try:
            updated_count = Notification.objects.filter(
                user=request.user,
                is_read=False
            ).update(
                is_read=True,
                read_at=timezone.now()
            )
            
            return Response({
                'success': True,
                'message': f'{updated_count} notifications marked as read',
                'unread_count': 0
            })
            
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {e}")
            return Response({
                'success': False,
                'error': 'Failed to mark all notifications as read'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Get unread notifications count",
        description="Get the count of unread notifications for the user"
    )
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get unread notifications count"""
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        return Response({'unread_count': count})
    
    @extend_schema(
        summary="Get notification statistics",
        description="Get comprehensive notification statistics for the user"
    )
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get notification statistics for the user"""
        try:
            stats = Notification.objects.filter(user=request.user).aggregate(
                total=Count('id'),
                unread=Count('id', filter=Q(is_read=False)),
                by_type=Count('notification_type'),
                by_priority=Count('priority')
            )
            
            # Get breakdown by type
            type_breakdown = Notification.objects.filter(
                user=request.user
            ).values('notification_type').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Get breakdown by priority
            priority_breakdown = Notification.objects.filter(
                user=request.user
            ).values('priority').annotate(
                count=Count('id')
            ).order_by('-count')
            
            return Response({
                'total_notifications': stats['total'],
                'unread_notifications': stats['unread'],
                'read_notifications': stats['total'] - stats['unread'],
                'read_rate': (stats['total'] - stats['unread']) / max(stats['total'], 1) * 100,
                'type_breakdown': list(type_breakdown),
                'priority_breakdown': list(priority_breakdown)
            })
            
        except Exception as e:
            logger.error(f"Error getting notification stats: {e}")
            return Response({
                'error': 'Failed to get notification statistics'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Delete old notifications",
        description="Delete old read notifications (older than specified days)",
        parameters=[
            OpenApiParameter(
                name='days',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Number of days (default: 30)'
            )
        ]
    )
    @action(detail=False, methods=['delete'])
    def cleanup(self, request):
        """Delete old read notifications"""
        try:
            days = int(request.query_params.get('days', 30))
            cutoff_date = timezone.now() - timezone.timedelta(days=days)
            
            deleted_count = Notification.objects.filter(
                user=request.user,
                is_read=True,
                created_at__lt=cutoff_date
            ).delete()[0]
            
            return Response({
                'success': True,
                'message': f'Deleted {deleted_count} old notifications',
                'deleted_count': deleted_count
            })
            
        except Exception as e:
            logger.error(f"Error cleaning up notifications: {e}")
            return Response({
                'success': False,
                'error': 'Failed to clean up old notifications'
            }, status=status.HTTP_400_BAD_REQUEST)


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing notification preferences"""
    
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get preferences for the authenticated user"""
        return NotificationPreference.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set user when creating preference"""
        serializer.save(user=self.request.user)


class NotificationTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing notification templates (read-only for regular users)"""
    
    serializer_class = NotificationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get active notification templates"""
        return NotificationTemplate.objects.filter(is_active=True)


class WebSocketConnectionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing WebSocket connections (read-only)"""
    
    serializer_class = WebSocketConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get connections for the authenticated user"""
        return WebSocketConnection.objects.filter(user=self.request.user)


class AdminNotificationViewSet(viewsets.ModelViewSet):
    """Admin-only ViewSet for managing all notifications"""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = NotificationPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'type', 'priority', 'is_read', 'is_sent']
    
    def get_queryset(self):
        """Get all notifications for admin"""
        return Notification.objects.all().order_by('-created_at')
    
    @extend_schema(
        summary="Broadcast notification to all users",
        description="Send a notification to all active users"
    )
    @action(detail=False, methods=['post'])
    def broadcast(self, request):
        """Broadcast notification to all users"""
        try:
            title = request.data.get('title')
            message = request.data.get('message')
            notification_type = request.data.get('notification_type', 'announcement')
            
            if not title or not message:
                return Response({
                    'error': 'Title and message are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Use notification service to broadcast
            notification_service.broadcast_to_all_users(
                title=title,
                message=message,
                notification_type=notification_type
            )
            
            return Response({
                'success': True,
                'message': 'Broadcast sent successfully'
            })
            
        except Exception as e:
            logger.error(f"Error broadcasting notification: {e}")
            return Response({
                'success': False,
                'error': 'Failed to broadcast notification'
            }, status=status.HTTP_400_BAD_REQUEST)
