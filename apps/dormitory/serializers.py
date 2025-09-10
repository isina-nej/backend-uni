from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    DormitoryComplex, DormitoryBuilding, DormitoryFloor,
    DormitoryRoom, DormitoryAccommodation, DormitoryStaff,
    DormitoryMaintenance
)

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    """سریالایزر اساسی برای کاربر"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name', 'email']


class DormitoryComplexListSerializer(serializers.ModelSerializer):
    """سریالایزر لیست مجموعه‌های خوابگاهی"""
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    total_buildings = serializers.SerializerMethodField()
    total_capacity = serializers.SerializerMethodField()
    
    class Meta:
        model = DormitoryComplex
        fields = [
            'id', 'name', 'name_en', 'code', 'gender', 
            'manager_name', 'total_buildings', 'total_capacity',
            'is_active', 'created_at'
        ]
    
    def get_total_buildings(self, obj):
        return obj.buildings.count()
    
    def get_total_capacity(self, obj):
        return sum(building.total_capacity for building in obj.buildings.all())


class DormitoryComplexDetailSerializer(serializers.ModelSerializer):
    """سریالایزر جزئیات مجموعه خوابگاهی"""
    manager = UserBasicSerializer(read_only=True)
    buildings_count = serializers.SerializerMethodField()
    total_rooms = serializers.SerializerMethodField()
    total_capacity = serializers.SerializerMethodField()
    occupancy_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = DormitoryComplex
        fields = [
            'id', 'name', 'name_en', 'code', 'gender', 'address', 
            'phone', 'manager', 'is_active', 'established_date',
            'description', 'facilities', 'rules', 'buildings_count',
            'total_rooms', 'total_capacity', 'occupancy_rate',
            'created_at', 'updated_at'
        ]
    
    def get_buildings_count(self, obj):
        return obj.buildings.count()
    
    def get_total_rooms(self, obj):
        return sum(building.total_rooms for building in obj.buildings.all())
    
    def get_total_capacity(self, obj):
        return sum(building.total_capacity for building in obj.buildings.all())
    
    def get_occupancy_rate(self, obj):
        total_capacity = self.get_total_capacity(obj)
        if total_capacity == 0:
            return 0
        
        total_occupied = 0
        for building in obj.buildings.all():
            for floor in building.floors.all():
                for room in floor.rooms.all():
                    total_occupied += room.current_occupancy
        
        return round((total_occupied / total_capacity) * 100, 2)


class DormitoryBuildingListSerializer(serializers.ModelSerializer):
    """سریالایزر لیست ساختمان‌های خوابگاه"""
    complex_name = serializers.CharField(source='complex.name', read_only=True)
    supervisor_name = serializers.CharField(source='supervisor.get_full_name', read_only=True)
    total_rooms = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = DormitoryBuilding
        fields = [
            'id', 'name', 'code', 'complex_name', 'floor_count',
            'total_rooms', 'maintenance_status', 'supervisor_name',
            'is_active', 'created_at'
        ]


class DormitoryFloorSerializer(serializers.ModelSerializer):
    """سریالایزر طبقه خوابگاه"""
    supervisor = UserBasicSerializer(read_only=True)
    rooms_count = serializers.SerializerMethodField()
    total_capacity = serializers.SerializerMethodField()
    
    class Meta:
        model = DormitoryFloor
        fields = [
            'id', 'floor_number', 'name', 'supervisor', 'rooms_count',
            'total_capacity', 'has_common_room', 'has_kitchen',
            'has_bathroom', 'is_active', 'description'
        ]
    
    def get_rooms_count(self, obj):
        return obj.rooms.count()
    
    def get_total_capacity(self, obj):
        return obj.total_capacity


class DormitoryBuildingDetailSerializer(serializers.ModelSerializer):
    """سریالایزر جزئیات ساختمان خوابگاه"""
    complex = DormitoryComplexListSerializer(read_only=True)
    supervisor = UserBasicSerializer(read_only=True)
    floors = DormitoryFloorSerializer(many=True, read_only=True)
    total_rooms = serializers.SerializerMethodField()
    total_capacity = serializers.SerializerMethodField()
    
    class Meta:
        model = DormitoryBuilding
        fields = [
            'id', 'complex', 'name', 'code', 'floor_count',
            'construction_year', 'total_area', 'is_active',
            'maintenance_status', 'has_elevator', 'has_laundry',
            'has_kitchen', 'has_study_room', 'has_prayer_room',
            'supervisor', 'floors', 'total_rooms', 'total_capacity',
            'created_at', 'updated_at'
        ]
    
    def get_total_rooms(self, obj):
        return obj.total_rooms
    
    def get_total_capacity(self, obj):
        return obj.total_capacity


class DormitoryRoomListSerializer(serializers.ModelSerializer):
    """سریالایزر لیست اتاق‌های خوابگاه"""
    floor_info = serializers.SerializerMethodField()
    current_occupancy = serializers.IntegerField(read_only=True)
    available_beds = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = DormitoryRoom
        fields = [
            'id', 'room_code', 'room_number', 'floor_info', 'room_type',
            'capacity', 'current_occupancy', 'available_beds', 'is_full',
            'status', 'monthly_rent', 'is_active'
        ]
    
    def get_floor_info(self, obj):
        return f"{obj.floor.building.complex.name} - {obj.floor.building.name} - طبقه {obj.floor.floor_number}"


class DormitoryRoomDetailSerializer(serializers.ModelSerializer):
    """سریالایزر جزئیات اتاق خوابگاه"""
    floor = DormitoryFloorSerializer(read_only=True)
    current_occupancy = serializers.IntegerField(read_only=True)
    available_beds = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    current_residents = serializers.SerializerMethodField()
    
    class Meta:
        model = DormitoryRoom
        fields = [
            'id', 'floor', 'room_number', 'room_code', 'room_type',
            'capacity', 'area', 'status', 'is_active', 'current_occupancy',
            'available_beds', 'is_full', 'current_residents',
            'has_private_bathroom', 'has_balcony', 'has_air_conditioning',
            'has_heating', 'has_internet', 'academic_level_restriction',
            'min_gpa', 'special_conditions', 'monthly_rent', 'deposit',
            'description', 'maintenance_notes', 'created_at', 'updated_at'
        ]
    
    def get_current_residents(self, obj):
        accommodations = obj.accommodations.filter(
            status__in=['APPROVED', 'ACTIVE'],
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date()
        ).select_related('student')
        
        return [
            {
                'id': acc.student.id,
                'name': acc.student.get_full_name(),
                'student_id': getattr(acc.student, 'student_id', ''),
                'start_date': acc.start_date,
                'end_date': acc.end_date
            }
            for acc in accommodations
        ]


class DormitoryAccommodationListSerializer(serializers.ModelSerializer):
    """سریالایزر لیست اسکان‌های خوابگاه"""
    student = UserBasicSerializer(read_only=True)
    room_info = serializers.SerializerMethodField()
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = DormitoryAccommodation
        fields = [
            'id', 'student', 'room_info', 'start_date', 'end_date',
            'status', 'monthly_payment', 'approved_by_name',
            'approved_at', 'created_at'
        ]
    
    def get_room_info(self, obj):
        room = obj.room
        return f"{room.room_code} - {room.get_room_type_display()}"


class DormitoryAccommodationDetailSerializer(serializers.ModelSerializer):
    """سریالایزر جزئیات اسکان خوابگاه"""
    student = UserBasicSerializer(read_only=True)
    room = DormitoryRoomListSerializer(read_only=True)
    approved_by = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = DormitoryAccommodation
        fields = [
            'id', 'student', 'room', 'start_date', 'end_date',
            'actual_end_date', 'status', 'is_active', 'monthly_payment',
            'deposit_paid', 'approved_by', 'approved_at', 'application_notes',
            'admin_notes', 'termination_reason', 'created_at', 'updated_at'
        ]


class DormitoryStaffSerializer(serializers.ModelSerializer):
    """سریالایزر کارکنان خوابگاه"""
    user = UserBasicSerializer(read_only=True)
    complex_name = serializers.CharField(source='complex.name', read_only=True)
    building_name = serializers.CharField(source='building.name', read_only=True)
    
    class Meta:
        model = DormitoryStaff
        fields = [
            'id', 'user', 'complex_name', 'building_name', 'role',
            'shift', 'start_date', 'end_date', 'is_active',
            'emergency_contact', 'notes', 'created_at'
        ]


class DormitoryMaintenanceListSerializer(serializers.ModelSerializer):
    """سریالایزر لیست درخواست‌های تعمیرات"""
    room_info = serializers.SerializerMethodField()
    reported_by = UserBasicSerializer(read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = DormitoryMaintenance
        fields = [
            'id', 'title', 'room_info', 'category', 'priority',
            'status', 'reported_by', 'assigned_to_name',
            'reported_at', 'estimated_cost'
        ]
    
    def get_room_info(self, obj):
        room = obj.room
        return f"{room.room_code} - {room.floor.building.name}"


class DormitoryMaintenanceDetailSerializer(serializers.ModelSerializer):
    """سریالایزر جزئیات درخواست تعمیرات"""
    room = DormitoryRoomListSerializer(read_only=True)
    reported_by = UserBasicSerializer(read_only=True)
    assigned_to = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = DormitoryMaintenance
        fields = [
            'id', 'room', 'reported_by', 'title', 'description',
            'priority', 'category', 'status', 'assigned_to',
            'reported_at', 'assigned_at', 'started_at', 'completed_at',
            'estimated_cost', 'actual_cost', 'admin_notes',
            'technician_notes', 'completion_notes', 'updated_at'
        ]


# سریالایزرهای ایجاد و ویرایش

class DormitoryComplexCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DormitoryComplex
        fields = [
            'name', 'name_en', 'code', 'gender', 'address',
            'phone', 'manager', 'is_active', 'established_date',
            'description', 'facilities', 'rules'
        ]


class DormitoryAccommodationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DormitoryAccommodation
        fields = [
            'student', 'room', 'start_date', 'end_date',
            'monthly_payment', 'deposit_paid', 'application_notes'
        ]
    
    def validate(self, data):
        # بررسی تاریخ‌ها
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError(
                'تاریخ شروع باید قبل از تاریخ پایان باشد'
            )
        
        # بررسی ظرفیت اتاق
        room = data['room']
        conflicting_accommodations = DormitoryAccommodation.objects.filter(
            room=room,
            status__in=['APPROVED', 'ACTIVE'],
            start_date__lt=data['end_date'],
            end_date__gt=data['start_date']
        )
        
        if conflicting_accommodations.count() >= room.capacity:
            raise serializers.ValidationError(
                'ظرفیت اتاق در این بازه زمانی تکمیل است'
            )
        
        return data


class DormitoryMaintenanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DormitoryMaintenance
        fields = [
            'room', 'title', 'description', 'priority',
            'category', 'estimated_cost'
        ]
