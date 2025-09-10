#!/usr/bin/env python3
"""
اسکریپت ایجاد داده‌های نمونه برای سیستم مدیریت خوابگاه
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# تنظیم Django
sys.path.append('/path/to/your/project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.dormitory.models import (
    DormitoryComplex, DormitoryBuilding, DormitoryFloor,
    DormitoryRoom, DormitoryAccommodation, DormitoryStaff,
    DormitoryMaintenance
)

User = get_user_model()

def create_sample_users():
    """ایجاد کاربران نمونه"""
    print("ایجاد کاربران نمونه...")
    
    users = {}
    
    # مدیران خوابگاه
    users['manager_male'] = User.objects.create_user(
        username='dormmanager_m',
        email='manager.male@university.ac.ir',
        first_name='احمد',
        last_name='رضایی',
        role='STAFF',
        password='password123'
    )
    
    users['manager_female'] = User.objects.create_user(
        username='dormmanager_f',
        email='manager.female@university.ac.ir',
        first_name='فاطمه',
        last_name='محمدی',
        role='STAFF',
        password='password123'
    )
    
    # سرپرستان ساختمان
    for i in range(1, 5):
        users[f'supervisor_{i}'] = User.objects.create_user(
            username=f'supervisor_{i}',
            email=f'supervisor{i}@university.ac.ir',
            first_name=f'سرپرست{i}',
            last_name='احمدی',
            role='STAFF',
            password='password123'
        )
    
    # دانشجویان نمونه
    for i in range(1, 21):
        gender = 'MALE' if i <= 10 else 'FEMALE'
        users[f'student_{i}'] = User.objects.create_user(
            username=f'student_{i:03d}',
            email=f'student{i}@student.university.ac.ir',
            first_name=f'دانشجو{i}',
            last_name='تست',
            role='STUDENT',
            student_id=f'40012{i:04d}',
            password='password123'
        )
    
    # تعمیرکاران
    for i in range(1, 4):
        users[f'technician_{i}'] = User.objects.create_user(
            username=f'technician_{i}',
            email=f'tech{i}@university.ac.ir',
            first_name=f'تعمیرکار{i}',
            last_name='فنی',
            role='STAFF',
            password='password123'
        )
    
    print(f"✅ {len(users)} کاربر ایجاد شد")
    return users

def create_dormitory_complexes(users):
    """ایجاد مجموعه‌های خوابگاهی"""
    print("ایجاد مجموعه‌های خوابگاهی...")
    
    complexes = {}
    
    # خوابگاه برادران
    complexes['male'] = DormitoryComplex.objects.create(
        name='خوابگاه برادران شهید بهشتی',
        name_en='Shahid Beheshti Male Dormitory',
        code='BR-BEH',
        gender='MALE',
        address='تهران، خیابان ولیعصر، دانشگاه شهید بهشتی',
        phone='021-29903000',
        manager=users['manager_male'],
        established_date=date(1995, 9, 1),
        facilities=[
            'اتاق مطالعه مشترک',
            'آشپزخانه مشترک',
            'رختشویخانه',
            'نمازخانه',
            'سالن ورزش',
            'پارکینگ'
        ],
        rules=[
            'ورود مهمان تا ساعت 20',
            'سکوت از ساعت 23',
            'نظافت روزانه اتاق الزامی',
            'استفاده از لوازم مشترک با رعایت نوبت'
        ],
        description='خوابگاه مدرن برادران با امکانات کامل'
    )
    
    # خوابگاه خواهران
    complexes['female'] = DormitoryComplex.objects.create(
        name='خوابگاه خواهران فاطمه زهرا(س)',
        name_en='Fatimah Zahra Female Dormitory',
        code='SI-FAT',
        gender='FEMALE',
        address='تهران، خیابان انقلاب، نبش خیابان فاطمی',
        phone='021-29903100',
        manager=users['manager_female'],
        established_date=date(1998, 9, 1),
        facilities=[
            'اتاق مطالعه مشترک',
            'آشپزخانه مشترک',
            'رختشویخانه',
            'نمازخانه',
            'سالن فعالیت‌های فرهنگی',
            'باغچه کوچک'
        ],
        rules=[
            'ورود مهمان تا ساعت 19',
            'سکوت از ساعت 22:30',
            'نظافت روزانه اتاق الزامی',
            'رعایت حجاب در فضاهای مشترک'
        ],
        description='خوابگاه مناسب خواهران با فضای آرام'
    )
    
    print(f"✅ {len(complexes)} مجموعه خوابگاهی ایجاد شد")
    return complexes

def create_dormitory_buildings(complexes, users):
    """ایجاد ساختمان‌های خوابگاه"""
    print("ایجاد ساختمان‌های خوابگاه...")
    
    buildings = {}
    
    # ساختمان‌های خوابگاه برادران
    buildings['male_a'] = DormitoryBuilding.objects.create(
        complex=complexes['male'],
        name='ساختمان الف',
        code='A',
        floor_count=4,
        construction_year=1995,
        total_area=2000,
        maintenance_status='GOOD',
        has_elevator=True,
        has_laundry=True,
        has_kitchen=True,
        has_study_room=True,
        has_prayer_room=True,
        supervisor=users['supervisor_1']
    )
    
    buildings['male_b'] = DormitoryBuilding.objects.create(
        complex=complexes['male'],
        name='ساختمان ب',
        code='B',
        floor_count=3,
        construction_year=2005,
        total_area=1500,
        maintenance_status='GOOD',
        has_elevator=False,
        has_laundry=True,
        has_kitchen=True,
        has_study_room=False,
        has_prayer_room=True,
        supervisor=users['supervisor_2']
    )
    
    # ساختمان‌های خوابگاه خواهران
    buildings['female_a'] = DormitoryBuilding.objects.create(
        complex=complexes['female'],
        name='ساختمان الف',
        code='A',
        floor_count=5,
        construction_year=1998,
        total_area=2500,
        maintenance_status='GOOD',
        has_elevator=True,
        has_laundry=True,
        has_kitchen=True,
        has_study_room=True,
        has_prayer_room=True,
        supervisor=users['supervisor_3']
    )
    
    buildings['female_b'] = DormitoryBuilding.objects.create(
        complex=complexes['female'],
        name='ساختمان ب',
        code='B',
        floor_count=4,
        construction_year=2010,
        total_area=2200,
        maintenance_status='GOOD',
        has_elevator=True,
        has_laundry=True,
        has_kitchen=True,
        has_study_room=True,
        has_prayer_room=True,
        supervisor=users['supervisor_4']
    )
    
    print(f"✅ {len(buildings)} ساختمان ایجاد شد")
    return buildings

def create_dormitory_floors(buildings):
    """ایجاد طبقات"""
    print("ایجاد طبقات...")
    
    floors = []
    
    for building_key, building in buildings.items():
        for floor_num in range(1, building.floor_count + 1):
            floor = DormitoryFloor.objects.create(
                building=building,
                floor_number=floor_num,
                name=f'طبقه {floor_num}',
                has_common_room=floor_num == 1,  # فقط طبقه اول اتاق مشترک
                has_kitchen=True,
                has_bathroom=True,
                description=f'طبقه {floor_num} ساختمان {building.name}'
            )
            floors.append(floor)
    
    print(f"✅ {len(floors)} طبقه ایجاد شد")
    return floors

def create_dormitory_rooms(floors):
    """ایجاد اتاق‌ها"""
    print("ایجاد اتاق‌ها...")
    
    rooms = []
    room_types = ['DOUBLE', 'TRIPLE', 'SINGLE', 'QUAD']
    capacities = {'SINGLE': 1, 'DOUBLE': 2, 'TRIPLE': 3, 'QUAD': 4}
    
    for floor in floors:
        # تعداد اتاق‌ها بر اساس طبقه
        if floor.floor_number == 1:
            room_count = 10  # طبقه اول کمتر (اتاق‌های مشترک)
        elif floor.floor_number <= 3:
            room_count = 15
        else:
            room_count = 12  # طبقات بالا کمتر
        
        for room_num in range(1, room_count + 1):
            # تنوع در نوع اتاق‌ها
            if room_num <= 3:
                room_type = 'SINGLE'
            elif room_num <= 10:
                room_type = 'DOUBLE'
            elif room_num <= 13:
                room_type = 'TRIPLE'
            else:
                room_type = 'QUAD'
            
            # قیمت‌گذاری بر اساس نوع اتاق
            base_rent = {
                'SINGLE': 800000,
                'DOUBLE': 600000,
                'TRIPLE': 500000,
                'QUAD': 450000
            }
            
            room = DormitoryRoom.objects.create(
                floor=floor,
                room_number=f'{room_num:02d}',
                room_type=room_type,
                capacity=capacities[room_type],
                area=15 + (room_num % 3) * 5,  # مساحت 15-25 متر
                status='AVAILABLE',
                has_private_bathroom=room_type in ['SINGLE', 'QUAD'],
                has_balcony=room_num % 4 == 0,  # هر 4 اتاق یکی بالکن
                has_air_conditioning=floor.floor_number >= 3,
                has_heating=True,
                has_internet=True,
                monthly_rent=Decimal(base_rent[room_type]),
                deposit=Decimal(base_rent[room_type] * 2),
                academic_level_restriction=[],  # بدون محدودیت
                description=f'اتاق {room_type.lower()} در {floor.building.name}'
            )
            rooms.append(room)
    
    print(f"✅ {len(rooms)} اتاق ایجاد شد")
    return rooms

def create_staff_members(complexes, buildings, users):
    """ایجاد کارکنان خوابگاه"""
    print("ایجاد کارکنان...")
    
    staff_members = []
    
    # کارکنان مجموعه برادران
    staff_roles = [
        ('GUARD', 'NIGHT'),
        ('GUARD', 'MORNING'),
        ('CLEANER', 'MORNING'),
        ('MAINTENANCE', 'FULL_TIME'),
    ]
    
    user_index = 1
    for complex_key, complex_obj in complexes.items():
        for role, shift in staff_roles:
            if user_index <= 3:  # فقط برای تعمیرکاران
                user_key = f'technician_{user_index}'
                user_index += 1
            else:
                continue
                
            staff = DormitoryStaff.objects.create(
                user=users[user_key],
                complex=complex_obj,
                role=role,
                shift=shift,
                start_date=date.today() - timedelta(days=365),
                emergency_contact={
                    'name': 'تماس اضطراری',
                    'phone': '09123456789',
                    'relationship': 'خانواده'
                },
                notes=f'کارمند {role} در شیفت {shift}'
            )
            staff_members.append(staff)
    
    print(f"✅ {len(staff_members)} کارمند ایجاد شد")
    return staff_members

def create_sample_accommodations(rooms, users):
    """ایجاد اسکان‌های نمونه"""
    print("ایجاد اسکان‌های نمونه...")
    
    accommodations = []
    
    # انتخاب اتاق‌های مناسب برای دانشجویان
    male_rooms = [r for r in rooms if r.floor.building.complex.gender == 'MALE'][:10]
    female_rooms = [r for r in rooms if r.floor.building.complex.gender == 'FEMALE'][:10]
    
    # اسکان دانشجویان پسر
    for i, room in enumerate(male_rooms, 1):
        if i <= 10:  # فقط 10 دانشجوی اول
            student = users[f'student_{i}']
            accommodation = DormitoryAccommodation.objects.create(
                student=student,
                room=room,
                start_date=date.today() - timedelta(days=30),
                end_date=date.today() + timedelta(days=335),  # سال تحصیلی
                status='ACTIVE',
                monthly_payment=room.monthly_rent,
                deposit_paid=room.deposit,
                approved_by=users['manager_male'],
                approved_at=timezone.now() - timedelta(days=25),
                application_notes=f'درخواست اسکان دانشجو {student.get_full_name()}'
            )
            accommodations.append(accommodation)
    
    # اسکان دانشجویان دختر
    for i, room in enumerate(female_rooms, 11):
        if i <= 20:  # دانشجویان 11 تا 20
            student = users[f'student_{i}']
            accommodation = DormitoryAccommodation.objects.create(
                student=student,
                room=room,
                start_date=date.today() - timedelta(days=30),
                end_date=date.today() + timedelta(days=335),
                status='ACTIVE',
                monthly_payment=room.monthly_rent,
                deposit_paid=room.deposit,
                approved_by=users['manager_female'],
                approved_at=timezone.now() - timedelta(days=25),
                application_notes=f'درخواست اسکان دانشجو {student.get_full_name()}'
            )
            accommodations.append(accommodation)
    
    print(f"✅ {len(accommodations)} اسکان ایجاد شد")
    return accommodations

def create_maintenance_requests(rooms, users):
    """ایجاد درخواست‌های تعمیرات نمونه"""
    print("ایجاد درخواست‌های تعمیرات...")
    
    maintenance_requests = []
    
    # انواع مشکلات رایج
    issues = [
        ('مشکل برق اتاق', 'ELECTRICAL', 'HIGH'),
        ('نشتی شیر آب', 'PLUMBING', 'MEDIUM'),
        ('خرابی کولر', 'COOLING', 'LOW'),
        ('مشکل قفل درب', 'OTHER', 'MEDIUM'),
        ('تعمیر میز مطالعه', 'FURNITURE', 'LOW'),
    ]
    
    # ایجاد درخواست‌ها
    for i, (title, category, priority) in enumerate(issues, 1):
        room = rooms[i]  # انتخاب اتاق
        reporter = users[f'student_{i}'] if i <= 20 else users['manager_male']
        
        maintenance = DormitoryMaintenance.objects.create(
            room=room,
            reported_by=reporter,
            title=title,
            description=f'گزارش مشکل {title} در اتاق {room.room_code}',
            priority=priority,
            category=category,
            status='REPORTED',
            estimated_cost=Decimal(50000 + i * 10000),
            admin_notes='نیاز به بررسی'
        )
        maintenance_requests.append(maintenance)
    
    print(f"✅ {len(maintenance_requests)} درخواست تعمیرات ایجاد شد")
    return maintenance_requests

def main():
    """تابع اصلی"""
    print("🏠 شروع ایجاد داده‌های نمونه سیستم خوابگاه...")
    print("=" * 50)
    
    try:
        # ایجاد کاربران
        users = create_sample_users()
        
        # ایجاد مجموعه‌های خوابگاهی
        complexes = create_dormitory_complexes(users)
        
        # ایجاد ساختمان‌ها
        buildings = create_dormitory_buildings(complexes, users)
        
        # ایجاد طبقات
        floors = create_dormitory_floors(buildings)
        
        # ایجاد اتاق‌ها
        rooms = create_dormitory_rooms(floors)
        
        # ایجاد کارکنان
        staff_members = create_staff_members(complexes, buildings, users)
        
        # ایجاد اسکان‌ها
        accommodations = create_sample_accommodations(rooms, users)
        
        # ایجاد درخواست‌های تعمیرات
        maintenance_requests = create_maintenance_requests(rooms, users)
        
        print("=" * 50)
        print("✅ تمام داده‌های نمونه با موفقیت ایجاد شدند!")
        print("\n📊 خلاصه آمار:")
        print(f"👥 کاربران: {len(users)}")
        print(f"🏢 مجموعه‌های خوابگاهی: {len(complexes)}")
        print(f"🏠 ساختمان‌ها: {len(buildings)}")
        print(f"📊 طبقات: {len(floors)}")
        print(f"🏠 اتاق‌ها: {len(rooms)}")
        print(f"👷 کارکنان: {len(staff_members)}")
        print(f"🛏️ اسکان‌ها: {len(accommodations)}")
        print(f"🔧 درخواست‌های تعمیرات: {len(maintenance_requests)}")
        
        print("\n🔐 اطلاعات ورود:")
        print("مدیر برادران: dormmanager_m / password123")
        print("مدیر خواهران: dormmanager_f / password123")
        print("دانشجو نمونه: student_001 / password123")
        
    except Exception as e:
        print(f"❌ خطا در ایجاد داده‌ها: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
