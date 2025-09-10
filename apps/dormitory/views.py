from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.utils import timezone

from .models import (
    DormitoryComplex, DormitoryBuilding, DormitoryFloor,
    DormitoryRoom, DormitoryAccommodation, DormitoryStaff,
    DormitoryMaintenance
)
from .serializers import (
    DormitoryComplexListSerializer, DormitoryComplexDetailSerializer,
    DormitoryComplexCreateSerializer, DormitoryBuildingListSerializer,
    DormitoryBuildingDetailSerializer, DormitoryRoomListSerializer,
    DormitoryRoomDetailSerializer, DormitoryAccommodationListSerializer,
    DormitoryAccommodationDetailSerializer, DormitoryAccommodationCreateSerializer,
    DormitoryStaffSerializer, DormitoryMaintenanceListSerializer,
    DormitoryMaintenanceDetailSerializer, DormitoryMaintenanceCreateSerializer
)


class DormitoryComplexViewSet(viewsets.ModelViewSet):
    """ViewSet برای مجموعه‌های خوابگاهی"""
    queryset = DormitoryComplex.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'is_active']
    search_fields = ['name', 'name_en', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DormitoryComplexListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DormitoryComplexCreateSerializer
        return DormitoryComplexDetailSerializer
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """آمار مجموعه خوابگاهی"""
        complex_obj = self.get_object()
        
        # محاسبه آمار
        total_buildings = complex_obj.buildings.count()
        total_rooms = sum(building.total_rooms for building in complex_obj.buildings.all())
        total_capacity = sum(building.total_capacity for building in complex_obj.buildings.all())
        
        # محاسبه تعداد ساکنان فعلی
        current_occupancy = 0
        for building in complex_obj.buildings.all():
            for floor in building.floors.all():
                for room in floor.rooms.all():
                    current_occupancy += room.current_occupancy
        
        occupancy_rate = (current_occupancy / total_capacity * 100) if total_capacity > 0 else 0
        
        # آمار اتاق‌ها بر اساس وضعیت
        room_status_stats = {}
        for building in complex_obj.buildings.all():
            for floor in building.floors.all():
                for room in floor.rooms.all():
                    status_key = room.get_status_display()
                    room_status_stats[status_key] = room_status_stats.get(status_key, 0) + 1
        
        # آمار تعمیرات
        maintenance_stats = DormitoryMaintenance.objects.filter(
            room__floor__building__complex=complex_obj
        ).values('status').annotate(count=Count('id'))
        
        data = {
            'total_buildings': total_buildings,
            'total_rooms': total_rooms,
            'total_capacity': total_capacity,
            'current_occupancy': current_occupancy,
            'occupancy_rate': round(occupancy_rate, 2),
            'available_beds': total_capacity - current_occupancy,
            'room_status_distribution': room_status_stats,
            'maintenance_requests': {item['status']: item['count'] for item in maintenance_stats}
        }
        
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def available_rooms(self, request, pk=None):
        """اتاق‌های در دسترس"""
        complex_obj = self.get_object()
        
        available_rooms = DormitoryRoom.objects.filter(
            floor__building__complex=complex_obj,
            status='AVAILABLE',
            is_active=True
        ).select_related('floor__building')
        
        # فیلتر بر اساس نوع اتاق
        room_type = request.query_params.get('room_type')
        if room_type:
            available_rooms = available_rooms.filter(room_type=room_type)
        
        # فیلتر بر اساس ظرفیت
        min_capacity = request.query_params.get('min_capacity')
        if min_capacity:
            available_rooms = available_rooms.filter(capacity__gte=min_capacity)
        
        serializer = DormitoryRoomListSerializer(available_rooms, many=True)
        return Response(serializer.data)


class DormitoryBuildingViewSet(viewsets.ModelViewSet):
    """ViewSet برای ساختمان‌های خوابگاه"""
    queryset = DormitoryBuilding.objects.select_related('complex', 'supervisor')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['complex', 'maintenance_status', 'is_active']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['complex', 'code']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DormitoryBuildingListSerializer
        return DormitoryBuildingDetailSerializer


class DormitoryRoomViewSet(viewsets.ModelViewSet):
    """ViewSet برای اتاق‌های خوابگاه"""
    queryset = DormitoryRoom.objects.select_related(
        'floor__building__complex'
    ).prefetch_related('accommodations__student')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'floor__building__complex', 'floor__building', 
        'room_type', 'status', 'is_active'
    ]
    search_fields = ['room_number', 'room_code']
    ordering_fields = ['room_number', 'capacity', 'monthly_rent']
    ordering = ['floor__building__complex', 'floor__building', 'floor__floor_number', 'room_number']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DormitoryRoomListSerializer
        return DormitoryRoomDetailSerializer
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """اتاق‌های در دسترس"""
        queryset = self.get_queryset().filter(
            status='AVAILABLE',
            is_active=True
        )
        
        # فیلتر بر اساس جنسیت کاربر
        if hasattr(request.user, 'profile') and hasattr(request.user.profile, 'gender'):
            user_gender = request.user.profile.gender.upper()
            queryset = queryset.filter(floor__building__complex__gender=user_gender)
        
        # فیلترهای اضافی
        room_type = request.query_params.get('room_type')
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        
        max_rent = request.query_params.get('max_rent')
        if max_rent:
            queryset = queryset.filter(monthly_rent__lte=max_rent)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def maintenance_history(self, request, pk=None):
        """تاریخچه تعمیرات اتاق"""
        room = self.get_object()
        maintenances = DormitoryMaintenance.objects.filter(
            room=room
        ).order_by('-reported_at')
        
        serializer = DormitoryMaintenanceListSerializer(maintenances, many=True)
        return Response(serializer.data)


class DormitoryAccommodationViewSet(viewsets.ModelViewSet):
    """ViewSet برای اسکان‌های خوابگاه"""
    queryset = DormitoryAccommodation.objects.select_related(
        'student', 'room__floor__building__complex', 'approved_by'
    )
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'status', 'room__floor__building__complex',
        'room__floor__building', 'is_active'
    ]
    search_fields = [
        'student__first_name', 'student__last_name',
        'room__room_code', 'room__room_number'
    ]
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DormitoryAccommodationListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DormitoryAccommodationCreateSerializer
        return DormitoryAccommodationDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # فیلتر بر اساس نقش کاربر
        if self.request.user.role == 'STUDENT':
            # دانشجو فقط اسکان‌های خود را می‌بیند
            queryset = queryset.filter(student=self.request.user)
        elif hasattr(self.request.user, 'managed_dormitory_complexes'):
            # مدیر خوابگاه فقط اسکان‌های مجموعه خود را می‌بیند
            managed_complexes = self.request.user.managed_dormitory_complexes.all()
            queryset = queryset.filter(room__floor__building__complex__in=managed_complexes)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_accommodations(self, request):
        """اسکان‌های کاربر جاری"""
        accommodations = self.get_queryset().filter(
            student=request.user,
            is_active=True
        )
        serializer = self.get_serializer(accommodations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """تأیید درخواست اسکان"""
        accommodation = self.get_object()
        
        if accommodation.status != 'PENDING':
            return Response(
                {'error': 'فقط درخواست‌های در انتظار تأیید قابل تأیید هستند'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        accommodation.status = 'APPROVED'
        accommodation.approved_by = request.user
        accommodation.approved_at = timezone.now()
        accommodation.save()
        
        serializer = self.get_serializer(accommodation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """رد درخواست اسکان"""
        accommodation = self.get_object()
        
        if accommodation.status != 'PENDING':
            return Response(
                {'error': 'فقط درخواست‌های در انتظار تأیید قابل رد هستند'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reason = request.data.get('reason', '')
        accommodation.status = 'CANCELLED'
        accommodation.admin_notes = reason
        accommodation.save()
        
        serializer = self.get_serializer(accommodation)
        return Response(serializer.data)


class DormitoryStaffViewSet(viewsets.ModelViewSet):
    """ViewSet برای کارکنان خوابگاه"""
    queryset = DormitoryStaff.objects.select_related('user', 'complex', 'building')
    serializer_class = DormitoryStaffSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['complex', 'role', 'shift', 'is_active']
    search_fields = ['user__first_name', 'user__last_name']
    ordering_fields = ['user__last_name', 'role', 'start_date']
    ordering = ['complex', 'role', 'user__last_name']


class DormitoryMaintenanceViewSet(viewsets.ModelViewSet):
    """ViewSet برای درخواست‌های تعمیرات"""
    queryset = DormitoryMaintenance.objects.select_related(
        'room__floor__building__complex', 'reported_by', 'assigned_to'
    )
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'status', 'priority', 'category',
        'room__floor__building__complex', 'assigned_to'
    ]
    search_fields = ['title', 'description', 'room__room_code']
    ordering_fields = ['reported_at', 'priority']
    ordering = ['-reported_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DormitoryMaintenanceListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DormitoryMaintenanceCreateSerializer
        return DormitoryMaintenanceDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """محولی درخواست تعمیرات"""
        maintenance = self.get_object()
        assigned_to_id = request.data.get('assigned_to')
        
        if not assigned_to_id:
            return Response(
                {'error': 'شناسه کاربر محول شده الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            assigned_user = User.objects.get(id=assigned_to_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'کاربر یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        maintenance.assigned_to = assigned_user
        maintenance.status = 'ASSIGNED'
        maintenance.assigned_at = timezone.now()
        maintenance.save()
        
        serializer = self.get_serializer(maintenance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def start_work(self, request, pk=None):
        """شروع کار روی درخواست تعمیرات"""
        maintenance = self.get_object()
        
        if maintenance.status != 'ASSIGNED':
            return Response(
                {'error': 'فقط درخواست‌های محول شده قابل شروع هستند'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        maintenance.status = 'IN_PROGRESS'
        maintenance.started_at = timezone.now()
        maintenance.save()
        
        serializer = self.get_serializer(maintenance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """تکمیل درخواست تعمیرات"""
        maintenance = self.get_object()
        
        if maintenance.status != 'IN_PROGRESS':
            return Response(
                {'error': 'فقط درخواست‌های در حال انجام قابل تکمیل هستند'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        completion_notes = request.data.get('completion_notes', '')
        actual_cost = request.data.get('actual_cost')
        
        maintenance.status = 'COMPLETED'
        maintenance.completed_at = timezone.now()
        maintenance.completion_notes = completion_notes
        
        if actual_cost:
            maintenance.actual_cost = actual_cost
        
        maintenance.save()
        
        serializer = self.get_serializer(maintenance)
        return Response(serializer.data)
