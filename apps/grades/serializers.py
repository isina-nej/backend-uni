from rest_framework import serializers
from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    professor_name = serializers.CharField(source='professor.username', read_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'student', 'student_name', 'course', 'course_title', 'score', 'grade_letter', 'date_assigned', 'professor', 'professor_name']
