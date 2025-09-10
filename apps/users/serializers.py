# ==============================================================================
# SERIALIZERS FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from config.validators import AdvancedValidators
from .models import (
    Ministry, University, Faculty, Department, ResearchCenter, 
    AdministrativeUnit, Position, AccessLevel, Employee, EmployeeDuty, User,
    StudentCategory, AcademicProgram, Student, StudentCategoryAssignment
)


# ==============================================================================
# AUTHENTICATION SERIALIZERS
# ==============================================================================

class UserRegistrationSerializer(serializers.ModelSerializer):
    """ثبت‌نام کاربر جدید"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'national_id', 'username', 'email', 'password', 'password_confirm',
            'user_type', 'phone', 'first_name', 'last_name', 'birth_date',
            'preferred_language', 'timezone'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(_("رمزهای عبور مطابقت ندارند"))
        attrs.pop('password_confirm')
        
        # Apply advanced validation
        try:
            AdvancedValidators.validate_student_registration(attrs)
        except serializers.ValidationError:
            raise
            
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """ورود کاربر"""
    national_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        national_id = attrs.get('national_id')
        password = attrs.get('password')

        if national_id and password:
            user = authenticate(username=national_id, password=password)
            
            if not user:
                raise serializers.ValidationError(_("کد ملی یا رمز عبور اشتباه است"))
            
            if not user.is_active:
                raise serializers.ValidationError(_("حساب کاربری غیرفعال است"))
            
            if user.is_account_locked:
                raise serializers.ValidationError(_("حساب کاربری قفل شده است"))
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError(_("کد ملی و رمز عبور الزامی است"))


class UserListSerializer(serializers.ModelSerializer):
    """لیست کاربران"""
    full_name = serializers.SerializerMethodField()
    user_type_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 'user_type', 'user_type_display',
            'phone', 'is_active', 'last_activity'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_user_type_display(self, obj):
        return obj.get_user_type_display()


class UserProfileSerializer(serializers.ModelSerializer):
    """پروفایل کاربر"""
    employee_info = serializers.SerializerMethodField()
    student_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'national_id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone', 'avatar', 'preferred_language', 'timezone',
            'two_factor_enabled', 'last_activity', 'is_active',
            'employee_info', 'student_info'
        ]
        read_only_fields = ['id', 'national_id', 'last_activity']

    def get_employee_info(self, obj):
        if obj.employee:
            return {
                'id': obj.employee.id,
                'employee_id': obj.employee.employee_id,
                'position': obj.employee.position.title,
                'unit': obj.employee.primary_unit.name,
                'academic_rank': obj.employee.get_academic_rank_display(),
                'hire_date': obj.employee.hire_date
            }
        return None

    def get_student_info(self, obj):
        if obj.student:
            return {
                'id': obj.student.id,
                'student_id': obj.student.student_id,
                'program': obj.student.academic_program.name,
                'current_semester': obj.student.current_semester,
                'gpa': obj.student.cumulative_gpa,
                'status': obj.student.get_academic_status_display()
            }
        return None


# ==============================================================================
# ORGANIZATIONAL HIERARCHY SERIALIZERS
# ==============================================================================

class MinistrySerializer(serializers.ModelSerializer):
    """وزارت"""
    universities_count = serializers.SerializerMethodField()

    class Meta:
        model = Ministry
        fields = '__all__'

    def get_universities_count(self, obj):
        return obj.universities.filter(is_active=True).count()


class UniversityListSerializer(serializers.ModelSerializer):
    """لیست دانشگاه‌ها"""
    ministry_name = serializers.CharField(source='ministry.name', read_only=True)
    faculties_count = serializers.SerializerMethodField()
    students_count = serializers.IntegerField(source='student_count', read_only=True)

    class Meta:
        model = University
        fields = [
            'id', 'name', 'name_en', 'code', 'type', 'ministry_name',
            'address', 'phone', 'website', 'established_year',
            'faculties_count', 'students_count', 'national_ranking',
            'is_active'
        ]

    def get_faculties_count(self, obj):
        return obj.faculties.filter(is_active=True).count()


class UniversityDetailSerializer(serializers.ModelSerializer):
    """جزئیات دانشگاه"""
    ministry = MinistrySerializer(read_only=True)
    faculties = serializers.SerializerMethodField()
    research_centers = serializers.SerializerMethodField()
    administrative_units = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = '__all__'

    def get_faculties(self, obj):
        faculties = obj.faculties.filter(is_active=True)
        return FacultyListSerializer(faculties, many=True).data

    def get_research_centers(self, obj):
        centers = obj.research_centers.filter(is_active=True)
        return ResearchCenterListSerializer(centers, many=True).data

    def get_administrative_units(self, obj):
        units = obj.administrative_units.filter(is_active=True)
        return AdministrativeUnitListSerializer(units, many=True).data


class FacultyListSerializer(serializers.ModelSerializer):
    """لیست دانشکده‌ها"""
    university_name = serializers.CharField(source='university.name', read_only=True)
    departments_count = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = [
            'id', 'name', 'name_en', 'code', 'university_name',
            'phone', 'email', 'departments_count', 'student_count',
            'faculty_member_count', 'is_active'
        ]

    def get_departments_count(self, obj):
        return obj.departments.filter(is_active=True).count()


class FacultyDetailSerializer(serializers.ModelSerializer):
    """جزئیات دانشکده"""
    university = UniversityListSerializer(read_only=True)
    departments = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = '__all__'

    def get_departments(self, obj):
        departments = obj.departments.filter(is_active=True)
        return DepartmentListSerializer(departments, many=True).data


class DepartmentListSerializer(serializers.ModelSerializer):
    """لیست گروه‌های آموزشی"""
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    university_name = serializers.CharField(source='faculty.university.name', read_only=True)

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'name_en', 'code', 'faculty_name', 'university_name',
            'field_of_study', 'phone', 'email', 'student_count',
            'faculty_member_count', 'course_count', 'is_active'
        ]


class DepartmentDetailSerializer(serializers.ModelSerializer):
    """جزئیات گروه آموزشی"""
    faculty = FacultyListSerializer(read_only=True)
    academic_programs = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = '__all__'

    def get_academic_programs(self, obj):
        programs = obj.academic_programs.filter(is_active=True)
        return AcademicProgramListSerializer(programs, many=True).data


class ResearchCenterListSerializer(serializers.ModelSerializer):
    """لیست مراکز تحقیقاتی"""
    university_name = serializers.CharField(source='university.name', read_only=True)

    class Meta:
        model = ResearchCenter
        fields = [
            'id', 'name', 'name_en', 'code', 'university_name',
            'research_type', 'phone', 'email', 'researcher_count',
            'project_count', 'publication_count', 'is_active'
        ]


class ResearchCenterDetailSerializer(serializers.ModelSerializer):
    """جزئیات مرکز تحقیقاتی"""
    university = UniversityListSerializer(read_only=True)

    class Meta:
        model = ResearchCenter
        fields = '__all__'


class AdministrativeUnitListSerializer(serializers.ModelSerializer):
    """لیست واحدهای اداری"""
    university_name = serializers.CharField(source='university.name', read_only=True)
    parent_unit_name = serializers.CharField(source='parent_unit.name', read_only=True)

    class Meta:
        model = AdministrativeUnit
        fields = [
            'id', 'name', 'name_en', 'code', 'unit_type', 'university_name',
            'parent_unit_name', 'phone', 'email', 'employee_count', 'is_active'
        ]


class AdministrativeUnitDetailSerializer(serializers.ModelSerializer):
    """جزئیات واحد اداری"""
    university = UniversityListSerializer(read_only=True)
    parent_unit = AdministrativeUnitListSerializer(read_only=True)
    child_units = AdministrativeUnitListSerializer(many=True, read_only=True)
    employees = serializers.SerializerMethodField()

    class Meta:
        model = AdministrativeUnit
        fields = '__all__'

    def get_employees(self, obj):
        employees = obj.primary_employees.filter(is_active=True)
        return EmployeeListSerializer(employees, many=True).data


# ==============================================================================
# POSITION AND ACCESS CONTROL SERIALIZERS
# ==============================================================================

class PositionSerializer(serializers.ModelSerializer):
    """پست‌های سازمانی"""
    employees_count = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = '__all__'

    def get_employees_count(self, obj):
        return obj.employee_set.filter(is_active=True).count()


class AccessLevelSerializer(serializers.ModelSerializer):
    """سطوح دسترسی"""
    class Meta:
        model = AccessLevel
        fields = '__all__'


# ==============================================================================
# EMPLOYEE SERIALIZERS
# ==============================================================================

class EmployeeListSerializer(serializers.ModelSerializer):
    """لیست کارکنان"""
    position_title = serializers.CharField(source='position.title', read_only=True)
    unit_name = serializers.CharField(source='primary_unit.name', read_only=True)
    university_name = serializers.CharField(source='primary_unit.university.name', read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'first_name', 'last_name', 'national_id',
            'position_title', 'unit_name', 'university_name', 'academic_rank',
            'administrative_role', 'email', 'phone', 'hire_date',
            'employment_status', 'is_active'
        ]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """جزئیات کارمند"""
    position = PositionSerializer(read_only=True)
    primary_unit = AdministrativeUnitListSerializer(read_only=True)
    secondary_units = AdministrativeUnitListSerializer(many=True, read_only=True)
    access_level = AccessLevelSerializer(read_only=True)
    duties = serializers.SerializerMethodField()
    years_of_service = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = '__all__'

    def get_duties(self, obj):
        duties = obj.duties.filter(is_active=True).order_by('-start_date')[:5]
        return EmployeeDutySerializer(duties, many=True).data


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    """ایجاد/ویرایش کارمند"""
    class Meta:
        model = Employee
        fields = [
            'national_id', 'first_name', 'last_name', 'first_name_en', 'last_name_en',
            'birth_date', 'gender', 'email', 'phone', 'address', 'employee_id',
            'hire_date', 'employment_type', 'employment_status', 'position',
            'primary_unit', 'secondary_units', 'academic_rank', 'administrative_role',
            'access_level', 'salary_grade', 'bank_account', 'education_level',
            'field_of_study', 'contract_end_date', 'retirement_date', 'notes'
        ]

    def validate_national_id(self, value):
        """اعتبارسنجی کد ملی"""
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("کد ملی باید ۱۰ رقم باشد")
        return value

    def validate_employee_id(self, value):
        """اعتبارسنجی شماره پرسنلی"""
        if self.instance:
            # در حالت ویرایش
            if Employee.objects.exclude(pk=self.instance.pk).filter(employee_id=value).exists():
                raise serializers.ValidationError("این شماره پرسنلی قبلاً استفاده شده است")
        else:
            # در حالت ایجاد
            if Employee.objects.filter(employee_id=value).exists():
                raise serializers.ValidationError("این شماره پرسنلی قبلاً استفاده شده است")
        return value


class EmployeeDutySerializer(serializers.ModelSerializer):
    """وظایف کارکنان"""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)

    class Meta:
        model = EmployeeDuty
        fields = '__all__'


# ==============================================================================
# STUDENT SERIALIZERS
# ==============================================================================

class StudentCategorySerializer(serializers.ModelSerializer):
    """دسته‌های دانشجویی"""
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = StudentCategory
        fields = '__all__'

    def get_students_count(self, obj):
        return obj.student_assignments.filter(status='ACTIVE').count()


class AcademicProgramListSerializer(serializers.ModelSerializer):
    """لیست برنامه‌های تحصیلی"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    faculty_name = serializers.CharField(source='department.faculty.name', read_only=True)
    university_name = serializers.CharField(source='department.faculty.university.name', read_only=True)
    remaining_capacity = serializers.ReadOnlyField()

    class Meta:
        model = AcademicProgram
        fields = [
            'id', 'name', 'name_en', 'code', 'program_type', 'program_mode',
            'department_name', 'faculty_name', 'university_name',
            'total_credits', 'duration_semesters', 'tuition_per_semester',
            'max_capacity', 'current_enrollment', 'remaining_capacity',
            'is_accepting_students', 'is_active'
        ]


class AcademicProgramDetailSerializer(serializers.ModelSerializer):
    """جزئیات برنامه تحصیلی"""
    department = DepartmentListSerializer(read_only=True)
    students = serializers.SerializerMethodField()
    remaining_capacity = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()

    class Meta:
        model = AcademicProgram
        fields = '__all__'

    def get_students(self, obj):
        students = obj.students.filter(is_active=True)[:10]  # فقط ۱۰ نفر اول
        return StudentListSerializer(students, many=True).data


class StudentListSerializer(serializers.ModelSerializer):
    """لیست دانشجویان"""
    program_name = serializers.CharField(source='academic_program.name', read_only=True)
    department_name = serializers.CharField(source='academic_program.department.name', read_only=True)
    faculty_name = serializers.CharField(source='academic_program.department.faculty.name', read_only=True)
    university_name = serializers.CharField(source='university.name', read_only=True)
    academic_standing = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'last_name', 'national_id',
            'program_name', 'department_name', 'faculty_name', 'university_name',
            'student_type', 'academic_status', 'financial_status',
            'current_semester', 'cumulative_gpa', 'academic_standing',
            'entrance_year', 'email', 'phone', 'is_active'
        ]


class StudentDetailSerializer(serializers.ModelSerializer):
    """جزئیات دانشجو"""
    academic_program = AcademicProgramListSerializer(read_only=True)
    category_assignments = serializers.SerializerMethodField()
    academic_record = serializers.SerializerMethodField()
    university = serializers.SerializerMethodField()
    faculty = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    academic_standing = serializers.ReadOnlyField()
    is_graduating_soon = serializers.ReadOnlyField()
    academic_year = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = '__all__'

    def get_category_assignments(self, obj):
        assignments = obj.category_assignments.filter(status='ACTIVE')
        return StudentCategoryAssignmentSerializer(assignments, many=True).data

    def get_academic_record(self, obj):
        try:
            return {"message": "Academic record exists"}
        except:
            return None

    def get_university(self, obj):
        return {
            'id': obj.university.id,
            'name': obj.university.name,
            'code': obj.university.code
        }

    def get_faculty(self, obj):
        return {
            'id': obj.faculty.id,
            'name': obj.faculty.name,
            'code': obj.faculty.code
        }

    def get_department(self, obj):
        return {
            'id': obj.department.id,
            'name': obj.department.name,
            'code': obj.department.code
        }


class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    """ایجاد/ویرایش دانشجو"""
    class Meta:
        model = Student
        fields = [
            'national_id', 'first_name', 'last_name', 'first_name_en', 'last_name_en',
            'birth_date', 'gender', 'email', 'phone', 'address', 'student_id',
            'university_student_id', 'academic_program', 'student_type',
            'academic_status', 'financial_status', 'marital_status',
            'military_service_status', 'entrance_year', 'entrance_semester',
            'current_semester', 'dormitory_resident', 'dormitory_room',
            'meal_plan', 'father_name', 'father_job', 'mother_name', 'mother_job',
            'guardian_phone', 'permanent_address', 'current_address',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation',
            'blood_type', 'medical_conditions', 'medications', 'allergies'
        ]

    def validate_national_id(self, value):
        """اعتبارسنجی کد ملی"""
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("کد ملی باید ۱۰ رقم باشد")
        return value

    def validate_student_id(self, value):
        """اعتبارسنجی شماره دانشجویی"""
        if self.instance:
            # در حالت ویرایش
            if Student.objects.exclude(pk=self.instance.pk).filter(student_id=value).exists():
                raise serializers.ValidationError("این شماره دانشجویی قبلاً استفاده شده است")
        else:
            # در حالت ایجاد
            if Student.objects.filter(student_id=value).exists():
                raise serializers.ValidationError("این شماره دانشجویی قبلاً استفاده شده است")
        return value


class StudentCategoryAssignmentSerializer(serializers.ModelSerializer):
    """تخصیص دانشجو به دسته"""
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_active = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()

    class Meta:
        model = StudentCategoryAssignment
        fields = '__all__'


# AcademicRecord serializer removed - will be implemented later

# ==============================================================================
# STATISTICAL SERIALIZERS
# ==============================================================================

class UniversityStatsSerializer(serializers.Serializer):
    """آمار دانشگاه"""
    total_students = serializers.IntegerField()
    total_faculty = serializers.IntegerField()
    total_staff = serializers.IntegerField()
    total_faculties = serializers.IntegerField()
    total_departments = serializers.IntegerField()
    total_programs = serializers.IntegerField()
    total_research_centers = serializers.IntegerField()
    student_by_level = serializers.DictField()
    student_by_status = serializers.DictField()
    student_by_type = serializers.DictField()
    faculty_by_rank = serializers.DictField()


class DashboardStatsSerializer(serializers.Serializer):
    """آمار داشبورد"""
    total_universities = serializers.IntegerField()
    total_students = serializers.IntegerField()
    total_employees = serializers.IntegerField()
    total_faculties = serializers.IntegerField()
    total_departments = serializers.IntegerField()
    active_programs = serializers.IntegerField()
    recent_enrollments = serializers.IntegerField()
    students_by_university_type = serializers.DictField()
    enrollment_trends = serializers.ListField()
