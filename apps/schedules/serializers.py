from rest_framework import serializers
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    professor_name = serializers.CharField(source='professor.username', read_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'course', 'course_title', 'day_of_week', 'start_time', 'end_time', 'location', 'professor', 'professor_name']
