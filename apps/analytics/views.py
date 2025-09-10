# ==============================================================================
# ANALYTICS API VIEWS
# نماهای API آنالیتیکس
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Dashboard, Widget, Report, ReportExecution, AnalyticsMetric
from .serializers import (
    DashboardSerializer, WidgetSerializer, ReportSerializer,
    ReportExecutionSerializer, AnalyticsMetricSerializer,
    DashboardDataSerializer, DataSourceSerializer, ReportRequestSerializer,
    AnalyticsQuerySerializer, SystemAnalyticsSerializer, DashboardCreateSerializer
)
from .services import analytics_service
import logging

logger = logging.getLogger(__name__)


class AnalyticsPagination(PageNumberPagination):
    """Custom pagination for analytics"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class DashboardViewSet(viewsets.ModelViewSet):
    """ViewSet for managing dashboards"""
    
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = AnalyticsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dashboard_type', 'is_public', 'is_active']
    
    def get_queryset(self):
        """Get dashboards accessible to the user"""
        user = self.request.user
        
        if user.is_superuser:
            return Dashboard.objects.all().order_by('-created_at')
        
        # Get dashboards user can access
        queryset = Dashboard.objects.filter(
            Q(created_by=user) |  # Own dashboards
            Q(is_public=True) |   # Public dashboards
            Q(allowed_users=user)  # Explicitly allowed
        ).distinct().order_by('-created_at')
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return DashboardCreateSerializer
        return DashboardSerializer
    
    @extend_schema(
        summary="Get dashboard data",
        description="Get complete dashboard data with all widgets"
    )
    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):
        """Get dashboard data with all widgets"""
        try:
            dashboard = self.get_object()
            dashboard_data = analytics_service.get_dashboard_data(dashboard, request.user)
            
            return Response(dashboard_data)
            
        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return Response({
                'error': 'Failed to get dashboard data'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Clone dashboard",
        description="Create a copy of an existing dashboard"
    )
    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        """Clone an existing dashboard"""
        try:
            original_dashboard = self.get_object()
            
            # Create new dashboard
            new_dashboard = Dashboard.objects.create(
                title=f"{original_dashboard.title} (Copy)",
                description=original_dashboard.description,
                dashboard_type=original_dashboard.dashboard_type,
                created_by=request.user,
                layout_config=original_dashboard.layout_config,
                refresh_interval=original_dashboard.refresh_interval
            )
            
            # Clone widgets
            for widget in original_dashboard.widgets.all():
                Widget.objects.create(
                    dashboard=new_dashboard,
                    title=widget.title,
                    description=widget.description,
                    chart_type=widget.chart_type,
                    data_source=widget.data_source,
                    query_config=widget.query_config,
                    aggregation_config=widget.aggregation_config,
                    position_x=widget.position_x,
                    position_y=widget.position_y,
                    width=widget.width,
                    height=widget.height,
                    chart_config=widget.chart_config,
                    refresh_interval=widget.refresh_interval,
                    cache_duration=widget.cache_duration,
                    order=widget.order
                )
            
            serializer = DashboardSerializer(new_dashboard, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error cloning dashboard: {e}")
            return Response({
                'error': 'Failed to clone dashboard'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Set as default dashboard",
        description="Set this dashboard as the default for the user"
    )
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Set dashboard as default for user"""
        try:
            dashboard = self.get_object()
            
            # Remove default from other dashboards
            Dashboard.objects.filter(
                created_by=request.user,
                is_default=True
            ).update(is_default=False)
            
            # Set this as default
            dashboard.is_default = True
            dashboard.save()
            
            return Response({'message': 'Dashboard set as default'})
            
        except Exception as e:
            logger.error(f"Error setting default dashboard: {e}")
            return Response({
                'error': 'Failed to set default dashboard'
            }, status=status.HTTP_400_BAD_REQUEST)


class WidgetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing widgets"""
    
    serializer_class = WidgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dashboard', 'chart_type', 'is_active']
    
    def get_queryset(self):
        """Get widgets for accessible dashboards"""
        user = self.request.user
        
        # Get accessible dashboards
        accessible_dashboards = Dashboard.objects.filter(
            Q(created_by=user) |
            Q(is_public=True) |
            Q(allowed_users=user)
        ).distinct()
        
        return Widget.objects.filter(
            dashboard__in=accessible_dashboards
        ).order_by('dashboard', 'order')
    
    @extend_schema(
        summary="Get widget data",
        description="Get processed data for a specific widget"
    )
    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):
        """Get widget data"""
        try:
            widget = self.get_object()
            widget_data = analytics_service.get_widget_data(widget)
            
            return Response({
                'widget_id': str(widget.id),
                'title': widget.title,
                'chart_type': widget.chart_type,
                'data': widget_data,
                'last_updated': timezone.now()
            })
            
        except Exception as e:
            logger.error(f"Error getting widget data: {e}")
            return Response({
                'error': 'Failed to get widget data'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Refresh widget data",
        description="Force refresh widget data and clear cache"
    )
    @action(detail=True, methods=['post'])
    def refresh(self, request, pk=None):
        """Refresh widget data"""
        try:
            widget = self.get_object()
            
            # Clear cache for this widget
            from django.core.cache import cache
            cache_key = f"widget_data_{widget.id}_{hash(str(widget.query_config))}"
            cache.delete(cache_key)
            
            # Get fresh data
            widget_data = analytics_service.get_widget_data(widget)
            
            return Response({
                'message': 'Widget data refreshed',
                'data': widget_data
            })
            
        except Exception as e:
            logger.error(f"Error refreshing widget data: {e}")
            return Response({
                'error': 'Failed to refresh widget data'
            }, status=status.HTTP_400_BAD_REQUEST)


class ReportViewSet(viewsets.ModelViewSet):
    """ViewSet for managing reports"""
    
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = AnalyticsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['report_type', 'frequency', 'is_active']
    
    def get_queryset(self):
        """Get reports accessible to the user"""
        user = self.request.user
        
        if user.is_superuser:
            return Report.objects.all().order_by('-created_at')
        
        queryset = Report.objects.filter(
            Q(created_by=user) |
            Q(is_public=True) |
            Q(allowed_users=user)
        ).distinct().order_by('-created_at')
        
        return queryset
    
    @extend_schema(
        summary="Execute report",
        description="Generate and execute a report",
        request=ReportRequestSerializer
    )
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """Execute a report"""
        try:
            report = self.get_object()
            
            # Generate report
            execution = analytics_service.generate_report(report, request.user)
            
            serializer = ReportExecutionSerializer(execution)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except PermissionError:
            return Response({
                'error': 'Access denied to this report'
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(f"Error executing report: {e}")
            return Response({
                'error': 'Failed to execute report'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Get report executions",
        description="Get execution history for a report"
    )
    @action(detail=True, methods=['get'])
    def executions(self, request, pk=None):
        """Get report execution history"""
        try:
            report = self.get_object()
            executions = report.executions.order_by('-executed_at')[:10]  # Last 10 executions
            
            serializer = ReportExecutionSerializer(executions, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting report executions: {e}")
            return Response({
                'error': 'Failed to get report executions'
            }, status=status.HTTP_400_BAD_REQUEST)


class ReportExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing report executions"""
    
    serializer_class = ReportExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = AnalyticsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'executed_by']
    
    def get_queryset(self):
        """Get executions for accessible reports"""
        user = self.request.user
        
        if user.is_superuser:
            return ReportExecution.objects.all().order_by('-executed_at')
        
        # Get accessible reports
        accessible_reports = Report.objects.filter(
            Q(created_by=user) |
            Q(is_public=True) |
            Q(allowed_users=user)
        ).distinct()
        
        return ReportExecution.objects.filter(
            report__in=accessible_reports
        ).order_by('-executed_at')


class AnalyticsViewSet(viewsets.ViewSet):
    """ViewSet for general analytics operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Get available data sources",
        description="Get list of available data sources for widgets"
    )
    @action(detail=False, methods=['get'])
    def data_sources(self, request):
        """Get available data sources"""
        try:
            sources = analytics_service.get_available_data_sources()
            serializer = DataSourceSerializer(sources, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting data sources: {e}")
            return Response({
                'error': 'Failed to get data sources'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Execute custom query",
        description="Execute a custom analytics query",
        request=AnalyticsQuerySerializer
    )
    @action(detail=False, methods=['post'])
    def query(self, request):
        """Execute custom analytics query"""
        try:
            serializer = AnalyticsQuerySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            data_source_name = serializer.validated_data['data_source']
            filters = serializer.validated_data.get('filters', {})
            
            # Get data source
            data_source = analytics_service.data_registry.get_source(data_source_name)
            if not data_source:
                return Response({
                    'error': f'Data source {data_source_name} not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Execute query
            result = data_source['query_func'](filters=filters)
            
            return Response({
                'data_source': data_source_name,
                'result': result,
                'executed_at': timezone.now()
            })
            
        except Exception as e:
            logger.error(f"Error executing custom query: {e}")
            return Response({
                'error': 'Failed to execute query'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Get system analytics",
        description="Get overall system analytics and statistics"
    )
    @action(detail=False, methods=['get'])
    def system_stats(self, request):
        """Get system-wide analytics"""
        try:
            # Calculate system statistics
            from django.contrib.auth import get_user_model
            from apps.courses.models import Course
            User = get_user_model()
            
            stats = {
                'total_users': User.objects.count(),
                'active_users': User.objects.filter(is_active=True).count(),
                'total_courses': Course.objects.count() if hasattr(Course, 'objects') else 0,
                'total_enrollments': 0,  # Would calculate from enrollments
                'average_grade': 0.0,    # Would calculate from grades
                'attendance_rate': 0.0,  # Would calculate from attendance
                'revenue_this_month': 0.0,  # Would calculate from payments
                'dashboards_count': Dashboard.objects.count(),
                'reports_count': Report.objects.count(),
                'last_updated': timezone.now()
            }
            
            # Get user activity data
            user_activity = analytics_service.data_registry.get_source('user_activity')
            if user_activity:
                activity_data = user_activity['query_func']()
                stats.update(activity_data)
            
            serializer = SystemAnalyticsSerializer(stats)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return Response({
                'error': 'Failed to get system statistics'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Get user's default dashboard",
        description="Get the default dashboard for the current user"
    )
    @action(detail=False, methods=['get'])
    def default_dashboard(self, request):
        """Get user's default dashboard"""
        try:
            # Try to get user's default dashboard
            default_dashboard = Dashboard.objects.filter(
                created_by=request.user,
                is_default=True,
                is_active=True
            ).first()
            
            if not default_dashboard:
                # Get first accessible dashboard
                default_dashboard = Dashboard.objects.filter(
                    Q(created_by=request.user) |
                    Q(is_public=True) |
                    Q(allowed_users=request.user),
                    is_active=True
                ).first()
            
            if default_dashboard:
                dashboard_data = analytics_service.get_dashboard_data(default_dashboard, request.user)
                return Response(dashboard_data)
            else:
                return Response({
                    'message': 'No accessible dashboards found'
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"Error getting default dashboard: {e}")
            return Response({
                'error': 'Failed to get default dashboard'
            }, status=status.HTTP_400_BAD_REQUEST)


class DataSourceListView(APIView):
    """List available data sources"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="List Data Sources",
        description="Get all available data sources for analytics",
        responses={200: DataSourceSerializer(many=True)}
    )
    def get(self, request):
        """List all available data sources"""
        try:
            sources = analytics_service.get_available_data_sources()
            serializer = DataSourceSerializer(sources, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error listing data sources: {e}")
            return Response({
                'error': 'Failed to list data sources'
            }, status=status.HTTP_400_BAD_REQUEST)


class DataSourceDataView(APIView):
    """Get data from a specific data source"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Get Data Source Data",
        description="Get data from a specific data source",
        parameters=[
            OpenApiParameter(
                name="source_name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Name of the data source"
            ),
            OpenApiParameter(
                name="filters",
                type=OpenApiTypes.OBJECT,
                location=OpenApiParameter.QUERY,
                description="JSON filters for the data source"
            )
        ]
    )
    def get(self, request, source_name=None):
        """Get data from a specific data source"""
        try:
            # Get filters from query params
            filters = request.GET.get('filters')
            if filters:
                import json
                try:
                    filters = json.loads(filters)
                except json.JSONDecodeError:
                    filters = None
            
            # Get data from source
            data = analytics_service.get_data_source_data(source_name, filters)
            
            if data is not None:
                return Response({
                    'source_name': source_name,
                    'data': data,
                    'timestamp': timezone.now()
                })
            else:
                return Response({
                    'error': f'Data source "{source_name}" not found'
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"Error getting data source data: {e}")
            return Response({
                'error': 'Failed to get data source data'
            }, status=status.HTTP_400_BAD_REQUEST)
