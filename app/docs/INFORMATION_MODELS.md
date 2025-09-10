# مدل‌های اطلاعاتی و گزارش‌گیری - Information and Reporting Models

## مدل‌های SQLAlchemy برای سیستم اطلاعاتی

```python
# app/models/information.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ReportType(str, enum.Enum):
    ACADEMIC = "آموزشی"
    FINANCIAL = "مالی"
    ADMINISTRATIVE = "اداری"
    STUDENT = "دانشجویی"
    EMPLOYEE = "کارمندی"
    LIBRARY = "کتابخانه‌ای"
    RESEARCH = "پژوهشی"
    OPERATIONAL = "عملیاتی"
    COMPLIANCE = "انطباقی"
    CUSTOM = "سفارشی"

class ReportFormat(str, enum.Enum):
    PDF = "PDF"
    EXCEL = "Excel"
    CSV = "CSV"
    HTML = "HTML"
    JSON = "JSON"
    XML = "XML"

class ReportFrequency(str, enum.Enum):
    DAILY = "روزانه"
    WEEKLY = "هفتگی"
    MONTHLY = "ماهانه"
    QUARTERLY = "فصلی"
    SEMI_ANNUAL = "شش‌ماهه"
    ANNUAL = "سالانه"
    ON_DEMAND = "درخواست"

class DashboardType(str, enum.Enum):
    EXECUTIVE = "مدیرعامل"
    ACADEMIC = "آموزشی"
    FINANCIAL = "مالی"
    OPERATIONAL = "عملیاتی"
    STUDENT = "دانشجویی"
    FACULTY = "دانشکده"
    DEPARTMENT = "بخش"
    CUSTOM = "سفارشی"

class DataSourceType(str, enum.Enum):
    DATABASE = "پایگاه داده"
    API = "API"
    FILE = "فایل"
    EXTERNAL_SYSTEM = "سیستم خارجی"
    MANUAL_ENTRY = "ورود دستی"

class MetricType(str, enum.Enum):
    COUNT = "شمارش"
    SUM = "جمع"
    AVERAGE = "میانگین"
    PERCENTAGE = "درصد"
    RATIO = "نسبت"
    TREND = "روند"

class AlertType(str, enum.Enum):
    INFO = "اطلاعاتی"
    WARNING = "هشدار"
    ERROR = "خطا"
    CRITICAL = "بحرانی"

class AlertStatus(str, enum.Enum):
    ACTIVE = "فعال"
    ACKNOWLEDGED = "تایید شده"
    RESOLVED = "حل شده"
    DISMISSED = "رد شده"

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    report_type = Column(Enum(ReportType), nullable=False)
    description = Column(Text)
    query_definition = Column(JSON)
    parameters = Column(JSON)
    template_path = Column(String(500))
    output_format = Column(Enum(ReportFormat), default=ReportFormat.PDF)
    frequency = Column(Enum(ReportFrequency), default=ReportFrequency.ON_DEMAND)
    schedule_config = Column(JSON)
    access_level = Column(String(20), default='internal')  # public, internal, confidential, restricted
    required_permissions = Column(JSON)
    is_active = Column(Boolean, default=True)
    is_scheduled = Column(Boolean, default=False)
    last_run_date = Column(DateTime)
    next_run_date = Column(DateTime)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    version = Column(String(20), default="1.0")
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    executions = relationship("ReportExecution", back_populates="report")
    subscriptions = relationship("ReportSubscription", back_populates="report")

class ReportExecution(Base):
    __tablename__ = 'report_executions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey('reports.id'), nullable=False)
    execution_date = Column(DateTime, default=datetime.utcnow)
    parameters_used = Column(JSON)
    status = Column(String(20), default='running')  # running, completed, failed, cancelled
    execution_time_seconds = Column(Float)
    records_processed = Column(Integer)
    file_path = Column(String(500))
    file_size = Column(Integer)
    error_message = Column(Text)
    executed_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    is_manual = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    report = relationship("Report", back_populates="executions")
    executed_by_employee = relationship("Employee", foreign_keys=[executed_by])

class ReportSubscription(Base):
    __tablename__ = 'report_subscriptions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey('reports.id'), nullable=False)
    subscriber_type = Column(String(20), nullable=False)  # employee, role, department
    employee_id = Column(Integer, ForeignKey('employees.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))
    department_id = Column(Integer, ForeignKey('departments.id'))
    email = Column(String(255))
    format = Column(Enum(ReportFormat), default=ReportFormat.PDF)
    frequency = Column(Enum(ReportFrequency))
    is_active = Column(Boolean, default=True)
    last_sent_date = Column(DateTime)
    next_send_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    report = relationship("Report", back_populates="subscriptions")
    employee = relationship("Employee", foreign_keys=[employee_id])

class Dashboard(Base):
    __tablename__ = 'dashboards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    dashboard_type = Column(Enum(DashboardType), nullable=False)
    description = Column(Text)
    layout_config = Column(JSON)
    widgets = Column(JSON)
    access_level = Column(String(20), default='internal')
    required_permissions = Column(JSON)
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    refresh_interval_minutes = Column(Integer, default=60)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    last_modified_by = Column(Integer, ForeignKey('employees.id'))
    last_modified_date = Column(DateTime)
    version = Column(String(20), default="1.0")
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    last_modified_by_employee = relationship("Employee", foreign_keys=[last_modified_by])
    widgets_data = relationship("DashboardWidget", back_populates="dashboard")

class DashboardWidget(Base):
    __tablename__ = 'dashboard_widgets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dashboard_id = Column(Integer, ForeignKey('dashboards.id'), nullable=False)
    widget_type = Column(String(50), nullable=False)  # chart, table, metric, text, etc.
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    description = Column(Text)
    data_source = Column(JSON)
    configuration = Column(JSON)
    position_x = Column(Integer)
    position_y = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    refresh_interval_minutes = Column(Integer, default=60)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    dashboard = relationship("Dashboard", back_populates="widgets_data")

class DataSource(Base):
    __tablename__ = 'data_sources'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    source_type = Column(Enum(DataSourceType), nullable=False)
    connection_string = Column(String(500))
    database_name = Column(String(100))
    table_name = Column(String(100))
    api_endpoint = Column(String(500))
    api_key = Column(String(255))
    file_path = Column(String(500))
    file_format = Column(String(20))
    refresh_schedule = Column(JSON)
    last_refresh_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    access_level = Column(String(20), default='internal')
    required_permissions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class Metric(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    metric_type = Column(Enum(MetricType), nullable=False)
    description = Column(Text)
    formula = Column(Text)
    data_source_id = Column(Integer, ForeignKey('data_sources.id'))
    parameters = Column(JSON)
    unit = Column(String(50))
    decimal_places = Column(Integer, default=2)
    target_value = Column(Float)
    threshold_warning = Column(Float)
    threshold_critical = Column(Float)
    is_active = Column(Boolean, default=True)
    last_calculated_date = Column(DateTime)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    data_source = relationship("DataSource", back_populates="metrics")
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    values = relationship("MetricValue", back_populates="metric")

class MetricValue(Base):
    __tablename__ = 'metric_values'

    id = Column(Integer, primary_key=True, autoincrement=True)
    metric_id = Column(Integer, ForeignKey('metrics.id'), nullable=False)
    value = Column(Float, nullable=False)
    calculated_date = Column(DateTime, nullable=False)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    parameters_used = Column(JSON)
    is_manual = Column(Boolean, default=False)
    recorded_by = Column(Integer, ForeignKey('employees.id'))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    metric = relationship("Metric", back_populates="values")
    recorded_by_employee = relationship("Employee", foreign_keys=[recorded_by])

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    alert_type = Column(Enum(AlertType), nullable=False)
    severity = Column(String(20), default='medium')  # low, medium, high, critical
    message = Column(Text, nullable=False)
    description = Column(Text)
    trigger_condition = Column(JSON)
    affected_entities = Column(JSON)
    status = Column(Enum(AlertStatus), default=AlertStatus.ACTIVE)
    acknowledged_by = Column(Integer, ForeignKey('employees.id'))
    acknowledged_date = Column(DateTime)
    resolved_by = Column(Integer, ForeignKey('employees.id'))
    resolved_date = Column(DateTime)
    resolution_notes = Column(Text)
    escalation_rules = Column(JSON)
    notification_channels = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    acknowledged_by_employee = relationship("Employee", foreign_keys=[acknowledged_by])
    resolved_by_employee = relationship("Employee", foreign_keys=[resolved_by])

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # system, alert, reminder, announcement
    priority = Column(String(20), default='normal')  # low, normal, high, urgent
    recipient_type = Column(String(20), nullable=False)  # user, role, department, all
    recipient_user_id = Column(Integer, ForeignKey('employees.id'))
    recipient_role_id = Column(Integer, ForeignKey('roles.id'))
    recipient_department_id = Column(Integer, ForeignKey('departments.id'))
    channels = Column(JSON)  # email, sms, in_app, push
    scheduled_date = Column(DateTime)
    expiry_date = Column(DateTime)
    is_read = Column(Boolean, default=False)
    read_date = Column(DateTime)
    is_archived = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    recipient_user = relationship("Employee", foreign_keys=[recipient_user_id])
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(String(20), nullable=False)  # INSERT, UPDATE, DELETE
    old_values = Column(JSON)
    new_values = Column(JSON)
    changed_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    change_reason = Column(String(255))
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    changed_by_employee = relationship("Employee", foreign_keys=[changed_by])

class SystemLog(Base):
    __tablename__ = 'system_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    log_level = Column(String(20), nullable=False)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    category = Column(String(50), nullable=False)  # system, security, performance, business
    message = Column(Text, nullable=False)
    details = Column(JSON)
    source = Column(String(100))  # module or component name
    user_id = Column(Integer, ForeignKey('employees.id'))
    session_id = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    request_id = Column(String(100))
    response_time_ms = Column(Integer)
    error_code = Column(String(20))
    stack_trace = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("Employee", foreign_keys=[user_id])

class DataExport(Base):
    __tablename__ = 'data_exports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    description = Column(Text)
    export_type = Column(String(50), nullable=False)  # full, incremental, filtered
    data_source = Column(JSON)
    filters = Column(JSON)
    format = Column(Enum(ReportFormat), default=ReportFormat.CSV)
    compression = Column(String(20))  # none, zip, gzip
    file_path = Column(String(500))
    file_size = Column(Integer)
    record_count = Column(Integer)
    status = Column(String(20), default='pending')  # pending, running, completed, failed
    requested_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    completed_date = Column(DateTime)
    expiry_date = Column(DateTime)
    download_count = Column(Integer, default=0)
    last_download_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    requested_by_employee = relationship("Employee", foreign_keys=[requested_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class BackupLog(Base):
    __tablename__ = 'backup_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    backup_type = Column(String(50), nullable=False)  # full, incremental, differential
    backup_name = Column(String(255), nullable=False)
    description = Column(Text)
    database_name = Column(String(100))
    file_path = Column(String(500))
    file_size = Column(Integer)
    compression_ratio = Column(Float)
    status = Column(String(20), default='running')  # running, completed, failed
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer)
    initiated_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    verified_by = Column(Integer, ForeignKey('employees.id'))
    verification_date = Column(DateTime)
    error_message = Column(Text)
    retention_days = Column(Integer)
    is_encrypted = Column(Boolean, default=True)
    encryption_method = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    initiated_by_employee = relationship("Employee", foreign_keys=[initiated_by])
    verified_by_employee = relationship("Employee", foreign_keys=[verified_by])

class PerformanceMetric(Base):
    __tablename__ = 'performance_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    metric_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # system, application, database, network
    value = Column(Float, nullable=False)
    unit = Column(String(20))
    threshold_warning = Column(Float)
    threshold_critical = Column(Float)
    measured_at = Column(DateTime, nullable=False)
    server_name = Column(String(100))
    component_name = Column(String(100))
    additional_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class IntegrationLog(Base):
    __tablename__ = 'integration_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    integration_name = Column(String(100), nullable=False)
    integration_type = Column(String(50), nullable=False)  # api, database, file, webhook
    direction = Column(String(20), nullable=False)  # inbound, outbound
    status = Column(String(20), default='success')  # success, failed, partial
    request_data = Column(JSON)
    response_data = Column(JSON)
    error_message = Column(Text)
    processing_time_ms = Column(Integer)
    record_count = Column(Integer)
    initiated_by = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    initiated_by_employee = relationship("Employee", foreign_keys=[initiated_by])
```

## Pydantic Schemas برای سیستم اطلاعاتی

```python
# app/schemas/information.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ReportType(str, Enum):
    ACADEMIC = "آموزشی"
    FINANCIAL = "مالی"
    ADMINISTRATIVE = "اداری"
    STUDENT = "دانشجویی"
    EMPLOYEE = "کارمندی"
    LIBRARY = "کتابخانه‌ای"
    RESEARCH = "پژوهشی"
    OPERATIONAL = "عملیاتی"
    COMPLIANCE = "انطباقی"
    CUSTOM = "سفارشی"

class ReportFormat(str, Enum):
    PDF = "PDF"
    EXCEL = "Excel"
    CSV = "CSV"
    HTML = "HTML"
    JSON = "JSON"
    XML = "XML"

class ReportFrequency(str, Enum):
    DAILY = "روزانه"
    WEEKLY = "هفتگی"
    MONTHLY = "ماهانه"
    QUARTERLY = "فصلی"
    SEMI_ANNUAL = "شش‌ماهه"
    ANNUAL = "سالانه"
    ON_DEMAND = "درخواست"

class DashboardType(str, Enum):
    EXECUTIVE = "مدیرعامل"
    ACADEMIC = "آموزشی"
    FINANCIAL = "مالی"
    OPERATIONAL = "عملیاتی"
    STUDENT = "دانشجویی"
    FACULTY = "دانشکده"
    DEPARTMENT = "بخش"
    CUSTOM = "سفارشی"

class DataSourceType(str, Enum):
    DATABASE = "پایگاه داده"
    API = "API"
    FILE = "فایل"
    EXTERNAL_SYSTEM = "سیستم خارجی"
    MANUAL_ENTRY = "ورود دستی"

class MetricType(str, Enum):
    COUNT = "شمارش"
    SUM = "جمع"
    AVERAGE = "میانگین"
    PERCENTAGE = "درصد"
    RATIO = "نسبت"
    TREND = "روند"

class AlertType(str, Enum):
    INFO = "اطلاعاتی"
    WARNING = "هشدار"
    ERROR = "خطا"
    CRITICAL = "بحرانی"

class AlertStatus(str, Enum):
    ACTIVE = "فعال"
    ACKNOWLEDGED = "تایید شده"
    RESOLVED = "حل شده"
    DISMISSED = "رد شده"

# Report schemas
class ReportBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    report_type: ReportType
    description: Optional[str] = None
    query_definition: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    template_path: Optional[str] = None
    output_format: ReportFormat = ReportFormat.PDF
    frequency: ReportFrequency = ReportFrequency.ON_DEMAND
    schedule_config: Optional[Dict[str, Any]] = None
    access_level: str = "internal"
    required_permissions: Optional[Dict[str, Any]] = None
    is_scheduled: bool = False
    version: str = "1.0"
    tags: Optional[Dict[str, Any]] = None

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    report_type: Optional[ReportType] = None
    description: Optional[str] = None
    query_definition: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    template_path: Optional[str] = None
    output_format: Optional[ReportFormat] = None
    frequency: Optional[ReportFrequency] = None
    schedule_config: Optional[Dict[str, Any]] = None
    access_level: Optional[str] = None
    required_permissions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_scheduled: Optional[bool] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    version: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None

class Report(ReportBase):
    id: int
    is_active: bool
    last_run_date: Optional[datetime] = None
    next_run_date: Optional[datetime] = None
    created_by: int
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReportWithDetails(Report):
    created_by_employee: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None
    executions_count: int = 0
    subscriptions_count: int = 0

# Report Execution schemas
class ReportExecutionBase(BaseModel):
    parameters_used: Optional[Dict[str, Any]] = None

class ReportExecutionCreate(ReportExecutionBase):
    report_id: int

class ReportExecution(ReportExecutionBase):
    id: int
    report_id: int
    execution_date: datetime
    status: str
    execution_time_seconds: Optional[float] = None
    records_processed: Optional[int] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    error_message: Optional[str] = None
    executed_by: int
    is_manual: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ReportExecutionWithDetails(ReportExecution):
    report: Optional[Dict[str, Any]] = None
    executed_by_employee: Optional[Dict[str, Any]] = None

# Dashboard schemas
class DashboardBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    dashboard_type: DashboardType
    description: Optional[str] = None
    layout_config: Optional[Dict[str, Any]] = None
    widgets: Optional[Dict[str, Any]] = None
    access_level: str = "internal"
    required_permissions: Optional[Dict[str, Any]] = None
    is_public: bool = False
    refresh_interval_minutes: int = 60
    version: str = "1.0"
    tags: Optional[Dict[str, Any]] = None

class DashboardCreate(DashboardBase):
    pass

class DashboardUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    dashboard_type: Optional[DashboardType] = None
    description: Optional[str] = None
    layout_config: Optional[Dict[str, Any]] = None
    widgets: Optional[Dict[str, Any]] = None
    access_level: Optional[str] = None
    required_permissions: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    is_active: Optional[bool] = None
    refresh_interval_minutes: Optional[int] = None
    last_modified_by: Optional[int] = None
    last_modified_date: Optional[datetime] = None
    version: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None

class Dashboard(DashboardBase):
    id: int
    is_active: bool
    created_by: int
    last_modified_by: Optional[int] = None
    last_modified_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DashboardWithDetails(Dashboard):
    created_by_employee: Optional[Dict[str, Any]] = None
    last_modified_by_employee: Optional[Dict[str, Any]] = None
    widgets_count: int = 0

# Data Source schemas
class DataSourceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    source_type: DataSourceType
    connection_string: Optional[str] = None
    database_name: Optional[str] = None
    table_name: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_key: Optional[str] = None
    file_path: Optional[str] = None
    file_format: Optional[str] = None
    refresh_schedule: Optional[Dict[str, Any]] = None
    access_level: str = "internal"
    required_permissions: Optional[Dict[str, Any]] = None

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    source_type: Optional[DataSourceType] = None
    connection_string: Optional[str] = None
    database_name: Optional[str] = None
    table_name: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_key: Optional[str] = None
    file_path: Optional[str] = None
    file_format: Optional[str] = None
    refresh_schedule: Optional[Dict[str, Any]] = None
    last_refresh_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    access_level: Optional[str] = None
    required_permissions: Optional[Dict[str, Any]] = None

class DataSource(DataSourceBase):
    id: int
    last_refresh_date: Optional[datetime] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DataSourceWithDetails(DataSource):
    created_by_employee: Optional[Dict[str, Any]] = None

# Metric schemas
class MetricBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    metric_type: MetricType
    description: Optional[str] = None
    formula: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    unit: Optional[str] = None
    decimal_places: int = 2
    target_value: Optional[float] = None
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None

class MetricCreate(MetricBase):
    data_source_id: Optional[int] = None

class MetricUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    metric_type: Optional[MetricType] = None
    description: Optional[str] = None
    formula: Optional[str] = None
    data_source_id: Optional[int] = None
    parameters: Optional[Dict[str, Any]] = None
    unit: Optional[str] = None
    decimal_places: Optional[int] = None
    target_value: Optional[float] = None
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None
    is_active: Optional[bool] = None
    last_calculated_date: Optional[datetime] = None

class Metric(MetricBase):
    id: int
    data_source_id: Optional[int] = None
    is_active: bool
    last_calculated_date: Optional[datetime] = None
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MetricWithDetails(Metric):
    data_source: Optional[Dict[str, Any]] = None
    created_by_employee: Optional[Dict[str, Any]] = None
    current_value: Optional[float] = None
    values_count: int = 0

# Alert schemas
class AlertBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    alert_type: AlertType
    severity: str = "medium"
    message: str = Field(..., min_length=1)
    description: Optional[str] = None
    trigger_condition: Optional[Dict[str, Any]] = None
    affected_entities: Optional[Dict[str, Any]] = None
    escalation_rules: Optional[Dict[str, Any]] = None
    notification_channels: Optional[Dict[str, Any]] = None

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    alert_type: Optional[AlertType] = None
    severity: Optional[str] = None
    message: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    trigger_condition: Optional[Dict[str, Any]] = None
    affected_entities: Optional[Dict[str, Any]] = None
    status: Optional[AlertStatus] = None
    acknowledged_by: Optional[int] = None
    acknowledged_date: Optional[datetime] = None
    resolved_by: Optional[int] = None
    resolved_date: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    escalation_rules: Optional[Dict[str, Any]] = None
    notification_channels: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class Alert(AlertBase):
    id: int
    status: AlertStatus
    acknowledged_by: Optional[int] = None
    acknowledged_date: Optional[datetime] = None
    resolved_by: Optional[int] = None
    resolved_date: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AlertWithDetails(Alert):
    acknowledged_by_employee: Optional[Dict[str, Any]] = None
    resolved_by_employee: Optional[Dict[str, Any]] = None

# Notification schemas
class NotificationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    notification_type: str = Field(..., min_length=1, max_length=50)
    priority: str = "normal"
    recipient_type: str = Field(..., min_length=1, max_length=20)
    channels: Optional[Dict[str, Any]] = None
    scheduled_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

class NotificationCreate(NotificationBase):
    recipient_user_id: Optional[int] = None
    recipient_role_id: Optional[int] = None
    recipient_department_id: Optional[int] = None
    email: Optional[EmailStr] = None

class NotificationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    message: Optional[str] = Field(None, min_length=1)
    notification_type: Optional[str] = Field(None, min_length=1, max_length=50)
    priority: Optional[str] = None
    recipient_type: Optional[str] = Field(None, min_length=1, max_length=20)
    recipient_user_id: Optional[int] = None
    recipient_role_id: Optional[int] = None
    recipient_department_id: Optional[int] = None
    email: Optional[EmailStr] = None
    channels: Optional[Dict[str, Any]] = None
    scheduled_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    is_read: Optional[bool] = None
    read_date: Optional[datetime] = None
    is_archived: Optional[bool] = None

class Notification(NotificationBase):
    id: int
    recipient_user_id: Optional[int] = None
    recipient_role_id: Optional[int] = None
    recipient_department_id: Optional[int] = None
    email: Optional[EmailStr] = None
    is_read: bool
    read_date: Optional[datetime] = None
    is_archived: bool
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationWithDetails(Notification):
    recipient_user: Optional[Dict[str, Any]] = None
    created_by_employee: Optional[Dict[str, Any]] = None

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
class ReportSearchFilters(BaseModel):
    report_type: Optional[ReportType] = None
    output_format: Optional[ReportFormat] = None
    frequency: Optional[ReportFrequency] = None
    access_level: Optional[str] = None
    is_active: Optional[bool] = None
    is_scheduled: Optional[bool] = None
    created_by: Optional[int] = None
    approved_by: Optional[int] = None
    search: Optional[str] = None

class DashboardSearchFilters(BaseModel):
    dashboard_type: Optional[DashboardType] = None
    access_level: Optional[str] = None
    is_public: Optional[bool] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None

class AlertSearchFilters(BaseModel):
    alert_type: Optional[AlertType] = None
    severity: Optional[str] = None
    status: Optional[AlertStatus] = None
    acknowledged_by: Optional[int] = None
    resolved_by: Optional[int] = None
    is_active: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

class NotificationSearchFilters(BaseModel):
    notification_type: Optional[str] = None
    priority: Optional[str] = None
    recipient_type: Optional[str] = None
    recipient_user_id: Optional[int] = None
    is_read: Optional[bool] = None
    is_archived: Optional[bool] = None
    created_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

class MetricSearchFilters(BaseModel):
    metric_type: Optional[MetricType] = None
    data_source_id: Optional[int] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None

class DataSourceSearchFilters(BaseModel):
    source_type: Optional[DataSourceType] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None
```

این پیاده‌سازی کامل مدل‌های اطلاعاتی و گزارش‌گیری شامل تمام ویژگی‌های مورد نیاز برای سیستم گزارش‌گیری و تحلیل داده‌های دانشگاهی ایران است.
