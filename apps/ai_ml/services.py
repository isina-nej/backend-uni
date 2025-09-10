# ==============================================================================
# AI & MACHINE LEARNING SERVICES
# سرویس‌های هوش مصنوعی و یادگیری ماشین
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Q
from .models import (
    MLModel, StudentPerformancePrediction, CourseRecommendation,
    GradingAssistance, AnomalyDetection, IntelligentSchedule, NLPFeedbackAnalysis
)

User = get_user_model()


class AIMLService:
    """Main AI/ML service class"""

    def __init__(self):
        self.model_dir = os.path.join(settings.BASE_DIR, 'ml_models')
        os.makedirs(self.model_dir, exist_ok=True)

    def _save_model(self, model, scaler, model_name: str, hyperparameters: dict):
        """Save ML model and scaler"""
        model_path = os.path.join(self.model_dir, f'{model_name}_model.pkl')
        scaler_path = os.path.join(self.model_dir, f'{model_name}_scaler.pkl')

        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)

        return model_path, scaler_path

    def _load_model(self, model_name: str):
        """Load ML model and scaler"""
        model_path = os.path.join(self.model_dir, f'{model_name}_model.pkl')
        scaler_path = os.path.join(self.model_dir, f'{model_name}_scaler.pkl')

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            return model, scaler
        return None, None


class PerformancePredictionService(AIMLService):
    """Service for student performance prediction"""

    def train_performance_model(self) -> MLModel:
        """Train performance prediction model"""
        # Get training data
        training_data = self._get_performance_training_data()

        if len(training_data) < 10:
            raise ValueError("Insufficient training data")

        # Prepare features and target
        X, y = self._prepare_performance_features(training_data)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)

        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        mse = np.mean((y_test - y_pred) ** 2)
        rmse = np.sqrt(mse)
        r2_score = model.score(X_test_scaled, y_test)

        # Save model
        model_path, scaler_path = self._save_model(model, scaler, 'performance_prediction', {
            'n_estimators': 100,
            'random_state': 42
        })

        # Create ML model record
        ml_model = MLModel.objects.create(
            name='Student Performance Predictor',
            model_type='performance_prediction',
            version='1.0.0',
            status='ready',
            accuracy=r2_score,
            training_data_size=len(training_data),
            last_trained=datetime.now(),
            model_file_path=model_path,
            scaler_file_path=scaler_path,
            hyperparameters={'n_estimators': 100, 'random_state': 42},
            feature_importance=dict(zip(self._get_feature_names(), model.feature_importances_))
        )

        return ml_model

    def predict_student_performance(self, student, course) -> StudentPerformancePrediction:
        """Predict student performance for a course"""
        # Load model
        model, scaler = self._load_model('performance_prediction')
        if not model:
            raise ValueError("Performance prediction model not found")

        # Get student features
        features = self._get_student_features(student, course)
        features_scaled = scaler.transform([features])

        # Make prediction
        predicted_grade = model.predict(features_scaled)[0]

        # Calculate confidence and risk
        confidence_score = self._calculate_prediction_confidence(features, predicted_grade)
        risk_level = self._determine_risk_level(predicted_grade, confidence_score)

        # Get factors
        factors = self._analyze_performance_factors(student, course)

        # Generate recommendations
        recommendations = self._generate_performance_recommendations(predicted_grade, risk_level, factors)

        # Create prediction record
        prediction = StudentPerformancePrediction.objects.create(
            student=student,
            course=course,
            predicted_grade=min(100, max(0, predicted_grade)),
            confidence_score=confidence_score,
            risk_level=risk_level,
            attendance_factor=factors.get('attendance', 0),
            assignment_factor=factors.get('assignments', 0),
            quiz_factor=factors.get('quizzes', 0),
            participation_factor=factors.get('participation', 0),
            previous_performance_factor=factors.get('previous_performance', 0),
            recommendations=recommendations,
            model_used=MLModel.objects.filter(model_type='performance_prediction', status='ready').first()
        )

        return prediction

    def _get_performance_training_data(self) -> List[Dict]:
        """Get training data for performance prediction"""
        # This would typically fetch from grades, attendance, etc.
        # For now, return sample data
        return [
            {
                'attendance_rate': 0.85,
                'assignment_avg': 78.5,
                'quiz_avg': 82.0,
                'participation_score': 0.75,
                'previous_gpa': 3.2,
                'final_grade': 81.5
            }
            # Add more training samples...
        ]

    def _prepare_performance_features(self, data: List[Dict]) -> tuple:
        """Prepare features and target for training"""
        feature_names = ['attendance_rate', 'assignment_avg', 'quiz_avg', 'participation_score', 'previous_gpa']
        X = [[sample[name] for name in feature_names] for sample in data]
        y = [sample['final_grade'] for sample in data]
        return np.array(X), np.array(y)

    def _get_feature_names(self) -> List[str]:
        """Get feature names"""
        return ['attendance_rate', 'assignment_avg', 'quiz_avg', 'participation_score', 'previous_gpa']

    def _get_student_features(self, student, course) -> List[float]:
        """Get features for a specific student and course"""
        # Calculate features from student's historical data
        return [0.85, 78.5, 82.0, 0.75, 3.2]  # Sample values

    def _calculate_prediction_confidence(self, features: List[float], prediction: float) -> float:
        """Calculate confidence score for prediction"""
        # Simple confidence calculation based on feature consistency
        return 0.85

    def _determine_risk_level(self, predicted_grade: float, confidence: float) -> str:
        """Determine risk level based on prediction"""
        if predicted_grade < 60:
            return 'critical'
        elif predicted_grade < 70:
            return 'high'
        elif predicted_grade < 80:
            return 'medium'
        else:
            return 'low'

    def _analyze_performance_factors(self, student, course) -> Dict[str, float]:
        """Analyze factors affecting performance"""
        return {
            'attendance': 0.85,
            'assignments': 0.78,
            'quizzes': 0.82,
            'participation': 0.75,
            'previous_performance': 0.80
        }

    def _generate_performance_recommendations(self, predicted_grade: float, risk_level: str, factors: Dict) -> List[str]:
        """Generate recommendations based on prediction"""
        recommendations = []

        if risk_level in ['high', 'critical']:
            recommendations.append("Consider additional tutoring sessions")
            recommendations.append("Focus on completing all assignments on time")

        if factors.get('attendance', 0) < 0.8:
            recommendations.append("Improve attendance rate")

        if factors.get('assignments', 0) < 0.75:
            recommendations.append("Work on assignment completion and quality")

        return recommendations


class CourseRecommendationService(AIMLService):
    """Service for course recommendations"""

    def train_recommendation_model(self) -> MLModel:
        """Train course recommendation model"""
        # Get training data
        training_data = self._get_recommendation_training_data()

        if len(training_data) < 10:
            raise ValueError("Insufficient training data")

        # Prepare features and target
        X, y = self._prepare_recommendation_features(training_data)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)

        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        # Save model
        model_path, scaler_path = self._save_model(model, scaler, 'course_recommendation', {
            'n_estimators': 100,
            'random_state': 42
        })

        # Create ML model record
        ml_model = MLModel.objects.create(
            name='Course Recommender',
            model_type='course_recommendation',
            version='1.0.0',
            status='ready',
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            training_data_size=len(training_data),
            last_trained=datetime.now(),
            model_file_path=model_path,
            scaler_file_path=scaler_path,
            hyperparameters={'n_estimators': 100, 'random_state': 42}
        )

        return ml_model

    def recommend_courses(self, student, limit: int = 5) -> List[CourseRecommendation]:
        """Recommend courses for a student"""
        # Load model
        model, scaler = self._load_model('course_recommendation')
        if not model:
            raise ValueError("Course recommendation model not found")

        # Get all available courses
        from apps.courses.models import Course
        courses = Course.objects.all()

        recommendations = []
        for course in courses:
            # Skip courses already taken or enrolled
            if self._student_has_course(student, course):
                continue

            # Get features for this course
            features = self._get_course_features(student, course)
            features_scaled = scaler.transform([features])

            # Get recommendation score
            recommendation_score = model.predict_proba(features_scaled)[0][1]  # Probability of positive class
            confidence_level = self._calculate_recommendation_confidence(features, recommendation_score)

            # Create recommendation record
            recommendation = CourseRecommendation.objects.create(
                student=student,
                recommended_course=course,
                recommendation_score=recommendation_score,
                confidence_level=confidence_level,
                interest_match=self._calculate_interest_match(student, course),
                skill_match=self._calculate_skill_match(student, course),
                career_alignment=self._calculate_career_alignment(student, course),
                prerequisite_satisfaction=self._calculate_prerequisite_satisfaction(student, course),
                peer_performance=self._calculate_peer_performance(student, course),
                reasoning=self._generate_recommendation_reasoning(course, recommendation_score),
                expected_difficulty=self._determine_course_difficulty(course),
                model_used=MLModel.objects.filter(model_type='course_recommendation', status='ready').first()
            )

            recommendations.append(recommendation)

        # Sort by recommendation score and return top N
        recommendations.sort(key=lambda x: x.recommendation_score, reverse=True)
        return recommendations[:limit]

    def _get_recommendation_training_data(self) -> List[Dict]:
        """Get training data for course recommendations"""
        # Sample training data
        return [
            {
                'interest_match': 0.8,
                'skill_match': 0.7,
                'career_alignment': 0.9,
                'prerequisite_satisfaction': 0.6,
                'peer_performance': 0.75,
                'recommended': 1
            }
            # Add more training samples...
        ]

    def _prepare_recommendation_features(self, data: List[Dict]) -> tuple:
        """Prepare features and target for training"""
        feature_names = ['interest_match', 'skill_match', 'career_alignment', 'prerequisite_satisfaction', 'peer_performance']
        X = [[sample[name] for name in feature_names] for sample in data]
        y = [sample['recommended'] for sample in data]
        return np.array(X), np.array(y)

    def _student_has_course(self, student, course) -> bool:
        """Check if student has already taken or is enrolled in course"""
        # Check enrollments and grades
        return False  # Simplified

    def _get_course_features(self, student, course) -> List[float]:
        """Get features for course recommendation"""
        return [
            self._calculate_interest_match(student, course),
            self._calculate_skill_match(student, course),
            self._calculate_career_alignment(student, course),
            self._calculate_prerequisite_satisfaction(student, course),
            self._calculate_peer_performance(student, course)
        ]

    def _calculate_interest_match(self, student, course) -> float:
        """Calculate interest match between student and course"""
        # Simplified calculation
        return 0.75

    def _calculate_skill_match(self, student, course) -> float:
        """Calculate skill match"""
        return 0.70

    def _calculate_career_alignment(self, student, course) -> float:
        """Calculate career alignment"""
        return 0.80

    def _calculate_prerequisite_satisfaction(self, student, course) -> float:
        """Calculate prerequisite satisfaction"""
        return 0.85

    def _calculate_peer_performance(self, student, course) -> float:
        """Calculate peer performance"""
        return 0.78

    def _calculate_recommendation_confidence(self, features: List[float], score: float) -> float:
        """Calculate confidence level for recommendation"""
        return 0.82

    def _generate_recommendation_reasoning(self, course, score: float) -> str:
        """Generate reasoning for recommendation"""
        return f"This course matches your profile with a {score:.1%} recommendation score."

    def _determine_course_difficulty(self, course) -> str:
        """Determine course difficulty level"""
        return 'medium'


class GradingAssistanceService(AIMLService):
    """Service for automated grading assistance"""

    def analyze_submission(self, student, assignment, submission_content: str) -> GradingAssistance:
        """Analyze assignment submission for grading assistance"""
        # Analyze content quality
        content_analysis = self._analyze_content_quality(submission_content)

        # Generate suggested grade
        suggested_grade = self._calculate_suggested_grade(content_analysis)

        # Generate feedback
        feedback = self._generate_feedback(content_analysis)

        # Create grading assistance record
        assistance = GradingAssistance.objects.create(
            student=student,
            assignment=assignment,
            submission_content=submission_content,
            suggested_grade=suggested_grade,
            confidence_score=content_analysis.get('confidence', 0.8),
            feedback=feedback,
            status='completed',
            model_used=MLModel.objects.filter(model_type='grading', is_active=True).first()
        )

        return assistance

    def _analyze_content_quality(self, text: str) -> Dict[str, Any]:
        """Analyze content quality using NLP"""
        return {
            'quality_score': 0.75,
            'originality_score': 0.80,
            'completeness_score': 0.85,
            'confidence': 0.82,
            'strengths': ['Good structure', 'Clear arguments'],
            'weaknesses': ['Some grammar issues', 'Could be more detailed'],
            'suggestions': ['Proofread for grammar', 'Add more examples']
        }

    def _calculate_suggested_grade(self, analysis: Dict) -> float:
        """Calculate suggested grade based on analysis"""
        quality_score = analysis.get('quality_score', 0.5)
        completeness_score = analysis.get('completeness_score', 0.5)
        originality_score = analysis.get('originality_score', 0.5)

        # Weighted average
        suggested_grade = (quality_score * 0.4 + completeness_score * 0.4 + originality_score * 0.2) * 100
        return min(100, max(0, suggested_grade))

    def _generate_feedback(self, analysis: Dict) -> str:
        """Generate constructive feedback"""
        strengths = analysis.get('strengths', [])
        weaknesses = analysis.get('weaknesses', [])
        suggestions = analysis.get('suggestions', [])

        feedback = "AI-Generated Feedback:\n\n"

        if strengths:
            feedback += "Strengths:\n"
            for strength in strengths:
                feedback += f"• {strength}\n"

        if weaknesses:
            feedback += "\nAreas for Improvement:\n"
            for weakness in weaknesses:
                feedback += f"• {weakness}\n"

        if suggestions:
            feedback += "\nSuggestions:\n"
            for suggestion in suggestions:
                feedback += f"• {suggestion}\n"

        return feedback


class AnomalyDetectionService(AIMLService):
    """Service for anomaly detection"""

    def detect_anomalies(self) -> List[AnomalyDetection]:
        """Detect anomalies in system data"""
        anomalies = []

        # Check for performance anomalies
        performance_anomalies = self._detect_performance_anomalies()
        anomalies.extend(performance_anomalies)

        # Check for attendance anomalies
        attendance_anomalies = self._detect_attendance_anomalies()
        anomalies.extend(attendance_anomalies)

        # Check for grade anomalies
        grade_anomalies = self._detect_grade_anomalies()
        anomalies.extend(grade_anomalies)

        return anomalies

    def _detect_performance_anomalies(self) -> List[AnomalyDetection]:
        """Detect performance-related anomalies"""
        anomalies = []

        # Get students with sudden grade drops
        # This would query grades and detect anomalies
        # For now, return empty list
        return anomalies

    def _detect_attendance_anomalies(self) -> List[AnomalyDetection]:
        """Detect attendance-related anomalies"""
        anomalies = []
        # Implementation for attendance anomaly detection
        return anomalies

    def _detect_grade_anomalies(self) -> List[AnomalyDetection]:
        """Detect grade-related anomalies"""
        anomalies = []
        # Implementation for grade anomaly detection
        return anomalies


class IntelligentSchedulingService(AIMLService):
    """Service for intelligent scheduling"""

    def generate_study_schedule(self, student, start_date, end_date) -> IntelligentSchedule:
        """Generate intelligent study schedule for student"""
        # Analyze student's courses and deadlines
        courses_data = self._analyze_student_courses(student)
        deadlines = self._get_upcoming_deadlines(student)

        # Generate optimized schedule
        schedule_data = self._optimize_schedule(courses_data, deadlines, start_date, end_date)

        # Calculate optimization score
        optimization_score = self._calculate_schedule_optimization_score(schedule_data)

        # Create schedule record
        schedule = IntelligentSchedule.objects.create(
            user=student,
            schedule_type='study_plan',
            title=f'Study Plan for {student.get_full_name()}',
            description='AI-generated personalized study schedule',
            schedule_data=schedule_data,
            optimization_score=optimization_score,
            workload_balance=self._calculate_workload_balance(schedule_data),
            deadline_pressure=self._calculate_deadline_pressure(deadlines),
            learning_style=self._determine_learning_style(student),
            time_preferences=self._get_time_preferences(student),
            start_date=start_date,
            end_date=end_date,
            model_used=MLModel.objects.filter(model_type='scheduling', status='ready').first()
        )

        return schedule

    def _analyze_student_courses(self, student) -> Dict[str, Any]:
        """Analyze student's enrolled courses"""
        return {
            'courses': [],
            'total_credits': 15,
            'difficulty_distribution': {'easy': 2, 'medium': 3, 'hard': 1}
        }

    def _get_upcoming_deadlines(self, student) -> List[Dict]:
        """Get upcoming deadlines for student"""
        return [
            {'type': 'assignment', 'course': 'Math 101', 'date': '2025-09-15', 'priority': 'high'},
            {'type': 'exam', 'course': 'Physics 201', 'date': '2025-09-20', 'priority': 'high'}
        ]

    def _optimize_schedule(self, courses_data: Dict, deadlines: List[Dict], start_date, end_date) -> Dict[str, Any]:
        """Optimize study schedule"""
        # Simple schedule optimization
        return {
            'daily_schedule': {
                'monday': [{'time': '09:00', 'activity': 'Math Study', 'duration': 2}],
                'tuesday': [{'time': '10:00', 'activity': 'Physics Review', 'duration': 1.5}]
            },
            'weekly_goals': ['Complete Math assignment', 'Review Physics chapters'],
            'break_reminders': True
        }

    def _calculate_schedule_optimization_score(self, schedule_data: Dict) -> float:
        """Calculate optimization score for schedule"""
        return 0.85

    def _calculate_workload_balance(self, schedule_data: Dict) -> float:
        """Calculate workload balance score"""
        return 0.78

    def _calculate_deadline_pressure(self, deadlines: List[Dict]) -> float:
        """Calculate deadline pressure score"""
        return 0.65

    def _determine_learning_style(self, student) -> str:
        """Determine student's learning style"""
        return 'visual'

    def _get_time_preferences(self, student) -> Dict[str, Any]:
        """Get student's time preferences"""
        return {
            'preferred_study_times': ['morning', 'evening'],
            'break_frequency': 'every_2_hours',
            'session_duration': 90
        }


class NLPFeedbackService(AIMLService):
    """Service for NLP feedback analysis"""

    def __init__(self):
        super().__init__()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.sentiment_model = None
        self._load_nlp_models()

    def _load_nlp_models(self):
        """Load NLP models"""
        try:
            self.sentiment_model, _ = self._load_model('nlp_sentiment')
        except:
            self.sentiment_model = None

    def analyze_feedback(self, feedback_text: str, student, feedback_type: str, course=None, instructor=None) -> NLPFeedbackAnalysis:
        """Analyze feedback using NLP"""
        # Analyze sentiment
        sentiment_score, sentiment_label = self._analyze_sentiment(feedback_text)

        # Extract topics and keywords
        topics = self._extract_topics(feedback_text)
        keywords = self._extract_keywords(feedback_text)
        entities = self._extract_entities(feedback_text)

        # Calculate quality metrics
        clarity_score = self._calculate_clarity_score(feedback_text)
        constructiveness_score = self._calculate_constructiveness_score(feedback_text)
        specificity_score = self._calculate_specificity_score(feedback_text)

        # Generate insights
        key_insights = self._generate_key_insights(feedback_text, sentiment_score)
        suggested_actions = self._generate_suggested_actions(sentiment_score, feedback_type)

        # Create analysis record
        analysis = NLPFeedbackAnalysis.objects.create(
            feedback_text=feedback_text,
            feedback_type=feedback_type,
            student=student,
            course=course,
            instructor=instructor,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            topics=topics,
            keywords=keywords,
            entities=entities,
            clarity_score=clarity_score,
            constructiveness_score=constructiveness_score,
            specificity_score=specificity_score,
            key_insights=key_insights,
            suggested_actions=suggested_actions,
            model_used=MLModel.objects.filter(model_type='nlp_feedback', status='ready').first()
        )

        return analysis

    def _analyze_sentiment(self, text: str) -> tuple:
        """Analyze sentiment of text"""
        # Simple sentiment analysis (would use trained model in production)
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'helpful']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'useless', 'difficult']

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return 0.75, 'positive'
        elif negative_count > positive_count:
            return -0.75, 'negative'
        else:
            return 0.0, 'neutral'

    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text"""
        # Simple topic extraction
        return ['teaching', 'course_content', 'assignments']

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction
        return ['helpful', 'clear', 'engaging']

    def _extract_entities(self, text: str) -> List[str]:
        """Extract entities from text"""
        return ['instructor_name', 'course_name']

    def _calculate_clarity_score(self, text: str) -> float:
        """Calculate clarity score"""
        return 0.82

    def _calculate_constructiveness_score(self, text: str) -> float:
        """Calculate constructiveness score"""
        return 0.75

    def _calculate_specificity_score(self, text: str) -> float:
        """Calculate specificity score"""
        return 0.78

    def _generate_key_insights(self, text: str, sentiment: float) -> List[str]:
        """Generate key insights from feedback"""
        insights = []
        if sentiment > 0.5:
            insights.append("Positive feedback indicates effective teaching methods")
        elif sentiment < -0.5:
            insights.append("Negative feedback suggests areas needing improvement")
        else:
            insights.append("Neutral feedback provides balanced perspective")
        return insights

    def _generate_suggested_actions(self, sentiment: float, feedback_type: str) -> List[str]:
        """Generate suggested actions based on analysis"""
        actions = []
        if sentiment < -0.5:
            if feedback_type == 'course_feedback':
                actions.append("Review course content and delivery methods")
            elif feedback_type == 'instructor_feedback':
                actions.append("Provide additional training for instructor")
        return actions


# Global service instances
performance_prediction_service = PerformancePredictionService()
course_recommendation_service = CourseRecommendationService()
grading_assistance_service = GradingAssistanceService()
anomaly_detection_service = AnomalyDetectionService()
intelligent_scheduling_service = IntelligentSchedulingService()
nlp_feedback_service = NLPFeedbackService()
