from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch, Count, Q, Avg
from django.core.cache import cache
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from config.filters import CourseFilter
from config.versioning import VersionedViewMixin
from config.error_handling import get_error_response, ErrorMessages
from apps.users.models import User
from .models import Course
from .serializers import (
    CourseSerializer, CourseListSerializer, CourseDetailSerializer,
    CourseEnrollmentSerializer
)


class CourseViewSet(VersionedViewMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = CourseFilter
    search_fields = ['title', 'code', 'description']
    ordering_fields = ['title', 'code', 'created_at', 'student_count']
    ordering = ['-created_at']
    swagger_tags = ['Courses']

    @extend_schema(
        summary='فهرست دوره‌های آموزشی',
        description='دریافت فهرست دوره‌های آموزشی با امکان فیلتر و جستجو',
        parameters=[
            OpenApiParameter(
                name='title',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='جستجو در عنوان دوره'
            ),
            OpenApiParameter(
                name='professor',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='فیلتر بر اساس استاد'
            ),
        ],
        responses={200: CourseListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """Get list of courses with filtering and search"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='ایجاد دوره آموزشی جدید',
        description='ایجاد دوره آموزشی جدید (فقط برای مدیران)',
        request=CourseSerializer,
        responses={201: CourseSerializer},
        examples=[
            OpenApiExample(
                'Course Creation Example',
                value={
                    'title': 'مبانی برنامه‌نویسی',
                    'code': 'CS101',
                    'description': 'دوره مبانی برنامه‌نویسی',
                    'professor': 1
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        """Create a new course"""
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return CourseListSerializer
        elif self.action == 'retrieve':
            return CourseDetailSerializer
        elif self.action in ['enroll_student', 'unenroll_student']:
            return CourseEnrollmentSerializer
        return CourseSerializer

    def get_queryset(self):
        """Optimized queryset with caching and select_related"""
        cache_key = f'courses_queryset_{self.request.user.id}'
        queryset = cache.get(cache_key)

        if queryset is None:
            base_queryset = Course.objects.select_related(
                'professor'
            ).prefetch_related(
                'students',
                Prefetch('students', queryset=User.objects.only('id', 'username', 'first_name', 'last_name'))
            ).annotate(
                student_count=Count('students')
            )

            user = self.request.user
            if user.user_type == 'ADMIN':
                queryset = base_queryset
            elif user.user_type == 'EMPLOYEE':
                queryset = base_queryset.filter(professor=user)
            else:
                queryset = base_queryset.filter(students=user)

            # Cache for 5 minutes
            cache.set(cache_key, queryset, 300)

        return queryset

    @extend_schema(
        summary='ثبت‌نام دانشجو در دوره',
        description='ثبت‌نام دانشجو در دوره آموزشی',
        request=CourseEnrollmentSerializer,
        responses={
            200: OpenApiExample(
                'Success Response',
                value={
                    'message': 'Student enrolled successfully',
                    'student': {
                        'id': 5,
                        'username': 'student123',
                        'full_name': 'علی احمدی'
                    }
                }
            )
        }
    )
    @action(detail=True, methods=['post'])
    def enroll_student(self, request, pk=None):
        """Enroll a student in course with validation"""
        course = self.get_object()
        serializer = CourseEnrollmentSerializer(
            data=request.data, 
            context={'course': course}
        )
        
        if serializer.is_valid():
            student_id = serializer.validated_data['student_id']
            try:
                student = User.objects.get(id=student_id)
                course.students.add(student)

                # Clear cache
                cache.delete_pattern(f'courses_queryset_*')
                cache.delete('courses_statistics')

                return Response({
                    'message': 'Student enrolled successfully',
                    'student': {
                        'id': student.id,
                        'username': student.username,
                        'full_name': f"{student.first_name} {student.last_name}".strip()
                    }
                })

            except User.DoesNotExist:
                return get_error_response('STUDENT_NOT_FOUND', status_code=404)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='حذف ثبت‌نام دانشجو از دوره',
        description='حذف ثبت‌نام دانشجو از دوره آموزشی',
        request=CourseEnrollmentSerializer,
        responses={200: 'Success'}
    )
    @action(detail=True, methods=['post'])
    def unenroll_student(self, request, pk=None):
        """Unenroll a student from course"""
        course = self.get_object()
        serializer = CourseEnrollmentSerializer(data=request.data)
        
        if serializer.is_valid():
            student_id = serializer.validated_data['student_id']
            try:
                student = User.objects.get(id=student_id)

                if not course.students.filter(id=student.id).exists():
                    return get_error_response('STUDENT_NOT_ENROLLED', status_code=400)

                course.students.remove(student)

                # Clear cache
                cache.delete_pattern(f'courses_queryset_*')
                cache.delete('courses_statistics')

                return Response({
                    'message': 'Student unenrolled successfully',
                    'student': {
                        'id': student.id,
                        'username': student.username,
                        'full_name': f"{student.first_name} {student.last_name}".strip()
                    }
                })

            except User.DoesNotExist:
                return get_error_response('STUDENT_NOT_FOUND', status_code=404)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='آمار دوره‌های آموزشی',
        description='دریافت آمار کلی دوره‌های آموزشی',
        responses={
            200: OpenApiExample(
                'Statistics Response',
                value={
                    'total_courses': 25,
                    'active_courses': 20,
                    'inactive_courses': 5,
                    'avg_students_per_course': 18.5
                }
            )
        }
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get course statistics"""
        cache_key = 'courses_statistics'
        stats = cache.get(cache_key)

        if stats is None:
            total_courses = Course.objects.count()
            active_courses = Course.objects.filter(students__isnull=False).distinct().count()
            avg_students_per_course = Course.objects.annotate(
                student_count=Count('students')
            ).aggregate(avg=Avg('student_count'))['avg'] or 0

            stats = {
                'total_courses': total_courses,
                'active_courses': active_courses,
                'inactive_courses': total_courses - active_courses,
                'avg_students_per_course': round(avg_students_per_course, 2)
            }

            cache.set(cache_key, stats, 600)  # Cache for 10 minutes

        return Response(stats)
