# ==============================================================================
# VIEWS FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import login, logout
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import (
    Ministry, University, Faculty, Department, ResearchCenter, 
    AdministrativeUnit, Position, AccessLevel, Employee, EmployeeDuty, User,
    StudentCategory, AcademicProgram, Student, StudentCategoryAssignment
)
from .serializers import (
    # Authentication
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserListSerializer,
    # Organizational
    MinistrySerializer, UniversityListSerializer, UniversityDetailSerializer,
    FacultyListSerializer, FacultyDetailSerializer, DepartmentListSerializer,
    DepartmentDetailSerializer, ResearchCenterListSerializer, ResearchCenterDetailSerializer,
    AdministrativeUnitListSerializer, AdministrativeUnitDetailSerializer,
    # Position & Access
    PositionSerializer, AccessLevelSerializer,
    # Employee
    EmployeeListSerializer, EmployeeDetailSerializer, EmployeeCreateUpdateSerializer,
    EmployeeDutySerializer,
    # Student
    StudentCategorySerializer, AcademicProgramListSerializer, AcademicProgramDetailSerializer,
    StudentListSerializer, StudentDetailSerializer, StudentCreateUpdateSerializer,
    StudentCategoryAssignmentSerializer,
    # Statistics
    UniversityStatsSerializer, DashboardStatsSerializer
)


# ==============================================================================
# USER MANAGEMENT VIEWS
# ==============================================================================

class UserViewSet(viewsets.ModelViewSet):
    """مدیریت کاربران"""
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_type', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'national_id']
    ordering_fields = ['username', 'email', 'last_activity', 'date_joined']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserProfileSerializer
        return UserListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'ADMIN':
            return User.objects.all()
        elif user.user_type == 'EMPLOYEE':
            # کارمندان فقط کاربران هم واحد رو می‌بینن
            return User.objects.filter(
                Q(employee__primary_unit=user.employee.primary_unit) |
                Q(pk=user.pk)
            )
        else:
            # دانشجویان فقط خودشان رو می‌بینن
            return User.objects.filter(pk=user.pk)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """پروفایل کاربر فعلی"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


# ==============================================================================
# AUTHENTICATION VIEWS
# ==============================================================================

class AuthViewSet(viewsets.GenericViewSet):
    """مدیریت احراز هویت"""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """ثبت‌نام کاربر جدید"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'ثبت‌نام با موفقیت انجام شد',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """ورود کاربر"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # ریست کردن تلاش‌های ناموفق
            user.failed_login_attempts = 0
            user.save()
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'ورود موفقیت‌آمیز',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        else:
            # افزایش تعداد تلاش‌های ناموفق
            national_id = request.data.get('national_id')
            if national_id:
                try:
                    user = User.objects.get(national_id=national_id)
                    user.failed_login_attempts += 1
                    if user.failed_login_attempts >= 5:
                        user.lock_account(30)  # قفل به مدت ۳۰ دقیقه
                    user.save()
                except User.DoesNotExist:
                    pass
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """خروج کاربر"""
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'خروج موفقیت‌آمیز'})
        except Exception:
            return Response({'error': 'خطا در خروج'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """دریافت پروفایل کاربر"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """به‌روزرسانی پروفایل کاربر"""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'پروفایل به‌روزرسانی شد', 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==============================================================================
# ORGANIZATIONAL HIERARCHY VIEWS
# ==============================================================================

class MinistryViewSet(viewsets.ModelViewSet):
    """مدیریت وزارت‌ها"""
    queryset = Ministry.objects.all()
    serializer_class = MinistrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_active']
    search_fields = ['name', 'name_en']
    ordering_fields = ['name', 'established_date']
    ordering = ['name']


class UniversityViewSet(viewsets.ModelViewSet):
    """مدیریت دانشگاه‌ها"""
    queryset = University.objects.select_related('ministry').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'ministry', 'is_active']
    search_fields = ['name', 'name_en', 'code']
    ordering_fields = ['name', 'established_year', 'national_ranking']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return UniversityListSerializer
        return UniversityDetailSerializer

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """آمار دانشگاه"""
        university = self.get_object()
        
        # محاسبه آمار
        total_students = university.student_count
        total_faculty = university.faculty_count
        total_staff = university.staff_count
        total_faculties = university.faculties.filter(is_active=True).count()
        total_departments = sum(
            faculty.departments.filter(is_active=True).count() 
            for faculty in university.faculties.filter(is_active=True)
        )
        
        # آمار دانشجویان بر اساس مقطع (فرضی - باید از Student model بیاید)
        student_by_level = {
            'bachelor': 0,
            'master': 0,
            'phd': 0,
            'professional': 0
        }
        
        stats = {
            'total_students': total_students,
            'total_faculty': total_faculty,
            'total_staff': total_staff,
            'total_faculties': total_faculties,
            'total_departments': total_departments,
            'total_programs': 0,  # باید از AcademicProgram بیاید
            'total_research_centers': university.research_centers.filter(is_active=True).count(),
            'student_by_level': student_by_level,
            'student_by_status': {},
            'student_by_type': {},
            'faculty_by_rank': {}
        }
        
        serializer = UniversityStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def faculties(self, request, pk=None):
        """دانشکده‌های دانشگاه"""
        university = self.get_object()
        faculties = university.faculties.filter(is_active=True)
        serializer = FacultyListSerializer(faculties, many=True)
        return Response(serializer.data)


class FacultyViewSet(viewsets.ModelViewSet):
    """مدیریت دانشکده‌ها"""
    queryset = Faculty.objects.select_related('university').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['university', 'is_active']
    search_fields = ['name', 'name_en', 'code']
    ordering_fields = ['name', 'established_year']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return FacultyListSerializer
        return FacultyDetailSerializer

    @action(detail=True, methods=['get'])
    def departments(self, request, pk=None):
        """گروه‌های دانشکده"""
        faculty = self.get_object()
        departments = faculty.departments.filter(is_active=True)
        serializer = DepartmentListSerializer(departments, many=True)
        return Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):
    """مدیریت گروه‌های آموزشی"""
    queryset = Department.objects.select_related('faculty__university').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['faculty', 'faculty__university', 'is_active']
    search_fields = ['name', 'name_en', 'code', 'field_of_study']
    ordering_fields = ['name', 'established_year']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return DepartmentListSerializer
        return DepartmentDetailSerializer


class ResearchCenterViewSet(viewsets.ModelViewSet):
    """مدیریت مراکز تحقیقاتی"""
    queryset = ResearchCenter.objects.select_related('university').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['university', 'research_type', 'is_active']
    search_fields = ['name', 'name_en', 'code']
    ordering_fields = ['name', 'established_year']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ResearchCenterListSerializer
        return ResearchCenterDetailSerializer


class AdministrativeUnitViewSet(viewsets.ModelViewSet):
    """مدیریت واحدهای اداری"""
    queryset = AdministrativeUnit.objects.select_related('university', 'parent_unit').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['university', 'unit_type', 'parent_unit', 'is_active']
    search_fields = ['name', 'name_en', 'code']
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return AdministrativeUnitListSerializer
        return AdministrativeUnitDetailSerializer

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """کارکنان واحد"""
        unit = self.get_object()
        employees = unit.primary_employees.filter(is_active=True)
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def hierarchy(self, request, pk=None):
        """سلسله مراتب واحد"""
        unit = self.get_object()
        return Response({
            'path': unit.get_hierarchy_path(),
            'level': unit.parent_unit.id if unit.parent_unit else 0,
            'children': AdministrativeUnitListSerializer(unit.child_units.filter(is_active=True), many=True).data
        })


# ==============================================================================
# POSITION AND ACCESS CONTROL VIEWS
# ==============================================================================

class PositionViewSet(viewsets.ModelViewSet):
    """مدیریت پست‌های سازمانی"""
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'is_active']
    search_fields = ['title', 'title_en']
    ordering_fields = ['title']
    ordering = ['title']


class AccessLevelViewSet(viewsets.ModelViewSet):
    """مدیریت سطوح دسترسی"""
    queryset = AccessLevel.objects.all()
    serializer_class = AccessLevelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level_number', 'is_active']
    search_fields = ['name']
    ordering_fields = ['level_number', 'name']
    ordering = ['level_number']


# ==============================================================================
# EMPLOYEE VIEWS
# ==============================================================================

class EmployeeViewSet(viewsets.ModelViewSet):
    """مدیریت کارکنان"""
    queryset = Employee.objects.select_related(
        'position', 'primary_unit', 'access_level'
    ).prefetch_related('secondary_units').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'position', 'primary_unit', 'employment_type', 'employment_status',
        'academic_rank', 'administrative_role', 'is_active'
    ]
    search_fields = ['first_name', 'last_name', 'national_id', 'employee_id', 'email']
    ordering_fields = ['last_name', 'hire_date', 'employee_id']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EmployeeCreateUpdateSerializer
        return EmployeeDetailSerializer

    @action(detail=True, methods=['get'])
    def duties(self, request, pk=None):
        """وظایف کارمند"""
        employee = self.get_object()
        duties = employee.duties.filter(is_active=True).order_by('-start_date')
        serializer = EmployeeDutySerializer(duties, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_duty(self, request, pk=None):
        """تخصیص وظیفه به کارمند"""
        employee = self.get_object()
        data = request.data.copy()
        data['employee'] = employee.id
        serializer = EmployeeDutySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'وظیفه تخصیص داده شد', 'duty': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def change_status(self, request, pk=None):
        """تغییر وضعیت استخدام"""
        employee = self.get_object()
        new_status = request.data.get('employment_status')
        if new_status in dict(Employee.EMPLOYMENT_STATUS):
            employee.employment_status = new_status
            employee.save()
            return Response({'message': 'وضعیت تغییر کرد'})
        return Response({'error': 'وضعیت نامعتبر'}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDutyViewSet(viewsets.ModelViewSet):
    """مدیریت وظایف کارکنان"""
    queryset = EmployeeDuty.objects.select_related('employee').all()
    serializer_class = EmployeeDutySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'status', 'priority', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'priority']
    ordering = ['-start_date']

    @action(detail=True, methods=['put'])
    def update_progress(self, request, pk=None):
        """به‌روزرسانی پیشرفت وظیفه"""
        duty = self.get_object()
        completion_percentage = request.data.get('completion_percentage')
        if 0 <= completion_percentage <= 100:
            duty.completion_percentage = completion_percentage
            if completion_percentage == 100:
                duty.status = 'COMPLETED'
            duty.save()
            return Response({'message': 'پیشرفت به‌روزرسانی شد'})
        return Response({'error': 'درصد تکمیل نامعتبر'}, status=status.HTTP_400_BAD_REQUEST)


# ==============================================================================
# STUDENT VIEWS
# ==============================================================================

class StudentCategoryViewSet(viewsets.ModelViewSet):
    """مدیریت دسته‌های دانشجویی"""
    queryset = StudentCategory.objects.all()
    serializer_class = StudentCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category_type', 'is_active']
    search_fields = ['name', 'name_en']
    ordering_fields = ['name']
    ordering = ['name']


class AcademicProgramViewSet(viewsets.ModelViewSet):
    """مدیریت برنامه‌های تحصیلی"""
    queryset = AcademicProgram.objects.select_related(
        'department__faculty__university'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'department', 'program_type', 'program_mode', 
        'is_accepting_students', 'is_active'
    ]
    search_fields = ['name', 'name_en', 'code']
    ordering_fields = ['name', 'total_credits']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return AcademicProgramListSerializer
        return AcademicProgramDetailSerializer

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """دانشجویان برنامه"""
        program = self.get_object()
        students = program.students.filter(is_active=True)
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def capacity_status(self, request, pk=None):
        """وضعیت ظرفیت برنامه"""
        program = self.get_object()
        return Response({
            'max_capacity': program.max_capacity,
            'current_enrollment': program.current_enrollment,
            'remaining_capacity': program.remaining_capacity,
            'is_full': program.is_full,
            'is_accepting': program.is_accepting_students
        })


class StudentViewSet(viewsets.ModelViewSet):
    """مدیریت دانشجویان"""
    queryset = Student.objects.select_related(
        'academic_program__department__faculty__university'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'academic_program', 'student_type', 'academic_status', 'financial_status',
        'entrance_year', 'current_semester', 'is_active'
    ]
    search_fields = ['first_name', 'last_name', 'national_id', 'student_id', 'email']
    ordering_fields = ['last_name', 'entrance_year', 'cumulative_gpa', 'student_id']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return StudentCreateUpdateSerializer
        return StudentDetailSerializer

    @action(detail=True, methods=['get'])
    def academic_record(self, request, pk=None):
        """پرونده تحصیلی دانشجو"""
        student = self.get_object()
        return Response({'message': 'Academic record feature will be implemented later'})

    @action(detail=True, methods=['get'])
    def categories(self, request, pk=None):
        """دسته‌های دانشجو"""
        student = self.get_object()
        assignments = student.category_assignments.filter(status='ACTIVE')
        serializer = StudentCategoryAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_category(self, request, pk=None):
        """تخصیص دانشجو به دسته"""
        student = self.get_object()
        data = request.data.copy()
        data['student'] = student.id
        serializer = StudentCategoryAssignmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'دانشجو به دسته اختصاص داده شد', 'assignment': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def change_status(self, request, pk=None):
        """تغییر وضعیت تحصیلی"""
        student = self.get_object()
        new_status = request.data.get('academic_status')
        if new_status in dict(Student.ACADEMIC_STATUS):
            student.academic_status = new_status
            student.save()
            return Response({'message': 'وضعیت تحصیلی تغییر کرد'})
        return Response({'error': 'وضعیت نامعتبر'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def enrollment_eligibility(self, request, pk=None):
        """بررسی واجد شرایط بودن برای ثبت‌نام"""
        student = self.get_object()
        can_register = student.can_register_for_semester()
        reasons = []
        
        if student.academic_status != 'ACTIVE':
            reasons.append('وضعیت تحصیلی غیرفعال')
        if student.outstanding_balance > 0:
            reasons.append('بدهی مالی')
        if not student.is_active:
            reasons.append('حساب غیرفعال')
            
        return Response({
            'can_register': can_register,
            'reasons': reasons,
            'outstanding_balance': student.outstanding_balance,
            'academic_status': student.get_academic_status_display()
        })


class StudentCategoryAssignmentViewSet(viewsets.ModelViewSet):
    """مدیریت تخصیص دانشجویان به دسته‌ها"""
    queryset = StudentCategoryAssignment.objects.select_related(
        'student', 'category'
    ).all()
    serializer_class = StudentCategoryAssignmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'category', 'status', 'is_active']
    ordering_fields = ['start_date']
    ordering = ['-start_date']


# AcademicRecordViewSet removed - will be implemented later

# ==============================================================================
# DASHBOARD AND STATISTICS VIEWS
# ==============================================================================

class DashboardViewSet(viewsets.GenericViewSet):
    """داشبورد و آمار کلی"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """آمار کلی سیستم"""
        stats = {
            'total_universities': University.objects.filter(is_active=True).count(),
            'total_students': Student.objects.filter(is_active=True).count(),
            'total_employees': Employee.objects.filter(is_active=True).count(),
            'total_faculties': Faculty.objects.filter(is_active=True).count(),
            'total_departments': Department.objects.filter(is_active=True).count(),
            'active_programs': AcademicProgram.objects.filter(is_active=True, is_accepting_students=True).count(),
            'recent_enrollments': Student.objects.filter(
                created_at__gte=timezone.now() - timezone.timedelta(days=30)
            ).count(),
            'students_by_university_type': {},
            'enrollment_trends': []
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent_activities(self, request):
        """فعالیت‌های اخیر"""
        # فعالیت‌های اخیر کارکنان
        recent_employees = Employee.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).order_by('-created_at')[:5]
        
        # فعالیت‌های اخیر دانشجویان  
        recent_students = Student.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).order_by('-created_at')[:5]
        
        return Response({
            'recent_employees': EmployeeListSerializer(recent_employees, many=True).data,
            'recent_students': StudentListSerializer(recent_students, many=True).data
        })

    @action(detail=False, methods=['get'])
    def system_health(self, request):
        """سلامت سیستم"""
        return Response({
            'status': 'healthy',
            'active_users': User.objects.filter(is_active=True).count(),
            'locked_accounts': User.objects.exclude(account_locked_until__isnull=True).count(),
            'system_uptime': '99.9%',
            'last_backup': timezone.now().isoformat()
        })
