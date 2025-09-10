# ==============================================================================
# COMPREHENSIVE CRUD VIEWS FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg, Sum
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from config.filters import UserFilter, CourseFilter


# ==============================================================================
# GRADES MANAGEMENT
# ==============================================================================

from apps.grades.models import Grade
from apps.grades.serializers import GradeSerializer


class GradeFilter(django_filters.FilterSet):
    """Advanced filtering for grades"""
    student = django_filters.NumberFilter(field_name='student__id')
    course = django_filters.NumberFilter(field_name='course__id')
    min_score = django_filters.NumberFilter(field_name='score', lookup_expr='gte')
    max_score = django_filters.NumberFilter(field_name='score', lookup_expr='lte')
    exam_type = django_filters.ChoiceFilter(choices=Grade.GRADE_TYPES)
    passed = django_filters.BooleanFilter(method='filter_passed')

    class Meta:
        model = Grade
        fields = ['student', 'course', 'exam_type']

    def filter_passed(self, queryset, name, value):
        if value:
            return queryset.filter(score__gte=10)
        else:
            return queryset.filter(score__lt=10)


class GradeViewSet(viewsets.ModelViewSet):
    """مدیریت نمرات"""
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = GradeFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__username', 'course__title', 'course__code']
    ordering_fields = ['score', 'created_at', 'exam_date']
    ordering = ['-created_at']

    def get_queryset(self):
        """Optimized queryset with user permissions"""
        user = self.request.user
        base_queryset = Grade.objects.select_related('student', 'course', 'course__professor')

        if user.user_type == 'ADMIN':
            return base_queryset
        elif user.user_type == 'EMPLOYEE':
            # Professors see only their course grades
            return base_queryset.filter(course__professor=user)
        else:
            # Students see only their own grades
            return base_queryset.filter(student=user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Grade statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total_grades': queryset.count(),
            'average_score': queryset.aggregate(avg=Avg('score'))['avg'] or 0,
            'pass_rate': queryset.filter(score__gte=10).count() / max(queryset.count(), 1) * 100,
            'grade_distribution': queryset.values('exam_type').annotate(count=Count('id'))
        }
        
        return Response(stats)


# ==============================================================================
# ATTENDANCE MANAGEMENT  
# ==============================================================================

import django_filters
from apps.attendance.models import Attendance
from apps.attendance.serializers import AttendanceSerializer


class AttendanceFilter(django_filters.FilterSet):
    """Advanced filtering for attendance"""
    student = django_filters.NumberFilter(field_name='student__id')
    course = django_filters.NumberFilter(field_name='course__id')
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    status = django_filters.ChoiceFilter(choices=Attendance.STATUS_CHOICES)

    class Meta:
        model = Attendance
        fields = ['student', 'course', 'status', 'date']


class AttendanceViewSet(viewsets.ModelViewSet):
    """مدیریت حضور و غیاب"""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = AttendanceFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__username', 'course__title']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        """Optimized queryset with user permissions"""
        user = self.request.user
        base_queryset = Attendance.objects.select_related('student', 'course')

        if user.user_type == 'ADMIN':
            return base_queryset
        elif user.user_type == 'EMPLOYEE':
            return base_queryset.filter(course__professor=user)
        else:
            return base_queryset.filter(student=user)

    @action(detail=False, methods=['post'])
    def bulk_mark(self, request):
        """Bulk mark attendance"""
        course_id = request.data.get('course_id')
        date = request.data.get('date')
        attendances = request.data.get('attendances', [])

        if not all([course_id, date, attendances]):
            return Response(
                {'error': 'course_id, date, and attendances are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        created_count = 0
        for attendance_data in attendances:
            student_id = attendance_data.get('student_id')
            attendance_status = attendance_data.get('status', 'PRESENT')

            Attendance.objects.update_or_create(
                student_id=student_id,
                course_id=course_id,
                date=date,
                defaults={'status': attendance_status}
            )
            created_count += 1

        return Response({
            'message': f'{created_count} attendance records processed',
            'course_id': course_id,
            'date': date
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Attendance statistics"""
        queryset = self.get_queryset()
        
        total_records = queryset.count()
        present_count = queryset.filter(status='PRESENT').count()
        
        stats = {
            'total_records': total_records,
            'present_count': present_count,
            'absent_count': queryset.filter(status='ABSENT').count(),
            'late_count': queryset.filter(status='LATE').count(),
            'attendance_rate': (present_count / max(total_records, 1)) * 100
        }
        
        return Response(stats)


# ==============================================================================
# SCHEDULES MANAGEMENT
# ==============================================================================

from apps.schedules.models import Schedule
from apps.schedules.serializers import ScheduleSerializer


class ScheduleFilter(django_filters.FilterSet):
    """Advanced filtering for schedules"""
    course = django_filters.NumberFilter(field_name='course__id')
    professor = django_filters.NumberFilter(field_name='course__professor__id')
    day_of_week = django_filters.ChoiceFilter(choices=Schedule.DAYS_OF_WEEK)
    start_time_after = django_filters.TimeFilter(field_name='start_time', lookup_expr='gte')
    start_time_before = django_filters.TimeFilter(field_name='start_time', lookup_expr='lte')

    class Meta:
        model = Schedule
        fields = ['course', 'day_of_week', 'classroom']


class ScheduleViewSet(viewsets.ModelViewSet):
    """مدیریت برنامه کلاسی"""
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = ScheduleFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['course__title', 'course__code', 'classroom']
    ordering_fields = ['day_of_week', 'start_time', 'end_time']
    ordering = ['day_of_week', 'start_time']

    def get_queryset(self):
        """Optimized queryset with user permissions"""
        user = self.request.user
        base_queryset = Schedule.objects.select_related('course', 'course__professor')

        if user.user_type == 'ADMIN':
            return base_queryset
        elif user.user_type == 'EMPLOYEE':
            return base_queryset.filter(course__professor=user)
        else:
            # Students see schedules for their enrolled courses
            return base_queryset.filter(course__students=user)

    @action(detail=False, methods=['get'])
    def weekly_schedule(self, request):
        """Get weekly schedule for current user"""
        user = request.user
        queryset = self.get_queryset()
        
        # Group by day of week
        weekly_data = {}
        for schedule in queryset:
            day = schedule.get_day_of_week_display()
            if day not in weekly_data:
                weekly_data[day] = []
            
            weekly_data[day].append({
                'id': schedule.id,
                'course': schedule.course.title,
                'course_code': schedule.course.code,
                'start_time': schedule.start_time,
                'end_time': schedule.end_time,
                'classroom': schedule.classroom
            })
        
        return Response(weekly_data)

    @action(detail=False, methods=['get'])
    def conflicts(self, request):
        """Check for schedule conflicts"""
        conflicts = []
        schedules = self.get_queryset()
        
        for schedule in schedules:
            overlapping = schedules.filter(
                day_of_week=schedule.day_of_week,
                start_time__lt=schedule.end_time,
                end_time__gt=schedule.start_time
            ).exclude(id=schedule.id)
            
            if overlapping.exists():
                conflicts.append({
                    'schedule_id': schedule.id,
                    'course': schedule.course.title,
                    'conflicts_with': [
                        {
                            'schedule_id': s.id,
                            'course': s.course.title,
                            'time': f"{s.start_time} - {s.end_time}"
                        }
                        for s in overlapping
                    ]
                })
        
        return Response({'conflicts': conflicts})


# ==============================================================================
# EXAMS MANAGEMENT
# ==============================================================================

from apps.exams.models import Exam
from apps.exams.serializers import ExamSerializer


class ExamFilter(django_filters.FilterSet):
    """Advanced filtering for exams"""
    course = django_filters.NumberFilter(field_name='course__id')
    exam_type = django_filters.ChoiceFilter(choices=Exam.EXAM_TYPES)
    date_from = django_filters.DateTimeFilter(field_name='exam_date', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name='exam_date', lookup_expr='lte')
    duration_min = django_filters.NumberFilter(field_name='duration', lookup_expr='gte')
    duration_max = django_filters.NumberFilter(field_name='duration', lookup_expr='lte')

    class Meta:
        model = Exam
        fields = ['course', 'exam_type', 'exam_date']


class ExamViewSet(viewsets.ModelViewSet):
    """مدیریت امتحانات"""
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = ExamFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['course__title', 'course__code', 'title']
    ordering_fields = ['exam_date', 'duration', 'created_at']
    ordering = ['exam_date']

    def get_queryset(self):
        """Optimized queryset with user permissions"""
        user = self.request.user
        base_queryset = Exam.objects.select_related('course', 'course__professor')

        if user.user_type == 'ADMIN':
            return base_queryset
        elif user.user_type == 'EMPLOYEE':
            return base_queryset.filter(course__professor=user)
        else:
            # Students see exams for their enrolled courses
            return base_queryset.filter(course__students=user)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming exams"""
        from django.utils import timezone
        
        upcoming_exams = self.get_queryset().filter(
            exam_date__gte=timezone.now()
        ).order_by('exam_date')[:10]
        
        serializer = self.get_serializer(upcoming_exams, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def calendar(self, request):
        """Get exam calendar for current month"""
        from django.utils import timezone
        from datetime import datetime
        
        # Get month parameter or use current month
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        if month and year:
            start_date = datetime(int(year), int(month), 1)
            if int(month) == 12:
                end_date = datetime(int(year) + 1, 1, 1)
            else:
                end_date = datetime(int(year), int(month) + 1, 1)
        else:
            now = timezone.now()
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if now.month == 12:
                end_date = now.replace(year=now.year + 1, month=1, day=1)
            else:
                end_date = now.replace(month=now.month + 1, day=1)
        
        exams = self.get_queryset().filter(
            exam_date__gte=start_date,
            exam_date__lt=end_date
        ).order_by('exam_date')
        
        calendar_data = {}
        for exam in exams:
            date_key = exam.exam_date.date().isoformat()
            if date_key not in calendar_data:
                calendar_data[date_key] = []
            
            calendar_data[date_key].append({
                'id': exam.id,
                'title': exam.title or exam.course.title,
                'course': exam.course.title,
                'time': exam.exam_date.time().isoformat(),
                'duration': exam.duration,
                'type': exam.exam_type
            })
        
        return Response(calendar_data)
