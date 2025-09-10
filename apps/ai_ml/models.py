00# ==============================================================================
# AI & MACHINE LEARNING MODELS
# مدل‌های هوش مصنوعی و یادگیری ماشین
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

User = get_user_model()


class MLModel(models.Model):
    """Machine Learning Model metadata"""

    MODEL_TYPES = [
        ('performance_prediction', 'Student Performance Prediction'),
        ('course_recommendation', 'Course Recommendation'),
        ('grading_assistance', 'Automated Grading Assistance'),
        ('anomaly_detection', 'Anomaly Detection'),
        ('scheduling', 'Intelligent Scheduling'),
        ('nlp_feedback', 'NLP Feedback Analysis'),
    ]

    STATUS_CHOICES = [
        ('training', 'Training'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
        ('deprecated', 'Deprecated'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Model Name")
    model_type = models.CharField(max_length=50, choices=MODEL_TYPES, verbose_name="Model Type")
    version = models.CharField(max_length=50, verbose_name="Version")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='training')

    # Model metadata
    accuracy = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    precision = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    recall = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    f1_score = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])

    # Training data
    training_data_size = models.IntegerField(default=0)
    last_trained = models.DateTimeField(null=True, blank=True)
    training_duration = models.DurationField(null=True, blank=True)

    # Model file paths
    model_file_path = models.CharField(max_length=500, null=True, blank=True)
    scaler_file_path = models.CharField(max_length=500, null=True, blank=True)

    # Configuration
    hyperparameters = models.JSONField(default=dict, blank=True)
    feature_importance = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ML Model"
        verbose_name_plural = "ML Models"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} v{self.version} ({self.get_model_type_display()})"


class StudentPerformancePrediction(models.Model):
    """Student performance predictions"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performance_predictions')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='performance_predictions')

    # Prediction data
    predicted_grade = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    confidence_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    risk_level = models.CharField(max_length=20, choices=[
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk')
    ])

    # Factors considered
    attendance_factor = models.FloatField(default=0)
    assignment_factor = models.FloatField(default=0)
    quiz_factor = models.FloatField(default=0)
    participation_factor = models.FloatField(default=0)
    previous_performance_factor = models.FloatField(default=0)

    # Recommendations
    recommendations = models.JSONField(default=list, blank=True)
    intervention_suggestions = models.TextField(blank=True)

    # Metadata
    model_used = models.ForeignKey(MLModel, on_delete=models.SET_NULL, null=True, related_name='performance_predictions')
    prediction_date = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Performance Prediction"
        verbose_name_plural = "Performance Predictions"
        unique_together = ['student', 'course']
        ordering = ['-prediction_date']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.course.name} ({self.predicted_grade:.1f}%)"


class CourseRecommendation(models.Model):
    """Course recommendations for students"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_recommendations')
    recommended_course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='recommendations')

    # Recommendation data
    recommendation_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    confidence_level = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    # Reasoning factors
    interest_match = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    skill_match = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    career_alignment = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    prerequisite_satisfaction = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    peer_performance = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    # Recommendation details
    reasoning = models.TextField(blank=True)
    prerequisites_needed = models.JSONField(default=list, blank=True)
    expected_difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('very_hard', 'Very Hard')
    ], default='medium')

    # Status
    is_viewed = models.BooleanField(default=False)
    is_enrolled = models.BooleanField(default=False)

    # Metadata
    model_used = models.ForeignKey(MLModel, on_delete=models.SET_NULL, null=True, related_name='course_recommendations')
    recommendation_date = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course Recommendation"
        verbose_name_plural = "Course Recommendations"
        unique_together = ['student', 'recommended_course']
        ordering = ['-recommendation_score', '-recommendation_date']

    def __str__(self):
        return f"{self.student.get_full_name()} → {self.recommended_course.name} ({self.recommendation_score:.2f})"


class GradingAssistance(models.Model):
    """Automated grading assistance"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey('assignments.Assignment', on_delete=models.CASCADE, related_name='grading_assistance')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grading_assistance')
    submission_content = models.TextField(blank=True)  # Store submission content directly

    # AI Analysis
    ai_suggested_grade = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    confidence_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    # Detailed analysis
    strengths = models.JSONField(default=list, blank=True)
    weaknesses = models.JSONField(default=list, blank=True)
    suggestions = models.JSONField(default=list, blank=True)

    # Content analysis
    content_quality_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    originality_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    completeness_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    # Feedback generation
    ai_generated_feedback = models.TextField(blank=True)
    feedback_quality_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    # Metadata
    model_used = models.ForeignKey(MLModel, on_delete=models.SET_NULL, null=True, related_name='grading_assistance')
    analysis_date = models.DateTimeField(auto_now_add=True)
    processing_time = models.DurationField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Grading Assistance"
        verbose_name_plural = "Grading Assistance"
        unique_together = ['assignment', 'student']
        ordering = ['-analysis_date']

    def __str__(self):
        return f"AI Grading: {self.student.get_full_name()} - {self.assignment.title}"


class AnomalyDetection(models.Model):
    """Anomaly detection in system data"""

    ANOMALY_TYPES = [
        ('performance_drop', 'Performance Drop'),
        ('attendance_issue', 'Attendance Issue'),
        ('grade_anomaly', 'Grade Anomaly'),
        ('login_anomaly', 'Login Anomaly'),
        ('system_abuse', 'System Abuse'),
        ('data_integrity', 'Data Integrity Issue'),
    ]

    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    anomaly_type = models.CharField(max_length=50, choices=ANOMALY_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='medium')

    # Affected entities
    affected_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='anomalies')
    affected_course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True, related_name='anomalies')

    # Anomaly details
    description = models.TextField()
    anomaly_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    confidence_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    # Detection data
    detected_metrics = models.JSONField(default=dict, blank=True)
    expected_values = models.JSONField(default=dict, blank=True)
    actual_values = models.JSONField(default=dict, blank=True)

    # Response
    is_investigated = models.BooleanField(default=False)
    investigation_notes = models.TextField(blank=True)
    resolution_status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('false_positive', 'False Positive'),
    ], default='open')

    # Metadata
    model_used = models.ForeignKey(MLModel, on_delete=models.SET_NULL, null=True, related_name='anomaly_detections')
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Anomaly Detection"
        verbose_name_plural = "Anomaly Detections"
        ordering = ['-detected_at']

    def __str__(self):
        return f"{self.get_anomaly_type_display()} - {self.get_severity_display()} ({self.anomaly_score:.2f})"


class IntelligentSchedule(models.Model):
    """AI-generated intelligent schedules"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='intelligent_schedules')
    schedule_type = models.CharField(max_length=50, choices=[
        ('study_plan', 'Study Plan'),
        ('exam_preparation', 'Exam Preparation'),
        ('assignment_deadlines', 'Assignment Deadlines'),
        ('course_load', 'Course Load Optimization'),
    ])

    # Schedule details
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # AI-generated schedule
    schedule_data = models.JSONField(default=dict, blank=True)
    optimization_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    # Factors considered
    workload_balance = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    deadline_pressure = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    learning_style = models.CharField(max_length=50, blank=True)
    time_preferences = models.JSONField(default=dict, blank=True)

    # Schedule metadata
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    # Metadata
    model_used = models.ForeignKey(MLModel, on_delete=models.SET_NULL, null=True, related_name='intelligent_schedules')
    generated_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Intelligent Schedule"
        verbose_name_plural = "Intelligent Schedules"
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.title}"


class NLPFeedbackAnalysis(models.Model):
    """Natural Language Processing for feedback analysis"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    feedback_text = models.TextField()
    feedback_type = models.CharField(max_length=50, choices=[
        ('course_feedback', 'Course Feedback'),
        ('instructor_feedback', 'Instructor Feedback'),
        ('assignment_feedback', 'Assignment Feedback'),
        ('system_feedback', 'System Feedback'),
    ])

    # Related entities
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nlp_feedbacks')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True, related_name='nlp_feedbacks')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='nlp_feedbacks_as_instructor')

    # NLP Analysis Results
    sentiment_score = models.FloatField(validators=[MinValueValidator(-1), MaxValueValidator(1)])  # -1 to 1
    sentiment_label = models.CharField(max_length=20, choices=[
        ('very_negative', 'Very Negative'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
        ('positive', 'Positive'),
        ('very_positive', 'Very Positive'),
    ])

    # Content analysis
    topics = models.JSONField(default=list, blank=True)
    keywords = models.JSONField(default=list, blank=True)
    entities = models.JSONField(default=list, blank=True)

    # Quality metrics
    clarity_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    constructiveness_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    specificity_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    # Actionable insights
    key_insights = models.JSONField(default=list, blank=True)
    suggested_actions = models.JSONField(default=list, blank=True)

    # Metadata
    model_used = models.ForeignKey(MLModel, on_delete=models.SET_NULL, null=True, related_name='nlp_analyses')
    analyzed_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.DurationField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "NLP Feedback Analysis"
        verbose_name_plural = "NLP Feedback Analyses"
        ordering = ['-analyzed_at']

    def __str__(self):
        return f"NLP Analysis: {self.sentiment_label} ({self.sentiment_score:.2f})"
