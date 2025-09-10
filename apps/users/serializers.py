from rest_framework import serializers
from .models import (
    User, OrganizationalUnit, Position, UserPosition, 
    Permission, UserPermission, AccessLog
)


class OrganizationalUnitSerializer(serializers.ModelSerializer):
    """سریالایزر واحدهای سازمانی"""
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


class PositionSerializer(serializers.ModelSerializer):
    """سریالایزر سمت‌های سازمانی"""
    organizational_unit_name = serializers.CharField(source='organizational_unit.name', read_only=True)
    
    class Meta:
        model = Position
        fields = ['id', 'title', 'organizational_unit', 'organizational_unit_name',
                 'position_level', 'authority_level', 'job_description', 
                 'required_qualifications', 'salary_grade', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserPositionSerializer(serializers.ModelSerializer):
    """سریالایزر تخصیص سمت‌ها"""
    position_title = serializers.CharField(source='position.title', read_only=True)
    unit_name = serializers.CharField(source='position.organizational_unit.name', read_only=True)
    
    class Meta:
        model = UserPosition
        fields = ['id', 'position', 'position_title', 'unit_name', 'start_date', 
                 'end_date', 'is_active', 'is_primary', 'appointment_letter', 'notes']
        read_only_fields = ['id']


class PermissionSerializer(serializers.ModelSerializer):
    """سریالایزر مجوزها"""
    
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'permission_type', 'description', 'module']
        read_only_fields = ['id']


class UserPermissionSerializer(serializers.ModelSerializer):
    """سریالایزر مجوزهای کاربران"""
    permission_name = serializers.CharField(source='permission.name', read_only=True)
    unit_name = serializers.CharField(source='organizational_unit.name', read_only=True)
    granted_by_name = serializers.CharField(source='granted_by.get_full_persian_name', read_only=True)
    
    class Meta:
        model = UserPermission
        fields = ['id', 'permission', 'permission_name', 'organizational_unit', 
                 'unit_name', 'granted_by', 'granted_by_name', 'granted_at', 
                 'expires_at', 'is_active']
        read_only_fields = ['id', 'granted_at', 'granted_by']


class UserSerializer(serializers.ModelSerializer):
    """سریالایزر کاربران"""
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


class AccessLogSerializer(serializers.ModelSerializer):
    """سریالایزر لاگ دسترسی"""
    user_name = serializers.CharField(source='user.get_full_persian_name', read_only=True)
    
    class Meta:
        model = AccessLog
        fields = ['id', 'user', 'user_name', 'action', 'resource', 
                 'ip_address', 'timestamp', 'success']
        read_only_fields = ['id', 'timestamp']
