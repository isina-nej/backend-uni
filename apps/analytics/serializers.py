# ==============================================================================
# ANALYTICS API SERIALIZERS
# سریالایزرهای API آنالیتیکس
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Dashboard, Widget, Report, ReportExecution, AnalyticsMetric

User = get_user_model()


class DashboardSerializer(serializers.ModelSerializer):
    """Serializer for Dashboard model"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    widget_count = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = Dashboard
        fields = [
            'id', 'title', 'description', 'dashboard_type',
            'created_by', 'created_by_username', 'is_public',
            'layout_config', 'refresh_interval', 'is_active',
            'is_default', 'created_at', 'updated_at', 'last_accessed',
            'access_count', 'widget_count', 'can_edit'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at',
            'last_accessed', 'access_count'
        ]
    
    def get_widget_count(self, obj):
        """Get count of active widgets"""
        return obj.widgets.filter(is_active=True).count()
    
    def get_can_edit(self, obj):
        """Check if current user can edit this dashboard"""
        request = self.context.get('request')
        if request and request.user:
            return obj.created_by == request.user or request.user.is_superuser
        return False
    
    def create(self, validated_data):
        """Set created_by to current user"""
        request = self.context.get('request')
        if request:
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class WidgetSerializer(serializers.ModelSerializer):
    """Serializer for Widget model"""
    
    dashboard_title = serializers.CharField(source='dashboard.title', read_only=True)
    
    class Meta:
        model = Widget
        fields = [
            'id', 'dashboard', 'dashboard_title', 'title', 'description',
            'chart_type', 'data_source', 'query_config', 'aggregation_config',
            'position_x', 'position_y', 'width', 'height', 'chart_config',
            'refresh_interval', 'cache_duration', 'is_active', 'order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_position_x(self, value):
        """Validate position_x is within reasonable bounds"""
        if value < 0 or value > 20:
            raise serializers.ValidationError("Position X must be between 0 and 20")
        return value
    
    def validate_position_y(self, value):
        """Validate position_y is within reasonable bounds"""
        if value < 0 or value > 50:
            raise serializers.ValidationError("Position Y must be between 0 and 50")
        return value


class WidgetDataSerializer(serializers.Serializer):
    """Serializer for widget data response"""
    
    widget_id = serializers.UUIDField()
    title = serializers.CharField()
    chart_type = serializers.CharField()
    data = serializers.JSONField()
    last_updated = serializers.DateTimeField()
    error = serializers.CharField(required=False)


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Report model"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    can_execute = serializers.SerializerMethodField()
    last_execution_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = [
            'id', 'title', 'description', 'report_type', 'data_sources',
            'filters', 'grouping', 'sorting', 'frequency', 'schedule_config',
            'created_by', 'created_by_username', 'is_public', 'export_formats',
            'is_active', 'last_generated', 'generation_count', 'created_at',
            'updated_at', 'can_execute', 'last_execution_status'
        ]
        read_only_fields = [
            'id', 'created_by', 'last_generated', 'generation_count',
            'created_at', 'updated_at'
        ]
    
    def get_can_execute(self, obj):
        """Check if current user can execute this report"""
        request = self.context.get('request')
        if request and request.user:
            return obj.can_access(request.user)
        return False
    
    def get_last_execution_status(self, obj):
        """Get status of last execution"""
        last_execution = obj.executions.first()
        if last_execution:
            return {
                'status': last_execution.status,
                'executed_at': last_execution.executed_at,
                'execution_time': last_execution.execution_time
            }
        return None
    
    def create(self, validated_data):
        """Set created_by to current user"""
        request = self.context.get('request')
        if request:
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class ReportExecutionSerializer(serializers.ModelSerializer):
    """Serializer for ReportExecution model"""
    
    report_title = serializers.CharField(source='report.title', read_only=True)
    executed_by_username = serializers.CharField(source='executed_by.username', read_only=True)
    file_size_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = ReportExecution
        fields = [
            'id', 'report', 'report_title', 'executed_by', 'executed_by_username',
            'executed_at', 'status', 'result_data', 'row_count', 'file_path',
            'file_size', 'file_size_formatted', 'execution_time', 'memory_usage',
            'error_message'
        ]
        read_only_fields = [
            'id', 'executed_at', 'execution_time', 'memory_usage',
            'row_count', 'file_size'
        ]
    
    def get_file_size_formatted(self, obj):
        """Format file size in human readable format"""
        if not obj.file_size:
            return None
        
        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"


class AnalyticsMetricSerializer(serializers.ModelSerializer):
    """Serializer for AnalyticsMetric model"""
    
    calculated_by_username = serializers.CharField(source='calculated_by.username', read_only=True)
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = AnalyticsMetric
        fields = [
            'id', 'metric_name', 'metric_type', 'value', 'context',
            'period_start', 'period_end', 'calculated_at', 'calculated_by',
            'calculated_by_username', 'expires_at', 'is_expired'
        ]
        read_only_fields = [
            'id', 'calculated_at', 'cache_key'
        ]
    
    def get_is_expired(self, obj):
        """Check if metric is expired"""
        return obj.is_expired()


class DashboardDataSerializer(serializers.Serializer):
    """Serializer for complete dashboard data"""
    
    dashboard_id = serializers.UUIDField()
    title = serializers.CharField()
    layout_config = serializers.JSONField()
    widgets = serializers.DictField()
    refresh_interval = serializers.IntegerField()
    last_updated = serializers.DateTimeField()


class DataSourceSerializer(serializers.Serializer):
    """Serializer for available data sources"""
    
    name = serializers.CharField()
    description = serializers.CharField()


class ChartConfigSerializer(serializers.Serializer):
    """Serializer for chart configuration"""
    
    chart_type = serializers.ChoiceField(choices=[
        'line', 'bar', 'pie', 'doughnut', 'area', 'scatter',
        'radar', 'heatmap', 'gauge', 'table', 'kpi'
    ])
    title = serializers.CharField(required=False)
    colors = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    legend = serializers.BooleanField(default=True)
    grid = serializers.BooleanField(default=True)
    responsive = serializers.BooleanField(default=True)
    animation = serializers.BooleanField(default=True)


class FilterConfigSerializer(serializers.Serializer):
    """Serializer for filter configuration"""
    
    field = serializers.CharField()
    operator = serializers.ChoiceField(choices=[
        'equals', 'not_equals', 'greater_than', 'less_than',
        'greater_equal', 'less_equal', 'contains', 'starts_with',
        'ends_with', 'in', 'not_in', 'between', 'is_null', 'is_not_null'
    ])
    value = serializers.JSONField()


class ReportRequestSerializer(serializers.Serializer):
    """Serializer for report generation request"""
    
    report_id = serializers.UUIDField()
    format = serializers.ChoiceField(
        choices=['json', 'csv', 'excel', 'pdf'],
        default='json'
    )
    filters = serializers.DictField(required=False)
    email_results = serializers.BooleanField(default=False)


class AnalyticsQuerySerializer(serializers.Serializer):
    """Serializer for custom analytics queries"""
    
    data_source = serializers.CharField()
    filters = serializers.DictField(required=False)
    aggregation = serializers.DictField(required=False)
    grouping = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    ordering = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    limit = serializers.IntegerField(min_value=1, max_value=1000, required=False)


class DashboardCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating dashboards with widgets"""
    
    widgets = WidgetSerializer(many=True, required=False)
    
    class Meta:
        model = Dashboard
        fields = [
            'title', 'description', 'dashboard_type', 'is_public',
            'layout_config', 'refresh_interval', 'widgets'
        ]
    
    def create(self, validated_data):
        """Create dashboard with widgets"""
        widgets_data = validated_data.pop('widgets', [])
        
        request = self.context.get('request')
        if request:
            validated_data['created_by'] = request.user
        
        dashboard = Dashboard.objects.create(**validated_data)
        
        # Create widgets
        for widget_data in widgets_data:
            Widget.objects.create(dashboard=dashboard, **widget_data)
        
        return dashboard


class SystemAnalyticsSerializer(serializers.Serializer):
    """Serializer for system-wide analytics"""
    
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_courses = serializers.IntegerField()
    total_enrollments = serializers.IntegerField()
    average_grade = serializers.FloatField()
    attendance_rate = serializers.FloatField()
    revenue_this_month = serializers.DecimalField(max_digits=12, decimal_places=2)
    dashboards_count = serializers.IntegerField()
    reports_count = serializers.IntegerField()
    last_updated = serializers.DateTimeField()
