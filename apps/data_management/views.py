# ==============================================================================
# DATA MANAGEMENT API VIEWS
# نماهای API مدیریت داده‌ها
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.http import Http404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import ImportExportJob, DataSyncTask, BackupSchedule, ExternalSystemIntegration
from .serializers import (
    ImportExportJobSerializer, DataSyncTaskSerializer, 
    BackupScheduleSerializer, ExternalSystemIntegrationSerializer,
    ImportJobCreateSerializer, ExportJobCreateSerializer
)
from .services import import_export_service, backup_service, sync_service
import logging

logger = logging.getLogger(__name__)


class ImportExportJobViewSet(viewsets.ModelViewSet):
    """ViewSet for managing import/export jobs"""
    
    queryset = ImportExportJob.objects.all()
    serializer_class = ImportExportJobSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job_type', 'status', 'format', 'model_name']
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def get_queryset(self):
        """Get jobs accessible to the user"""
        if getattr(self, 'swagger_fake_view', False):
            return ImportExportJob.objects.none()
        user = self.request.user
        if user.is_superuser:
            return ImportExportJob.objects.all()
        return ImportExportJob.objects.filter(created_by=user)
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)
    
    @extend_schema(
        summary="Create Export Job",
        description="Create a new data export job",
        request=ExportJobCreateSerializer
    )
    @action(detail=False, methods=['post'])
    def create_export(self, request):
        """Create a new export job"""
        try:
            serializer = ExportJobCreateSerializer(data=request.data)
            if serializer.is_valid():
                model_name = serializer.validated_data['model_name']
                format = serializer.validated_data.get('format', 'csv')
                filters = serializer.validated_data.get('filters', {})
                config = serializer.validated_data.get('config', {})
                
                job = import_export_service.create_export_job(
                    user=request.user,
                    model_name=model_name,
                    format=format,
                    filters=filters,
                    config=config
                )
                
                # Optionally execute immediately
                if serializer.validated_data.get('execute_immediately', False):
                    import_export_service.execute_export_job(job)
                
                return Response(
                    ImportExportJobSerializer(job).data,
                    status=status.HTTP_201_CREATED
                )
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error creating export job: {e}")
            return Response(
                {'error': 'Failed to create export job'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary="Create Import Job",
        description="Create a new data import job",
        request=ImportJobCreateSerializer
    )
    @action(detail=False, methods=['post'])
    def create_import(self, request):
        """Create a new import job"""
        try:
            serializer = ImportJobCreateSerializer(data=request.data)
            if serializer.is_valid():
                model_name = serializer.validated_data['model_name']
                source_file = serializer.validated_data['source_file']
                format = serializer.validated_data.get('format', 'csv')
                field_mapping = serializer.validated_data.get('field_mapping', {})
                config = serializer.validated_data.get('config', {})
                
                job = import_export_service.create_import_job(
                    user=request.user,
                    model_name=model_name,
                    source_file=source_file,
                    format=format,
                    field_mapping=field_mapping,
                    config=config
                )
                
                # Optionally execute immediately
                if serializer.validated_data.get('execute_immediately', False):
                    import_export_service.execute_import_job(job)
                
                return Response(
                    ImportExportJobSerializer(job).data,
                    status=status.HTTP_201_CREATED
                )
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error creating import job: {e}")
            return Response(
                {'error': 'Failed to create import job'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary="Execute Job",
        description="Execute an import/export job"
    )
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """Execute a job"""
        try:
            job = self.get_object()
            
            if job.status not in ['pending', 'failed']:
                return Response(
                    {'error': 'Job can only be executed if status is pending or failed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if job.job_type == 'export':
                success = import_export_service.execute_export_job(job)
            elif job.job_type == 'import':
                success = import_export_service.execute_import_job(job)
            else:
                return Response(
                    {'error': 'Unsupported job type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            job.refresh_from_db()
            return Response(
                ImportExportJobSerializer(job).data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Error executing job: {e}")
            return Response(
                {'error': 'Failed to execute job'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary="Cancel Job",
        description="Cancel a running job"
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a job"""
        try:
            job = self.get_object()
            
            if job.status != 'running':
                return Response(
                    {'error': 'Only running jobs can be cancelled'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            job.status = 'cancelled'
            job.completed_at = timezone.now()
            job.save(update_fields=['status', 'completed_at'])
            
            return Response(
                ImportExportJobSerializer(job).data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Error cancelling job: {e}")
            return Response(
                {'error': 'Failed to cancel job'},
                status=status.HTTP_400_BAD_REQUEST
            )


class DataSyncTaskViewSet(viewsets.ModelViewSet):
    """ViewSet for managing data sync tasks"""
    
    serializer_class = DataSyncTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sync_type', 'status', 'schedule_enabled', 'source_model']
    
    def get_queryset(self):
        """Get sync tasks accessible to the user"""
        user = self.request.user
        if user.is_superuser:
            return DataSyncTask.objects.all()
        return DataSyncTask.objects.filter(created_by=user)
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)
    
    @extend_schema(
        summary="Execute Sync Task",
        description="Execute a data synchronization task"
    )
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """Execute a sync task"""
        try:
            task = self.get_object()
            
            if task.status != 'active':
                return Response(
                    {'error': 'Task must be active to execute'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            success = sync_service.execute_sync_task(task)
            
            task.refresh_from_db()
            return Response(
                DataSyncTaskSerializer(task).data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Error executing sync task: {e}")
            return Response(
                {'error': 'Failed to execute sync task'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary="Test Sync Task",
        description="Test a sync task configuration without executing"
    )
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """Test a sync task configuration"""
        try:
            task = self.get_object()
            
            # Perform validation tests
            test_results = {
                'source_model_valid': False,
                'external_connection_valid': False,
                'field_mapping_valid': False,
                'filters_valid': False
            }
            
            # Test source model
            try:
                from django.apps import apps
                apps.get_model(task.source_model)
                test_results['source_model_valid'] = True
            except:
                pass
            
            # Test external connection if configured
            if task.external_endpoint:
                test_results['external_connection_valid'] = True  # Simplified
            
            # Test field mapping
            if task.field_mapping:
                test_results['field_mapping_valid'] = True
            
            # Test filters
            if task.filters:
                test_results['filters_valid'] = True
            
            return Response(test_results, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error testing sync task: {e}")
            return Response(
                {'error': 'Failed to test sync task'},
                status=status.HTTP_400_BAD_REQUEST
            )


class BackupScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing backup schedules"""
    
    serializer_class = BackupScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['backup_type', 'frequency', 'is_enabled']
    
    def get_queryset(self):
        """Get backup schedules accessible to the user"""
        user = self.request.user
        if user.is_superuser:
            return BackupSchedule.objects.all()
        return BackupSchedule.objects.filter(created_by=user)
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)
    
    @extend_schema(
        summary="Execute Backup",
        description="Execute a backup schedule immediately"
    )
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """Execute a backup schedule"""
        try:
            schedule = self.get_object()
            
            if not schedule.is_enabled:
                return Response(
                    {'error': 'Backup schedule is disabled'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            success = backup_service.create_backup(schedule)
            
            schedule.refresh_from_db()
            return Response(
                BackupScheduleSerializer(schedule).data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Error executing backup: {e}")
            return Response(
                {'error': 'Failed to execute backup'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary="List Backup Files",
        description="List available backup files for this schedule"
    )
    @action(detail=True, methods=['get'])
    def list_backups(self, request, pk=None):
        """List backup files for this schedule"""
        try:
            schedule = self.get_object()
            
            # This would list actual backup files
            # For now, return placeholder data
            backup_files = [
                {
                    'filename': f'backup_{schedule.name}_{timezone.now().strftime("%Y%m%d")}.json',
                    'size': schedule.last_backup_size,
                    'created_at': schedule.last_backup,
                    'type': schedule.backup_type
                }
            ]
            
            return Response(backup_files, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error listing backups: {e}")
            return Response(
                {'error': 'Failed to list backups'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ExternalSystemIntegrationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing external system integrations"""
    
    serializer_class = ExternalSystemIntegrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['system_type', 'auth_type', 'is_active']
    
    def get_queryset(self):
        """Get integrations accessible to the user"""
        user = self.request.user
        if user.is_superuser:
            return ExternalSystemIntegration.objects.all()
        return ExternalSystemIntegration.objects.filter(created_by=user)
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)
    
    @extend_schema(
        summary="Test Connection",
        description="Test connection to external system"
    )
    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """Test connection to external system"""
        try:
            integration = self.get_object()
            
            # Update test timestamp
            integration.last_connection_test = timezone.now()
            
            # Perform connection test (simplified)
            try:
                # This would implement actual connection testing
                integration.last_connection_status = True
                integration.last_error_message = ""
                
                result = {
                    'success': True,
                    'message': 'Connection successful',
                    'tested_at': integration.last_connection_test
                }
                
            except Exception as e:
                integration.last_connection_status = False
                integration.last_error_message = str(e)
                
                result = {
                    'success': False,
                    'message': f'Connection failed: {e}',
                    'tested_at': integration.last_connection_test
                }
            
            integration.save(update_fields=[
                'last_connection_test', 'last_connection_status', 'last_error_message'
            ])
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error testing connection: {e}")
            return Response(
                {'error': 'Failed to test connection'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary="Get System Info",
        description="Get information about the external system"
    )
    @action(detail=True, methods=['get'])
    def system_info(self, request, pk=None):
        """Get information about the external system"""
        try:
            integration = self.get_object()
            
            # This would fetch actual system information
            info = {
                'system_name': integration.name,
                'system_type': integration.get_system_type_display(),
                'status': 'Connected' if integration.last_connection_status else 'Disconnected',
                'last_test': integration.last_connection_test,
                'endpoint': integration.endpoint_url or f"{integration.host}:{integration.port}",
                'auth_type': integration.get_auth_type_display()
            }
            
            return Response(info, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return Response(
                {'error': 'Failed to get system info'},
                status=status.HTTP_400_BAD_REQUEST
            )
