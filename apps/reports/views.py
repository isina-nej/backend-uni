from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import models
from django.db.models import Count, Avg
from apps.users.models import User
from apps.courses.models import Course
from apps.grades.models import Grade
from apps.attendance.models import Attendance


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """General dashboard statistics"""
    if request.user.role not in ['admin', 'staff']:
        return Response({'error': 'Permission denied'}, status=403)
    
    stats = {
        'total_students': User.objects.filter(role='student').count(),
        'total_professors': User.objects.filter(role='professor').count(),
        'total_courses': Course.objects.count(),
        'total_grades': Grade.objects.count(),
        'average_grade': Grade.objects.aggregate(avg=Avg('score'))['avg'] or 0,
    }
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_report(request):
    """Individual student academic report"""
    if request.user.role != 'student':
        return Response({'error': 'Only students can access this report'}, status=403)
    
    user = request.user
    grades = Grade.objects.filter(student=user)
    attendance = Attendance.objects.filter(student=user)
    
    report = {
        'student_info': {
            'name': f"{user.first_name} {user.last_name}",
            'student_id': user.student_id,
            'department': user.department,
        },
        'academic_summary': {
            'total_courses': user.enrolled_courses.count(),
            'total_grades': grades.count(),
            'average_grade': grades.aggregate(avg=Avg('score'))['avg'] or 0,
            'attendance_rate': attendance.filter(is_present=True).count() / max(attendance.count(), 1) * 100,
        },
        'recent_grades': [
            {
                'course': grade.course.title,
                'score': float(grade.score),
                'date': grade.date_assigned
            }
            for grade in grades.order_by('-date_assigned')[:5]
        ]
    }
    return Response(report)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_report(request, course_id):
    """Course performance report for professors"""
    if request.user.role not in ['professor', 'admin']:
        return Response({'error': 'Permission denied'}, status=403)
    
    try:
        course = Course.objects.get(id=course_id)
        if request.user.role == 'professor' and course.professor != request.user:
            return Response({'error': 'You can only view reports for your own courses'}, status=403)
        
        grades = Grade.objects.filter(course=course)
        attendance = Attendance.objects.filter(schedule__course=course)
        
        report = {
            'course_info': {
                'title': course.title,
                'code': course.code,
                'professor': course.professor.username,
                'total_students': course.students.count(),
            },
            'performance_stats': {
                'total_grades': grades.count(),
                'average_grade': grades.aggregate(avg=Avg('score'))['avg'] or 0,
                'highest_grade': grades.aggregate(max=models.Max('score'))['max'] or 0,
                'lowest_grade': grades.aggregate(min=models.Min('score'))['min'] or 0,
                'attendance_rate': attendance.filter(is_present=True).count() / max(attendance.count(), 1) * 100,
            },
            'grade_distribution': [
                {'range': 'A (90-100)', 'count': grades.filter(score__gte=90).count()},
                {'range': 'B (80-89)', 'count': grades.filter(score__gte=80, score__lt=90).count()},
                {'range': 'C (70-79)', 'count': grades.filter(score__gte=70, score__lt=80).count()},
                {'range': 'D (60-69)', 'count': grades.filter(score__gte=60, score__lt=70).count()},
                {'range': 'F (0-59)', 'count': grades.filter(score__lt=60).count()},
            ]
        }
        return Response(report)
    
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)
