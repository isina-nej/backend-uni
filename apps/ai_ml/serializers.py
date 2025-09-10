# ==============================================================================
# AI & MACHINE LEARNING SERIALIZERS
# سریالایزرهای هوش مصنوعی و یادگیری ماشین
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import serializers
from .models import (
    MLModel, StudentPerformancePrediction, CourseRecommendation,
    GradingAssistance, AnomalyDetection, IntelligentSchedule, NLPFeedbackAnalysis
)


class MLModelSerializer(serializers.ModelSerializer):
    """Serializer for ML Model"""

    class Meta:
        model = MLModel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentPerformancePredictionSerializer(serializers.ModelSerializer):
    """Serializer for Student Performance Prediction"""

    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    model_name = serializers.CharField(source='model_used.name', read_only=True)

    class Meta:
        model = StudentPerformancePrediction
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for Course Recommendation"""

    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_name = serializers.CharField(source='recommended_course.name', read_only=True)
    course_code = serializers.CharField(source='recommended_course.code', read_only=True)
    model_name = serializers.CharField(source='model_used.name', read_only=True)

    class Meta:
        model = CourseRecommendation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class GradingAssistanceSerializer(serializers.ModelSerializer):
    """Serializer for Grading Assistance"""

    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    model_name = serializers.CharField(source='model_used.name', read_only=True)

    class Meta:
        model = GradingAssistance
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnomalyDetectionSerializer(serializers.ModelSerializer):
    """Serializer for Anomaly Detection"""

    affected_user_name = serializers.CharField(source='affected_user.get_full_name', read_only=True)
    affected_course_name = serializers.CharField(source='affected_course.name', read_only=True)
    model_name = serializers.CharField(source='model_used.name', read_only=True)

    class Meta:
        model = AnomalyDetection
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class IntelligentScheduleSerializer(serializers.ModelSerializer):
    """Serializer for Intelligent Schedule"""

    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    model_name = serializers.CharField(source='model_used.name', read_only=True)

    class Meta:
        model = IntelligentSchedule
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class NLPFeedbackAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for NLP Feedback Analysis"""

    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    model_name = serializers.CharField(source='model_used.name', read_only=True)

    class Meta:
        model = NLPFeedbackAnalysis
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


# Request Serializers
class PerformancePredictionRequestSerializer(serializers.Serializer):
    """Serializer for performance prediction request"""

    student_id = serializers.IntegerField()
    course_id = serializers.IntegerField()


class CourseRecommendationRequestSerializer(serializers.Serializer):
    """Serializer for course recommendation request"""

    student_id = serializers.IntegerField()
    limit = serializers.IntegerField(default=5, min_value=1, max_value=20)


class GradingAssistanceRequestSerializer(serializers.Serializer):
    """Serializer for grading assistance request"""

    student_id = serializers.IntegerField()
    assignment_id = serializers.IntegerField()
    submission_content = serializers.CharField()


class ScheduleGenerationRequestSerializer(serializers.Serializer):
    """Serializer for schedule generation request"""

    user_id = serializers.IntegerField()
    schedule_type = serializers.ChoiceField(choices=[
        ('study_plan', 'Study Plan'),
        ('exam_preparation', 'Exam Preparation'),
        ('assignment_deadlines', 'Assignment Deadlines'),
        ('course_load', 'Course Load Optimization'),
    ])
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class NLPFeedbackRequestSerializer(serializers.Serializer):
    """Serializer for NLP feedback analysis request"""

    feedback_text = serializers.CharField(max_length=5000)
    feedback_type = serializers.ChoiceField(choices=[
        ('course_feedback', 'Course Feedback'),
        ('instructor_feedback', 'Instructor Feedback'),
        ('assignment_feedback', 'Assignment Feedback'),
        ('system_feedback', 'System Feedback'),
    ])
    student_id = serializers.IntegerField()
    course_id = serializers.IntegerField(required=False)
    instructor_id = serializers.IntegerField(required=False)


class ModelTrainingRequestSerializer(serializers.Serializer):
    """Serializer for model training request"""

    model_type = serializers.ChoiceField(choices=[
        ('performance_prediction', 'Performance Prediction'),
        ('course_recommendation', 'Course Recommendation'),
        ('grading_assistance', 'Grading Assistance'),
        ('anomaly_detection', 'Anomaly Detection'),
        ('scheduling', 'Intelligent Scheduling'),
        ('nlp_feedback', 'NLP Feedback Analysis'),
    ])
    hyperparameters = serializers.JSONField(required=False, default=dict)
