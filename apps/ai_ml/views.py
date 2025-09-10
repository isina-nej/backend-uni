# ==============================================================================
# AI & MACHINE LEARNING VIEWS
# نماهای API هوش مصنوعی و یادگیری ماشین
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging
from datetime import datetime, date

from .models import (
    MLModel, StudentPerformancePrediction, CourseRecommendation,
    GradingAssistance, AnomalyDetection, IntelligentSchedule, NLPFeedbackAnalysis
)
from .serializers import (
    MLModelSerializer, StudentPerformancePredictionSerializer, CourseRecommendationSerializer,
    GradingAssistanceSerializer, AnomalyDetectionSerializer, IntelligentScheduleSerializer,
    NLPFeedbackAnalysisSerializer, PerformancePredictionRequestSerializer,
    CourseRecommendationRequestSerializer, GradingAssistanceRequestSerializer,
    ScheduleGenerationRequestSerializer, NLPFeedbackRequestSerializer, ModelTrainingRequestSerializer,
    AIMLDashboardSerializer
)
from .services import (
    performance_prediction_service, course_recommendation_service,
    grading_assistance_service, anomaly_detection_service,
    intelligent_scheduling_service, nlp_feedback_service
)

logger = logging.getLogger(__name__)


class MLModelViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ML Models"""

    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Temporarily disabled for testing
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['model_type', 'status']

    @extend_schema(
        summary="Train ML Model",
        description="Train a new ML model",
        request=ModelTrainingRequestSerializer
    )
    @action(detail=False, methods=['post'])
    def train_model(self, request):
        """Train a new ML model"""
        serializer = ModelTrainingRequestSerializer(data=request.data)
        if serializer.is_valid():
            model_type = serializer.validated_data['model_type']

            try:
                if model_type == 'performance_prediction':
                    model = performance_prediction_service.train_performance_model()
                elif model_type == 'course_recommendation':
                    model = course_recommendation_service.train_recommendation_model()
                else:
                    return Response(
                        {'error': f'Model type {model_type} not supported yet'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                response_serializer = MLModelSerializer(model)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Model training failed: {str(e)}")
                return Response(
                    {'error': f'Model training failed: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentPerformancePredictionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Student Performance Predictions"""

    queryset = StudentPerformancePrediction.objects.all()
    serializer_class = StudentPerformancePredictionSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Temporarily disabled for testing
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'course', 'risk_level']

    @extend_schema(
        summary="Predict Student Performance",
        description="Generate performance prediction for a student in a course",
        request=PerformancePredictionRequestSerializer
    )
    @action(detail=False, methods=['post'])
    def predict_performance(self, request):
        """Predict student performance"""
        serializer = PerformancePredictionRequestSerializer(data=request.data)
        if serializer.is_valid():
            student_id = serializer.validated_data['student_id']
            course_id = serializer.validated_data['course_id']

            try:
                from django.contrib.auth import get_user_model
                from apps.courses.models import Course

                User = get_user_model()
                student = User.objects.get(id=student_id)
                course = Course.objects.get(id=course_id)

                prediction = performance_prediction_service.predict_student_performance(student, course)
                response_serializer = StudentPerformancePredictionSerializer(prediction)

                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            except User.DoesNotExist:
                return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
            except Course.DoesNotExist:
                return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Performance prediction failed: {str(e)}")
                return Response(
                    {'error': f'Prediction failed: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Course Recommendations"""

    queryset = CourseRecommendation.objects.all()
    serializer_class = CourseRecommendationSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Temporarily disabled for testing
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'is_viewed', 'is_enrolled']

    @extend_schema(
        summary="Get Course Recommendations",
        description="Get personalized course recommendations for a student",
        request=CourseRecommendationRequestSerializer
    )
    @action(detail=False, methods=['post'])
    def get_recommendations(self, request):
        """Get course recommendations"""
        serializer = CourseRecommendationRequestSerializer(data=request.data)
        if serializer.is_valid():
            student_id = serializer.validated_data['student_id']
            limit = serializer.validated_data['limit']

            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                student = User.objects.get(id=student_id)

                recommendations = course_recommendation_service.recommend_courses(student, limit)
                response_serializer = CourseRecommendationSerializer(recommendations, many=True)

                return Response(response_serializer.data, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Course recommendation failed: {str(e)}")
                return Response(
                    {'error': f'Recommendation failed: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Mark Recommendation as Viewed",
        description="Mark a course recommendation as viewed"
    )
    @action(detail=True, methods=['post'])
    def mark_viewed(self, request, pk=None):
        """Mark recommendation as viewed"""
        try:
            recommendation = self.get_object()
            recommendation.is_viewed = True
            recommendation.save()

            return Response({'message': 'Recommendation marked as viewed'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Mark Recommendation as Enrolled",
        description="Mark a course recommendation as enrolled"
    )
    @action(detail=True, methods=['post'])
    def mark_enrolled(self, request, pk=None):
        """Mark recommendation as enrolled"""
        try:
            recommendation = self.get_object()
            recommendation.is_enrolled = True
            recommendation.save()

            return Response({'message': 'Recommendation marked as enrolled'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GradingAssistanceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Grading Assistance"""

    queryset = GradingAssistance.objects.all()
    serializer_class = GradingAssistanceSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Temporarily disabled for testing
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'assignment', 'model_used', 'status']

    @extend_schema(
        summary="Analyze Submission",
        description="Get AI-powered grading assistance for assignment submission",
        request=GradingAssistanceRequestSerializer
    )
    @action(detail=False, methods=['post'])
    def analyze_submission(self, request):
        """Analyze assignment submission"""
        serializer = GradingAssistanceRequestSerializer(data=request.data)
        if serializer.is_valid():
            student_id = serializer.validated_data['student_id']
            assignment_id = serializer.validated_data['assignment_id']
            submission_content = serializer.validated_data['submission_content']

            try:
                from django.contrib.auth import get_user_model
                from apps.assignments.models import Assignment

                User = get_user_model()
                student = User.objects.get(id=student_id)
                assignment = Assignment.objects.get(id=assignment_id)

                assistance = grading_assistance_service.analyze_submission(
                    student, assignment, submission_content
                )
                response_serializer = GradingAssistanceSerializer(assistance)

                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            except User.DoesNotExist:
                return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
            except Assignment.DoesNotExist:
                return Response({'error': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Grading assistance failed: {str(e)}")
                return Response(
                    {'error': f'Analysis failed: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnomalyDetectionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Anomaly Detection"""

    queryset = AnomalyDetection.objects.all()
    serializer_class = AnomalyDetectionSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Temporarily disabled for testing
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['anomaly_type', 'severity', 'resolution_status']

    @extend_schema(
        summary="Detect Anomalies",
        description="Run anomaly detection on system data"
    )
    @action(detail=False, methods=['post'])
    def detect_anomalies(self, request):
        """Detect anomalies in system data"""
        try:
            anomalies = anomaly_detection_service.detect_anomalies()
            response_serializer = AnomalyDetectionSerializer(anomalies, many=True)

            return Response({
                'message': f'Detected {len(anomalies)} anomalies',
                'anomalies': response_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Anomaly detection failed: {str(e)}")
            return Response(
                {'error': f'Anomaly detection failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Resolve Anomaly",
        description="Mark an anomaly as resolved"
    )
    @action(detail=True, methods=['post'])
    def resolve_anomaly(self, request, pk=None):
        """Resolve an anomaly"""
        try:
            anomaly = self.get_object()
            anomaly.resolution_status = 'resolved'
            anomaly.is_investigated = True
            anomaly.investigation_notes = request.data.get('notes', '')
            anomaly.save()

            return Response({'message': 'Anomaly resolved'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IntelligentScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Intelligent Schedules"""

    queryset = IntelligentSchedule.objects.all()
    serializer_class = IntelligentScheduleSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Temporarily disabled for testing
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'schedule_type', 'is_active']

    @extend_schema(
        summary="Generate Schedule",
        description="Generate intelligent schedule for user",
        request=ScheduleGenerationRequestSerializer
    )
    @action(detail=False, methods=['post'])
    def generate_schedule(self, request):
        """Generate intelligent schedule"""
        serializer = ScheduleGenerationRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            schedule_type = serializer.validated_data['schedule_type']
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']

            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(id=user_id)

                schedule = intelligent_scheduling_service.generate_schedule(
                    user, schedule_type, start_date, end_date
                )
                response_serializer = IntelligentScheduleSerializer(schedule)

                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Schedule generation failed: {str(e)}")
                return Response(
                    {'error': f'Schedule generation failed: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NLPFeedbackAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for NLP Feedback Analysis"""

    queryset = NLPFeedbackAnalysis.objects.all()
    serializer_class = NLPFeedbackAnalysisSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Temporarily disabled for testing
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['feedback_type', 'sentiment', 'priority']

    @extend_schema(
        summary="Analyze Feedback",
        description="Analyze feedback text using NLP",
        request=NLPFeedbackRequestSerializer
    )
    @action(detail=False, methods=['post'])
    def analyze_feedback(self, request):
        """Analyze feedback using NLP"""
        serializer = NLPFeedbackRequestSerializer(data=request.data)
        if serializer.is_valid():
            feedback_text = serializer.validated_data['feedback_text']
            feedback_type = serializer.validated_data['feedback_type']

            try:
                analysis = nlp_feedback_service.analyze_feedback(feedback_text, feedback_type)
                response_serializer = NLPFeedbackAnalysisSerializer(analysis)

                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"NLP feedback analysis failed: {str(e)}")
                return Response(
                    {'error': f'Analysis failed: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AIMLDashboardViewSet(viewsets.ViewSet):
    """Dashboard for AI/ML insights"""

    serializer_class = AIMLDashboardSerializer
    # permission_classes = [permissions.IsAuthenticated]  # Temporarily disabled for testing

    @extend_schema(
        summary="Get AI/ML Dashboard",
        description="Get comprehensive AI/ML dashboard data"
    )
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get AI/ML dashboard data"""
        try:
            dashboard_data = {
                'total_models': MLModel.objects.count(),
                'active_models': MLModel.objects.filter(status='ready').count(),
                'predictions_today': StudentPerformancePrediction.objects.filter(
                    created_at__date=date.today()
                ).count(),
                'recommendations_today': CourseRecommendation.objects.filter(
                    created_at__date=date.today()
                ).count(),
                'grading_assistances_today': GradingAssistance.objects.filter(
                    created_at__date=date.today()
                ).count(),
                'anomalies_detected': AnomalyDetection.objects.filter(
                    created_at__date=date.today()
                ).count(),
                'schedules_generated': IntelligentSchedule.objects.filter(
                    created_at__date=date.today()
                ).count(),
                'feedback_analyzed': NLPFeedbackAnalysis.objects.filter(
                    created_at__date=date.today()
                ).count(),
            }

            return Response(dashboard_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Dashboard data retrieval failed: {str(e)}")
            return Response(
                {'error': f'Dashboard data retrieval failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
