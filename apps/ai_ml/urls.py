# ==============================================================================
# AI & MACHINE LEARNING URLS
# مسیرهای URL هوش مصنوعی و یادگیری ماشین
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MLModelViewSet, StudentPerformancePredictionViewSet, CourseRecommendationViewSet,
    GradingAssistanceViewSet, AnomalyDetectionViewSet, IntelligentScheduleViewSet,
    NLPFeedbackAnalysisViewSet, AIMLDashboardViewSet
)

# Create router
router = DefaultRouter()
router.register(r'models', MLModelViewSet, basename='ml-model')
router.register(r'performance-predictions', StudentPerformancePredictionViewSet, basename='performance-prediction')
router.register(r'course-recommendations', CourseRecommendationViewSet, basename='course-recommendation')
router.register(r'grading-assistance', GradingAssistanceViewSet, basename='grading-assistance')
router.register(r'anomaly-detection', AnomalyDetectionViewSet, basename='anomaly-detection')
router.register(r'intelligent-schedules', IntelligentScheduleViewSet, basename='intelligent-schedule')
router.register(r'nlp-feedback-analysis', NLPFeedbackAnalysisViewSet, basename='nlp-feedback-analysis')
router.register(r'dashboard', AIMLDashboardViewSet, basename='ai-ml-dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
