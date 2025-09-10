# ==============================================================================
# DATA MANAGEMENT SERVICES
# سرویس‌های مدیریت داده‌ها
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import os
import csv
import json
import uuid
import zipfile
import pandas as pd
from io import StringIO, BytesIO
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from django.apps import apps
from django.core.management import call_command
from django.core.serializers import serialize, deserialize
from django.db import transaction, models
from django.conf import settings
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import ImportExportJob, DataSyncTask, BackupSchedule, ExternalSystemIntegration
import logging

logger = logging.getLogger(__name__)


class DataImportExportService:
    """Service for handling data import/export operations"""
    
    def __init__(self):
        self.supported_formats = ['csv', 'json', 'excel', 'xml']
        self.chunk_size = 1000  # Process records in chunks
    
    def create_export_job(self, user, model_name: str, format: str = 'csv', 
                         filters: Dict = None, config: Dict = None) -> ImportExportJob:
        """Create a new export job"""
        try:
            # Validate model exists
            model_class = apps.get_model(model_name)
            
            job = ImportExportJob.objects.create(
                job_type='export',
                title=f"Export {model_class._meta.verbose_name_plural}",
                description=f"Export data from {model_name}",
                model_name=model_name,
                format=format,
                filters=filters or {},
                config=config or {},
                created_by=user
            )
            
            logger.info(f"Created export job {job.id} for model {model_name}")
            return job
            
        except Exception as e:
            logger.error(f"Error creating export job: {e}")
            raise
    
    def execute_export_job(self, job: ImportExportJob) -> bool:
        """Execute an export job"""
        try:
            job.start_job()
            
            # Get model class
            model_class = apps.get_model(job.model_name)
            
            # Apply filters
            queryset = model_class.objects.all()
            if job.filters:
                queryset = queryset.filter(**job.filters)
            
            job.total_records = queryset.count()
            job.save(update_fields=['total_records'])
            
            # Export based on format
            if job.format == 'csv':
                result_content = self._export_to_csv(queryset, job)
            elif job.format == 'json':
                result_content = self._export_to_json(queryset, job)
            elif job.format == 'excel':
                result_content = self._export_to_excel(queryset, job)
            else:
                raise ValueError(f"Unsupported format: {job.format}")
            
            # Save result file
            filename = f"export_{job.model_name}_{job.id}.{job.format}"
            job.result_file.save(filename, ContentFile(result_content))
            
            job.complete_job()
            logger.info(f"Export job {job.id} completed successfully")
            return True
            
        except Exception as e:
            error_msg = f"Export job failed: {e}"
            job.fail_job(error_msg)
            logger.error(error_msg)
            return False
    
    def _export_to_csv(self, queryset, job: ImportExportJob) -> bytes:
        """Export queryset to CSV format"""
        output = StringIO()
        writer = None
        processed = 0
        
        for chunk in self._get_chunks(queryset, self.chunk_size):
            for obj in chunk:
                if writer is None:
                    # Initialize CSV writer with field names
                    fieldnames = [f.name for f in obj._meta.fields]
                    writer = csv.DictWriter(output, fieldnames=fieldnames)
                    writer.writeheader()
                
                # Convert object to dict
                row_data = {}
                for field in obj._meta.fields:
                    value = getattr(obj, field.name)
                    if hasattr(value, 'isoformat'):  # DateTime fields
                        value = value.isoformat()
                    elif hasattr(value, '__str__'):  # Convert to string
                        value = str(value)
                    row_data[field.name] = value
                
                writer.writerow(row_data)
                processed += 1
                
                # Update progress
                if processed % 100 == 0:
                    job.processed_records = processed
                    job.progress_percentage = (processed / job.total_records) * 100
                    job.save(update_fields=['processed_records', 'progress_percentage'])
        
        job.success_records = processed
        job.save(update_fields=['success_records'])
        
        return output.getvalue().encode('utf-8')
    
    def _export_to_json(self, queryset, job: ImportExportJob) -> bytes:
        """Export queryset to JSON format"""
        data = []
        processed = 0
        
        for chunk in self._get_chunks(queryset, self.chunk_size):
            serialized_chunk = serialize('json', chunk)
            chunk_data = json.loads(serialized_chunk)
            data.extend(chunk_data)
            
            processed += len(chunk)
            job.processed_records = processed
            job.progress_percentage = (processed / job.total_records) * 100
            job.save(update_fields=['processed_records', 'progress_percentage'])
        
        job.success_records = processed
        job.save(update_fields=['success_records'])
        
        return json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
    
    def _export_to_excel(self, queryset, job: ImportExportJob) -> bytes:
        """Export queryset to Excel format"""
        # Convert to DataFrame
        data = []
        processed = 0
        
        for chunk in self._get_chunks(queryset, self.chunk_size):
            for obj in chunk:
                row_data = {}
                for field in obj._meta.fields:
                    value = getattr(obj, field.name)
                    if hasattr(value, 'isoformat'):  # DateTime fields
                        value = value.isoformat()
                    row_data[field.name] = value
                
                data.append(row_data)
                processed += 1
                
                if processed % 100 == 0:
                    job.processed_records = processed
                    job.progress_percentage = (processed / job.total_records) * 100
                    job.save(update_fields=['processed_records', 'progress_percentage'])
        
        # Create Excel file
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        
        job.success_records = processed
        job.save(update_fields=['success_records'])
        
        return output.getvalue()
    
    def create_import_job(self, user, model_name: str, source_file, 
                         format: str = 'csv', field_mapping: Dict = None,
                         config: Dict = None) -> ImportExportJob:
        """Create a new import job"""
        try:
            # Validate model exists
            model_class = apps.get_model(model_name)
            
            job = ImportExportJob.objects.create(
                job_type='import',
                title=f"Import {model_class._meta.verbose_name_plural}",
                description=f"Import data to {model_name}",
                model_name=model_name,
                format=format,
                source_file=source_file,
                field_mapping=field_mapping or {},
                config=config or {},
                created_by=user
            )
            
            logger.info(f"Created import job {job.id} for model {model_name}")
            return job
            
        except Exception as e:
            logger.error(f"Error creating import job: {e}")
            raise
    
    def execute_import_job(self, job: ImportExportJob) -> bool:
        """Execute an import job"""
        try:
            job.start_job()
            
            # Read and parse source file
            if job.format == 'csv':
                data = self._read_csv_file(job.source_file)
            elif job.format == 'json':
                data = self._read_json_file(job.source_file)
            elif job.format == 'excel':
                data = self._read_excel_file(job.source_file)
            else:
                raise ValueError(f"Unsupported format: {job.format}")
            
            job.total_records = len(data)
            job.save(update_fields=['total_records'])
            
            # Import data
            model_class = apps.get_model(job.model_name)
            success_count = 0
            error_count = 0
            
            with transaction.atomic():
                for i, record in enumerate(data):
                    try:
                        # Apply field mapping
                        mapped_data = self._apply_field_mapping(record, job.field_mapping)
                        
                        # Create or update object
                        obj = model_class(**mapped_data)
                        obj.save()
                        
                        success_count += 1
                        
                    except Exception as e:
                        error_count += 1
                        job.errors.append({
                            'record': i + 1,
                            'data': record,
                            'error': str(e)
                        })
                    
                    # Update progress
                    if (i + 1) % 100 == 0:
                        job.processed_records = i + 1
                        job.success_records = success_count
                        job.error_records = error_count
                        job.progress_percentage = ((i + 1) / job.total_records) * 100
                        job.save(update_fields=[
                            'processed_records', 'success_records', 
                            'error_records', 'progress_percentage', 'errors'
                        ])
            
            job.processed_records = len(data)
            job.success_records = success_count
            job.error_records = error_count
            job.complete_job()
            
            logger.info(f"Import job {job.id} completed: {success_count} success, {error_count} errors")
            return True
            
        except Exception as e:
            error_msg = f"Import job failed: {e}"
            job.fail_job(error_msg)
            logger.error(error_msg)
            return False
    
    def _read_csv_file(self, file) -> List[Dict]:
        """Read data from CSV file"""
        file.seek(0)
        content = file.read().decode('utf-8')
        csv_data = csv.DictReader(StringIO(content))
        return list(csv_data)
    
    def _read_json_file(self, file) -> List[Dict]:
        """Read data from JSON file"""
        file.seek(0)
        content = file.read().decode('utf-8')
        return json.loads(content)
    
    def _read_excel_file(self, file) -> List[Dict]:
        """Read data from Excel file"""
        file.seek(0)
        df = pd.read_excel(file)
        return df.to_dict('records')
    
    def _apply_field_mapping(self, record: Dict, field_mapping: Dict) -> Dict:
        """Apply field mapping to record"""
        if not field_mapping:
            return record
        
        mapped_record = {}
        for source_field, target_field in field_mapping.items():
            if source_field in record:
                mapped_record[target_field] = record[source_field]
        
        # Add unmapped fields
        for field, value in record.items():
            if field not in field_mapping and field not in mapped_record:
                mapped_record[field] = value
        
        return mapped_record
    
    def _get_chunks(self, queryset, chunk_size: int):
        """Yield chunks of queryset"""
        count = queryset.count()
        for i in range(0, count, chunk_size):
            yield queryset[i:i + chunk_size]


class BackupService:
    """Service for handling database backups"""
    
    def __init__(self):
        self.backup_dir = getattr(settings, 'BACKUP_DIR', 'backups')
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """Ensure backup directory exists"""
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, schedule: BackupSchedule) -> bool:
        """Create a backup based on schedule configuration"""
        try:
            backup_filename = self._generate_backup_filename(schedule)
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            logger.info(f"Starting backup: {schedule.name}")
            
            if schedule.backup_type == 'full':
                success = self._create_full_backup(backup_path, schedule)
            elif schedule.backup_type == 'schema_only':
                success = self._create_schema_backup(backup_path, schedule)
            elif schedule.backup_type == 'data_only':
                success = self._create_data_backup(backup_path, schedule)
            else:
                logger.error(f"Unsupported backup type: {schedule.backup_type}")
                return False
            
            if success:
                # Update schedule status
                schedule.last_backup = timezone.now()
                schedule.last_backup_status = 'completed'
                schedule.last_backup_size = os.path.getsize(backup_path)
                schedule.save(update_fields=[
                    'last_backup', 'last_backup_status', 'last_backup_size'
                ])
                
                # Cleanup old backups
                self._cleanup_old_backups(schedule)
                
                logger.info(f"Backup completed successfully: {backup_filename}")
            
            return success
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            schedule.last_backup_status = 'failed'
            schedule.save(update_fields=['last_backup_status'])
            return False
    
    def _create_full_backup(self, backup_path: str, schedule: BackupSchedule) -> bool:
        """Create a full database backup"""
        try:
            # Use Django's dumpdata command
            with open(backup_path, 'w', encoding='utf-8') as f:
                call_command('dumpdata', 
                           exclude=['contenttypes', 'auth.permission'],
                           indent=2,
                           stdout=f)
            
            # Compress if enabled
            if schedule.compress_backup:
                self._compress_backup(backup_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Full backup failed: {e}")
            return False
    
    def _create_schema_backup(self, backup_path: str, schedule: BackupSchedule) -> bool:
        """Create a schema-only backup"""
        try:
            # This would need to be implemented based on database type
            # For now, we'll create a simplified version
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write("-- Schema backup placeholder\n")
                f.write(f"-- Created: {timezone.now()}\n")
            
            return True
            
        except Exception as e:
            logger.error(f"Schema backup failed: {e}")
            return False
    
    def _create_data_backup(self, backup_path: str, schedule: BackupSchedule) -> bool:
        """Create a data-only backup"""
        try:
            # Use dumpdata but exclude certain apps/models
            with open(backup_path, 'w', encoding='utf-8') as f:
                call_command('dumpdata',
                           exclude=['contenttypes', 'auth.permission', 'sessions'],
                           indent=2,
                           stdout=f)
            
            return True
            
        except Exception as e:
            logger.error(f"Data backup failed: {e}")
            return False
    
    def _generate_backup_filename(self, schedule: BackupSchedule) -> str:
        """Generate backup filename"""
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        name_slug = schedule.name.replace(' ', '_').lower()
        extension = 'json'
        
        if schedule.compress_backup:
            extension = 'json.gz'
        
        return f"{name_slug}_{schedule.backup_type}_{timestamp}.{extension}"
    
    def _compress_backup(self, backup_path: str):
        """Compress backup file"""
        import gzip
        
        with open(backup_path, 'rb') as f_in:
            with gzip.open(f"{backup_path}.gz", 'wb') as f_out:
                f_out.writelines(f_in)
        
        # Remove original file
        os.remove(backup_path)
    
    def _cleanup_old_backups(self, schedule: BackupSchedule):
        """Remove old backups beyond retention limit"""
        try:
            # Find backup files for this schedule
            name_slug = schedule.name.replace(' ', '_').lower()
            backup_files = []
            
            for filename in os.listdir(self.backup_dir):
                if filename.startswith(name_slug):
                    filepath = os.path.join(self.backup_dir, filename)
                    backup_files.append({
                        'path': filepath,
                        'mtime': os.path.getmtime(filepath)
                    })
            
            # Sort by modification time (newest first)
            backup_files.sort(key=lambda x: x['mtime'], reverse=True)
            
            # Remove old backups
            if len(backup_files) > schedule.max_backups_to_keep:
                for backup_file in backup_files[schedule.max_backups_to_keep:]:
                    os.remove(backup_file['path'])
                    logger.info(f"Removed old backup: {backup_file['path']}")
            
        except Exception as e:
            logger.error(f"Cleanup old backups failed: {e}")


class DataSyncService:
    """Service for data synchronization with external systems"""
    
    def __init__(self):
        self.timeout = 30
    
    def execute_sync_task(self, task: DataSyncTask) -> bool:
        """Execute a data synchronization task"""
        try:
            logger.info(f"Starting sync task: {task.name}")
            
            # Get source data
            source_model = apps.get_model(task.source_model)
            source_data = source_model.objects.all()
            
            if task.filters:
                source_data = source_data.filter(**task.filters)
            
            # Apply transformations
            transformed_data = self._apply_transformations(source_data, task.transform_rules)
            
            # Sync based on sync type
            if task.sync_type == 'one_way':
                success = self._one_way_sync(transformed_data, task)
            elif task.sync_type == 'two_way':
                success = self._two_way_sync(transformed_data, task)
            else:
                logger.error(f"Unsupported sync type: {task.sync_type}")
                return False
            
            if success:
                task.last_run = timezone.now()
                task.last_sync_status = 'success'
                task.last_sync_message = f"Synced {len(transformed_data)} records"
                task.total_synced_records += len(transformed_data)
            else:
                task.last_sync_status = 'failed'
                task.last_sync_message = "Sync operation failed"
            
            task.save(update_fields=[
                'last_run', 'last_sync_status', 'last_sync_message', 'total_synced_records'
            ])
            
            return success
            
        except Exception as e:
            logger.error(f"Sync task failed: {e}")
            task.last_sync_status = 'failed'
            task.last_sync_message = str(e)
            task.save(update_fields=['last_sync_status', 'last_sync_message'])
            return False
    
    def _apply_transformations(self, data, transform_rules: List) -> List:
        """Apply transformation rules to data"""
        if not transform_rules:
            return data
        
        transformed = []
        for item in data:
            # Apply each transformation rule
            for rule in transform_rules:
                # This would implement various transformation logic
                # For now, just pass through
                pass
            transformed.append(item)
        
        return transformed
    
    def _one_way_sync(self, data, task: DataSyncTask) -> bool:
        """Perform one-way synchronization"""
        try:
            # This would implement the actual sync logic
            # For now, just simulate
            logger.info(f"One-way sync: {len(data)} records")
            return True
        except Exception as e:
            logger.error(f"One-way sync failed: {e}")
            return False
    
    def _two_way_sync(self, data, task: DataSyncTask) -> bool:
        """Perform two-way synchronization"""
        try:
            # This would implement bidirectional sync logic
            logger.info(f"Two-way sync: {len(data)} records")
            return True
        except Exception as e:
            logger.error(f"Two-way sync failed: {e}")
            return False


# Initialize services
import_export_service = DataImportExportService()
backup_service = BackupService()
sync_service = DataSyncService()
