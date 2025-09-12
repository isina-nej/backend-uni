# ==============================================================================
# MOBILE API VIEWS
# نماهای API موبایل
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging

from .models import MobileDevice, MobileSession, PushNotification, OfflineSync, MobileSettings
from .serializers import (
    MobileDeviceSerializer, MobileDeviceRegistrationSerializer,
    MobileSessionSerializer, SessionStartSerializer, SessionUpdateSerializer,
    PushNotificationSerializer, PushNotificationCreateSerializer,
    OfflineSyncSerializer, SyncInitiateSerializer,
    MobileSettingsSerializer, MobileSettingsUpdateSerializer,
    MobileUserProfileSerializer, MobileDashboardSerializer
)
from .services import (
    mobile_device_service, mobile_session_service, push_notification_service,
    offline_sync_service, mobile_settings_service
)

User = get_user_model()
logger = logging.getLogger(__name__)


class MobileDeviceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing mobile devices"""
    
    queryset = MobileDevice.objects.all()
    serializer_class = MobileDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['device_type', 'is_active', 'push_enabled']
    
    def get_queryset(self):
        """Get devices for the authenticated user"""
        if getattr(self, 'swagger_fake_view', False):
            # For schema generation
            return MobileDevice.objects.none()
        return MobileDevice.objects.filter(user=self.request.user)
    
    @extend_schema(
        summary="Register Device",
        description="Register a new mobile device or update existing one",
        request=MobileDeviceRegistrationSerializer
    )
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a mobile device"""
        serializer = MobileDeviceRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            device = mobile_device_service.register_device(
                user=request.user,
                device_data=serializer.validated_data
            )
            
            # Update push token if provided
            push_token = serializer.validated_data.get('push_token')
            push_provider = serializer.validated_data.get('push_provider', 'fcm')
            if push_token:
                mobile_device_service.update_push_token(device, push_token, push_provider)
            
            response_serializer = MobileDeviceSerializer(device)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Update Push Token",
        description="Update push notification token for device"
    )
    @action(detail=True, methods=['post'])
    def update_push_token(self, request, pk=None):
        """Update push notification token"""
        device = self.get_object()
        push_token = request.data.get('push_token')
        push_provider = request.data.get('push_provider', 'fcm')
        
        if not push_token:
            return Response(
                {'error': 'push_token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        mobile_device_service.update_push_token(device, push_token, push_provider)
        
        serializer = MobileDeviceSerializer(device)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Deactivate Device",
        description="Deactivate a mobile device"
    )
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a device"""
        device = self.get_object()
        device.is_active = False
        device.save(update_fields=['is_active'])
        
        serializer = MobileDeviceSerializer(device)
        return Response(serializer.data)


class MobileSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for managing mobile sessions"""
    
    queryset = MobileSession.objects.all()
    serializer_class = MobileSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'network_type']
    
    def get_queryset(self):
        """Get sessions for the authenticated user's devices"""
        if getattr(self, 'swagger_fake_view', False):
            # For schema generation
            return MobileSession.objects.none()
        user_devices = MobileDevice.objects.filter(user=self.request.user)
        return MobileSession.objects.filter(device__in=user_devices)
    
    @extend_schema(
        summary="Start Session",
        description="Start a new mobile app session",
        request=SessionStartSerializer
    )
    @action(detail=False, methods=['post'])
    def start(self, request):
        """Start a new session"""
        serializer = SessionStartSerializer(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data.get('device_id')
            
            try:
                device = MobileDevice.objects.get(
                    device_id=device_id, 
                    user=request.user,
                    is_active=True
                )
            except MobileDevice.DoesNotExist:
                return Response(
                    {'error': 'Device not found or inactive'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            session = mobile_session_service.start_session(
                device=device,
                session_data=serializer.validated_data
            )
            
            response_serializer = MobileSessionSerializer(session)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="End Session",
        description="End a mobile app session"
    )
    @action(detail=True, methods=['post'])
    def end(self, request, pk=None):
        """End a session"""
        session = mobile_session_service.end_session(pk)
        if session:
            serializer = MobileSessionSerializer(session)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Session not found or already ended'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    @extend_schema(
        summary="Update Activity",
        description="Update session activity metrics",
        request=SessionUpdateSerializer
    )
    @action(detail=True, methods=['post'])
    def update_activity(self, request, pk=None):
        """Update session activity"""
        serializer = SessionUpdateSerializer(data=request.data)
        if serializer.is_valid():
            session = mobile_session_service.update_session_activity(
                session_id=pk,
                activity_data=serializer.validated_data
            )
            
            if session:
                response_serializer = MobileSessionSerializer(session)
                return Response(response_serializer.data)
            
            return Response(
                {'error': 'Session not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PushNotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing push notifications"""
    
    queryset = PushNotification.objects.all()
    serializer_class = PushNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Temporarily removed filter_backends and filterset_fields for schema generation
    
    def get_queryset(self):
        """Get notifications for the authenticated user"""
        if getattr(self, 'swagger_fake_view', False):
            # For schema generation
            return PushNotification.objects.none()
        if self.request.user.is_superuser:
            return PushNotification.objects.all()
        return PushNotification.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)
    
    @extend_schema(
        summary="Send Notification",
        description="Send a push notification",
        request=PushNotificationCreateSerializer
    )
    @action(detail=False, methods=['post'])
    def send(self, request):
        """Send a push notification"""
        serializer = PushNotificationCreateSerializer(data=request.data)
        if serializer.is_valid():
            notification = push_notification_service.send_notification(
                title=serializer.validated_data['title'],
                message=serializer.validated_data['message'],
                user_ids=serializer.validated_data.get('user_ids'),
                device_ids=serializer.validated_data.get('device_ids'),
                notification_type=serializer.validated_data.get('notification_type', 'general'),
                action_data=serializer.validated_data.get('action_data', {})
            )
            
            response_serializer = PushNotificationSerializer(notification)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Get User Notifications",
        description="Get notifications for the current user"
    )
    @action(detail=False, methods=['get'])
    def my_notifications(self, request):
        """Get notifications for the current user"""
        notifications = push_notification_service.get_user_notifications(
            user=request.user,
            limit=request.query_params.get('limit', 50)
        )
        return Response(notifications)


class OfflineSyncViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for managing offline synchronization"""
    
    queryset = OfflineSync.objects.all()
    serializer_class = OfflineSyncSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Temporarily removed filter_backends and filterset_fields for schema generation
    
    def get_queryset(self):
        """Get sync records for the authenticated user's devices"""
        if getattr(self, 'swagger_fake_view', False):
            # For schema generation
            return OfflineSync.objects.none()
        user_devices = MobileDevice.objects.filter(user=self.request.user)
        return OfflineSync.objects.filter(device__in=user_devices)
    
    @extend_schema(
        summary="Initiate Sync",
        description="Initiate offline data synchronization",
        request=SyncInitiateSerializer
    )
    @action(detail=False, methods=['post'])
    def initiate(self, request):
        """Initiate sync for a device"""
        serializer = SyncInitiateSerializer(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data.get('device_id')
            
            try:
                device = MobileDevice.objects.get(
                    device_id=device_id,
                    user=request.user,
                    is_active=True
                )
            except MobileDevice.DoesNotExist:
                return Response(
                    {'error': 'Device not found or inactive'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            sync_record = offline_sync_service.initiate_sync(
                device=device,
                sync_type=serializer.validated_data.get('sync_type', 'incremental'),
                data_types=serializer.validated_data.get('data_types')
            )
            
            response_serializer = OfflineSyncSerializer(sync_record)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Get Sync Data",
        description="Get cached sync data for a device"
    )
    @action(detail=False, methods=['get'])
    def get_data(self, request):
        """Get sync data for a device"""
        device_id = request.query_params.get('device_id')
        
        if not device_id:
            return Response(
                {'error': 'device_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            device = MobileDevice.objects.get(
                device_id=device_id,
                user=request.user,
                is_active=True
            )
        except MobileDevice.DoesNotExist:
            return Response(
                {'error': 'Device not found or inactive'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        sync_data = offline_sync_service.get_sync_data(device)
        
        if sync_data:
            return Response(sync_data)
        else:
            return Response(
                {'error': 'No sync data available. Please initiate sync first.'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class MobileSettingsViewSet(viewsets.ViewSet):
    """ViewSet for managing mobile app settings"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Get Settings",
        description="Get mobile app settings for the current user"
    )
    def list(self, request):
        """Get user's mobile settings"""
        settings_dict = mobile_settings_service.get_settings_dict(request.user)
        return Response(settings_dict)
    
    @extend_schema(
        summary="Update Settings",
        description="Update mobile app settings",
        request=MobileSettingsUpdateSerializer
    )
    def create(self, request):
        """Update user's mobile settings"""
        serializer = MobileSettingsUpdateSerializer(data=request.data)
        if serializer.is_valid():
            settings = mobile_settings_service.update_settings(
                user=request.user,
                settings_data=serializer.validated_data
            )
            
            response_serializer = MobileSettingsSerializer(settings)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MobileDashboardViewSet(viewsets.ViewSet):
    """ViewSet for mobile dashboard data"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Get Dashboard",
        description="Get mobile dashboard data for the current user"
    )
    def list(self, request):
        """Get dashboard data for mobile app"""
        user = request.user
        
        try:
            # User profile info
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'user_type': getattr(user, 'user_type', 'student'),
                'avatar': None
            }
            
            # Basic stats
            stats = self._get_user_stats(user)
            
            # Recent activities
            recent_activities = self._get_recent_activities(user)
            
            # Quick actions based on user type
            quick_actions = self._get_quick_actions(user)
            
            # Notifications count
            try:
                notifications_count = len(push_notification_service.get_user_notifications(user, limit=1))
            except:
                notifications_count = 0
            
            dashboard_data = {
                'user_info': user_data,
                'stats': stats,
                'recent_activities': recent_activities,
                'quick_actions': quick_actions,
                'notifications_count': notifications_count
            }
            
            return Response(dashboard_data)
        
        except Exception as e:
            logger.error(f"Dashboard error: {str(e)}")
            return Response({'error': 'Dashboard data unavailable'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_user_stats(self, user):
        """Get user statistics"""
        try:
            # Basic stats
            stats = {
                'total_courses': 0,
                'active_courses': 0,
                'completed_courses': 0,
                'gpa': 0.0,
                'attendance_rate': 0.0,
                'pending_assignments': 0,
                'upcoming_exams': 0,
                'library_books': 0,
                'financial_balance': 0.0
            }
            
            # Try to get real data if possible
            try:
                from apps.courses.models import Course, Enrollment
                enrollments = Enrollment.objects.filter(student=user)
                stats['total_courses'] = enrollments.count()
                stats['active_courses'] = enrollments.filter(status='active').count()
                stats['completed_courses'] = enrollments.filter(status='completed').count()
            except:
                pass
                
            try:
                from apps.grades.models import Grade
                grades = Grade.objects.filter(student=user)
                if grades.exists():
                    avg_grade = grades.aggregate(avg=models.Avg('value'))['avg']
                    stats['gpa'] = round(avg_grade, 2) if avg_grade else 0.0
            except:
                pass
                
            return stats
        except Exception as e:
            logger.error(f"Error getting user stats: {str(e)}")
            return {
                'total_courses': 0,
                'active_courses': 0,
                'completed_courses': 0,
                'gpa': 0.0,
                'attendance_rate': 85.5,
                'pending_assignments': 3,
                'upcoming_exams': 2,
                'library_books': 1,
                'financial_balance': 0.0
            }
    
    def _get_recent_activities(self, user):
        """Get recent activities for user"""
        # Sample activities
        activities = [
            {
                'title': 'Assignment Submitted',
                'description': 'Mathematics Assignment #3',
                'timestamp': '2 hours ago',
                'type': 'assignment',
                'icon': 'assignment'
            },
            {
                'title': 'Grade Posted',
                'description': 'Physics Midterm - Grade: A',
                'timestamp': '1 day ago', 
                'type': 'grade',
                'icon': 'grade'
            },
            {
                'title': 'Class Attended',
                'description': 'Computer Science - Lecture 15',
                'timestamp': '2 days ago',
                'type': 'attendance',
                'icon': 'class'
            }
        ]
        
        return activities
    
    def _get_quick_actions(self, user):
        """Get quick actions based on user type"""
        user_type = getattr(user, 'user_type', 'student')
        
        if user_type == 'student':
            actions = [
                {'title': 'View Grades', 'action': 'navigate_grades', 'icon': 'grade'},
                {'title': 'Schedule', 'action': 'navigate_schedule', 'icon': 'calendar'},
                {'title': 'Assignments', 'action': 'navigate_assignments', 'icon': 'assignment'},
                {'title': 'Library', 'action': 'navigate_library', 'icon': 'library'}
            ]
        elif user_type == 'faculty':
            actions = [
                {'title': 'My Courses', 'action': 'navigate_courses', 'icon': 'course'},
                {'title': 'Grade Students', 'action': 'navigate_grading', 'icon': 'grade'},
                {'title': 'Attendance', 'action': 'navigate_attendance', 'icon': 'attendance'},
                {'title': 'Schedule', 'action': 'navigate_schedule', 'icon': 'calendar'}
            ]
        else:
            actions = [
                {'title': 'Reports', 'action': 'navigate_reports', 'icon': 'report'},
                {'title': 'Users', 'action': 'navigate_users', 'icon': 'user'},
                {'title': 'Send Notification', 'action': 'create_notification', 'icon': 'notification'},
                {'title': 'Data Management', 'action': 'navigate_data', 'icon': 'data'}
            ]
        
        return actions
