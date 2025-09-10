from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from .models import (
    Ministry, University, Faculty, Department, ResearchCenter, AdministrativeUnit,
    Position, Employee, Student, AccessControl, UserAccess, AuditLog,
    User, OrganizationalUnit, UserPosition, Permission, UserPermission, AccessLog
)
from .serializers import (
    MinistrySerializer, UniversitySerializer, FacultySerializer, DepartmentSerializer,
    ResearchCenterSerializer, AdministrativeUnitSerializer, PositionSerializer,
    EmployeeSerializer, StudentSerializer, AccessControlSerializer,
    UserAccessSerializer, AuditLogSerializer,
    UserSerializer, UserBasicSerializer, OrganizationalUnitSerializer,
    UserPositionSerializer, PermissionSerializer, UserPermissionSerializer,
    AccessLogOldSerializer
)


class MinistryViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای وزارت‌ها
    """
    queryset = Ministry.objects.filter(is_active=True)
    serializer_class = MinistrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'is_active']
    search_fields = ['name', 'name_en', 'minister']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def universities(self, request, pk=None):
        """دریافت دانشگاه‌های یک وزارت"""
        ministry = self.get_object()
        universities = ministry.university_set.filter(is_active=True)
        serializer = UniversitySerializer(universities, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """آمار وزارت"""
        ministry = self.get_object()
        universities = ministry.university_set.filter(is_active=True)

        stats = {
            'universities_count': universities.count(),
            'total_students': universities.aggregate(total=Count('students'))['total'] or 0,
            'total_faculty': universities.aggregate(total=Count('employees', filter=Q(employees__employee_type='ACADEMIC')))['total'] or 0,
            'total_staff': universities.aggregate(total=Count('employees', filter=~Q(employees__employee_type='ACADEMIC')))['total'] or 0,
        }
        return Response(stats)


class UniversityViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای دانشگاه‌ها
    """
    queryset = University.objects.filter(is_active=True)
    serializer_class = UniversitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ministry', 'type', 'is_active']
    search_fields = ['name', 'name_en', 'code', 'president']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def faculties(self, request, pk=None):
        """دریافت دانشکده‌های دانشگاه"""
        university = self.get_object()
        faculties = university.faculties.filter(is_active=True)
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def research_centers(self, request, pk=None):
        """دریافت مراکز پژوهشی دانشگاه"""
        university = self.get_object()
        centers = university.research_centers.filter(is_active=True)
        serializer = ResearchCenterSerializer(centers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def administrative_units(self, request, pk=None):
        """دریافت واحدهای اداری دانشگاه"""
        university = self.get_object()
        units = university.administrative_units.filter(is_active=True)
        serializer = AdministrativeUnitSerializer(units, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """دریافت کارکنان دانشگاه"""
        university = self.get_object()
        employees = university.employees.filter(is_active=True)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """دریافت دانشجویان دانشگاه"""
        university = self.get_object()
        students = university.students.filter(is_active=True)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """آمار دانشگاه"""
        university = self.get_object()

        stats = {
            'faculties_count': university.faculties.filter(is_active=True).count(),
            'departments_count': sum(faculty.departments.filter(is_active=True).count() for faculty in university.faculties.filter(is_active=True)),
            'research_centers_count': university.research_centers.filter(is_active=True).count(),
            'administrative_units_count': university.administrative_units.filter(is_active=True).count(),
            'students_count': university.students.filter(is_active=True).count(),
            'employees_count': university.employees.filter(is_active=True).count(),
            'academic_staff_count': university.employees.filter(employee_type='ACADEMIC', is_active=True).count(),
            'administrative_staff_count': university.employees.filter(employee_type='ADMINISTRATIVE', is_active=True).count(),
        }
        return Response(stats)


class FacultyViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای دانشکده‌ها
    """
    queryset = Faculty.objects.filter(is_active=True)
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['university', 'is_active']
    search_fields = ['name', 'name_en', 'code', 'dean']
    ordering = ['university', 'name']

    @action(detail=True, methods=['get'])
    def departments(self, request, pk=None):
        """دریافت گروه‌های دانشکده"""
        faculty = self.get_object()
        departments = faculty.departments.filter(is_active=True)
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """دریافت کارکنان دانشکده"""
        faculty = self.get_object()
        employees = Employee.objects.filter(
            Q(department__faculty=faculty) | Q(administrative_unit__university=faculty.university),
            is_active=True
        ).distinct()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای گروه‌های آموزشی
    """
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['faculty', 'is_active']
    search_fields = ['name', 'name_en', 'code', 'head', 'field_of_study']
    ordering = ['faculty', 'name']

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """دریافت کارکنان گروه"""
        department = self.get_object()
        employees = department.employees.filter(is_active=True)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """دریافت دانشجویان گروه"""
        department = self.get_object()
        students = department.students.filter(is_active=True)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class ResearchCenterViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای مراکز پژوهشی
    """
    queryset = ResearchCenter.objects.filter(is_active=True)
    serializer_class = ResearchCenterSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['university', 'is_active']
    search_fields = ['name', 'name_en', 'code', 'director', 'research_field']
    ordering = ['university', 'name']

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """دریافت پژوهشگران مرکز"""
        center = self.get_object()
        employees = center.employees.filter(is_active=True)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class AdministrativeUnitViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای واحدهای اداری
    """
    queryset = AdministrativeUnit.objects.filter(is_active=True)
    serializer_class = AdministrativeUnitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['university', 'category', 'unit_type', 'is_active']
    search_fields = ['name', 'name_en', 'code', 'manager']
    ordering = ['university', 'name']

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """دریافت کارکنان واحد اداری"""
        unit = self.get_object()
        employees = unit.employees.filter(is_active=True)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class PositionViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای سمت‌های سازمانی
    """
    queryset = Position.objects.filter(is_active=True)
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['organizational_unit', 'position_level', 'authority_level', 'employment_type', 'is_active']
    search_fields = ['title', 'title_en', 'code', 'job_description']
    ordering = ['position_level', 'title']

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """دریافت کارکنان دارای این سمت"""
        position = self.get_object()
        employees = position.employees.filter(is_active=True)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای کارکنان
    """
    queryset = Employee.objects.filter(is_active=True)
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['university', 'employee_type', 'position', 'department', 'administrative_unit', 'research_center', 'gender', 'status', 'is_active']
    search_fields = ['first_name', 'last_name', 'first_name_en', 'last_name_en', 'national_id', 'employee_id', 'email']
    ordering = ['last_name', 'first_name']

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """آمار کارکنان"""
        stats = {
            'total_employees': self.queryset.count(),
            'by_type': {},
            'by_gender': {},
            'by_academic_rank': {},
            'average_performance': self.queryset.aggregate(avg=Avg('performance_score'))['avg'] or 0,
        }

        # آمار بر اساس نوع کارمند
        for employee_type, _ in Employee.EMPLOYEE_TYPE_CHOICES:
            count = self.queryset.filter(employee_type=employee_type).count()
            if count > 0:
                stats['by_type'][employee_type] = count

        # آمار بر اساس جنسیت
        for gender, _ in [('MALE', 'مرد'), ('FEMALE', 'زن')]:
            count = self.queryset.filter(gender=gender).count()
            if count > 0:
                stats['by_gender'][gender] = count

        # آمار بر اساس رتبه علمی
        for rank, _ in Employee.ACADEMIC_RANK_CHOICES:
            count = self.queryset.filter(academic_rank=rank).count()
            if count > 0:
                stats['by_academic_rank'][rank] = count

        return Response(stats)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای دانشجویان
    """
    queryset = Student.objects.filter(is_active=True)
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['university', 'department', 'student_type', 'academic_level', 'academic_status', 'financial_status', 'gender', 'is_active', 'is_international']
    search_fields = ['first_name', 'last_name', 'first_name_en', 'last_name_en', 'national_id', 'student_id', 'email']
    ordering = ['last_name', 'first_name']

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """آمار دانشجویان"""
        stats = {
            'total_students': self.queryset.count(),
            'by_academic_level': {},
            'by_student_type': {},
            'by_gender': {},
            'by_financial_status': {},
            'international_students': self.queryset.filter(is_international=True).count(),
            'veteran_children': self.queryset.filter(is_veteran_child=True).count(),
            'athletes': self.queryset.filter(is_athlete=True).count(),
            'average_gpa': self.queryset.aggregate(avg=Avg('gpa'))['avg'] or 0,
        }

        # آمار بر اساس مقطع تحصیلی
        for level, _ in Student.ACADEMIC_LEVEL_CHOICES:
            count = self.queryset.filter(academic_level=level).count()
            if count > 0:
                stats['by_academic_level'][level] = count

        # آمار بر اساس نوع پذیرش
        for student_type, _ in Student.STUDENT_TYPE_CHOICES:
            count = self.queryset.filter(student_type=student_type).count()
            if count > 0:
                stats['by_student_type'][student_type] = count

        # آمار بر اساس جنسیت
        for gender, _ in [('MALE', 'مرد'), ('FEMALE', 'زن')]:
            count = self.queryset.filter(gender=gender).count()
            if count > 0:
                stats['by_gender'][gender] = count

        # آمار بر اساس وضعیت مالی
        for status, _ in Student.FINANCIAL_STATUS_CHOICES:
            count = self.queryset.filter(financial_status=status).count()
            if count > 0:
                stats['by_financial_status'][status] = count

        return Response(stats)


class AccessControlViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای کنترل دسترسی
    """
    queryset = AccessControl.objects.filter(is_active=True)
    serializer_class = AccessControlSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['permission_type', 'module', 'resource_type', 'is_active']
    search_fields = ['name', 'codename', 'description']
    ordering = ['module', 'name']


class UserAccessViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای دسترسی‌های کاربران
    """
    queryset = UserAccess.objects.filter(is_active=True)
    serializer_class = UserAccessSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'permission', 'university', 'faculty', 'department', 'administrative_unit', 'is_active']
    ordering = ['-granted_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'super_admin':
            return self.queryset
        # کاربران عادی فقط دسترسی‌های خود را می‌بینند
        return self.queryset.filter(user=user)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet برای لاگ فعالیت‌ها
    """
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'action', 'resource_type', 'success']
    search_fields = ['user__username', 'action', 'resource_type', 'ip_address']
    ordering = ['-timestamp']

    def get_queryset(self):
        user = self.request.user
        # فقط ادمین‌ها و بازرسان می‌توانند لاگ‌ها را ببینند
        if user.is_superuser or user.role in ['super_admin', 'auditor']:
            return self.queryset
        # کاربران عادی فقط لاگ‌های خود را می‌بینند
        return self.queryset.filter(user=user)


# ViewSets قدیمی برای سازگاری
class OrganizationalUnitViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای واحدهای سازمانی (سازگاری با مدل‌های قدیمی)
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


class AccessLogOldViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet برای لاگ دسترسی (فقط خواندنی)
    """
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogOldSerializer
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
