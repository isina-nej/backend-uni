# Reports app serializers
from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    total_students = serializers.IntegerField()
    total_professors = serializers.IntegerField()
    total_courses = serializers.IntegerField()
    total_grades = serializers.IntegerField()
    average_grade = serializers.FloatField()


class StudentReportSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    student_name = serializers.CharField()
    courses = serializers.ListField()
    grades = serializers.ListField()
    attendance_rate = serializers.FloatField()


class CourseReportSerializer(serializers.Serializer):
    course_id = serializers.CharField()
    course_name = serializers.CharField()
    enrolled_students = serializers.IntegerField()
    average_grade = serializers.FloatField()
    completion_rate = serializers.FloatField()
