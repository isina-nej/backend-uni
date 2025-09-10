from django.core.management.base import BaseCommand
from apps.users.models import OrganizationalUnit, Position, Permission, User
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Create initial university organizational structure and users'

    def handle(self, *args, **options):
        self.stdout.write('Creating university organizational structure...')
        
        # ایجاد دانشگاه
        university, created = OrganizationalUnit.objects.get_or_create(
            code='UNIV',
            defaults={
                'name': 'دانشگاه',
                'unit_type': 'university',
                'order': 1
            }
        )
        
        # ایجاد حوزه ریاست
        presidency, created = OrganizationalUnit.objects.get_or_create(
            code='PRES',
            defaults={
                'name': 'حوزه ریاست',
                'unit_type': 'presidency',
                'parent': university,
                'order': 1
            }
        )
        
        # ایجاد معاونت‌ها
        vice_presidencies = [
            ('VP-EDU', 'معاونت آموزشی', 'vice_education'),
            ('VP-RES', 'معاونت پژوهش و فناوری', 'vice_research'),
            ('VP-STU', 'معاونت دانشجویی', 'vice_student'),
            ('VP-PLAN', 'معاونت برنامه‌ریزی و توسعه منابع', 'vice_planning'),
            ('VP-ADMIN', 'معاونت اداری و مالی', 'vice_admin'),
            ('VP-CONST', 'معاونت عمرانی', 'vice_construction'),
            ('VP-CULT', 'معاونت فرهنگی و اجتماعی', 'vice_cultural'),
            ('VP-INTL', 'معاونت بین‌الملل', 'vice_international'),
            ('VP-TECH', 'معاونت فناوری‌های دیجیتال', 'vice_technology'),
        ]
        
        for i, (code, name, unit_type) in enumerate(vice_presidencies, 1):
            OrganizationalUnit.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'unit_type': unit_type,
                    'parent': university,
                    'order': i + 1
                }
            )
        
        # ایجاد دانشکده‌ها
        faculties = [
            ('FAC-ENG', 'دانشکده فنی و مهندسی'),
            ('FAC-SCI', 'دانشکده علوم پایه'),
            ('FAC-HUM', 'دانشکده علوم انسانی'),
            ('FAC-MGT', 'دانشکده مدیریت'),
            ('FAC-MED', 'دانشکده پزشکی'),
            ('FAC-ART', 'دانشکده هنر'),
        ]
        
        for i, (code, name) in enumerate(faculties, 1):
            faculty, created = OrganizationalUnit.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'unit_type': 'faculty',
                    'parent': university,
                    'order': 100 + i
                }
            )
            
            # ایجاد گروه‌های آموزشی برای هر دانشکده
            if code == 'FAC-ENG':
                departments = [
                    ('DEPT-CS', 'گروه مهندسی کامپیوتر'),
                    ('DEPT-EE', 'گروه مهندسی برق'),
                    ('DEPT-ME', 'گروه مهندسی مکانیک'),
                    ('DEPT-CE', 'گروه مهندسی عمران'),
                ]
                for j, (dept_code, dept_name) in enumerate(departments, 1):
                    OrganizationalUnit.objects.get_or_create(
                        code=dept_code,
                        defaults={
                            'name': dept_name,
                            'unit_type': 'department',
                            'parent': faculty,
                            'order': j
                        }
                    )
        
        self.stdout.write('Creating positions...')
        
        # ایجاد سمت‌ها
        positions_data = [
            # سمت‌های مدیریتی
            ('رئیس دانشگاه', presidency, 'executive', 5),
            ('معاون آموزشی', OrganizationalUnit.objects.get(code='VP-EDU'), 'executive', 4),
            ('معاون پژوهشی', OrganizationalUnit.objects.get(code='VP-RES'), 'executive', 4),
            ('دکان دانشکده', OrganizationalUnit.objects.get(code='FAC-ENG'), 'executive', 4),
            ('رئیس گروه', OrganizationalUnit.objects.get(code='DEPT-CS'), 'senior', 3),
            
            # سمت‌های آکادمیک
            ('استاد', OrganizationalUnit.objects.get(code='DEPT-CS'), 'academic', 4),
            ('دانشیار', OrganizationalUnit.objects.get(code='DEPT-CS'), 'academic', 3),
            ('استادیار', OrganizationalUnit.objects.get(code='DEPT-CS'), 'academic', 3),
            ('مربی', OrganizationalUnit.objects.get(code='DEPT-CS'), 'academic', 2),
            
            # سمت‌های اداری
            ('مدیر امور آموزش', OrganizationalUnit.objects.get(code='VP-EDU'), 'middle', 3),
            ('کارشناس آموزش', OrganizationalUnit.objects.get(code='VP-EDU'), 'specialist', 2),
            ('منشی', OrganizationalUnit.objects.get(code='VP-EDU'), 'administrative', 1),
        ]
        
        for title, unit, level, authority in positions_data:
            Position.objects.get_or_create(
                title=title,
                organizational_unit=unit,
                defaults={
                    'position_level': level,
                    'authority_level': authority,
                    'job_description': f'شرح وظایف {title}'
                }
            )
        
        self.stdout.write('Creating permissions...')
        
        # ایجاد مجوزها
        permissions_data = [
            ('مشاهده کاربران', 'view_users', 'read', 'users'),
            ('ویرایش کاربران', 'edit_users', 'write', 'users'),
            ('حذف کاربران', 'delete_users', 'delete', 'users'),
            ('مدیریت دروس', 'manage_courses', 'manage', 'courses'),
            ('ثبت نمرات', 'assign_grades', 'write', 'grades'),
            ('مشاهده گزارش‌ها', 'view_reports', 'report', 'reports'),
            ('مدیریت مالی', 'manage_financial', 'financial', 'financial'),
            ('بازرسی سیستم', 'audit_system', 'audit', 'system'),
        ]
        
        for name, codename, perm_type, module in permissions_data:
            Permission.objects.get_or_create(
                codename=codename,
                defaults={
                    'name': name,
                    'permission_type': perm_type,
                    'module': module,
                    'description': f'اجازه {name}'
                }
            )
        
        self.stdout.write('Creating sample users...')
        
        # ایجاد کاربران نمونه
        sample_users = [
            {
                'username': 'admin',
                'password': 'admin123',
                'role': 'super_admin',
                'persian_first_name': 'مدیر',
                'persian_last_name': 'سیستم',
                'is_superuser': True,
                'is_staff': True,
                'primary_unit': presidency
            },
            {
                'username': 'president',
                'password': 'president123',
                'role': 'president',
                'persian_first_name': 'علی',
                'persian_last_name': 'احمدی',
                'employee_id': 'EMP001',
                'primary_unit': presidency
            },
            {
                'username': 'prof.smith',
                'password': 'password123',
                'role': 'faculty',
                'persian_first_name': 'محمد',
                'persian_last_name': 'رضایی',
                'employee_id': 'EMP002',
                'academic_rank': 'professor',
                'primary_unit': OrganizationalUnit.objects.get(code='DEPT-CS')
            },
            {
                'username': 'student1',
                'password': 'password123',
                'role': 'undergraduate',
                'persian_first_name': 'فاطمه',
                'persian_last_name': 'محمدی',
                'student_id': 'STU001',
                'field_of_study': 'مهندسی کامپیوتر',
                'primary_unit': OrganizationalUnit.objects.get(code='DEPT-CS')
            },
            {
                'username': 'staff1',
                'password': 'password123',
                'role': 'administrative',
                'persian_first_name': 'حسن',
                'persian_last_name': 'کریمی',
                'employee_id': 'EMP003',
                'employment_type': 'permanent',
                'primary_unit': OrganizationalUnit.objects.get(code='VP-EDU')
            }
        ]
        
        for user_data in sample_users:
            username = user_data.pop('username')
            password = user_data.pop('password')
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    **user_data,
                    'password': make_password(password),
                    'email': f'{username}@university.edu',
                    'is_active': True,
                    'is_verified': True
                }
            )
            
            if created:
                self.stdout.write(f'Created user: {username}')
        
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully created university organizational structure and sample users!'
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                '\nSample login credentials:\n'
                'Admin: admin / admin123\n'
                'President: president / president123\n'
                'Professor: prof.smith / password123\n'
                'Student: student1 / password123\n'
                'Staff: staff1 / password123'
            )
        )
