#!/usr/bin/env python3
# ==============================================================================
# SIMPLE SAMPLE DATA GENERATOR FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import os
import sys
import django
from datetime import datetime, date

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import (
    Ministry, University, Faculty, Department, Position, AccessLevel,
    Employee, User, StudentCategory, AcademicProgram, Student
)

def create_simple_sample_data():
    """Create simple sample data for testing"""
    print("🏗️  Creating simple sample data")
    print("=" * 40)
    
    try:
        # 1. Ministry
        ministry, created = Ministry.objects.get_or_create(
            name='وزارت علوم',
            defaults={
                'name_en': 'Ministry of Science',
                'type': 'SCIENCE',
                'minister_name': 'دکتر وزیر',
                'address': 'تهران',
                'phone': '021-88888888',
                'website': 'https://msrt.ir',
                'established_date': date(1979, 1, 1),
                'description': 'وزارت علوم'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Ministry: {ministry.name}")
        
        # 2. University
        university, created = University.objects.get_or_create(
            name='دانشگاه تهران',
            defaults={
                'name_en': 'University of Tehran',
                'code': 'UT001',
                'type': 'STATE',
                'ministry': ministry,
                'established_year': 1934,
                'website': 'https://ut.ac.ir',
                'phone': '021-61111111',
                'email': 'info@ut.ac.ir',
                'address': 'تهران',
                'accreditation_status': 'معتبر',
                'president_name': 'دکتر رئیس'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} University: {university.name}")
        
        # 3. Faculty
        faculty, created = Faculty.objects.get_or_create(
            name='دانشکده مهندسی',
            defaults={
                'name_en': 'Engineering Faculty',
                'code': 'ENG',
                'university': university,
                'phone': '021-61111100',
                'email': 'eng@ut.ac.ir'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Faculty: {faculty.name}")
        
        # 4. Department
        department, created = Department.objects.get_or_create(
            name='گروه کامپیوتر',
            defaults={
                'name_en': 'Computer Department',
                'code': 'CE',
                'faculty': faculty,
                'phone': '021-61111120',
                'email': 'ce@ut.ac.ir'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Department: {department.name}")
        
        # 5. Create superuser
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@ut.ac.ir',
                'first_name': 'ادمین',
                'last_name': 'سیستم',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        print(f"{'✅ Created' if created else '✅ Found'} Admin User: {admin_user.username}")
        
        print("\n" + "=" * 40)
        print("✅ Simple sample data created!")
        print("🔑 Admin login: admin / admin123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_simple_sample_data()
