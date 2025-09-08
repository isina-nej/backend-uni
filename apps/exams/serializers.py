from rest_framework import serializers
from .models import Exam


class ExamSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    professor_name = serializers.CharField(source='professor.username', read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'course', 'course_title', 'title', 'date', 'start_time', 'end_time', 'location', 'professor', 'professor_name']
