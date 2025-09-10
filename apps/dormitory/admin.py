from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    DormitoryComplex, DormitoryBuilding, DormitoryFloor, 
    DormitoryRoom, DormitoryAccommodation, DormitoryStaff,
    DormitoryMaintenance
)


@admin.register(DormitoryComplex)
class DormitoryComplexAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'code', 'gender', 'manager', 'total_buildings', 
        'total_capacity', 'is_active', 'created_at'
    ]
    list_filter = ['gender', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'manager__first_name', 'manager__last_name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'name_en', 'code', 'gender')
        }),
        ('مدیریت', {
            'fields': ('manager',)
        }),
        ('اطلاعات تماس', {
            'fields': ('address', 'phone')
        }),
        ('تنظیمات', {
            'fields': ('is_active', 'established_date', 'description')
        }),
        ('امکانات و قوانین', {
            'fields': ('facilities', 'rules'),
            'classes': ('collapse',)
        }),
        ('سیستمی', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def total_buildings(self, obj):
        return obj.buildings.count()
    total_buildings.short_description = 'تعداد ساختمان'
    
    def total_capacity(self, obj):
        total = sum(building.total_capacity for building in obj.buildings.all())
        return total
    total_capacity.short_description = 'ظرفیت کل'


class DormitoryFloorInline(admin.TabularInline):
    model = DormitoryFloor
    extra = 0
    fields = ['floor_number', 'name', 'supervisor', 'is_active']
    show_change_link = True


@admin.register(DormitoryBuilding)
class DormitoryBuildingAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'complex', 'code', 'floor_count', 'total_rooms',
        'maintenance_status', 'supervisor', 'is_active'
    ]
    list_filter = [
        'complex', 'maintenance_status', 'is_active', 
        'has_elevator', 'has_laundry'
    ]
    search_fields = ['name', 'code', 'complex__name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_rooms']
    inlines = [DormitoryFloorInline]
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('complex', 'name', 'code', 'floor_count')
        }),
        ('مشخصات فیزیکی', {
            'fields': ('construction_year', 'total_area')
        }),
        ('وضعیت', {
            'fields': ('is_active', 'maintenance_status')
        }),
        ('امکانات', {
            'fields': (
                'has_elevator', 'has_laundry', 'has_kitchen', 
                'has_study_room', 'has_prayer_room'
            )
        }),
        ('مدیریت', {
            'fields': ('supervisor',)
        }),
        ('سیستمی', {
            'fields': ('id', 'total_rooms', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def total_rooms(self, obj):
        return obj.total_rooms
    total_rooms.short_description = 'تعداد اتاق'


class DormitoryRoomInline(admin.TabularInline):
    model = DormitoryRoom
    extra = 0
    fields = [
        'room_number', 'room_type', 'capacity', 'status', 
        'monthly_rent', 'is_active'
    ]
    show_change_link = True


@admin.register(DormitoryFloor)
class DormitoryFloorAdmin(admin.ModelAdmin):
    list_display = [
        'building', 'floor_number', 'name', 'room_count',
        'total_capacity', 'supervisor', 'is_active'
    ]
    list_filter = ['building__complex', 'building', 'is_active']
    search_fields = ['building__name', 'name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [DormitoryRoomInline]
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('building', 'floor_number', 'name')
        }),
        ('مدیریت', {
            'fields': ('supervisor',)
        }),
        ('امکانات', {
            'fields': ('has_common_room', 'has_kitchen', 'has_bathroom')
        }),
        ('وضعیت', {
            'fields': ('is_active', 'description')
        }),
        ('سیستمی', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def room_count(self, obj):
        return obj.rooms.count()
    room_count.short_description = 'تعداد اتاق'
    
    def total_capacity(self, obj):
        return obj.total_capacity
    total_capacity.short_description = 'ظرفیت کل'


@admin.register(DormitoryRoom)
class DormitoryRoomAdmin(admin.ModelAdmin):
    list_display = [
        'room_code', 'floor', 'room_type', 'capacity', 
        'current_occupancy', 'status', 'monthly_rent', 'is_active'
    ]
    list_filter = [
        'floor__building__complex', 'floor__building', 'room_type', 
        'status', 'is_active', 'has_private_bathroom'
    ]
    search_fields = ['room_number', 'room_code', 'floor__building__name']
    readonly_fields = [
        'id', 'room_code', 'current_occupancy', 'available_beds', 
        'is_full', 'created_at', 'updated_at'
    ]
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('floor', 'room_number', 'room_code', 'room_type')
        }),
        ('ظرفیت و وضعیت', {
            'fields': ('capacity', 'current_occupancy', 'available_beds', 'status', 'is_active')
        }),
        ('مشخصات فیزیکی', {
            'fields': ('area',)
        }),
        ('امکانات', {
            'fields': (
                'has_private_bathroom', 'has_balcony', 'has_air_conditioning',
                'has_heating', 'has_internet'
            )
        }),
        ('محدودیت‌ها و شرایط', {
            'fields': ('academic_level_restriction', 'min_gpa', 'special_conditions'),
            'classes': ('collapse',)
        }),
        ('قیمت‌گذاری', {
            'fields': ('monthly_rent', 'deposit')
        }),
        ('یادداشت‌ها', {
            'fields': ('description', 'maintenance_notes'),
            'classes': ('collapse',)
        }),
        ('سیستمی', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def current_occupancy(self, obj):
        occupancy = obj.current_occupancy
        capacity = obj.capacity
        if occupancy >= capacity:
            color = 'red'
        elif occupancy > capacity * 0.8:
            color = 'orange'
        else:
            color = 'green'
        return format_html(
            '<span style="color: {};">{}/{}</span>',
            color, occupancy, capacity
        )
    current_occupancy.short_description = 'اشغال فعلی'


@admin.register(DormitoryAccommodation)
class DormitoryAccommodationAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'room', 'start_date', 'end_date', 
        'status', 'monthly_payment', 'approved_by'
    ]
    list_filter = [
        'status', 'room__floor__building__complex',
        'start_date', 'end_date', 'is_active'
    ]
    search_fields = [
        'student__first_name', 'student__last_name', 
        'room__room_code', 'room__room_number'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('student', 'room')
        }),
        ('تاریخ‌ها', {
            'fields': ('start_date', 'end_date', 'actual_end_date')
        }),
        ('وضعیت', {
            'fields': ('status', 'is_active')
        }),
        ('اطلاعات مالی', {
            'fields': ('monthly_payment', 'deposit_paid')
        }),
        ('تأیید', {
            'fields': ('approved_by', 'approved_at')
        }),
        ('یادداشت‌ها', {
            'fields': ('application_notes', 'admin_notes', 'termination_reason'),
            'classes': ('collapse',)
        }),
        ('سیستمی', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'student', 'room__floor__building__complex', 'approved_by'
        )


@admin.register(DormitoryStaff)
class DormitoryStaffAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'complex', 'role', 'shift', 
        'building', 'start_date', 'is_active'
    ]
    list_filter = [
        'complex', 'role', 'shift', 'is_active', 'start_date'
    ]
    search_fields = [
        'user__first_name', 'user__last_name', 
        'complex__name', 'building__name'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('user', 'complex', 'building')
        }),
        ('اطلاعات شغلی', {
            'fields': ('role', 'shift')
        }),
        ('تاریخ‌ها', {
            'fields': ('start_date', 'end_date')
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
        ('اطلاعات اضافی', {
            'fields': ('emergency_contact', 'notes'),
            'classes': ('collapse',)
        }),
        ('سیستمی', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(DormitoryMaintenance)
class DormitoryMaintenanceAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'room', 'category', 'priority', 
        'status', 'reported_by', 'assigned_to', 'reported_at'
    ]
    list_filter = [
        'status', 'priority', 'category',
        'room__floor__building__complex',
        'reported_at'
    ]
    search_fields = [
        'title', 'description', 
        'room__room_code', 'reported_by__first_name'
    ]
    readonly_fields = ['id', 'reported_at', 'updated_at']
    date_hierarchy = 'reported_at'
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('room', 'title', 'description')
        }),
        ('دسته‌بندی', {
            'fields': ('category', 'priority')
        }),
        ('گزارش‌دهنده', {
            'fields': ('reported_by',)
        }),
        ('وضعیت و محولی', {
            'fields': ('status', 'assigned_to')
        }),
        ('تاریخ‌ها', {
            'fields': (
                'reported_at', 'assigned_at', 
                'started_at', 'completed_at'
            )
        }),
        ('هزینه', {
            'fields': ('estimated_cost', 'actual_cost')
        }),
        ('یادداشت‌ها', {
            'fields': ('admin_notes', 'technician_notes', 'completion_notes'),
            'classes': ('collapse',)
        }),
        ('سیستمی', {
            'fields': ('id', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'room__floor__building__complex', 'reported_by', 'assigned_to'
        )
