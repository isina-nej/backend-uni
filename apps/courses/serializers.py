from rest_framework import serializers
from django.db import transaction
from config.validators import AdvancedValidators
from .models import Course
from apps.users.models import User


class CourseSerializer(serializers.ModelSerializer):
    professor_name = serializers.CharField(source='professor.username', read_only=True)
    professor_full_name = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()
    is_full = serializers.SerializerMethodField()
    enrollment_status = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'code', 'description', 'professor', 'professor_name', 
            'professor_full_name', 'students', 'student_count', 'is_full',
            'enrollment_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['student_count', 'is_full', 'enrollment_status']

    def get_professor_full_name(self, obj):
        if obj.professor:
            return f"{obj.professor.first_name} {obj.professor.last_name}".strip()
        return ""

    def get_student_count(self, obj):
        return getattr(obj, 'student_count', obj.students.count())

    def get_is_full(self, obj):
        return self.get_student_count(obj) >= 50

    def get_enrollment_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.user_type == 'STUDENT':
            return obj.students.filter(id=request.user.id).exists()
        return None

    def validate_professor(self, value):
        """Validate professor qualification"""
        if value and value.user_type != 'EMPLOYEE':
            raise serializers.ValidationError("Professor must be an employee")
        
        # Additional professor validation
        try:
            AdvancedValidators.validate_professor_qualification(value, None)
        except Exception:
            # Skip validation if course not available yet
            pass
            
        return value

    def validate_title(self, value):
        """Validate course title"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Course title must be at least 3 characters")
        return value.strip()

    def validate_code(self, value):
        """Validate course code"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Course code is required and must be at least 2 characters")
        
        # Check uniqueness (excluding current instance)
        queryset = Course.objects.filter(code=value.strip())
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("Course with this code already exists")
            
        return value.strip()


class CourseEnrollmentSerializer(serializers.Serializer):
    """Serializer for course enrollment"""
    student_id = serializers.IntegerField()
    
    def validate_student_id(self, value):
        """Validate student exists and is active"""
        try:
            student = User.objects.get(id=value, user_type='STUDENT')
            if not student.is_active:
                raise serializers.ValidationError("Student account is not active")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Student not found")

    def validate(self, attrs):
        """Validate enrollment"""
        course = self.context.get('course')
        student_id = attrs.get('student_id')
        
        if course and student_id:
            try:
                student = User.objects.get(id=student_id)
                AdvancedValidators.validate_course_enrollment(student, course)
            except Exception as e:
                raise serializers.ValidationError(str(e))
                
        return attrs


class CourseListSerializer(serializers.ModelSerializer):
    """Simplified serializer for course lists"""
    professor_name = serializers.CharField(source='professor.username', read_only=True)
    student_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'professor_name', 'student_count', 'created_at']
        
    def get_student_count(self, obj):
        return getattr(obj, 'student_count', obj.students.count())


class CourseDetailSerializer(CourseSerializer):
    """Detailed course serializer with student list"""
    students_list = serializers.SerializerMethodField()
    
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['students_list']
        
    def get_students_list(self, obj):
        students = obj.students.all()[:10]  # Limit to first 10 students
        return [
            {
                'id': student.id,
                'username': student.username,
                'full_name': f"{student.first_name} {student.last_name}".strip()
            }
            for student in students
        ]
