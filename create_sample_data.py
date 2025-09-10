#!/usr/bin/env python3
# ==============================================================================
# SAMPLE DATA GENERATOR FOR UNIVERSITY MANAGEMENT SYSTEM
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
    Ministry, University, Faculty, Department, ResearchCenter,
    AdministrativeUnit, Position, AccessLevel, Employee, EmployeeDuty,
    User, StudentCategory, AcademicProgram, Student, StudentCategoryAssignment
)

def create_sample_data():
    """Create sample data for testing"""
    print("🏗️  Creating sample data for University Management System")
    print("=" * 60)
    
    try:
        # 1. Create Ministry
        ministry, created = Ministry.objects.get_or_create(
            name='وزارت علوم، تحقیقات و فناوری',
            defaults={
                'name_en': 'Ministry of Science, Research and Technology',
                'type': 'SCIENCE',
                'minister_name': 'دکتر حسین ذوالفقاری',
                'address': 'تهران، خیابان وزرا، ساختمان وزارت علوم',
                'phone': '021-88888888',
                'website': 'https://msrt.ir',
                'established_date': date(1979, 1, 1),
                'description': 'وزارت علوم، تحقیقات و فناوری جمهوری اسلامی ایران'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Ministry: {ministry.name}")
        
        # 2. Create University
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
                'address': 'تهران، خیابان کارگر شمالی',
                'accreditation_status': 'معتبر',
                'president_name': 'دکتر محمد رضا پورمحمد'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} University: {university.name}")
        
        # 3. Create Faculty
        faculty, created = Faculty.objects.get_or_create(
            name='دانشکده مهندسی',
            defaults={
                'name_en': 'Faculty of Engineering',
                'code': 'ENG',
                'university': university,
                'phone': '021-61111100',
                'email': 'engineering@ut.ac.ir'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Faculty: {faculty.name}")
        
        # 4. Create Department
        department, created = Department.objects.get_or_create(
            name='گروه مهندسی کامپیوتر',
            defaults={
                'name_en': 'Computer Engineering Department',
                'code': 'CE',
                'faculty': faculty,
                'phone': '021-61111120',
                'email': 'ce@ut.ac.ir'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Department: {department.name}")
        
        # 5. Create Research Center
        research_center, created = ResearchCenter.objects.get_or_create(
            name='مرکز تحقیقات هوش مصنوعی',
            defaults={
                'name_en': 'Artificial Intelligence Research Center',
                'code': 'AIRC',
                'university': university,
                'phone': '021-61111150',
                'email': 'ai@ut.ac.ir'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Research Center: {research_center.name}")
        
        # 6. Create Administrative Unit
        admin_unit, created = AdministrativeUnit.objects.get_or_create(
            name='دفتر امور دانشجویی',
            defaults={
                'name_en': 'Student Affairs Office',
                'code': 'SAO',
                'university': university,
                'phone': '021-61111200',
                'email': 'students@ut.ac.ir'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Administrative Unit: {admin_unit.name}")
        
        # 7. Create Position
        position, created = Position.objects.get_or_create(
            title='استاد',
            defaults={
                'title_en': 'Professor',
                'responsibilities': 'تدریس، پژوهش، راهنمایی دانشجو',
                'requirements': 'دکترای تخصصی در رشته مربوطه'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Position: {position.title}")
        
        # 8. Create Access Level
        access_level, created = AccessLevel.objects.get_or_create(
            name='سطح استاد',
            defaults={
                'level_number': 5,
                'description': 'دسترسی کامل به سیستم آموزشی'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Access Level: {access_level.name}")
        
        # 9. Create Employee
        employee, created = Employee.objects.get_or_create(
            employee_id='EMP001',
            defaults={
                'first_name': 'علی',
                'last_name': 'احمدی',
                'first_name_en': 'Ali',
                'last_name_en': 'Ahmadi',
                'national_id': '1234567890',
                'birth_date': date(1975, 5, 15),
                'phone': '09121234567',
                'email': 'a.ahmadi@ut.ac.ir',
                'position': position,
                'primary_unit': admin_unit,
                'access_level': access_level,
                'hire_date': date(2010, 9, 1),
                'employment_type': 'FULL_TIME',
                'employment_status': 'ACTIVE',
                'academic_rank': 'FULL_PROF'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Employee: {employee.get_full_name()}")
        
        # 10. Create Student Category
        student_category, created = StudentCategory.objects.get_or_create(
            name='دانشجوی کارشناسی',
            defaults={
                'name_en': 'Undergraduate Student',
                'description': 'دانشجویان مقطع کارشناسی'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Student Category: {student_category.name}")
        
        # 11. Create Academic Program
        academic_program, created = AcademicProgram.objects.get_or_create(
            name='مهندسی کامپیوتر',
            defaults={
                'name_en': 'Computer Engineering',
                'code': 'CE-BS',
                'department': department,
                'duration_semesters': 8,
                'min_credits': 140,
                'max_credits': 160
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Academic Program: {academic_program.name}")
        
        # 12. Create Student
        student, created = Student.objects.get_or_create(
            student_id='STD001',
            defaults={
                'first_name': 'سارا',
                'last_name': 'محمدی',
                'first_name_en': 'Sara',
                'last_name_en': 'Mohammadi',
                'national_id': '0987654321',
                'birth_date': date(2002, 8, 20),
                'phone': '09129876543',
                'email': 's.mohammadi@ut.ac.ir',
                'university': university,
                'current_program': academic_program,
                'entry_year': 1402,
                'entry_semester': 'FALL',
                'student_status': 'ACTIVE'
            }
        )
        print(f"{'✅ Created' if created else '✅ Found'} Student: {student.get_full_name()}")
        
        # 13. Create User for Employee
        user_employee, created = User.objects.get_or_create(
            username='prof.ahmadi',
            defaults={
                'email': 'a.ahmadi@ut.ac.ir',
                'first_name': 'علی',
                'last_name': 'احمدی',
                'user_type': 'EMPLOYEE',
                'employee': employee,
                'is_staff': True,
                'is_active': True
            }
        )
        if created:
            user_employee.set_password('professor123')
            user_employee.save()
        print(f"{'✅ Created' if created else '✅ Found'} User (Employee): {user_employee.username}")
        
        # 14. Create User for Student
        user_student, created = User.objects.get_or_create(
            username='sara.mohammadi',
            defaults={
                'email': 's.mohammadi@ut.ac.ir',
                'first_name': 'سارا',
                'last_name': 'محمدی',
                'user_type': 'STUDENT',
                'student': student,
                'is_active': True
            }
        )
        if created:
            user_student.set_password('student123')
            user_student.save()
        print(f"{'✅ Created' if created else '✅ Found'} User (Student): {user_student.username}")
        
        print("\n" + "=" * 60)
        print("✅ Sample data creation completed successfully!")
        print(f"📊 Total objects created:")
        print(f"   • Ministries: {Ministry.objects.count()}")
        print(f"   • Universities: {University.objects.count()}")
        print(f"   • Faculties: {Faculty.objects.count()}")
        print(f"   • Departments: {Department.objects.count()}")
        print(f"   • Research Centers: {ResearchCenter.objects.count()}")
        print(f"   • Administrative Units: {AdministrativeUnit.objects.count()}")
        print(f"   • Positions: {Position.objects.count()}")
        print(f"   • Access Levels: {AccessLevel.objects.count()}")
        print(f"   • Employees: {Employee.objects.count()}")
        print(f"   • Students: {Student.objects.count()}")
        print(f"   • Academic Programs: {AcademicProgram.objects.count()}")
        print(f"   • Users: {User.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_sample_data()
