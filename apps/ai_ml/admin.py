# ==============================================================================
# AI & MACHINE LEARNING ADMIN
# پنل مدیریت هوش مصنوعی و یادگیری ماشین
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    MLModel, StudentPerformancePrediction, CourseRecommendation,
    GradingAssistance, AnomalyDetection, IntelligentSchedule, NLPFeedbackAnalysis
)


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'version', 'status', 'accuracy', 'last_trained']
    list_filter = ['model_type', 'status', 'last_trained']
    search_fields = ['name', 'version']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'model_type', 'version', 'status')
        }),
        ('Performance Metrics', {
            'fields': ('accuracy', 'precision', 'recall', 'f1_score'),
            'classes': ('collapse',)
        }),
        ('Training Information', {
            'fields': ('training_data_size', 'last_trained', 'training_duration'),
            'classes': ('collapse',)
        }),
        ('File Paths', {
            'fields': ('model_file_path', 'scaler_file_path'),
            'classes': ('collapse',)
        }),
        ('Configuration', {
            'fields': ('hyperparameters', 'feature_importance'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(StudentPerformancePrediction)
class StudentPerformancePredictionAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'predicted_grade', 'confidence_score', 'risk_level', 'prediction_date']
    list_filter = ['risk_level', 'prediction_date', 'course']
    search_fields = ['student__first_name', 'student__last_name', 'student__email', 'course__name']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('student', 'course', 'model_used')
        }),
        ('Prediction Results', {
            'fields': ('predicted_grade', 'confidence_score', 'risk_level')
        }),
        ('Factors', {
            'fields': ('attendance_factor', 'assignment_factor', 'quiz_factor', 'participation_factor', 'previous_performance_factor'),
            'classes': ('collapse',)
        }),
        ('Recommendations', {
            'fields': ('recommendations', 'intervention_suggestions'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('prediction_date', 'valid_until', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'course', 'model_used')


@admin.register(CourseRecommendation)
class CourseRecommendationAdmin(admin.ModelAdmin):
    list_display = ['student', 'recommended_course', 'recommendation_score', 'confidence_level', 'is_viewed', 'is_enrolled']
    list_filter = ['is_viewed', 'is_enrolled', 'recommendation_date', 'expected_difficulty']
    search_fields = ['student__first_name', 'student__last_name', 'recommended_course__name']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('student', 'recommended_course', 'model_used')
        }),
        ('Recommendation Data', {
            'fields': ('recommendation_score', 'confidence_level', 'expected_difficulty')
        }),
        ('Factors', {
            'fields': ('interest_match', 'skill_match', 'career_alignment', 'prerequisite_satisfaction', 'peer_performance'),
            'classes': ('collapse',)
        }),
        ('Details', {
            'fields': ('reasoning', 'prerequisites_needed'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_viewed', 'is_enrolled'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('recommendation_date', 'expires_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'recommended_course', 'model_used')


@admin.register(GradingAssistance)
class GradingAssistanceAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'submission_student', 'ai_suggested_grade', 'confidence_score', 'analysis_date']
    list_filter = ['analysis_date', 'assignment__course']
    search_fields = ['assignment__title', 'submission__student__first_name', 'submission__student__last_name']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('assignment', 'submission', 'model_used')
        }),
        ('AI Analysis', {
            'fields': ('ai_suggested_grade', 'confidence_score')
        }),
        ('Detailed Analysis', {
            'fields': ('strengths', 'weaknesses', 'suggestions'),
            'classes': ('collapse',)
        }),
        ('Content Scores', {
            'fields': ('content_quality_score', 'originality_score', 'completeness_score'),
            'classes': ('collapse',)
        }),
        ('Feedback', {
            'fields': ('ai_generated_feedback', 'feedback_quality_score'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('analysis_date', 'processing_time', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('assignment', 'submission', 'model_used')

    def submission_student(self, obj):
        return obj.submission.student.get_full_name()
    submission_student.short_description = "Student"


@admin.register(AnomalyDetection)
class AnomalyDetectionAdmin(admin.ModelAdmin):
    list_display = ['anomaly_type', 'severity', 'affected_user', 'anomaly_score', 'resolution_status', 'detected_at']
    list_filter = ['anomaly_type', 'severity', 'resolution_status', 'detected_at']
    search_fields = ['affected_user__first_name', 'affected_user__last_name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('anomaly_type', 'severity', 'model_used')
        }),
        ('Affected Entities', {
            'fields': ('affected_user', 'affected_course')
        }),
        ('Anomaly Details', {
            'fields': ('description', 'anomaly_score', 'confidence_score')
        }),
        ('Detection Data', {
            'fields': ('detected_metrics', 'expected_values', 'actual_values'),
            'classes': ('collapse',)
        }),
        ('Investigation', {
            'fields': ('is_investigated', 'investigation_notes', 'resolution_status', 'resolved_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('detected_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('affected_user', 'affected_course', 'model_used')


@admin.register(IntelligentSchedule)
class IntelligentScheduleAdmin(admin.ModelAdmin):
    list_display = ['user', 'schedule_type', 'title', 'optimization_score', 'is_active', 'generated_at']
    list_filter = ['schedule_type', 'is_active', 'generated_at']
    search_fields = ['user__first_name', 'user__last_name', 'title']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'schedule_type', 'title', 'description', 'model_used')
        }),
        ('Schedule Data', {
            'fields': ('schedule_data', 'optimization_score')
        }),
        ('Factors', {
            'fields': ('workload_balance', 'deadline_pressure', 'learning_style', 'time_preferences'),
            'classes': ('collapse',)
        }),
        ('Schedule Period', {
            'fields': ('start_date', 'end_date', 'is_active'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('generated_at', 'last_updated', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'model_used')


@admin.register(NLPFeedbackAnalysis)
class NLPFeedbackAnalysisAdmin(admin.ModelAdmin):
    list_display = ['student', 'feedback_type', 'sentiment_label', 'sentiment_score', 'analyzed_at']
    list_filter = ['feedback_type', 'sentiment_label', 'analyzed_at']
    search_fields = ['student__first_name', 'student__last_name', 'feedback_text']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('student', 'course', 'instructor', 'feedback_type', 'model_used')
        }),
        ('Feedback Content', {
            'fields': ('feedback_text',),
            'classes': ('collapse',)
        }),
        ('Sentiment Analysis', {
            'fields': ('sentiment_score', 'sentiment_label')
        }),
        ('Content Analysis', {
            'fields': ('topics', 'keywords', 'entities'),
            'classes': ('collapse',)
        }),
        ('Quality Metrics', {
            'fields': ('clarity_score', 'constructiveness_score', 'specificity_score'),
            'classes': ('collapse',)
        }),
        ('Insights', {
            'fields': ('key_insights', 'suggested_actions'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('analyzed_at', 'processing_time', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'course', 'instructor', 'model_used')
