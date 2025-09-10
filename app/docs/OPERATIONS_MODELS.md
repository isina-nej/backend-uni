# مدل‌های عملیاتی و زیرساخت - Operations and Infrastructure Models

## مدل‌های SQLAlchemy برای سیستم عملیاتی

```python
# app/models/operations.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class SystemComponent(str, enum.Enum):
    WEB_SERVER = "وب سرور"
    DATABASE = "پایگاه داده"
    CACHE = "کش"
    MESSAGE_QUEUE = "صف پیام"
    LOAD_BALANCER = "بالانس‌کننده بار"
    FILE_STORAGE = "ذخیره‌سازی فایل"
    MONITORING = "مانیتورینگ"
    BACKUP_SYSTEM = "سیستم پشتیبان‌گیری"
    LOGGING_SYSTEM = "سیستم لاگ‌گیری"
    API_GATEWAY = "درگاه API"
    AUTHENTICATION = "احراز هویت"
    EMAIL_SERVICE = "سرویس ایمیل"
    NOTIFICATION = "اعلان"
    SCHEDULER = "زمان‌بندی"

class ComponentStatus(str, enum.Enum):
    HEALTHY = "سالم"
    WARNING = "هشدار"
    CRITICAL = "بحرانی"
    DOWN = "خارج از سرویس"
    MAINTENANCE = "در حال تعمیر"
    UNKNOWN = "نامشخص"

class MaintenanceType(str, enum.Enum):
    SCHEDULED = "برنامه‌ریزی شده"
    UNSCHEDULED = "غیر برنامه‌ریزی شده"
    EMERGENCY = "اورژانسی"
    PREVENTIVE = "پیشگیرانه"
    CORRECTIVE = "اصلاحی"

class BackupType(str, enum.Enum):
    FULL = "کامل"
    INCREMENTAL = "تزمینی"
    DIFFERENTIAL = "تفاضلی"
    LOG = "لاگ"
    FILE_SYSTEM = "سیستم فایل"

class BackupStatus(str, enum.Enum):
    PENDING = "در انتظار"
    RUNNING = "در حال اجرا"
    COMPLETED = "تکمیل شده"
    FAILED = "ناموفق"
    CANCELLED = "لغو شده"
    VERIFIED = "تایید شده"

class DeploymentType(str, enum.Enum):
    WEB_APP = "اپلیکیشن وب"
    API = "API"
    DATABASE_MIGRATION = "مهاجرت پایگاه داده"
    CONFIGURATION = "پیکربندی"
    INFRASTRUCTURE = "زیرساخت"
    ROLLBACK = "بازگشت"

class DeploymentStatus(str, enum.Enum):
    PENDING = "در انتظار"
    DEPLOYING = "در حال استقرار"
    DEPLOYED = "استقرار شده"
    FAILED = "ناموفق"
    ROLLED_BACK = "بازگشت شده"
    CANCELLED = "لغو شده"

class IncidentPriority(str, enum.Enum):
    LOW = "کم"
    MEDIUM = "متوسط"
    HIGH = "بالا"
    CRITICAL = "بحرانی"
    URGENT = "فوری"

class IncidentStatus(str, enum.Enum):
    OPEN = "باز"
    INVESTIGATING = "در حال بررسی"
    RESOLVED = "حل شده"
    CLOSED = "بسته"
    CANCELLED = "لغو شده"

class ResourceType(str, enum.Enum):
    CPU = "پردازنده"
    MEMORY = "حافظه"
    DISK = "دیسک"
    NETWORK = "شبکه"
    DATABASE_CONNECTION = "اتصال پایگاه داده"
    CACHE_CONNECTION = "اتصال کش"
    QUEUE_CONNECTION = "اتصال صف"

class AlertType(str, enum.Enum):
    SYSTEM = "سیستمی"
    APPLICATION = "اپلیکیشن"
    PERFORMANCE = "کارایی"
    SECURITY = "امنیتی"
    BUSINESS = "کسب‌وکار"

class AlertSeverity(str, enum.Enum):
    INFO = "اطلاعاتی"
    WARNING = "هشدار"
    ERROR = "خطا"
    CRITICAL = "بحرانی"

class AlertStatus(str, enum.Enum):
    ACTIVE = "فعال"
    ACKNOWLEDGED = "تایید شده"
    RESOLVED = "حل شده"
    SUPPRESSED = "سرکوب شده"

class SystemComponent(Base):
    __tablename__ = 'system_components'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    component_type = Column(Enum(SystemComponent), nullable=False)
    description = Column(Text)
    host = Column(String(255))
    port = Column(Integer)
    version = Column(String(50))
    configuration = Column(JSON)
    dependencies = Column(JSON)
    health_check_url = Column(String(500))
    health_check_interval_seconds = Column(Integer, default=60)
    timeout_seconds = Column(Integer, default=30)
    status = Column(Enum(ComponentStatus), default=ComponentStatus.UNKNOWN)
    last_health_check = Column(DateTime)
    last_health_check_result = Column(JSON)
    is_active = Column(Boolean, default=True)
    is_critical = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    metrics = relationship("ComponentMetric", back_populates="component")
    maintenances = relationship("Maintenance", back_populates="component")
    incidents = relationship("Incident", back_populates="component")

class ComponentMetric(Base):
    __tablename__ = 'component_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    component_id = Column(Integer, ForeignKey('system_components.id'), nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_type = Column(Enum(ResourceType), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20))
    threshold_warning = Column(Float)
    threshold_critical = Column(Float)
    measured_at = Column(DateTime, nullable=False)
    additional_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    component = relationship("SystemComponent", back_populates="metrics")

class Maintenance(Base):
    __tablename__ = 'maintenances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    maintenance_id = Column(String(20), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    description = Column(Text)
    maintenance_type = Column(Enum(MaintenanceType), nullable=False)
    component_id = Column(Integer, ForeignKey('system_components.id'))
    planned_start_date = Column(DateTime, nullable=False)
    planned_end_date = Column(DateTime, nullable=False)
    actual_start_date = Column(DateTime)
    actual_end_date = Column(DateTime)
    status = Column(String(20), default='planned')  # planned, in_progress, completed, cancelled
    impact_level = Column(String(20), default='low')  # low, medium, high, critical
    notification_sent = Column(Boolean, default=False)
    notification_recipients = Column(JSON)
    pre_maintenance_checklist = Column(JSON)
    post_maintenance_checklist = Column(JSON)
    rollback_plan = Column(Text)
    requested_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    assigned_to = Column(Integer, ForeignKey('employees.id'))
    completed_by = Column(Integer, ForeignKey('employees.id'))
    completion_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    component = relationship("SystemComponent", back_populates="maintenances")
    requested_by_employee = relationship("Employee", foreign_keys=[requested_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    assigned_to_employee = relationship("Employee", foreign_keys=[assigned_to])
    completed_by_employee = relationship("Employee", foreign_keys=[completed_by])

class Backup(Base):
    __tablename__ = 'backups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    backup_id = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    backup_type = Column(Enum(BackupType), nullable=False)
    component_id = Column(Integer, ForeignKey('system_components.id'))
    database_name = Column(String(100))
    table_name = Column(String(100))
    file_path = Column(String(500))
    storage_location = Column(String(500))
    compression_type = Column(String(20))
    encryption_type = Column(String(50))
    status = Column(Enum(BackupStatus), default=BackupStatus.PENDING)
    size_bytes = Column(Integer)
    compression_ratio = Column(Float)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer)
    initiated_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    verified_by = Column(Integer, ForeignKey('employees.id'))
    verification_date = Column(DateTime)
    verification_result = Column(JSON)
    retention_days = Column(Integer, default=30)
    is_encrypted = Column(Boolean, default=True)
    encryption_key_id = Column(String(100))
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    component = relationship("SystemComponent", back_populates="backups")
    initiated_by_employee = relationship("Employee", foreign_keys=[initiated_by])
    verified_by_employee = relationship("Employee", foreign_keys=[verified_by])

class Deployment(Base):
    __tablename__ = 'deployments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    deployment_id = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    deployment_type = Column(Enum(DeploymentType), nullable=False)
    component_id = Column(Integer, ForeignKey('system_components.id'))
    version = Column(String(50), nullable=False)
    branch = Column(String(100))
    commit_hash = Column(String(100))
    build_number = Column(String(50))
    artifact_path = Column(String(500))
    configuration = Column(JSON)
    environment = Column(String(20), default='production')  # development, staging, production
    status = Column(Enum(DeploymentStatus), default=DeploymentStatus.PENDING)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer)
    initiated_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    deployed_by = Column(Integer, ForeignKey('employees.id'))
    rollback_deployment_id = Column(Integer, ForeignKey('deployments.id'))
    rollback_reason = Column(Text)
    test_results = Column(JSON)
    performance_metrics = Column(JSON)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    component = relationship("SystemComponent", back_populates="deployments")
    initiated_by_employee = relationship("Employee", foreign_keys=[initiated_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    deployed_by_employee = relationship("Employee", foreign_keys=[deployed_by])
    rollback_deployment = relationship("Deployment", remote_side=[id])

class Incident(Base):
    __tablename__ = 'incidents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(String(20), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Enum(IncidentPriority), nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.OPEN)
    component_id = Column(Integer, ForeignKey('system_components.id'))
    affected_services = Column(JSON)
    impact_description = Column(Text)
    root_cause = Column(Text)
    resolution = Column(Text)
    reported_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    reported_at = Column(DateTime, default=datetime.utcnow)
    assigned_to = Column(Integer, ForeignKey('employees.id'))
    assigned_at = Column(DateTime)
    resolved_by = Column(Integer, ForeignKey('employees.id'))
    resolved_at = Column(DateTime)
    closed_by = Column(Integer, ForeignKey('employees.id'))
    closed_at = Column(DateTime)
    sla_breach = Column(Boolean, default=False)
    escalation_level = Column(Integer, default=1)
    tags = Column(JSON)
    attachments = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    component = relationship("SystemComponent", back_populates="incidents")
    reported_by_employee = relationship("Employee", foreign_keys=[reported_by])
    assigned_to_employee = relationship("Employee", foreign_keys=[assigned_to])
    resolved_by_employee = relationship("Employee", foreign_keys=[resolved_by])
    closed_by_employee = relationship("Employee", foreign_keys=[closed_by])

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_id = Column(String(20), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(Enum(AlertType), nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False)
    status = Column(Enum(AlertStatus), default=AlertStatus.ACTIVE)
    component_id = Column(Integer, ForeignKey('system_components.id'))
    metric_name = Column(String(100))
    threshold_value = Column(Float)
    current_value = Column(Float)
    condition = Column(String(50))  # above, below, equals, not_equals
    rule_definition = Column(JSON)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    acknowledged_by = Column(Integer, ForeignKey('employees.id'))
    acknowledged_at = Column(DateTime)
    resolved_at = Column(DateTime)
    auto_resolve = Column(Boolean, default=False)
    notification_channels = Column(JSON)
    notification_sent = Column(Boolean, default=False)
    escalation_rules = Column(JSON)
    suppression_rules = Column(JSON)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    component = relationship("SystemComponent", back_populates="alerts")
    acknowledged_by_employee = relationship("Employee", foreign_keys=[acknowledged_by])

class LogEntry(Base):
    __tablename__ = 'log_entries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String(20), nullable=False)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    logger_name = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    exception = Column(Text)
    stack_trace = Column(Text)
    component_id = Column(Integer, ForeignKey('system_components.id'))
    user_id = Column(Integer, ForeignKey('employees.id'))
    session_id = Column(String(100))
    request_id = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    url = Column(String(500))
    method = Column(String(10))
    response_code = Column(Integer)
    response_time_ms = Column(Integer)
    additional_data = Column(JSON)
    archived = Column(Boolean, default=False)
    archive_date = Column(DateTime)

    # Relationships
    component = relationship("SystemComponent", back_populates="logs")
    user = relationship("Employee", foreign_keys=[user_id])

class Configuration(Base):
    __tablename__ = 'configurations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255), nullable=False)
    value = Column(Text)
    value_type = Column(String(20), default='string')  # string, number, boolean, json
    description = Column(Text)
    component_id = Column(Integer, ForeignKey('system_components.id'))
    environment = Column(String(20), default='production')
    is_encrypted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_modified_by = Column(Integer, ForeignKey('employees.id'))
    last_modified_at = Column(DateTime)

    # Relationships
    component = relationship("SystemComponent", back_populates="configurations")
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    last_modified_by_employee = relationship("Employee", foreign_keys=[last_modified_by])

class ScheduledTask(Base):
    __tablename__ = 'scheduled_tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    description = Column(Text)
    task_type = Column(String(50), nullable=False)  # backup, maintenance, report, sync
    component_id = Column(Integer, ForeignKey('system_components.id'))
    schedule_expression = Column(String(100), nullable=False)  # cron expression
    timezone = Column(String(50), default='Asia/Tehran')
    is_active = Column(Boolean, default=True)
    last_run_date = Column(DateTime)
    next_run_date = Column(DateTime)
    max_execution_time_minutes = Column(Integer, default=60)
    retry_count = Column(Integer, default=0)
    max_retry_count = Column(Integer, default=3)
    retry_delay_minutes = Column(Integer, default=5)
    parameters = Column(JSON)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    component = relationship("SystemComponent", back_populates="scheduled_tasks")
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class TaskExecution(Base):
    __tablename__ = 'task_executions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('scheduled_tasks.id'), nullable=False)
    execution_id = Column(String(20), unique=True, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer)
    status = Column(String(20), default='running')  # running, completed, failed, cancelled
    exit_code = Column(Integer)
    output = Column(Text)
    error_message = Column(Text)
    retry_attempt = Column(Integer, default=0)
    initiated_by = Column(String(20), default='scheduler')  # scheduler, manual, api
    manual_triggered_by = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    task = relationship("ScheduledTask", back_populates="executions")
    manual_triggered_by_employee = relationship("Employee", foreign_keys=[manual_triggered_by])

class ResourceUsage(Base):
    __tablename__ = 'resource_usage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    component_id = Column(Integer, ForeignKey('system_components.id'), nullable=False)
    resource_type = Column(Enum(ResourceType), nullable=False)
    usage_value = Column(Float, nullable=False)
    usage_percentage = Column(Float)
    measured_at = Column(DateTime, default=datetime.utcnow)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    additional_metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    component = relationship("SystemComponent", back_populates="resource_usage")

class PerformanceBaseline(Base):
    __tablename__ = 'performance_baselines'

    id = Column(Integer, primary_key=True, autoincrement=True)
    component_id = Column(Integer, ForeignKey('system_components.id'), nullable=False)
    metric_name = Column(String(100), nullable=False)
    baseline_type = Column(String(20), default='daily')  # hourly, daily, weekly, monthly
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    average_value = Column(Float)
    min_value = Column(Float)
    max_value = Column(Float)
    percentile_95 = Column(Float)
    percentile_99 = Column(Float)
    standard_deviation = Column(Float)
    sample_count = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    component = relationship("SystemComponent", back_populates="performance_baselines")
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class CapacityPlanning(Base):
    __tablename__ = 'capacity_planning'

    id = Column(Integer, primary_key=True, autoincrement=True)
    component_id = Column(Integer, ForeignKey('system_components.id'), nullable=False)
    planning_period = Column(String(20), nullable=False)  # monthly, quarterly, yearly
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    current_capacity = Column(JSON)
    projected_growth = Column(JSON)
    recommended_capacity = Column(JSON)
    cost_analysis = Column(JSON)
    risk_assessment = Column(JSON)
    implementation_plan = Column(JSON)
    status = Column(String(20), default='draft')  # draft, review, approved, implemented
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    reviewed_by = Column(Integer, ForeignKey('employees.id'))
    review_date = Column(DateTime)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    component = relationship("SystemComponent", back_populates="capacity_planning")
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    reviewed_by_employee = relationship("Employee", foreign_keys=[reviewed_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
```

## Pydantic Schemas برای سیستم عملیاتی

```python
# app/schemas/operations.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class SystemComponent(str, Enum):
    WEB_SERVER = "وب سرور"
    DATABASE = "پایگاه داده"
    CACHE = "کش"
    MESSAGE_QUEUE = "صف پیام"
    LOAD_BALANCER = "بالانس‌کننده بار"
    FILE_STORAGE = "ذخیره‌سازی فایل"
    MONITORING = "مانیتورینگ"
    BACKUP_SYSTEM = "سیستم پشتیبان‌گیری"
    LOGGING_SYSTEM = "سیستم لاگ‌گیری"
    API_GATEWAY = "درگاه API"
    AUTHENTICATION = "احراز هویت"
    EMAIL_SERVICE = "سرویس ایمیل"
    NOTIFICATION = "اعلان"
    SCHEDULER = "زمان‌بندی"

class ComponentStatus(str, Enum):
    HEALTHY = "سالم"
    WARNING = "هشدار"
    CRITICAL = "بحرانی"
    DOWN = "خارج از سرویس"
    MAINTENANCE = "در حال تعمیر"
    UNKNOWN = "نامشخص"

class MaintenanceType(str, Enum):
    SCHEDULED = "برنامه‌ریزی شده"
    UNSCHEDULED = "غیر برنامه‌ریزی شده"
    EMERGENCY = "اورژانسی"
    PREVENTIVE = "پیشگیرانه"
    CORRECTIVE = "اصلاحی"

class BackupType(str, Enum):
    FULL = "کامل"
    INCREMENTAL = "تزمینی"
    DIFFERENTIAL = "تفاضلی"
    LOG = "لاگ"
    FILE_SYSTEM = "سیستم فایل"

class BackupStatus(str, Enum):
    PENDING = "در انتظار"
    RUNNING = "در حال اجرا"
    COMPLETED = "تکمیل شده"
    FAILED = "ناموفق"
    CANCELLED = "لغو شده"
    VERIFIED = "تایید شده"

class DeploymentType(str, Enum):
    WEB_APP = "اپلیکیشن وب"
    API = "API"
    DATABASE_MIGRATION = "مهاجرت پایگاه داده"
    CONFIGURATION = "پیکربندی"
    INFRASTRUCTURE = "زیرساخت"
    ROLLBACK = "بازگشت"

class DeploymentStatus(str, Enum):
    PENDING = "در انتظار"
    DEPLOYING = "در حال استقرار"
    DEPLOYED = "استقرار شده"
    FAILED = "ناموفق"
    ROLLED_BACK = "بازگشت شده"
    CANCELLED = "لغو شده"

class IncidentPriority(str, Enum):
    LOW = "کم"
    MEDIUM = "متوسط"
    HIGH = "بالا"
    CRITICAL = "بحرانی"
    URGENT = "فوری"

class IncidentStatus(str, Enum):
    OPEN = "باز"
    INVESTIGATING = "در حال بررسی"
    RESOLVED = "حل شده"
    CLOSED = "بسته"
    CANCELLED = "لغو شده"

class ResourceType(str, Enum):
    CPU = "پردازنده"
    MEMORY = "حافظه"
    DISK = "دیسک"
    NETWORK = "شبکه"
    DATABASE_CONNECTION = "اتصال پایگاه داده"
    CACHE_CONNECTION = "اتصال کش"
    QUEUE_CONNECTION = "اتصال صف"

class AlertType(str, Enum):
    SYSTEM = "سیستمی"
    APPLICATION = "اپلیکیشن"
    PERFORMANCE = "کارایی"
    SECURITY = "امنیتی"
    BUSINESS = "کسب‌وکار"

class AlertSeverity(str, Enum):
    INFO = "اطلاعاتی"
    WARNING = "هشدار"
    ERROR = "خطا"
    CRITICAL = "بحرانی"

class AlertStatus(str, Enum):
    ACTIVE = "فعال"
    ACKNOWLEDGED = "تایید شده"
    RESOLVED = "حل شده"
    SUPPRESSED = "سرکوب شده"

# System Component schemas
class SystemComponentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    component_type: SystemComponent
    description: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    version: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    dependencies: Optional[Dict[str, Any]] = None
    health_check_url: Optional[str] = None
    health_check_interval_seconds: int = 60
    timeout_seconds: int = 30
    is_critical: bool = False

class SystemComponentCreate(SystemComponentBase):
    pass

class SystemComponentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    component_type: Optional[SystemComponent] = None
    description: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    version: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    dependencies: Optional[Dict[str, Any]] = None
    health_check_url: Optional[str] = None
    health_check_interval_seconds: Optional[int] = None
    timeout_seconds: Optional[int] = None
    status: Optional[ComponentStatus] = None
    last_health_check: Optional[datetime] = None
    last_health_check_result: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_critical: Optional[bool] = None

class SystemComponent(SystemComponentBase):
    id: int
    status: ComponentStatus
    last_health_check: Optional[datetime] = None
    last_health_check_result: Optional[Dict[str, Any]] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SystemComponentWithDetails(SystemComponent):
    created_by_employee: Optional[Dict[str, Any]] = None
    metrics_count: int = 0
    maintenances_count: int = 0
    incidents_count: int = 0

# Maintenance schemas
class MaintenanceBase(BaseModel):
    maintenance_id: str = Field(..., min_length=1, max_length=20)
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    maintenance_type: MaintenanceType
    planned_start_date: datetime
    planned_end_date: datetime
    impact_level: str = "low"
    notification_recipients: Optional[Dict[str, Any]] = None
    pre_maintenance_checklist: Optional[Dict[str, Any]] = None
    post_maintenance_checklist: Optional[Dict[str, Any]] = None
    rollback_plan: Optional[str] = None
    notes: Optional[str] = None

class MaintenanceCreate(MaintenanceBase):
    component_id: Optional[int] = None
    requested_by: int

class MaintenanceUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    maintenance_type: Optional[MaintenanceType] = None
    component_id: Optional[int] = None
    planned_start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    status: Optional[str] = None
    impact_level: Optional[str] = None
    notification_sent: Optional[bool] = None
    notification_recipients: Optional[Dict[str, Any]] = None
    pre_maintenance_checklist: Optional[Dict[str, Any]] = None
    post_maintenance_checklist: Optional[Dict[str, Any]] = None
    rollback_plan: Optional[str] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    completed_by: Optional[int] = None
    completion_date: Optional[datetime] = None
    notes: Optional[str] = None

class Maintenance(MaintenanceBase):
    id: int
    component_id: Optional[int] = None
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    status: str
    notification_sent: bool
    requested_by: int
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    completed_by: Optional[int] = None
    completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MaintenanceWithDetails(Maintenance):
    component: Optional[Dict[str, Any]] = None
    requested_by_employee: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None
    assigned_to_employee: Optional[Dict[str, Any]] = None
    completed_by_employee: Optional[Dict[str, Any]] = None

# Backup schemas
class BackupBase(BaseModel):
    backup_id: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    backup_type: BackupType
    database_name: Optional[str] = None
    table_name: Optional[str] = None
    file_path: Optional[str] = None
    storage_location: Optional[str] = None
    compression_type: Optional[str] = None
    encryption_type: Optional[str] = None
    retention_days: int = 30
    is_encrypted: bool = True
    encryption_key_id: Optional[str] = None

class BackupCreate(BackupBase):
    component_id: Optional[int] = None
    initiated_by: int

class BackupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    backup_type: Optional[BackupType] = None
    component_id: Optional[int] = None
    database_name: Optional[str] = None
    table_name: Optional[str] = None
    file_path: Optional[str] = None
    storage_location: Optional[str] = None
    compression_type: Optional[str] = None
    encryption_type: Optional[str] = None
    status: Optional[BackupStatus] = None
    size_bytes: Optional[int] = None
    compression_ratio: Optional[float] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    verified_by: Optional[int] = None
    verification_date: Optional[datetime] = None
    verification_result: Optional[Dict[str, Any]] = None
    retention_days: Optional[int] = None
    is_encrypted: Optional[bool] = None
    encryption_key_id: Optional[str] = None
    error_message: Optional[str] = None

class Backup(BackupBase):
    id: int
    component_id: Optional[int] = None
    status: BackupStatus
    size_bytes: Optional[int] = None
    compression_ratio: Optional[float] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    initiated_by: int
    verified_by: Optional[int] = None
    verification_date: Optional[datetime] = None
    verification_result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class BackupWithDetails(Backup):
    component: Optional[Dict[str, Any]] = None
    initiated_by_employee: Optional[Dict[str, Any]] = None
    verified_by_employee: Optional[Dict[str, Any]] = None

# Incident schemas
class IncidentBase(BaseModel):
    incident_id: str = Field(..., min_length=1, max_length=20)
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    priority: IncidentPriority
    severity: AlertSeverity
    affected_services: Optional[Dict[str, Any]] = None
    impact_description: Optional[str] = None
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    sla_breach: bool = False
    escalation_level: int = 1
    tags: Optional[Dict[str, Any]] = None
    attachments: Optional[Dict[str, Any]] = None

class IncidentCreate(IncidentBase):
    component_id: Optional[int] = None
    reported_by: int

class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    priority: Optional[IncidentPriority] = None
    severity: Optional[AlertSeverity] = None
    status: Optional[IncidentStatus] = None
    component_id: Optional[int] = None
    affected_services: Optional[Dict[str, Any]] = None
    impact_description: Optional[str] = None
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    assigned_to: Optional[int] = None
    assigned_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    closed_by: Optional[int] = None
    closed_at: Optional[datetime] = None
    sla_breach: Optional[bool] = None
    escalation_level: Optional[int] = None
    tags: Optional[Dict[str, Any]] = None
    attachments: Optional[Dict[str, Any]] = None

class Incident(IncidentBase):
    id: int
    component_id: Optional[int] = None
    status: IncidentStatus
    reported_by: int
    reported_at: datetime
    assigned_to: Optional[int] = None
    assigned_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    closed_by: Optional[int] = None
    closed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class IncidentWithDetails(Incident):
    component: Optional[Dict[str, Any]] = None
    reported_by_employee: Optional[Dict[str, Any]] = None
    assigned_to_employee: Optional[Dict[str, Any]] = None
    resolved_by_employee: Optional[Dict[str, Any]] = None
    closed_by_employee: Optional[Dict[str, Any]] = None

# Alert schemas
class AlertBase(BaseModel):
    alert_id: str = Field(..., min_length=1, max_length=20)
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    alert_type: AlertType
    severity: AlertSeverity
    component_id: Optional[int] = None
    metric_name: Optional[str] = None
    threshold_value: Optional[float] = None
    current_value: Optional[float] = None
    condition: Optional[str] = None
    rule_definition: Optional[Dict[str, Any]] = None
    notification_channels: Optional[Dict[str, Any]] = None
    escalation_rules: Optional[Dict[str, Any]] = None
    suppression_rules: Optional[Dict[str, Any]] = None
    tags: Optional[Dict[str, Any]] = None

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    message: Optional[str] = Field(None, min_length=1)
    alert_type: Optional[AlertType] = None
    severity: Optional[AlertSeverity] = None
    status: Optional[AlertStatus] = None
    component_id: Optional[int] = None
    metric_name: Optional[str] = None
    threshold_value: Optional[float] = None
    current_value: Optional[float] = None
    condition: Optional[str] = None
    rule_definition: Optional[Dict[str, Any]] = None
    acknowledged_by: Optional[int] = None
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    auto_resolve: Optional[bool] = None
    notification_channels: Optional[Dict[str, Any]] = None
    notification_sent: Optional[bool] = None
    escalation_rules: Optional[Dict[str, Any]] = None
    suppression_rules: Optional[Dict[str, Any]] = None
    tags: Optional[Dict[str, Any]] = None

class Alert(AlertBase):
    id: int
    status: AlertStatus
    triggered_at: datetime
    acknowledged_by: Optional[int] = None
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    auto_resolve: bool
    notification_sent: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AlertWithDetails(Alert):
    component: Optional[Dict[str, Any]] = None
    acknowledged_by_employee: Optional[Dict[str, Any]] = None

# Pagination schemas
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool

# Search and filter schemas
class SystemComponentSearchFilters(BaseModel):
    component_type: Optional[SystemComponent] = None
    status: Optional[ComponentStatus] = None
    is_active: Optional[bool] = None
    is_critical: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None

class MaintenanceSearchFilters(BaseModel):
    maintenance_type: Optional[MaintenanceType] = None
    status: Optional[str] = None
    component_id: Optional[int] = None
    requested_by: Optional[int] = None
    approved_by: Optional[int] = None
    assigned_to: Optional[int] = None
    completed_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None

class BackupSearchFilters(BaseModel):
    backup_type: Optional[BackupType] = None
    status: Optional[BackupStatus] = None
    component_id: Optional[int] = None
    initiated_by: Optional[int] = None
    verified_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None

class IncidentSearchFilters(BaseModel):
    priority: Optional[IncidentPriority] = None
    severity: Optional[AlertSeverity] = None
    status: Optional[IncidentStatus] = None
    component_id: Optional[int] = None
    reported_by: Optional[int] = None
    assigned_to: Optional[int] = None
    resolved_by: Optional[int] = None
    closed_by: Optional[int] = None
    sla_breach: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None

class AlertSearchFilters(BaseModel):
    alert_type: Optional[AlertType] = None
    severity: Optional[AlertSeverity] = None
    status: Optional[AlertStatus] = None
    component_id: Optional[int] = None
    acknowledged_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None

class DeploymentSearchFilters(BaseModel):
    deployment_type: Optional[DeploymentType] = None
    status: Optional[DeploymentStatus] = None
    component_id: Optional[int] = None
    environment: Optional[str] = None
    initiated_by: Optional[int] = None
    approved_by: Optional[int] = None
    deployed_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None

class LogEntrySearchFilters(BaseModel):
    level: Optional[str] = None
    logger_name: Optional[str] = None
    component_id: Optional[int] = None
    user_id: Optional[int] = None
    request_id: Optional[str] = None
    response_code: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None
```

این پیاده‌سازی کامل مدل‌های عملیاتی و زیرساخت شامل تمام ویژگی‌های مورد نیاز برای مانیتورینگ، پشتیبان‌گیری، استقرار، و عملیات سیستم دانشگاهی ایران است.
