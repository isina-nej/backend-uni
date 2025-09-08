from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    professor_name = serializers.CharField(source='professor.username', read_only=True)
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'description', 'professor', 'professor_name', 'students', 'student_count', 'created_at']

    def get_student_count(self, obj):
        return obj.students.count()
