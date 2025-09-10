from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import (
    User, OrganizationalUnit, Position, UserPosition, 
    Permission, UserPermission, AccessLog
)
from .serializers import (
    UserSerializer, UserBasicSerializer, OrganizationalUnitSerializer,
    PositionSerializer, UserPositionSerializer, PermissionSerializer,
    UserPermissionSerializer, AccessLogSerializer
)


class OrganizationalUnitViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای واحدهای سازمانی
    """
    queryset = OrganizationalUnit.objects.filter(is_active=True)
    serializer_class = OrganizationalUnitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['unit_type', 'parent']
    search_fields = ['name', 'code']
    ordering = ['parent', 'order', 'name']
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """دریافت ساختار درختی واحدهای سازمانی"""
        root_units = self.queryset.filter(parent=None)
        serializer = self.get_serializer(root_units, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """دریافت اعضای یک واحد سازمانی"""
        unit = self.get_object()
        members = User.objects.filter(primary_unit=unit)
        serializer = UserBasicSerializer(members, many=True)
        return Response(serializer.data)


class PositionViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای سمت‌های سازمانی
    """
    queryset = Position.objects.filter(is_active=True)
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['organizational_unit', 'position_level', 'authority_level']
    search_fields = ['title', 'job_description']
    ordering = ['organizational_unit', 'title']


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای کاربران با قابلیت‌های پیشرفته
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'primary_unit', 'employment_type', 'academic_rank', 'is_active']
    search_fields = ['username', 'persian_first_name', 'persian_last_name', 
                    'first_name', 'last_name', 'employee_id', 'student_id', 'national_id']
    ordering = ['persian_last_name', 'persian_first_name', 'username']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserBasicSerializer
        return UserSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # سوپر ادمین دسترسی کامل دارد
        if user.is_superuser or user.role == 'super_admin':
            return User.objects.all()
        
        # مدیران دسترسی به واحد خود و زیرمجموعه‌ها دارند
        if user.is_management():
            if user.primary_unit:
                # دریافت واحد کاربر و تمام زیرمجموعه‌ها
                unit_ids = [user.primary_unit.id]
                children = user.primary_unit.children.all()
                for child in children:
                    unit_ids.append(child.id)
                
                return User.objects.filter(
                    Q(primary_unit_id__in=unit_ids) | Q(id=user.id)
                )
        
        # کاربران عادی فقط اطلاعات خود را می‌بینند
        return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """دریافت اطلاعات کاربر فعلی"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assign_position(self, request, pk=None):
        """تخصیص سمت به کاربر"""
        user = self.get_object()
        position_id = request.data.get('position_id')
        start_date = request.data.get('start_date')
        is_primary = request.data.get('is_primary', False)
        
        try:
            position = Position.objects.get(id=position_id)
            user_position = UserPosition.objects.create(
                user=user,
                position=position,
                start_date=start_date,
                is_primary=is_primary
            )
            serializer = UserPositionSerializer(user_position)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Position.DoesNotExist:
            return Response({'error': 'سمت یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def grant_permission(self, request, pk=None):
        """اعطای مجوز به کاربر"""
        user = self.get_object()
        permission_id = request.data.get('permission_id')
        organizational_unit_id = request.data.get('organizational_unit_id')
        expires_at = request.data.get('expires_at')
        
        try:
            permission = Permission.objects.get(id=permission_id)
            organizational_unit = None
            if organizational_unit_id:
                organizational_unit = OrganizationalUnit.objects.get(id=organizational_unit_id)
            
            user_permission = UserPermission.objects.create(
                user=user,
                permission=permission,
                organizational_unit=organizational_unit,
                granted_by=request.user,
                expires_at=expires_at
            )
            serializer = UserPermissionSerializer(user_permission)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Permission.DoesNotExist:
            return Response({'error': 'مجوز یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """آمار کاربران"""
        if not request.user.is_management():
            return Response({'error': 'دسترسی غیرمجاز'}, status=status.HTTP_403_FORBIDDEN)
        
        stats = {
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'students': User.objects.filter(role__in=['student', 'undergraduate', 'graduate', 'phd']).count(),
            'faculty': User.objects.filter(role='faculty').count(),
            'staff': User.objects.filter(role__in=['staff', 'administrative', 'technical']).count(),
            'management': User.objects.filter(role__in=['president', 'vice_president', 'dean', 'manager']).count(),
        }
        
        # آمار بر اساس واحد سازمانی
        unit_stats = {}
        for unit in OrganizationalUnit.objects.filter(is_active=True):
            unit_stats[unit.name] = User.objects.filter(primary_unit=unit).count()
        
        stats['by_unit'] = unit_stats
        return Response(stats)


class UserPositionViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای تخصیص سمت‌ها
    """
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'position', 'is_active', 'is_primary']
    ordering = ['-start_date']


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet برای مجوزها (فقط خواندنی)
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['permission_type', 'module']
    search_fields = ['name', 'codename', 'description']


class UserPermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای مجوزهای کاربران
    """
    queryset = UserPermission.objects.filter(is_active=True)
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'permission', 'organizational_unit']
    ordering = ['-granted_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'super_admin':
            return self.queryset
        
        # مدیران می‌توانند مجوزهای واحد خود را ببینند
        if user.is_management():
            return self.queryset.filter(
                Q(organizational_unit=user.primary_unit) | Q(user=user)
            )
        
        # کاربران عادی فقط مجوزهای خود را می‌بینند
        return self.queryset.filter(user=user)


class AccessLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet برای لاگ دسترسی (فقط خواندنی)
    """
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'action', 'success']
    search_fields = ['user__username', 'action', 'resource']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        user = self.request.user
        
        # فقط ادمین‌ها و بازرسان می‌توانند لاگ‌ها را ببینند
        if user.is_superuser or user.role in ['super_admin', 'auditor']:
            return self.queryset
        
        # کاربران عادی فقط لاگ‌های خود را می‌بینند
        return self.queryset.filter(user=user)
