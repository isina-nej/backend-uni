# ==============================================================================
# ADVANCED FILTERS FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import django_filters
from django.db.models import Q, Count, Avg
from django_filters import rest_framework as filters
from django.core.cache import cache
from apps.courses.models import Course
from apps.users.models import User


class CourseFilter(django_filters.FilterSet):
    """Advanced filtering for courses"""

    # Basic filters
    title = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')
    professor = django_filters.NumberFilter(field_name='professor__id')
    professor_name = django_filters.CharFilter(method='filter_professor_name')

    # Date filters
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    # Student count filters
    min_students = django_filters.NumberFilter(method='filter_min_students')
    max_students = django_filters.NumberFilter(method='filter_max_students')

    # Status filters
    has_students = django_filters.BooleanFilter(method='filter_has_students')
    is_full = django_filters.BooleanFilter(method='filter_is_full')

    # Search
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Course
        fields = ['title', 'code', 'professor', 'created_at']

    def filter_professor_name(self, queryset, name, value):
        """Filter by professor name"""
        return queryset.filter(
            Q(professor__first_name__icontains=value) |
            Q(professor__last_name__icontains=value) |
            Q(professor__username__icontains=value)
        )

    def filter_min_students(self, queryset, name, value):
        """Filter courses with minimum number of students"""
        return queryset.annotate(
            student_count=Count('students')
        ).filter(student_count__gte=value)

    def filter_max_students(self, queryset, name, value):
        """Filter courses with maximum number of students"""
        return queryset.annotate(
            student_count=Count('students')
        ).filter(student_count__lte=value)

    def filter_has_students(self, queryset, name, value):
        """Filter courses that have/don't have students"""
        if value:
            return queryset.filter(students__isnull=False).distinct()
        else:
            return queryset.filter(students__isnull=True)

    def filter_is_full(self, queryset, name, value):
        """Filter courses that are full/not full"""
        # Assuming max capacity of 50
        if value:
            return queryset.annotate(
                student_count=Count('students')
            ).filter(student_count__gte=50)
        else:
            return queryset.annotate(
                student_count=Count('students')
            ).filter(student_count__lt=50)

    def filter_search(self, queryset, name, value):
        """Advanced search across multiple fields"""
        return queryset.filter(
            Q(title__icontains=value) |
            Q(code__icontains=value) |
            Q(description__icontains=value) |
            Q(professor__first_name__icontains=value) |
            Q(professor__last_name__icontains=value) |
            Q(professor__username__icontains=value)
        )


class UserFilter(django_filters.FilterSet):
    """Advanced filtering for users"""

    # Basic filters
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    user_type = django_filters.ChoiceFilter(choices=User.USER_TYPES)
    is_active = django_filters.BooleanFilter()

    # Date filters
    date_joined_after = django_filters.DateFilter(field_name='date_joined', lookup_expr='gte')
    date_joined_before = django_filters.DateFilter(field_name='date_joined', lookup_expr='lte')
    last_login_after = django_filters.DateFilter(field_name='last_login', lookup_expr='gte')
    last_login_before = django_filters.DateFilter(field_name='last_login', lookup_expr='lte')

    # Advanced filters
    has_employee = django_filters.BooleanFilter(method='filter_has_employee')
    has_student = django_filters.BooleanFilter(method='filter_has_student')

    # Search
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'is_active']

    def filter_has_employee(self, queryset, name, value):
        """Filter users that have/don't have employee profile"""
        if value:
            return queryset.filter(employee__isnull=False)
        else:
            return queryset.filter(employee__isnull=True)

    def filter_has_student(self, queryset, name, value):
        """Filter users that have/don't have student profile"""
        if value:
            return queryset.filter(student__isnull=False)
        else:
            return queryset.filter(student__isnull=True)

    def filter_search(self, queryset, name, value):
        """Advanced search across multiple fields"""
        return queryset.filter(
            Q(username__icontains=value) |
            Q(email__icontains=value) |
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(national_id__icontains=value) |
            Q(phone__icontains=value)
        )


# Filter backends
class AdvancedFilterBackend(filters.DjangoFilterBackend):
    """Enhanced filter backend with additional features"""

    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # Add request to filterset kwargs for custom filtering
        kwargs['request'] = request

        return kwargs

    def filter_queryset(self, request, queryset, view):
        """Apply filters with caching"""
        filterset = self.get_filterset(request, queryset, view)

        if filterset is None:
            return queryset

        # Cache filter results for performance
        cache_key = f'filter_{view.__class__.__name__}_{hash(str(request.GET))}'
        filtered_queryset = cache.get(cache_key)

        if filtered_queryset is None:
            filtered_queryset = filterset.qs
            cache.set(cache_key, filtered_queryset, 300)  # Cache for 5 minutes

        return filtered_queryset
