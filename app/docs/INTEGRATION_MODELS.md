# مدل‌های یکپارچه‌سازی و API - Integration and API Models

## مدل‌های SQLAlchemy برای سیستم یکپارچه‌سازی

```python
# app/models/integration.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class IntegrationType(str, enum.Enum):
    REST_API = "REST API"
    GRAPHQL_API = "GraphQL API"
    SOAP_API = "SOAP API"
    DATABASE = "پایگاه داده"
    FILE_SYSTEM = "سیستم فایل"
    MESSAGE_QUEUE = "صف پیام"
    WEBHOOK = "وب‌هوک"
    EMAIL = "ایمیل"
    SMS = "پیامک"
    FTP = "FTP"
    SFTP = "SFTP"
    LDAP = "LDAP"
    OAUTH = "OAuth"
    SAML = "SAML"
    WEBDAV = "WebDAV"

class IntegrationStatus(str, enum.Enum):
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    ERROR = "خطا"
    MAINTENANCE = "در حال تعمیر"
    DEPRECATED = "منسوخ شده"

class AuthenticationType(str, enum.Enum):
    NONE = "هیچ"
    BASIC = "پایه"
    BEARER_TOKEN = "توکن Bearer"
    API_KEY = "کلید API"
    OAUTH2 = "OAuth2"
    JWT = "JWT"
    CERTIFICATE = "گواهی دیجیتال"
    SIGNATURE = "امضا دیجیتال"

class DataFormat(str, enum.Enum):
    JSON = "JSON"
    XML = "XML"
    CSV = "CSV"
    YAML = "YAML"
    FORM_DATA = "فرم داده"
    MULTIPART = "چند بخشی"
    BINARY = "باینری"

class SyncDirection(str, enum.Enum):
    INBOUND = "ورودی"
    OUTBOUND = "خروجی"
    BIDIRECTIONAL = "دو طرفه"

class SyncStatus(str, enum.Enum):
    PENDING = "در انتظار"
    RUNNING = "در حال اجرا"
    COMPLETED = "تکمیل شده"
    FAILED = "ناموفق"
    CANCELLED = "لغو شده"
    PARTIAL_SUCCESS = "موفقیت جزئی"

class WebhookEvent(str, enum.Enum):
    STUDENT_CREATED = "ایجاد دانشجو"
    STUDENT_UPDATED = "به‌روزرسانی دانشجو"
    EMPLOYEE_CREATED = "ایجاد کارمند"
    EMPLOYEE_UPDATED = "به‌روزرسانی کارمند"
    COURSE_CREATED = "ایجاد درس"
    COURSE_UPDATED = "به‌روزرسانی درس"
    GRADE_SUBMITTED = "ثبت نمره"
    ATTENDANCE_MARKED = "ثبت حضور"
    PAYMENT_RECEIVED = "دریافت پرداخت"
    SYSTEM_ALERT = "هشدار سیستم"

class APIEndpoint(Base):
    __tablename__ = 'api_endpoints'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    path = Column(String(500), nullable=False)
    method = Column(String(10), nullable=False)  # GET, POST, PUT, DELETE, PATCH
    version = Column(String(20), default="v1")
    category = Column(String(50), nullable=False)  # academic, administrative, financial, etc.
    authentication_required = Column(Boolean, default=True)
    required_permissions = Column(JSON)
    rate_limit = Column(JSON)
    request_schema = Column(JSON)
    response_schema = Column(JSON)
    error_responses = Column(JSON)
    is_active = Column(Boolean, default=True)
    is_deprecated = Column(Boolean, default=False)
    deprecated_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class APIKey(Base):
    __tablename__ = 'api_keys'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    description = Column(Text)
    owner_type = Column(String(20), nullable=False)  # employee, system, integration
    owner_id = Column(Integer)
    permissions = Column(JSON)
    rate_limit = Column(JSON)
    ip_whitelist = Column(JSON)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime)
    last_used_at = Column(DateTime)
    usage_count = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class Integration(Base):
    __tablename__ = 'integrations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    integration_type = Column(Enum(IntegrationType), nullable=False)
    status = Column(Enum(IntegrationStatus), default=IntegrationStatus.ACTIVE)
    base_url = Column(String(500))
    authentication_type = Column(Enum(AuthenticationType), default=AuthenticationType.NONE)
    authentication_config = Column(JSON)
    headers = Column(JSON)
    timeout_seconds = Column(Integer, default=30)
    retry_count = Column(Integer, default=3)
    retry_delay_seconds = Column(Integer, default=5)
    data_format = Column(Enum(DataFormat), default=DataFormat.JSON)
    sync_direction = Column(Enum(SyncDirection), default=SyncDirection.BIDIRECTIONAL)
    sync_schedule = Column(JSON)
    last_sync_date = Column(DateTime)
    next_sync_date = Column(DateTime)
    error_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class Webhook(Base):
    __tablename__ = 'webhooks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    url = Column(String(500), nullable=False)
    method = Column(String(10), default="POST")
    headers = Column(JSON)
    authentication_type = Column(Enum(AuthenticationType), default=AuthenticationType.NONE)
    authentication_config = Column(JSON)
    events = Column(JSON)
    filters = Column(JSON)
    retry_count = Column(Integer, default=3)
    retry_delay_seconds = Column(Integer, default=5)
    timeout_seconds = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)
    is_secure = Column(Boolean, default=True)
    secret_key = Column(String(100))
    last_triggered_at = Column(DateTime)
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class WebhookDelivery(Base):
    __tablename__ = 'webhook_deliveries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    webhook_id = Column(Integer, ForeignKey('webhooks.id'), nullable=False)
    event = Column(Enum(WebhookEvent), nullable=False)
    payload = Column(JSON)
    response_status = Column(Integer)
    response_body = Column(Text)
    response_headers = Column(JSON)
    delivery_time_ms = Column(Integer)
    attempt_count = Column(Integer, default=1)
    max_attempts = Column(Integer, default=3)
    status = Column(String(20), default='success')  # success, failed, retrying
    error_message = Column(Text)
    delivered_at = Column(DateTime, default=datetime.utcnow)
    next_retry_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    webhook = relationship("Webhook", back_populates="deliveries")

class DataMapping(Base):
    __tablename__ = 'data_mappings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    source_integration_id = Column(Integer, ForeignKey('integrations.id'), nullable=False)
    target_integration_id = Column(Integer, ForeignKey('integrations.id'), nullable=False)
    source_entity = Column(String(100), nullable=False)
    target_entity = Column(String(100), nullable=False)
    field_mappings = Column(JSON)
    transformation_rules = Column(JSON)
    validation_rules = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    source_integration = relationship("Integration", foreign_keys=[source_integration_id])
    target_integration = relationship("Integration", foreign_keys=[target_integration_id])
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class SyncLog(Base):
    __tablename__ = 'sync_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    integration_id = Column(Integer, ForeignKey('integrations.id'), nullable=False)
    sync_id = Column(String(20), unique=True, nullable=False)
    direction = Column(Enum(SyncDirection), nullable=False)
    status = Column(Enum(SyncStatus), default=SyncStatus.PENDING)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer)
    records_processed = Column(Integer, default=0)
    records_success = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    data_volume_bytes = Column(Integer)
    error_message = Column(Text)
    error_details = Column(JSON)
    initiated_by = Column(String(20), default='system')  # system, manual, scheduled
    manual_initiated_by = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    integration = relationship("Integration", back_populates="sync_logs")
    manual_initiated_by_employee = relationship("Employee", foreign_keys=[manual_initiated_by])

class APIRequestLog(Base):
    __tablename__ = 'api_request_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String(50), unique=True, nullable=False)
    endpoint_id = Column(Integer, ForeignKey('api_endpoints.id'))
    method = Column(String(10), nullable=False)
    path = Column(String(500), nullable=False)
    query_params = Column(JSON)
    headers = Column(JSON)
    request_body = Column(Text)
    response_status = Column(Integer)
    response_body = Column(Text)
    response_headers = Column(JSON)
    response_time_ms = Column(Integer)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    user_id = Column(Integer, ForeignKey('employees.id'))
    api_key_id = Column(Integer, ForeignKey('api_keys.id'))
    session_id = Column(String(100))
    error_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    endpoint = relationship("APIEndpoint", foreign_keys=[endpoint_id])
    user = relationship("Employee", foreign_keys=[user_id])
    api_key = relationship("APIKey", foreign_keys=[api_key_id])

class ExternalSystem(Base):
    __tablename__ = 'external_systems'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    system_type = Column(String(50), nullable=False)  # ERP, CRM, LMS, HRMS, etc.
    vendor = Column(String(100))
    version = Column(String(50))
    base_url = Column(String(500))
    contact_person = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(20))
    support_contract = Column(JSON)
    integration_status = Column(Enum(IntegrationStatus), default=IntegrationStatus.INACTIVE)
    last_sync_date = Column(DateTime)
    next_sync_date = Column(DateTime)
    data_retention_days = Column(Integer, default=365)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class MessageQueue(Base):
    __tablename__ = 'message_queues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    queue_type = Column(String(20), nullable=False)  # rabbitmq, kafka, sqs, etc.
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    virtual_host = Column(String(100))
    username = Column(String(100))
    password = Column(String(100))
    ssl_enabled = Column(Boolean, default=False)
    exchange_name = Column(String(100))
    routing_key = Column(String(100))
    dead_letter_exchange = Column(String(100))
    max_retries = Column(Integer, default=3)
    message_ttl_seconds = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class QueueMessage(Base):
    __tablename__ = 'queue_messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    queue_id = Column(Integer, ForeignKey('message_queues.id'), nullable=False)
    message_id = Column(String(100), unique=True, nullable=False)
    correlation_id = Column(String(100))
    message_type = Column(String(50), nullable=False)
    priority = Column(Integer, default=1)
    payload = Column(JSON)
    headers = Column(JSON)
    status = Column(String(20), default='pending')  # pending, processing, completed, failed, dead_letter
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    error_message = Column(Text)
    processing_started_at = Column(DateTime)
    processing_completed_at = Column(DateTime)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    queue = relationship("MessageQueue", back_populates="messages")

class FileTransfer(Base):
    __tablename__ = 'file_transfers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transfer_id = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    description = Column(Text)
    transfer_type = Column(String(20), nullable=False)  # ftp, sftp, webdav, api
    source_path = Column(String(500), nullable=False)
    destination_path = Column(String(500), nullable=False)
    file_pattern = Column(String(100))
    schedule = Column(JSON)
    authentication_config = Column(JSON)
    compression = Column(String(20))
    encryption = Column(String(20))
    status = Column(String(20), default='pending')  # pending, running, completed, failed
    file_count = Column(Integer)
    total_size_bytes = Column(Integer)
    transferred_size_bytes = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer)
    error_message = Column(Text)
    initiated_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    initiated_by_employee = relationship("Employee", foreign_keys=[initiated_by])

class DataExport(Base):
    __tablename__ = 'data_exports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    export_id = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = str = Field(..., min_length=1, max_length=255)
    description = Column(Text)
    data_source = Column(JSON)
    filters = Column(JSON)
    format = Column(Enum(DataFormat), default=DataFormat.JSON)
    compression = Column(String(20))
    destination = Column(JSON)
    schedule = Column(JSON)
    status = Column(String(20), default='pending')  # pending, running, completed, failed
    record_count = Column(Integer)
    file_size_bytes = Column(Integer)
    file_path = Column(String(500))
    download_url = Column(String(500))
    expires_at = Column(DateTime)
    download_count = Column(Integer, default=0)
    last_download_at = Column(DateTime)
    initiated_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    initiated_by_employee = relationship("Employee", foreign_keys=[initiated_by])

class APIUsage(Base):
    __tablename__ = 'api_usage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    api_key_id = Column(Integer, ForeignKey('api_keys.id'))
    endpoint_id = Column(Integer, ForeignKey('api_endpoints.id'))
    user_id = Column(Integer, ForeignKey('employees.id'))
    method = Column(String(10), nullable=False)
    path = Column(String(500), nullable=False)
    response_status = Column(Integer)
    response_time_ms = Column(Integer)
    data_transferred_bytes = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    api_key = relationship("APIKey", foreign_keys=[api_key_id])
    endpoint = relationship("APIEndpoint", foreign_keys=[endpoint_id])
    user = relationship("Employee", foreign_keys=[user_id])

class IntegrationHealth(Base):
    __tablename__ = 'integration_health'

    id = Column(Integer, primary_key=True, autoincrement=True)
    integration_id = Column(Integer, ForeignKey('integrations.id'), nullable=False)
    check_type = Column(String(50), nullable=False)  # connectivity, performance, data_integrity
    status = Column(String(20), nullable=False)  # healthy, warning, critical, unknown
    response_time_ms = Column(Integer)
    error_message = Column(Text)
    details = Column(JSON)
    checked_at = Column(DateTime, default=datetime.utcnow)
    next_check_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    integration = relationship("Integration", back_populates="health_checks")
```

## Pydantic Schemas برای سیستم یکپارچه‌سازی

```python
# app/schemas/integration.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class IntegrationType(str, Enum):
    REST_API = "REST API"
    GRAPHQL_API = "GraphQL API"
    SOAP_API = "SOAP API"
    DATABASE = "پایگاه داده"
    FILE_SYSTEM = "سیستم فایل"
    MESSAGE_QUEUE = "صف پیام"
    WEBHOOK = "وب‌هوک"
    EMAIL = "ایمیل"
    SMS = "پیامک"
    FTP = "FTP"
    SFTP = "SFTP"
    LDAP = "LDAP"
    OAUTH = "OAuth"
    SAML = "SAML"
    WEBDAV = "WebDAV"

class IntegrationStatus(str, Enum):
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    ERROR = "خطا"
    MAINTENANCE = "در حال تعمیر"
    DEPRECATED = "منسوخ شده"

class AuthenticationType(str, Enum):
    NONE = "هیچ"
    BASIC = "پایه"
    BEARER_TOKEN = "توکن Bearer"
    API_KEY = "کلید API"
    OAUTH2 = "OAuth2"
    JWT = "JWT"
    CERTIFICATE = "گواهی دیجیتال"
    SIGNATURE = "امضا دیجیتال"

class DataFormat(str, Enum):
    JSON = "JSON"
    XML = "XML"
    CSV = "CSV"
    YAML = "YAML"
    FORM_DATA = "فرم داده"
    MULTIPART = "چند بخشی"
    BINARY = "باینری"

class SyncDirection(str, Enum):
    INBOUND = "ورودی"
    OUTBOUND = "خروجی"
    BIDIRECTIONAL = "دو طرفه"

class SyncStatus(str, Enum):
    PENDING = "در انتظار"
    RUNNING = "در حال اجرا"
    COMPLETED = "تکمیل شده"
    FAILED = "ناموفق"
    CANCELLED = "لغو شده"
    PARTIAL_SUCCESS = "موفقیت جزئی"

class WebhookEvent(str, Enum):
    STUDENT_CREATED = "ایجاد دانشجو"
    STUDENT_UPDATED = "به‌روزرسانی دانشجو"
    EMPLOYEE_CREATED = "ایجاد کارمند"
    EMPLOYEE_UPDATED = "به‌روزرسانی کارمند"
    COURSE_CREATED = "ایجاد درس"
    COURSE_UPDATED = "به‌روزرسانی درس"
    GRADE_SUBMITTED = "ثبت نمره"
    ATTENDANCE_MARKED = "ثبت حضور"
    PAYMENT_RECEIVED = "دریافت پرداخت"
    SYSTEM_ALERT = "هشدار سیستم"

# API Endpoint schemas
class APIEndpointBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    path: str = Field(..., min_length=1, max_length=500)
    method: str = Field(..., min_length=1, max_length=10)
    version: str = "v1"
    category: str = Field(..., min_length=1, max_length=50)
    authentication_required: bool = True
    required_permissions: Optional[Dict[str, Any]] = None
    rate_limit: Optional[Dict[str, Any]] = None
    request_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None
    error_responses: Optional[Dict[str, Any]] = None

class APIEndpointCreate(APIEndpointBase):
    pass

class APIEndpointUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    path: Optional[str] = Field(None, min_length=1, max_length=500)
    method: Optional[str] = Field(None, min_length=1, max_length=10)
    version: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    authentication_required: Optional[bool] = None
    required_permissions: Optional[Dict[str, Any]] = None
    rate_limit: Optional[Dict[str, Any]] = None
    request_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None
    error_responses: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_deprecated: Optional[bool] = None
    deprecated_at: Optional[datetime] = None

class APIEndpoint(APIEndpointBase):
    id: int
    is_active: bool
    is_deprecated: bool
    deprecated_at: Optional[datetime] = None
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class APIEndpointWithDetails(APIEndpoint):
    created_by_employee: Optional[Dict[str, Any]] = None

# API Key schemas
class APIKeyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    owner_type: str = Field(..., min_length=1, max_length=20)
    owner_id: Optional[int] = None
    permissions: Optional[Dict[str, Any]] = None
    rate_limit: Optional[Dict[str, Any]] = None
    ip_whitelist: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None

class APIKeyCreate(APIKeyBase):
    pass

class APIKeyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    owner_type: Optional[str] = Field(None, min_length=1, max_length=20)
    owner_id: Optional[int] = None
    permissions: Optional[Dict[str, Any]] = None
    rate_limit: Optional[Dict[str, Any]] = None
    ip_whitelist: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None

class APIKey(APIKeyBase):
    id: int
    key: str
    is_active: bool
    last_used_at: Optional[datetime] = None
    usage_count: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class APIKeyWithDetails(APIKey):
    created_by_employee: Optional[Dict[str, Any]] = None

# Integration schemas
class IntegrationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    integration_type: IntegrationType
    base_url: Optional[str] = None
    authentication_type: AuthenticationType = AuthenticationType.NONE
    authentication_config: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, Any]] = None
    timeout_seconds: int = 30
    retry_count: int = 3
    retry_delay_seconds: int = 5
    data_format: DataFormat = DataFormat.JSON
    sync_direction: SyncDirection = SyncDirection.BIDIRECTIONAL
    sync_schedule: Optional[Dict[str, Any]] = None

class IntegrationCreate(IntegrationBase):
    pass

class IntegrationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    integration_type: Optional[IntegrationType] = None
    status: Optional[IntegrationStatus] = None
    base_url: Optional[str] = None
    authentication_type: Optional[AuthenticationType] = None
    authentication_config: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, Any]] = None
    timeout_seconds: Optional[int] = None
    retry_count: Optional[int] = None
    retry_delay_seconds: Optional[int] = None
    data_format: Optional[DataFormat] = None
    sync_direction: Optional[SyncDirection] = None
    sync_schedule: Optional[Dict[str, Any]] = None
    last_sync_date: Optional[datetime] = None
    next_sync_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class Integration(IntegrationBase):
    id: int
    status: IntegrationStatus
    last_sync_date: Optional[datetime] = None
    next_sync_date: Optional[datetime] = None
    error_count: int
    success_count: int
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class IntegrationWithDetails(Integration):
    created_by_employee: Optional[Dict[str, Any]] = None
    sync_logs_count: int = 0
    health_checks_count: int = 0

# Webhook schemas
class WebhookBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    url: str = Field(..., min_length=1, max_length=500)
    method: str = "POST"
    headers: Optional[Dict[str, Any]] = None
    authentication_type: AuthenticationType = AuthenticationType.NONE
    authentication_config: Optional[Dict[str, Any]] = None
    events: Optional[Dict[str, Any]] = None
    filters: Optional[Dict[str, Any]] = None
    retry_count: int = 3
    retry_delay_seconds: int = 5
    timeout_seconds: int = 30
    is_secure: bool = True
    secret_key: Optional[str] = None

class WebhookCreate(WebhookBase):
    pass

class WebhookUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    url: Optional[str] = Field(None, min_length=1, max_length=500)
    method: Optional[str] = None
    headers: Optional[Dict[str, Any]] = None
    authentication_type: Optional[AuthenticationType] = None
    authentication_config: Optional[Dict[str, Any]] = None
    events: Optional[Dict[str, Any]] = None
    filters: Optional[Dict[str, Any]] = None
    retry_count: Optional[int] = None
    retry_delay_seconds: Optional[int] = None
    timeout_seconds: Optional[int] = None
    is_active: Optional[bool] = None
    is_secure: Optional[bool] = None
    secret_key: Optional[str] = None

class Webhook(WebhookBase):
    id: int
    is_active: bool
    last_triggered_at: Optional[datetime] = None
    success_count: int
    failure_count: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WebhookWithDetails(Webhook):
    created_by_employee: Optional[Dict[str, Any]] = None
    deliveries_count: int = 0

# Webhook Delivery schemas
class WebhookDeliveryBase(BaseModel):
    event: WebhookEvent
    payload: Optional[Dict[str, Any]] = None

class WebhookDeliveryCreate(WebhookDeliveryBase):
    webhook_id: int

class WebhookDelivery(WebhookDeliveryBase):
    id: int
    webhook_id: int
    response_status: Optional[int] = None
    response_body: Optional[str] = None
    response_headers: Optional[Dict[str, Any]] = None
    delivery_time_ms: Optional[int] = None
    attempt_count: int
    max_attempts: int
    status: str
    error_message: Optional[str] = None
    delivered_at: datetime
    next_retry_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class WebhookDeliveryWithDetails(WebhookDelivery):
    webhook: Optional[Dict[str, Any]] = None

# Data Mapping schemas
class DataMappingBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    source_integration_id: int
    target_integration_id: int
    source_entity: str = Field(..., min_length=1, max_length=100)
    target_entity: str = Field(..., min_length=1, max_length=100)
    field_mappings: Optional[Dict[str, Any]] = None
    transformation_rules: Optional[Dict[str, Any]] = None
    validation_rules: Optional[Dict[str, Any]] = None

class DataMappingCreate(DataMappingBase):
    pass

class DataMappingUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    source_integration_id: Optional[int] = None
    target_integration_id: Optional[int] = None
    source_entity: Optional[str] = Field(None, min_length=1, max_length=100)
    target_entity: Optional[str] = Field(None, min_length=1, max_length=100)
    field_mappings: Optional[Dict[str, Any]] = None
    transformation_rules: Optional[Dict[str, Any]] = None
    validation_rules: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class DataMapping(DataMappingBase):
    id: int
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DataMappingWithDetails(DataMapping):
    source_integration: Optional[Dict[str, Any]] = None
    target_integration: Optional[Dict[str, Any]] = None
    created_by_employee: Optional[Dict[str, Any]] = None

# Sync Log schemas
class SyncLogBase(BaseModel):
    direction: SyncDirection
    records_processed: int = 0
    records_success: int = 0
    records_failed: int = 0
    data_volume_bytes: Optional[int] = None
    error_message: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None
    initiated_by: str = "system"

class SyncLogCreate(SyncLogBase):
    integration_id: int

class SyncLog(SyncLogBase):
    id: int
    integration_id: int
    sync_id: str
    status: SyncStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    manual_initiated_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SyncLogWithDetails(SyncLog):
    integration: Optional[Dict[str, Any]] = None
    manual_initiated_by_employee: Optional[Dict[str, Any]] = None

# External System schemas
class ExternalSystemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    system_type: str = Field(..., min_length=1, max_length=50)
    vendor: Optional[str] = None
    version: Optional[str] = None
    base_url: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    support_contract: Optional[Dict[str, Any]] = None
    data_retention_days: int = 365

class ExternalSystemCreate(ExternalSystemBase):
    pass

class ExternalSystemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    system_type: Optional[str] = Field(None, min_length=1, max_length=50)
    vendor: Optional[str] = None
    version: Optional[str] = None
    base_url: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    support_contract: Optional[Dict[str, Any]] = None
    integration_status: Optional[IntegrationStatus] = None
    last_sync_date: Optional[datetime] = None
    next_sync_date: Optional[datetime] = None
    data_retention_days: Optional[int] = None
    is_active: Optional[bool] = None

class ExternalSystem(ExternalSystemBase):
    id: int
    integration_status: IntegrationStatus
    last_sync_date: Optional[datetime] = None
    next_sync_date: Optional[datetime] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ExternalSystemWithDetails(ExternalSystem):
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
class APIEndpointSearchFilters(BaseModel):
    method: Optional[str] = None
    category: Optional[str] = None
    version: Optional[str] = None
    authentication_required: Optional[bool] = None
    is_active: Optional[bool] = None
    is_deprecated: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None

class IntegrationSearchFilters(BaseModel):
    integration_type: Optional[IntegrationType] = None
    status: Optional[IntegrationStatus] = None
    authentication_type: Optional[AuthenticationType] = None
    data_format: Optional[DataFormat] = None
    sync_direction: Optional[SyncDirection] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None

class WebhookSearchFilters(BaseModel):
    method: Optional[str] = None
    authentication_type: Optional[AuthenticationType] = None
    is_active: Optional[bool] = None
    is_secure: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None

class ExternalSystemSearchFilters(BaseModel):
    system_type: Optional[str] = None
    vendor: Optional[str] = None
    integration_status: Optional[IntegrationStatus] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None

class SyncLogSearchFilters(BaseModel):
    integration_id: Optional[int] = None
    direction: Optional[SyncDirection] = None
    status: Optional[SyncStatus] = None
    initiated_by: Optional[str] = None
    manual_initiated_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

class APIRequestLogSearchFilters(BaseModel):
    endpoint_id: Optional[int] = None
    method: Optional[str] = None
    response_status: Optional[int] = None
    user_id: Optional[int] = None
    api_key_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None
```

این پیاده‌سازی کامل مدل‌های یکپارچه‌سازی و API شامل تمام ویژگی‌های مورد نیاز برای ارتباطات سیستم‌های دانشگاهی ایران است.
