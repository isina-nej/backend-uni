# ==============================================================================
# ANALYTICS ADMIN INTERFACE
# رابط مدیریتی آنالیتیکس
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Dashboard, Widget, Report, ReportExecution, AnalyticsMetric


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    """Admin interface for Dashboard model"""
    
    list_display = [
        'title', 'dashboard_type', 'created_by', 'is_public', 
        'is_active', 'access_count', 'created_at'
    ]
    list_filter = [
        'dashboard_type', 'is_public', 'is_active', 'created_at'
    ]
    search_fields = ['title', 'description', 'created_by__username']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_accessed', 'access_count']
    filter_horizontal = ['allowed_users']
    
    fieldsets = (
        (_('اطلاعات اصلی'), {
            'fields': ('id', 'title', 'description', 'dashboard_type')
        }),
        (_('کنترل دسترسی'), {
            'fields': ('created_by', 'is_public', 'allowed_users', 'allowed_roles')
        }),
        (_('پیکربندی'), {
            'fields': ('layout_config', 'refresh_interval', 'is_active', 'is_default')
        }),
        (_('آمار'), {
            'fields': ('access_count', 'last_accessed', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')


class WidgetInline(admin.TabularInline):
    """Inline widget admin for Dashboard"""
    
    model = Widget
    extra = 0
    fields = [
        'title', 'chart_type', 'data_source', 'position_x', 'position_y',
        'width', 'height', 'is_active', 'order'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    """Admin interface for Widget model"""
    
    list_display = [
        'title', 'dashboard', 'chart_type', 'data_source', 
        'is_active', 'order', 'created_at'
    ]
    list_filter = ['chart_type', 'is_active', 'dashboard__dashboard_type', 'created_at']
    search_fields = ['title', 'description', 'dashboard__title', 'data_source']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        (_('اطلاعات اصلی'), {
            'fields': ('id', 'dashboard', 'title', 'description', 'chart_type')
        }),
        (_('منبع داده'), {
            'fields': ('data_source', 'query_config', 'aggregation_config')
        }),
        (_('چیدمان'), {
            'fields': ('position_x', 'position_y', 'width', 'height', 'order')
        }),
        (_('پیکربندی نمودار'), {
            'fields': ('chart_config', 'refresh_interval', 'cache_duration')
        }),
        (_('وضعیت'), {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('dashboard')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin interface for Report model"""
    
    list_display = [
        'title', 'report_type', 'frequency', 'created_by', 
        'is_public', 'is_active', 'generation_count', 'last_generated'
    ]
    list_filter = [
        'report_type', 'frequency', 'is_public', 'is_active', 'created_at'
    ]
    search_fields = ['title', 'description', 'created_by__username']
    readonly_fields = [
        'id', 'last_generated', 'generation_count', 'created_at', 'updated_at'
    ]
    filter_horizontal = ['allowed_users']
    
    fieldsets = (
        (_('اطلاعات اصلی'), {
            'fields': ('id', 'title', 'description', 'report_type')
        }),
        (_('پیکربندی گزارش'), {
            'fields': ('data_sources', 'filters', 'grouping', 'sorting')
        }),
        (_('زمان‌بندی'), {
            'fields': ('frequency', 'schedule_config')
        }),
        (_('کنترل دسترسی'), {
            'fields': ('created_by', 'is_public', 'allowed_users', 'allowed_roles')
        }),
        (_('خروجی'), {
            'fields': ('export_formats',)
        }),
        (_('وضعیت و آمار'), {
            'fields': (
                'is_active', 'generation_count', 'last_generated', 
                'created_at', 'updated_at'
            )
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')


@admin.register(ReportExecution)
class ReportExecutionAdmin(admin.ModelAdmin):
    """Admin interface for ReportExecution model"""
    
    list_display = [
        'report', 'executed_by', 'status', 'executed_at', 
        'execution_time', 'row_count', 'file_size_formatted'
    ]
    list_filter = ['status', 'executed_at', 'report__report_type']
    search_fields = ['report__title', 'executed_by__username']
    readonly_fields = [
        'id', 'executed_at', 'execution_time', 'memory_usage', 
        'row_count', 'file_size'
    ]
    
    fieldsets = (
        (_('اطلاعات اجرا'), {
            'fields': ('id', 'report', 'executed_by', 'executed_at', 'status')
        }),
        (_('نتایج'), {
            'fields': ('result_data', 'row_count', 'file_path', 'file_size')
        }),
        (_('عملکرد'), {
            'fields': ('execution_time', 'memory_usage')
        }),
        (_('خطاها'), {
            'fields': ('error_message', 'error_traceback'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('report', 'executed_by')
    
    def file_size_formatted(self, obj):
        """Format file size in human readable format"""
        if not obj.file_size:
            return '-'
        
        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    file_size_formatted.short_description = _('اندازه فایل')


@admin.register(AnalyticsMetric)
class AnalyticsMetricAdmin(admin.ModelAdmin):
    """Admin interface for AnalyticsMetric model"""
    
    list_display = [
        'metric_name', 'metric_type', 'period_start', 'period_end',
        'calculated_at', 'expires_at', 'is_expired_status'
    ]
    list_filter = ['metric_type', 'calculated_at', 'expires_at']
    search_fields = ['metric_name', 'cache_key']
    readonly_fields = [
        'id', 'calculated_at', 'cache_key', 'is_expired_status'
    ]
    
    fieldsets = (
        (_('اطلاعات معیار'), {
            'fields': ('id', 'metric_name', 'metric_type', 'value')
        }),
        (_('دوره زمانی'), {
            'fields': ('period_start', 'period_end')
        }),
        (_('زمینه'), {
            'fields': ('context',)
        }),
        (_('کش'), {
            'fields': ('cache_key', 'expires_at', 'is_expired_status')
        }),
        (_('محاسبه'), {
            'fields': ('calculated_at', 'calculated_by')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('calculated_by')
    
    def is_expired_status(self, obj):
        """Show if metric is expired"""
        if obj.is_expired():
            return format_html(
                '<span style="color: red;">انقضا یافته</span>'
            )
        else:
            return format_html(
                '<span style="color: green;">معتبر</span>'
            )
    
    is_expired_status.short_description = _('وضعیت انقضا')


# Custom admin site title
admin.site.site_header = _('سیستم مدیریت دانشگاه - آنالیتیکس')
admin.site.site_title = _('آنالیتیکس دانشگاه')
admin.site.index_title = _('پنل مدیریت آنالیتیکس')
