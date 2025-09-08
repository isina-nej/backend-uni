from rest_framework import serializers
from .models import Assignment, Submission


class AssignmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    professor_name = serializers.CharField(source='professor.username', read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'course', 'course_title', 'professor', 
                 'professor_name', 'due_date', 'max_score', 'created_at']


class SubmissionSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    student_name = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'assignment_title', 'student', 'student_name', 
                 'submitted_at', 'content', 'file_url', 'score', 'feedback', 'graded_at']
