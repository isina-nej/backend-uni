from rest_framework import serializers
from .models import (
    Ministry, University, Faculty, Department, ResearchCenter, AdministrativeUnit,
    Position, Employee, Student, AccessControl, UserAccess, AuditLog,
    User, OrganizationalUnit, UserPosition, Permission, UserPermission, AccessLog
)


class MinistrySerializer(serializers.ModelSerializer):
    """سریالایزر وزارت"""
    universities_count = serializers.SerializerMethodField()

    class Meta:
        model = Ministry
        fields = ['id', 'name', 'name_en', 'type', 'minister', 'deputy_ministers',
                 'address', 'phone', 'website', 'established_date', 'is_active',
                 'universities_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_universities_count(self, obj):
        return obj.university_set.count()


class UniversitySerializer(serializers.ModelSerializer):
    """سریالایزر دانشگاه"""
    ministry_name = serializers.CharField(source='ministry.name', read_only=True)
    faculties_count = serializers.SerializerMethodField()
    departments_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    employees_count = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = ['id', 'ministry', 'ministry_name', 'name', 'name_en', 'code', 'type',
                 'address', 'phone', 'website', 'email', 'established_year', 'accreditation_status',
                 'president', 'board_of_trustees', 'student_count', 'faculty_count', 'staff_count',
                 'latitude', 'longitude', 'is_active', 'ranking',
                 'faculties_count', 'departments_count', 'students_count', 'employees_count',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_faculties_count(self, obj):
        return obj.faculties.count()

    def get_departments_count(self, obj):
        return sum(faculty.departments.count() for faculty in obj.faculties.all())

    def get_students_count(self, obj):
        return obj.students.count()

    def get_employees_count(self, obj):
        return obj.employees.count()


class FacultySerializer(serializers.ModelSerializer):
    """سریالایزر دانشکده"""
    university_name = serializers.CharField(source='university.name', read_only=True)
    departments_count = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = ['id', 'university', 'university_name', 'name', 'name_en', 'code',
                 'dean', 'vice_dean_education', 'vice_dean_research', 'vice_dean_student',
                 'address', 'phone', 'email', 'department_count', 'student_count',
                 'faculty_member_count', 'is_active', 'established_year',
                 'departments_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_departments_count(self, obj):
        return obj.departments.count()


class DepartmentSerializer(serializers.ModelSerializer):
    """سریالایزر گروه آموزشی"""
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    university_name = serializers.CharField(source='faculty.university.name', read_only=True)
    students_count = serializers.SerializerMethodField()
    employees_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'faculty', 'faculty_name', 'university_name', 'name', 'name_en', 'code',
                 'head', 'deputy_head', 'field_of_study', 'degree_levels', 'research_areas',
                 'student_count', 'faculty_member_count', 'course_count',
                 'phone', 'email', 'is_active', 'established_year',
                 'students_count', 'employees_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_students_count(self, obj):
        return obj.students.count()

    def get_employees_count(self, obj):
        return obj.employees.count()


class ResearchCenterSerializer(serializers.ModelSerializer):
    """سریالایزر مرکز تحقیقاتی"""
    university_name = serializers.CharField(source='university.name', read_only=True)
    employees_count = serializers.SerializerMethodField()

    class Meta:
        model = ResearchCenter
        fields = ['id', 'university', 'university_name', 'name', 'name_en', 'code',
                 'director', 'deputy_director', 'research_field', 'sub_fields', 'objectives',
                 'researcher_count', 'project_count', 'publication_count',
                 'address', 'phone', 'email', 'website', 'is_active', 'established_year',
                 'employees_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_employees_count(self, obj):
        return obj.employees.count()


class AdministrativeUnitSerializer(serializers.ModelSerializer):
    """سریالایزر واحد اداری"""
    university_name = serializers.CharField(source='university.name', read_only=True)
    employees_count = serializers.SerializerMethodField()

    class Meta:
        model = AdministrativeUnit
        fields = ['id', 'university', 'university_name', 'name', 'name_en', 'code',
                 'unit_type', 'category', 'manager', 'deputy_manager',
                 'responsibilities', 'sub_units', 'staff_count', 'budget',
                 'address', 'phone', 'email', 'is_active', 'established_year',
                 'employees_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_employees_count(self, obj):
        return obj.employees.count()


class PositionSerializer(serializers.ModelSerializer):
    """سریالایزر سمت سازمانی"""
    organizational_unit_name = serializers.CharField(source='organizational_unit.university.name', read_only=True)
    employees_count = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = ['id', 'title', 'title_en', 'code', 'position_level', 'authority_level',
                 'employment_type', 'job_description', 'required_qualifications',
                 'responsibilities', 'required_skills', 'base_salary', 'salary_grade',
                 'benefits', 'organizational_unit', 'organizational_unit_name',
                 'reports_to', 'is_active', 'employees_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_employees_count(self, obj):
        return obj.employees.count()


class EmployeeSerializer(serializers.ModelSerializer):
    """سریالایزر کارمند"""
    university_name = serializers.CharField(source='university.name', read_only=True)
    position_title = serializers.CharField(source='position.title', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    administrative_unit_name = serializers.CharField(source='administrative_unit.name', read_only=True, allow_null=True)
    research_center_name = serializers.CharField(source='research_center.name', read_only=True, allow_null=True)

    class Meta:
        model = Employee
        fields = ['id', 'university', 'university_name', 'national_id', 'first_name', 'last_name',
                 'first_name_en', 'last_name_en', 'academic_rank', 'education_level',
                 'field_of_study', 'university_of_study', 'employee_id', 'employee_type',
                 'position', 'position_title', 'department', 'department_name',
                 'administrative_unit', 'administrative_unit_name', 'research_center',
                 'research_center_name', 'phone', 'mobile', 'email', 'address',
                 'hire_date', 'contract_end_date', 'base_salary', 'allowances',
                 'birth_date', 'gender', 'marital_status', 'emergency_contact',
                 'performance_score', 'last_evaluation_date', 'is_active', 'status',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentSerializer(serializers.ModelSerializer):
    """سریالایزر دانشجو"""
    university_name = serializers.CharField(source='university.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    faculty_name = serializers.CharField(source='department.faculty.name', read_only=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'university', 'university_name', 'department', 'department_name',
                 'faculty_name', 'national_id', 'first_name', 'last_name', 'first_name_en',
                 'last_name_en', 'student_id', 'student_type', 'academic_level',
                 'academic_status', 'financial_status', 'field_of_study', 'entrance_year',
                 'expected_graduation_year', 'gpa', 'phone', 'mobile', 'email', 'address',
                 'birth_date', 'gender', 'marital_status', 'emergency_contact',
                 'special_categories', 'disabilities', 'achievements', 'scholarships',
                 'father_name', 'father_occupation', 'mother_name', 'mother_occupation',
                 'is_active', 'is_international', 'is_veteran_child', 'is_athlete',
                 'age', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_age(self, obj):
        return obj.get_age()


class AccessControlSerializer(serializers.ModelSerializer):
    """سریالایزر کنترل دسترسی"""

    class Meta:
        model = AccessControl
        fields = ['id', 'name', 'codename', 'permission_type', 'description', 'module',
                 'resource_type', 'scope', 'conditions', 'is_active',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserAccessSerializer(serializers.ModelSerializer):
    """سریالایزر دسترسی کاربران"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    permission_name = serializers.CharField(source='permission.name', read_only=True)
    university_name = serializers.CharField(source='university.name', read_only=True, allow_null=True)
    faculty_name = serializers.CharField(source='faculty.name', read_only=True, allow_null=True)
    department_name = serializers.CharField(source='department.name', read_only=True, allow_null=True)
    administrative_unit_name = serializers.CharField(source='administrative_unit.name', read_only=True, allow_null=True)
    granted_by_name = serializers.CharField(source='granted_by.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = UserAccess
        fields = ['id', 'user', 'user_name', 'permission', 'permission_name',
                 'university', 'university_name', 'faculty', 'faculty_name',
                 'department', 'department_name', 'administrative_unit',
                 'administrative_unit_name', 'granted_at', 'granted_by',
                 'granted_by_name', 'expires_at', 'is_active', 'reason',
                 'restrictions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'granted_at', 'created_at', 'updated_at']


class AuditLogSerializer(serializers.ModelSerializer):
    """سریالایزر لاگ فعالیت"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_name', 'action', 'resource_type', 'resource_id',
                 'ip_address', 'user_agent', 'session_id', 'success', 'error_message',
                 'response_status', 'details', 'old_values', 'new_values', 'timestamp']
        read_only_fields = ['id', 'timestamp']


# سریالایزرهای قدیمی برای سازگاری
class OrganizationalUnitSerializer(serializers.ModelSerializer):
    """سریالایزر واحدهای سازمانی (سازگاری با مدل‌های قدیمی)"""
    children = serializers.SerializerMethodField()
    full_path = serializers.CharField(source='get_full_path', read_only=True)

    class Meta:
        model = OrganizationalUnit
        fields = ['id', 'name', 'code', 'unit_type', 'parent', 'description',
                 'is_active', 'order', 'children', 'full_path', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return OrganizationalUnitSerializer(children, many=True).data


class UserPositionSerializer(serializers.ModelSerializer):
    """سریالایزر تخصیص سمت‌ها (سازگاری با مدل‌های قدیمی)"""
    position_title = serializers.CharField(source='position.title', read_only=True)
    unit_name = serializers.CharField(source='position.organizational_unit.name', read_only=True)

    class Meta:
        model = UserPosition
        fields = ['id', 'position', 'position_title', 'unit_name', 'start_date',
                 'end_date', 'is_active', 'is_primary', 'appointment_letter', 'notes']
        read_only_fields = ['id']


class PermissionSerializer(serializers.ModelSerializer):
    """سریالایزر مجوزها (سازگاری با مدل‌های قدیمی)"""

    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'permission_type', 'description', 'module']
        read_only_fields = ['id']


class UserPermissionSerializer(serializers.ModelSerializer):
    """سریالایزر مجوزهای کاربران (سازگاری با مدل‌های قدیمی)"""
    permission_name = serializers.CharField(source='permission.name', read_only=True)
    unit_name = serializers.CharField(source='organizational_unit.name', read_only=True)
    granted_by_name = serializers.CharField(source='granted_by.get_full_persian_name', read_only=True)

    class Meta:
        model = UserPermission
        fields = ['id', 'permission', 'permission_name', 'organizational_unit',
                 'unit_name', 'granted_by', 'granted_by_name', 'granted_at',
                 'expires_at', 'is_active']
        read_only_fields = ['id', 'granted_at', 'granted_by']


class AccessLogOldSerializer(serializers.ModelSerializer):
    """سریالایزر لاگ دسترسی (سازگاری با مدل‌های قدیمی)"""
    user_name = serializers.CharField(source='user.get_full_persian_name', read_only=True)

    class Meta:
        model = AccessLog
        fields = ['id', 'user', 'user_name', 'action', 'resource',
                 'ip_address', 'timestamp', 'success']
        read_only_fields = ['id', 'timestamp']


class UserSerializer(serializers.ModelSerializer):
    """سریالایزر کاربران پیشرفته"""
    full_persian_name = serializers.CharField(source='get_full_persian_name', read_only=True)
    primary_unit_name = serializers.CharField(source='primary_unit.name', read_only=True)
    positions = UserPositionSerializer(many=True, read_only=True)
    permissions = UserPermissionSerializer(source='user_permissions_custom', many=True, read_only=True)
    is_faculty = serializers.BooleanField(source='is_faculty_member', read_only=True)
    is_student_user = serializers.BooleanField(source='is_student', read_only=True)
    is_staff_user = serializers.BooleanField(source='is_staff_member', read_only=True)
    is_management_user = serializers.BooleanField(source='is_management', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'persian_first_name', 'persian_last_name', 'full_persian_name',
            'national_id', 'father_name', 'birth_date', 'gender',
            'phone', 'mobile', 'address',
            'role', 'employee_id', 'student_id', 'primary_unit', 'primary_unit_name',
            'academic_rank', 'field_of_study', 'degree',
            'employment_type', 'hire_date', 'salary_grade',
            'is_active', 'is_verified', 'date_joined',
            'positions', 'permissions',
            'is_faculty', 'is_student_user', 'is_staff_user', 'is_management_user'
        ]
        read_only_fields = [
            'id', 'date_joined', 'full_persian_name', 'primary_unit_name',
            'positions', 'permissions', 'is_faculty', 'is_student_user',
            'is_staff_user', 'is_management_user'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'national_id': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserBasicSerializer(serializers.ModelSerializer):
    """سریالایزر ساده کاربران برای لیست‌ها"""
    full_name = serializers.SerializerMethodField()
    unit_name = serializers.CharField(source='primary_unit.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'role', 'employee_id',
                 'student_id', 'unit_name', 'is_active']
        read_only_fields = ['id']

    def get_full_name(self, obj):
        persian_name = obj.get_full_persian_name()
        if persian_name:
            return persian_name
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
