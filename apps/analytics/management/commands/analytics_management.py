# ==============================================================================
# ANALYTICS MANAGEMENT COMMANDS
# دستورات مدیریت آنالیتیکس
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
from apps.analytics.models import Dashboard, Widget, Report, AnalyticsMetric
from apps.analytics.services import analytics_service
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    """Management command for analytics system operations"""
    
    help = 'Manage analytics system - create samples, generate reports, cleanup'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['create_samples', 'test_query', 'cleanup_metrics', 'generate_report', 'list_sources'],
            default='create_samples',
            help='Action to perform'
        )
        
        parser.add_argument(
            '--user',
            type=str,
            help='Username for operations requiring user context'
        )
        
        parser.add_argument(
            '--dashboard-id',
            type=str,
            help='Dashboard ID for specific operations'
        )
        
        parser.add_argument(
            '--data-source',
            type=str,
            default='student_count',
            help='Data source name for testing'
        )
        
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days for cleanup operations'
        )
    
    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'create_samples':
            self.create_sample_data(options)
        elif action == 'test_query':
            self.test_data_query(options)
        elif action == 'cleanup_metrics':
            self.cleanup_old_metrics(options)
        elif action == 'generate_report':
            self.generate_sample_report(options)
        elif action == 'list_sources':
            self.list_data_sources()
    
    def create_sample_data(self, options):
        """Create sample dashboards and widgets for testing"""
        try:
            # Get or create admin user
            username = options.get('user', 'admin')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User {username} not found')
                )
                return
            
            # Create sample dashboard
            dashboard, created = Dashboard.objects.get_or_create(
                title='Sample Analytics Dashboard',
                created_by=user,
                defaults={
                    'description': 'Sample dashboard for testing analytics features',
                    'dashboard_type': 'admin',
                    'is_public': True,
                    'layout_config': {
                        'grid_size': 12,
                        'row_height': 100
                    },
                    'refresh_interval': 300
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created dashboard: {dashboard.title}')
                )
            
            # Create sample widgets
            sample_widgets = [
                {
                    'title': 'Total Students',
                    'chart_type': 'kpi',
                    'data_source': 'student_count',
                    'position_x': 0,
                    'position_y': 0,
                    'width': 3,
                    'height': 2
                },
                {
                    'title': 'Students by Status',
                    'chart_type': 'pie',
                    'data_source': 'student_by_status',
                    'position_x': 3,
                    'position_y': 0,
                    'width': 4,
                    'height': 3
                },
                {
                    'title': 'Grade Distribution',
                    'chart_type': 'bar',
                    'data_source': 'grade_distribution',
                    'position_x': 7,
                    'position_y': 0,
                    'width': 5,
                    'height': 3
                },
                {
                    'title': 'Attendance Rate',
                    'chart_type': 'gauge',
                    'data_source': 'attendance_rate',
                    'position_x': 0,
                    'position_y': 2,
                    'width': 3,
                    'height': 2
                },
                {
                    'title': 'Revenue Summary',
                    'chart_type': 'kpi',
                    'data_source': 'revenue_summary',
                    'position_x': 0,
                    'position_y': 4,
                    'width': 3,
                    'height': 2
                }
            ]
            
            for widget_data in sample_widgets:
                widget, created = Widget.objects.get_or_create(
                    dashboard=dashboard,
                    title=widget_data['title'],
                    defaults=widget_data
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created widget: {widget.title}')
                    )
            
            # Create sample report
            report, created = Report.objects.get_or_create(
                title='Student Performance Report',
                created_by=user,
                defaults={
                    'description': 'Comprehensive student performance analysis',
                    'report_type': 'student_performance',
                    'data_sources': ['student_count', 'grade_distribution', 'attendance_rate'],
                    'frequency': 'weekly',
                    'export_formats': ['json', 'csv', 'excel'],
                    'is_public': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created report: {report.title}')
                )
            
            self.stdout.write(
                self.style.SUCCESS('Sample analytics data created successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating sample data: {e}')
            )
    
    def test_data_query(self, options):
        """Test a data source query"""
        try:
            data_source_name = options['data_source']
            
            # Get data source
            data_source = analytics_service.data_registry.get_source(data_source_name)
            if not data_source:
                self.stdout.write(
                    self.style.ERROR(f'Data source {data_source_name} not found')
                )
                return
            
            # Execute query
            self.stdout.write(f'Testing data source: {data_source_name}')
            result = data_source['query_func']()
            
            self.stdout.write(
                self.style.SUCCESS(f'Query result: {result}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error testing query: {e}')
            )
    
    def cleanup_old_metrics(self, options):
        """Clean up old analytics metrics"""
        try:
            days = options['days']
            cutoff_date = timezone.now() - timezone.timedelta(days=days)
            
            # Delete expired metrics
            deleted_count = AnalyticsMetric.objects.filter(
                expires_at__lt=cutoff_date
            ).delete()[0]
            
            self.stdout.write(
                self.style.SUCCESS(f'Deleted {deleted_count} expired metrics')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error cleaning up metrics: {e}')
            )
    
    def generate_sample_report(self, options):
        """Generate a sample report"""
        try:
            username = options.get('user', 'admin')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User {username} not found')
                )
                return
            
            # Get first available report
            report = Report.objects.filter(
                Q(created_by=user) | Q(is_public=True)
            ).first()
            
            if not report:
                self.stdout.write(
                    self.style.ERROR('No reports available')
                )
                return
            
            # Generate report
            self.stdout.write(f'Generating report: {report.title}')
            execution = analytics_service.generate_report(report, user)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Report generated successfully: {execution.id}\n'
                    f'Status: {execution.status}\n'
                    f'Rows: {execution.row_count}\n'
                    f'Execution time: {execution.execution_time}s'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error generating report: {e}')
            )
    
    def list_data_sources(self):
        """List all available data sources"""
        try:
            self.stdout.write(self.style.SUCCESS('Available Data Sources:'))
            self.stdout.write('=' * 50)
            
            sources = analytics_service.get_available_data_sources()
            for source in sources:
                self.stdout.write(
                    f"• {source['name']}: {source['description']}"
                )
            
            self.stdout.write(f'\nTotal: {len(sources)} data sources')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error listing data sources: {e}')
            )
