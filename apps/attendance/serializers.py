from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    course_title = serializers.CharField(source='schedule.course.title', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'schedule', 'course_title', 'date', 'is_present']
