#!/usr/bin/env python
"""
Django management command for data management operations
فرمان مدیریت جنگو برای عملیات مدیریت داده‌ها
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from apps.data_management.models import ImportExportJob, DataSyncTask, BackupSchedule
from apps.data_management.services import import_export_service, backup_service, sync_service
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Manage data operations (import, export, backup, sync)'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='action', help='Action to perform')

        # Import command
        import_parser = subparsers.add_parser('import', help='Import data')
        import_parser.add_argument('--file', required=True, help='File path to import')
        import_parser.add_argument('--model', required=True, help='Model name to import to')
        import_parser.add_argument('--format', choices=['csv', 'json', 'xlsx'], default='csv', help='File format')
        import_parser.add_argument('--dry-run', action='store_true', help='Dry run without actual import')

        # Export command
        export_parser = subparsers.add_parser('export', help='Export data')
        export_parser.add_argument('--model', required=True, help='Model name to export')
        export_parser.add_argument('--output', required=True, help='Output file path')
        export_parser.add_argument('--format', choices=['csv', 'json', 'xlsx'], default='csv', help='Export format')
        export_parser.add_argument('--filters', help='JSON string of filters to apply')

        # Backup command
        backup_parser = subparsers.add_parser('backup', help='Create backup')
        backup_parser.add_argument('--type', choices=['full', 'incremental', 'differential'], default='full', help='Backup type')
        backup_parser.add_argument('--output', help='Backup output path')
        backup_parser.add_argument('--compress', action='store_true', help='Compress backup')

        # Sync command
        sync_parser = subparsers.add_parser('sync', help='Sync data')
        sync_parser.add_argument('--task-id', help='Specific sync task ID to run')
        sync_parser.add_argument('--model', help='Model to sync')
        sync_parser.add_argument('--direction', choices=['import', 'export', 'both'], default='both', help='Sync direction')

        # Status command
        status_parser = subparsers.add_parser('status', help='Show status of operations')
        status_parser.add_argument('--type', choices=['jobs', 'sync', 'backup'], help='Operation type to check')

        # Cleanup command
        cleanup_parser = subparsers.add_parser('cleanup', help='Cleanup old data')
        cleanup_parser.add_argument('--days', type=int, default=30, help='Days to keep (default: 30)')

    def handle(self, *args, **options):
        action = options.get('action')
        
        if not action:
            self.print_help('manage.py', 'data_management')
            return

        try:
            if action == 'import':
                self.handle_import(options)
            elif action == 'export':
                self.handle_export(options)
            elif action == 'backup':
                self.handle_backup(options)
            elif action == 'sync':
                self.handle_sync(options)
            elif action == 'status':
                self.handle_status(options)
            elif action == 'cleanup':
                self.handle_cleanup(options)
            else:
                raise CommandError(f'Unknown action: {action}')
                
        except Exception as e:
            logger.error(f"Command failed: {e}")
            raise CommandError(f'Command failed: {e}')

    def handle_import(self, options):
        """Handle data import"""
        self.stdout.write(self.style.SUCCESS('🔄 Starting data import...'))
        
        file_path = options['file']
        model_name = options['model']
        file_format = options['format']
        dry_run = options.get('dry_run', False)
        
        # Create import job
        job_data = {
            'title': f'CLI Import: {model_name}',
            'job_type': 'import',
            'model_name': model_name,
            'format': file_format,
            'file_path': file_path,
            'description': f'Command line import of {model_name} from {file_path}',
            'dry_run': dry_run
        }
        
        try:
            # Use the service to create and execute job
            result = import_export_service.execute_import(
                file_path=file_path,
                model_name=model_name,
                format=file_format,
                dry_run=dry_run
            )
            
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(f'📊 Dry run completed. Would import {result.get("total_records", 0)} records')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Import completed. Imported {result.get("success_records", 0)} records')
                )
                
            if result.get('errors'):
                self.stdout.write(
                    self.style.ERROR(f'❌ {len(result["errors"])} errors occurred')
                )
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Import failed: {e}'))
            raise

    def handle_export(self, options):
        """Handle data export"""
        self.stdout.write(self.style.SUCCESS('🔄 Starting data export...'))
        
        model_name = options['model']
        output_path = options['output']
        file_format = options['format']
        filters = options.get('filters')
        
        try:
            # Parse filters if provided
            filter_dict = {}
            if filters:
                import json
                filter_dict = json.loads(filters)
            
            # Use the service to export data
            result = import_export_service.execute_export(
                model_name=model_name,
                output_path=output_path,
                format=file_format,
                filters=filter_dict
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Export completed. Exported {result.get("total_records", 0)} records to {output_path}')
            )
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Export failed: {e}'))
            raise

    def handle_backup(self, options):
        """Handle backup creation"""
        self.stdout.write(self.style.SUCCESS('🔄 Starting backup...'))
        
        backup_type = options['type']
        output_path = options.get('output')
        compress = options.get('compress', False)
        
        try:
            # Use the service to create backup
            result = backup_service.create_backup(
                backup_type=backup_type,
                output_path=output_path,
                compress=compress
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Backup completed. File: {result.get("file_path")}')
            )
            self.stdout.write(f'📊 Size: {result.get("size_mb", 0):.2f} MB')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Backup failed: {e}'))
            raise

    def handle_sync(self, options):
        """Handle data synchronization"""
        self.stdout.write(self.style.SUCCESS('🔄 Starting data sync...'))
        
        task_id = options.get('task_id')
        model_name = options.get('model')
        direction = options.get('direction', 'both')
        
        try:
            if task_id:
                # Run specific sync task
                task = DataSyncTask.objects.get(id=task_id)
                result = sync_service.execute_sync_task(task)
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Sync task "{task.name}" completed')
                )
            else:
                # Run sync for model
                result = sync_service.sync_model(model_name, direction)
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Model sync completed for {model_name}')
                )
            
            self.stdout.write(f'📊 Synced records: {result.get("synced_records", 0)}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Sync failed: {e}'))
            raise

    def handle_status(self, options):
        """Show status of operations"""
        operation_type = options.get('type')
        
        if not operation_type or operation_type == 'jobs':
            self.show_job_status()
        
        if not operation_type or operation_type == 'sync':
            self.show_sync_status()
            
        if not operation_type or operation_type == 'backup':
            self.show_backup_status()

    def show_job_status(self):
        """Show import/export job status"""
        self.stdout.write(self.style.SUCCESS('\n📋 Import/Export Jobs Status:'))
        
        # Recent jobs
        recent_jobs = ImportExportJob.objects.order_by('-created_at')[:10]
        
        if not recent_jobs:
            self.stdout.write('  No recent jobs found')
            return
        
        for job in recent_jobs:
            status_emoji = {
                'pending': '⏳',
                'running': '🔄',
                'completed': '✅',
                'failed': '❌',
                'cancelled': '🚫'
            }.get(job.status, '❓')
            
            self.stdout.write(
                f'  {status_emoji} {job.title} - {job.get_status_display()} '
                f'({job.success_records}/{job.total_records} records)'
            )

    def show_sync_status(self):
        """Show sync task status"""
        self.stdout.write(self.style.SUCCESS('\n🔄 Data Sync Tasks Status:'))
        
        active_tasks = DataSyncTask.objects.filter(status='active')
        
        if not active_tasks:
            self.stdout.write('  No active sync tasks found')
            return
        
        for task in active_tasks:
            last_run = task.last_run.strftime('%Y-%m-%d %H:%M') if task.last_run else 'Never'
            self.stdout.write(
                f'  🔄 {task.name} - Last run: {last_run} '
                f'({task.total_synced_records} total records synced)'
            )

    def show_backup_status(self):
        """Show backup schedule status"""
        self.stdout.write(self.style.SUCCESS('\n💾 Backup Schedules Status:'))
        
        schedules = BackupSchedule.objects.filter(is_enabled=True)
        
        if not schedules:
            self.stdout.write('  No active backup schedules found')
            return
        
        for schedule in schedules:
            last_backup = schedule.last_backup.strftime('%Y-%m-%d %H:%M') if schedule.last_backup else 'Never'
            size_mb = schedule.last_backup_size / (1024 * 1024) if schedule.last_backup_size else 0
            
            self.stdout.write(
                f'  💾 {schedule.name} - Last backup: {last_backup} '
                f'({size_mb:.2f} MB)'
            )

    def handle_cleanup(self, options):
        """Cleanup old data"""
        days = options['days']
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        
        self.stdout.write(self.style.SUCCESS(f'🧹 Cleaning up data older than {days} days...'))
        
        # Cleanup old jobs
        old_jobs = ImportExportJob.objects.filter(
            created_at__lt=cutoff_date,
            status__in=['completed', 'failed', 'cancelled']
        )
        job_count = old_jobs.count()
        old_jobs.delete()
        
        self.stdout.write(f'  ✅ Cleaned up {job_count} old import/export jobs')
        
        # Could add more cleanup logic here
        self.stdout.write(self.style.SUCCESS('🧹 Cleanup completed'))
