# ==============================================================================
# ANALYTICS DATA SERVICES
# خدمات داده آنالیتیکس
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from django.db.models import Q, Count, Avg, Sum, Max, Min, F
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import connection
import hashlib
import json

from .models import Dashboard, Widget, Report, ReportExecution, AnalyticsMetric

logger = logging.getLogger(__name__)
User = get_user_model()


class DataSourceRegistry:
    """Registry for available data sources"""
    
    def __init__(self):
        self._sources = {}
        self.register_default_sources()
    
    def register(self, name: str, query_func, description: str = ""):
        """Register a new data source"""
        self._sources[name] = {
            'query_func': query_func,
            'description': description
        }
    
    def get_source(self, name: str):
        """Get a registered data source"""
        return self._sources.get(name)
    
    def list_sources(self):
        """List all available data sources"""
        return list(self._sources.keys())
    
    def register_default_sources(self):
        """Register default data sources"""
        
        # Student analytics
        self.register('student_count', self._student_count, 'تعداد کل دانشجویان')
        self.register('student_by_status', self._student_by_status, 'دانشجویان بر اساس وضعیت')
        self.register('student_enrollment_trend', self._student_enrollment_trend, 'روند ثبت‌نام دانشجویان')
        
        # Course analytics
        self.register('course_count', self._course_count, 'تعداد کل دروس')
        self.register('course_enrollment', self._course_enrollment, 'ثبت‌نام در دروس')
        self.register('popular_courses', self._popular_courses, 'محبوب‌ترین دروس')
        
        # Grade analytics
        self.register('grade_distribution', self._grade_distribution, 'توزیع نمرات')
        self.register('average_grades', self._average_grades, 'میانگین نمرات')
        self.register('grade_trends', self._grade_trends, 'روند نمرات')
        
        # Attendance analytics
        self.register('attendance_rate', self._attendance_rate, 'نرخ حضور')
        self.register('attendance_by_course', self._attendance_by_course, 'حضور بر اساس درس')
        
        # Financial analytics
        self.register('revenue_summary', self._revenue_summary, 'خلاصه درآمد')
        self.register('payment_status', self._payment_status, 'وضعیت پرداخت‌ها')
        
        # System analytics
        self.register('user_activity', self._user_activity, 'فعالیت کاربران')
        self.register('login_stats', self._login_stats, 'آمار ورود به سیستم')
    
    # Default data source implementations
    def _student_count(self, filters=None, **kwargs):
        """Get total student count"""
        try:
            from apps.users.models import User
            queryset = User.objects.filter(groups__name='Students')
            
            if filters:
                # Apply filters
                if 'status' in filters:
                    queryset = queryset.filter(is_active=filters['status'])
                if 'date_from' in filters:
                    queryset = queryset.filter(date_joined__gte=filters['date_from'])
                if 'date_to' in filters:
                    queryset = queryset.filter(date_joined__lte=filters['date_to'])
            
            return {'total': queryset.count()}
        except Exception as e:
            logger.error(f"Error in _student_count: {e}")
            return {'total': 0}
    
    def _student_by_status(self, filters=None, **kwargs):
        """Get students by status"""
        try:
            from apps.users.models import User
            queryset = User.objects.filter(groups__name='Students')
            
            result = queryset.values('is_active').annotate(
                count=Count('id'),
                status_label=F('is_active')
            )
            
            return [
                {
                    'status': 'فعال' if item['is_active'] else 'غیرفعال',
                    'count': item['count']
                }
                for item in result
            ]
        except Exception as e:
            logger.error(f"Error in _student_by_status: {e}")
            return []
    
    def _course_count(self, filters=None, **kwargs):
        """Get total course count"""
        try:
            from apps.courses.models import Course
            queryset = Course.objects.all()
            
            if filters:
                if 'is_active' in filters:
                    queryset = queryset.filter(is_active=filters['is_active'])
            
            return {'total': queryset.count()}
        except Exception as e:
            logger.error(f"Error in _course_count: {e}")
            return {'total': 0}
    
    def _grade_distribution(self, filters=None, **kwargs):
        """Get grade distribution"""
        try:
            from apps.grades.models import Grade
            queryset = Grade.objects.all()
            
            if filters:
                if 'course_id' in filters:
                    queryset = queryset.filter(course_id=filters['course_id'])
                if 'date_from' in filters:
                    queryset = queryset.filter(created_at__gte=filters['date_from'])
            
            # Create grade ranges
            result = []
            ranges = [
                (90, 100, 'عالی'),
                (80, 89, 'خوب'),
                (70, 79, 'متوسط'),
                (60, 69, 'قابل قبول'),
                (0, 59, 'مردود')
            ]
            
            for min_grade, max_grade, label in ranges:
                count = queryset.filter(
                    score__gte=min_grade,
                    score__lte=max_grade
                ).count()
                
                result.append({
                    'range': label,
                    'count': count,
                    'min_grade': min_grade,
                    'max_grade': max_grade
                })
            
            return result
        except Exception as e:
            logger.error(f"Error in _grade_distribution: {e}")
            return []
    
    def _attendance_rate(self, filters=None, **kwargs):
        """Get attendance rate"""
        try:
            from apps.attendance.models import Attendance
            queryset = Attendance.objects.all()
            
            if filters:
                if 'course_id' in filters:
                    queryset = queryset.filter(course_id=filters['course_id'])
                if 'date_from' in filters:
                    queryset = queryset.filter(date__gte=filters['date_from'])
                if 'date_to' in filters:
                    queryset = queryset.filter(date__lte=filters['date_to'])
            
            total = queryset.count()
            present = queryset.filter(status='present').count()
            
            rate = (present / total * 100) if total > 0 else 0
            
            return {
                'total': total,
                'present': present,
                'absent': total - present,
                'rate': round(rate, 2)
            }
        except Exception as e:
            logger.error(f"Error in _attendance_rate: {e}")
            return {'total': 0, 'present': 0, 'absent': 0, 'rate': 0}
    
    def _revenue_summary(self, filters=None, **kwargs):
        """Get revenue summary"""
        try:
            from apps.financial.models import Payment
            queryset = Payment.objects.filter(status='completed')
            
            if filters:
                if 'date_from' in filters:
                    queryset = queryset.filter(created_at__gte=filters['date_from'])
                if 'date_to' in filters:
                    queryset = queryset.filter(created_at__lte=filters['date_to'])
            
            total_revenue = queryset.aggregate(total=Sum('amount'))['total'] or 0
            payment_count = queryset.count()
            average_payment = (total_revenue / payment_count) if payment_count > 0 else 0
            
            return {
                'total_revenue': float(total_revenue),
                'payment_count': payment_count,
                'average_payment': round(float(average_payment), 2)
            }
        except Exception as e:
            logger.error(f"Error in _revenue_summary: {e}")
            return {'total_revenue': 0, 'payment_count': 0, 'average_payment': 0}
    
    def _user_activity(self, filters=None, **kwargs):
        """Get user activity statistics"""
        try:
            from django.contrib.sessions.models import Session
            from django.utils import timezone
            
            # Active sessions in last 24 hours
            yesterday = timezone.now() - timedelta(days=1)
            active_sessions = Session.objects.filter(
                expire_date__gte=yesterday
            ).count()
            
            # Total users
            total_users = User.objects.filter(is_active=True).count()
            
            # Recent logins (approximate from user last_login)
            recent_logins = User.objects.filter(
                last_login__gte=yesterday
            ).count()
            
            return {
                'active_sessions': active_sessions,
                'total_users': total_users,
                'recent_logins': recent_logins,
                'activity_rate': round((recent_logins / total_users * 100) if total_users > 0 else 0, 2)
            }
        except Exception as e:
            logger.error(f"Error in _user_activity: {e}")
            return {'active_sessions': 0, 'total_users': 0, 'recent_logins': 0, 'activity_rate': 0}

    def _student_enrollment_trend(self, filters=None, **kwargs):
        """Get student enrollment trend over time"""
        try:
            from apps.users.models import User
            from django.db.models import Count
            from django.utils import timezone
            from datetime import timedelta
            
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=365)  # Last year
            
            # Get enrollments by month
            enrollments = User.objects.filter(
                groups__name='Students',
                date_joined__gte=start_date,
                date_joined__lte=end_date
            ).extra(
                select={'month': "strftime('%%Y-%%m', date_joined)"}
            ).values('month').annotate(count=Count('id')).order_by('month')
            
            return [
                {
                    'month': item['month'],
                    'enrollments': item['count']
                }
                for item in enrollments
            ]
        except Exception as e:
            logger.error(f"Error in _student_enrollment_trend: {e}")
            return []

    def _course_enrollment(self, filters=None, **kwargs):
        """Get course enrollment statistics"""
        try:
            from apps.courses.models import Course, CourseEnrollment
            
            enrollments = CourseEnrollment.objects.values(
                'course__title'
            ).annotate(
                enrollment_count=Count('id')
            ).order_by('-enrollment_count')[:10]
            
            return [
                {
                    'course': item['course__title'],
                    'enrollments': item['enrollment_count']
                }
                for item in enrollments
            ]
        except Exception as e:
            logger.error(f"Error in _course_enrollment: {e}")
            return []

    def _popular_courses(self, filters=None, **kwargs):
        """Get most popular courses"""
        try:
            from apps.courses.models import Course, CourseEnrollment
            
            popular = CourseEnrollment.objects.values(
                'course__title', 'course__code'
            ).annotate(
                enrollment_count=Count('id')
            ).order_by('-enrollment_count')[:5]
            
            return [
                {
                    'title': item['course__title'],
                    'code': item['course__code'],
                    'enrollments': item['enrollment_count']
                }
                for item in popular
            ]
        except Exception as e:
            logger.error(f"Error in _popular_courses: {e}")
            return []

    def _average_grades(self, filters=None, **kwargs):
        """Get average grades statistics"""
        try:
            from apps.grades.models import Grade
            from django.db.models import Avg
            
            avg_grade = Grade.objects.aggregate(
                average=Avg('grade')
            )['average'] or 0
            
            # Grade distribution by range
            ranges = [
                (17, 20, 'عالی'),
                (15, 17, 'خوب'),
                (12, 15, 'متوسط'),
                (10, 12, 'قابل قبول'),
                (0, 10, 'مردود')
            ]
            
            distribution = []
            for min_grade, max_grade, label in ranges:
                count = Grade.objects.filter(
                    grade__gte=min_grade,
                    grade__lt=max_grade
                ).count()
                distribution.append({
                    'range': label,
                    'count': count
                })
            
            return {
                'average_grade': round(avg_grade, 2),
                'distribution': distribution
            }
        except Exception as e:
            logger.error(f"Error in _average_grades: {e}")
            return {'average_grade': 0, 'distribution': []}

    def _grade_trends(self, filters=None, **kwargs):
        """Get grade trends over time"""
        try:
            from apps.grades.models import Grade
            from django.db.models import Avg
            from django.utils import timezone
            from datetime import timedelta
            
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=365)
            
            trends = Grade.objects.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            ).extra(
                select={'month': "strftime('%%Y-%%m', created_at)"}
            ).values('month').annotate(
                avg_grade=Avg('grade')
            ).order_by('month')
            
            return [
                {
                    'month': item['month'],
                    'average_grade': round(item['avg_grade'], 2) if item['avg_grade'] else 0
                }
                for item in trends
            ]
        except Exception as e:
            logger.error(f"Error in _grade_trends: {e}")
            return []

    def _attendance_by_course(self, filters=None, **kwargs):
        """Get attendance statistics by course"""
        try:
            from apps.attendance.models import AttendanceRecord
            from apps.courses.models import Course
            from django.db.models import Count, Q
            
            attendance_stats = AttendanceRecord.objects.values(
                'course__title'
            ).annotate(
                total_records=Count('id'),
                present_count=Count('id', filter=Q(status='present')),
                absent_count=Count('id', filter=Q(status='absent'))
            )
            
            return [
                {
                    'course': item['course__title'],
                    'total_sessions': item['total_records'],
                    'present': item['present_count'],
                    'absent': item['absent_count'],
                    'attendance_rate': round(
                        (item['present_count'] / item['total_records'] * 100) 
                        if item['total_records'] > 0 else 0, 2
                    )
                }
                for item in attendance_stats
            ]
        except Exception as e:
            logger.error(f"Error in _attendance_by_course: {e}")
            return []

    def _payment_status(self, filters=None, **kwargs):
        """Get payment status statistics"""
        try:
            from apps.financial.models import Payment
            from django.db.models import Count, Sum
            
            payment_stats = Payment.objects.values('status').annotate(
                count=Count('id'),
                total_amount=Sum('amount')
            )
            
            return [
                {
                    'status': item['status'],
                    'count': item['count'],
                    'total_amount': float(item['total_amount'] or 0)
                }
                for item in payment_stats
            ]
        except Exception as e:
            logger.error(f"Error in _payment_status: {e}")
            return []

    def _login_stats(self, filters=None, **kwargs):
        """Get login statistics"""
        try:
            from django.contrib.auth.models import User
            from django.utils import timezone
            from datetime import timedelta
            
            now = timezone.now()
            today = now.date()
            week_ago = today - timedelta(days=7)
            month_ago = today - timedelta(days=30)
            
            stats = {
                'today': User.objects.filter(
                    last_login__date=today
                ).count(),
                'this_week': User.objects.filter(
                    last_login__gte=week_ago
                ).count(),
                'this_month': User.objects.filter(
                    last_login__gte=month_ago
                ).count(),
                'total_users': User.objects.filter(is_active=True).count()
            }
            
            return stats
        except Exception as e:
            logger.error(f"Error in _login_stats: {e}")
            return {'today': 0, 'this_week': 0, 'this_month': 0, 'total_users': 0}


class AnalyticsService:
    """Main analytics service for data processing and visualization"""
    
    def __init__(self):
        self.data_registry = DataSourceRegistry()
    
    def get_widget_data(self, widget: Widget) -> Dict[str, Any]:
        """Get data for a specific widget"""
        try:
            # Check cache first
            cache_key = f"widget_data_{widget.id}_{hash(str(widget.query_config))}"
            cached_data = cache.get(cache_key)
            
            if cached_data is not None:
                return cached_data
            
            # Get data source
            data_source = self.data_registry.get_source(widget.data_source)
            if not data_source:
                return {'error': f'Data source {widget.data_source} not found'}
            
            # Execute query
            query_func = data_source['query_func']
            filters = widget.query_config.get('filters', {})
            aggregation = widget.aggregation_config
            
            raw_data = query_func(filters=filters, aggregation=aggregation)
            
            # Process data for chart type
            processed_data = self._process_data_for_chart(raw_data, widget.chart_type)
            
            # Cache the result
            cache.set(cache_key, processed_data, widget.cache_duration)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error getting widget data for {widget.id}: {e}")
            return {'error': str(e)}
    
    def _process_data_for_chart(self, data: Any, chart_type: str) -> Dict[str, Any]:
        """Process raw data for specific chart type"""
        if chart_type == 'kpi':
            # For KPI widgets, expect single value
            if isinstance(data, dict) and 'total' in data:
                return {
                    'value': data['total'],
                    'label': 'Total'
                }
            return {'value': data, 'label': 'Value'}
        
        elif chart_type in ['pie', 'doughnut']:
            # For pie charts, expect list with labels and values
            if isinstance(data, list):
                return {
                    'labels': [item.get('status', item.get('range', 'Unknown')) for item in data],
                    'values': [item.get('count', 0) for item in data]
                }
        
        elif chart_type in ['bar', 'line']:
            # For bar/line charts
            if isinstance(data, list):
                return {
                    'labels': [item.get('label', item.get('status', item.get('range', 'Unknown'))) for item in data],
                    'values': [item.get('count', item.get('value', 0)) for item in data]
                }
        
        elif chart_type == 'table':
            # For tables, return data as-is if it's a list
            if isinstance(data, list):
                return {'rows': data}
            elif isinstance(data, dict):
                return {'rows': [data]}
        
        # Default processing
        return {'data': data}
    
    def get_dashboard_data(self, dashboard: Dashboard, user: User) -> Dict[str, Any]:
        """Get all data for a dashboard"""
        try:
            if not dashboard.can_access(user):
                return {'error': 'Access denied'}
            
            # Update access statistics
            dashboard.update_access()
            
            # Get all active widgets
            widgets = dashboard.widgets.filter(is_active=True).order_by('order')
            
            widget_data = {}
            for widget in widgets:
                widget_data[str(widget.id)] = self.get_widget_data(widget)
            
            return {
                'dashboard_id': str(dashboard.id),
                'title': dashboard.title,
                'layout_config': dashboard.layout_config,
                'widgets': widget_data,
                'refresh_interval': dashboard.refresh_interval
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard data for {dashboard.id}: {e}")
            return {'error': str(e)}
    
    def generate_report(self, report: Report, user: User) -> ReportExecution:
        """Generate a report and return execution record"""
        try:
            # Check access
            if not report.can_access(user):
                raise PermissionError("Access denied to this report")
            
            # Create execution record
            execution = ReportExecution.objects.create(
                report=report,
                executed_by=user,
                status='running'
            )
            
            start_time = timezone.now()
            
            try:
                # Generate report data
                report_data = self._generate_report_data(report)
                
                # Calculate execution time
                execution_time = (timezone.now() - start_time).total_seconds()
                
                # Update execution record
                execution.status = 'completed'
                execution.result_data = report_data
                execution.row_count = len(report_data) if isinstance(report_data, list) else 1
                execution.execution_time = execution_time
                execution.save()
                
                # Update report statistics
                report.last_generated = timezone.now()
                report.generation_count += 1
                report.save(update_fields=['last_generated', 'generation_count'])
                
                return execution
                
            except Exception as e:
                # Mark execution as failed
                execution.status = 'failed'
                execution.error_message = str(e)
                execution.execution_time = (timezone.now() - start_time).total_seconds()
                execution.save()
                raise
                
        except Exception as e:
            logger.error(f"Error generating report {report.id}: {e}")
            raise
    
    def _generate_report_data(self, report: Report) -> List[Dict[str, Any]]:
        """Generate the actual report data"""
        try:
            # This is a simplified implementation
            # In practice, you'd have more complex logic based on report configuration
            
            data_sources = report.data_sources
            filters = report.filters
            result_data = []
            
            for source_name in data_sources:
                source = self.data_registry.get_source(source_name)
                if source:
                    source_data = source['query_func'](filters=filters)
                    if isinstance(source_data, list):
                        result_data.extend(source_data)
                    else:
                        result_data.append({
                            'source': source_name,
                            'data': source_data
                        })
            
            # Apply grouping and sorting if specified
            if report.grouping:
                # Implement grouping logic
                pass
            
            if report.sorting:
                # Implement sorting logic
                pass
            
            return result_data
            
        except Exception as e:
            logger.error(f"Error generating report data: {e}")
            raise
    
    def calculate_metric(self, metric_name: str, metric_type: str, 
                        period_start: datetime, period_end: datetime,
                        context: Dict = None) -> AnalyticsMetric:
        """Calculate and cache an analytics metric"""
        try:
            # Generate cache key
            context_str = json.dumps(context or {}, sort_keys=True)
            cache_key = hashlib.md5(
                f"{metric_name}_{metric_type}_{period_start}_{period_end}_{context_str}".encode()
            ).hexdigest()
            
            # Check if metric already exists and is not expired
            try:
                existing_metric = AnalyticsMetric.objects.get(cache_key=cache_key)
                if not existing_metric.is_expired():
                    return existing_metric
                else:
                    # Delete expired metric
                    existing_metric.delete()
            except AnalyticsMetric.DoesNotExist:
                pass
            
            # Calculate new metric value
            value = self._calculate_metric_value(metric_name, metric_type, period_start, period_end, context)
            
            # Create new metric record
            expires_at = timezone.now() + timedelta(hours=1)  # Cache for 1 hour
            
            metric = AnalyticsMetric.objects.create(
                metric_name=metric_name,
                metric_type=metric_type,
                value=value,
                context=context or {},
                period_start=period_start,
                period_end=period_end,
                cache_key=cache_key,
                expires_at=expires_at
            )
            
            return metric
            
        except Exception as e:
            logger.error(f"Error calculating metric {metric_name}: {e}")
            raise
    
    def _calculate_metric_value(self, metric_name: str, metric_type: str,
                               period_start: datetime, period_end: datetime,
                               context: Dict = None) -> Any:
        """Calculate the actual metric value"""
        try:
            if metric_type == 'student_performance':
                return self._calculate_student_performance_metric(metric_name, period_start, period_end, context)
            elif metric_type == 'course_analytics':
                return self._calculate_course_analytics_metric(metric_name, period_start, period_end, context)
            elif metric_type == 'financial_metrics':
                return self._calculate_financial_metric(metric_name, period_start, period_end, context)
            else:
                # Default calculation
                return {'value': 0, 'calculated_at': timezone.now().isoformat()}
                
        except Exception as e:
            logger.error(f"Error calculating metric value for {metric_name}: {e}")
            return {'error': str(e)}
    
    def _calculate_student_performance_metric(self, metric_name: str, 
                                            period_start: datetime, period_end: datetime,
                                            context: Dict = None) -> Dict:
        """Calculate student performance metrics"""
        try:
            from apps.grades.models import Grade
            
            queryset = Grade.objects.filter(
                created_at__gte=period_start,
                created_at__lte=period_end
            )
            
            if context and 'course_id' in context:
                queryset = queryset.filter(course_id=context['course_id'])
            
            if metric_name == 'average_grade':
                avg_grade = queryset.aggregate(avg=Avg('score'))['avg'] or 0
                return {'average': round(float(avg_grade), 2)}
            
            elif metric_name == 'pass_rate':
                total = queryset.count()
                passed = queryset.filter(score__gte=60).count()
                rate = (passed / total * 100) if total > 0 else 0
                return {'pass_rate': round(rate, 2), 'total': total, 'passed': passed}
            
            return {'value': 0}
            
        except Exception as e:
            logger.error(f"Error calculating student performance metric: {e}")
            return {'error': str(e)}
    
    def get_available_data_sources(self) -> List[Dict[str, str]]:
        """Get list of available data sources"""
        sources = []
        for name in self.data_registry.list_sources():
            source_info = self.data_registry.get_source(name)
            sources.append({
                'name': name,
                'description': source_info.get('description', '')
            })
        return sources


# Global analytics service instance
analytics_service = AnalyticsService()
