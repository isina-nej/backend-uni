# مدل‌های امنیتی و دسترسی - Security and Access Models

## مدل‌های SQLAlchemy برای سیستم امنیتی

```python
# app/models/security.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class AuthenticationMethod(str, enum.Enum):
    PASSWORD = "رمز عبور"
    TWO_FACTOR = "دو عاملی"
    BIOMETRIC = "بیومتریک"
    CERTIFICATE = "گواهی دیجیتال"
    SSO = "تک ورود"
    LDAP = "LDAP"
    OAUTH = "OAuth"

class SessionStatus(str, enum.Enum):
    ACTIVE = "فعال"
    EXPIRED = "منقضی"
    TERMINATED = "پایان یافته"
    SUSPENDED = "معلق"

class SecurityEventType(str, enum.Enum):
    LOGIN_SUCCESS = "ورود موفق"
    LOGIN_FAILURE = "ورود ناموفق"
    LOGOUT = "خروج"
    PASSWORD_CHANGE = "تغییر رمز عبور"
    PASSWORD_RESET = "بازنشانی رمز عبور"
    SESSION_TIMEOUT = "انقضای جلسه"
    UNAUTHORIZED_ACCESS = "دسترسی غیرمجاز"
    SUSPICIOUS_ACTIVITY = "فعالیت مشکوک"
    BRUTE_FORCE_ATTACK = "حمله brute force"
    SQL_INJECTION = "SQL injection"
    XSS_ATTACK = "حمله XSS"
    CSRF_ATTACK = "حمله CSRF"
    DATA_BREACH = "نقض داده"
    PRIVILEGE_ESCALATION = "ارتقای امتیاز"

class SecurityAlertLevel(str, enum.Enum):
    LOW = "کم"
    MEDIUM = "متوسط"
    HIGH = "بالا"
    CRITICAL = "بحرانی"

class EncryptionAlgorithm(str, enum.Enum):
    AES_256 = "AES-256"
    RSA_2048 = "RSA-2048"
    ECC = "ECC"
    SHA_256 = "SHA-256"

class AccessControlType(str, enum.Enum):
    ROLE_BASED = "بر پایه نقش"
    ATTRIBUTE_BASED = "بر پایه ویژگی"
    POLICY_BASED = "بر پایه سیاست"
    CONTEXT_BASED = "بر پایه زمینه"

class AuditAction(str, enum.Enum):
    CREATE = "ایجاد"
    READ = "خواندن"
    UPDATE = "به‌روزرسانی"
    DELETE = "حذف"
    EXECUTE = "اجرا"
    EXPORT = "صادرات"
    IMPORT = "واردات"
    LOGIN = "ورود"
    LOGOUT = "خروج"

class UserSession(Base):
    __tablename__ = 'user_sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    session_token = Column(String(500), unique=True, nullable=False)
    refresh_token = Column(String(500), unique=True)
    device_info = Column(JSON)
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(String(500))
    location = Column(JSON)
    status = Column(Enum(SessionStatus), default=SessionStatus.ACTIVE)
    login_time = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    expiry_time = Column(DateTime, nullable=False)
    is_secure = Column(Boolean, default=False)
    authentication_method = Column(Enum(AuthenticationMethod), default=AuthenticationMethod.PASSWORD)
    two_factor_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("Employee", back_populates="sessions")

class SecurityEvent(Base):
    __tablename__ = 'security_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(Enum(SecurityEventType), nullable=False)
    severity = Column(Enum(SecurityAlertLevel), default=SecurityAlertLevel.LOW)
    user_id = Column(Integer, ForeignKey('employees.id'))
    session_id = Column(Integer, ForeignKey('user_sessions.id'))
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    location = Column(JSON)
    resource = Column(String(500))  # URL, table, file, etc.
    action = Column(String(100))
    details = Column(JSON)
    is_suspicious = Column(Boolean, default=False)
    risk_score = Column(Float, default=0.0)
    response_taken = Column(Text)
    investigated_by = Column(Integer, ForeignKey('employees.id'))
    investigation_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("Employee", foreign_keys=[user_id])
    session = relationship("UserSession", foreign_keys=[session_id])
    investigator = relationship("Employee", foreign_keys=[investigated_by])

class SecurityPolicy(Base):
    __tablename__ = 'security_policies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    policy_type = Column(String(50), nullable=False)  # password, session, access, encryption
    rules = Column(JSON)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=1)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    effective_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    version = Column(String(20), default="1.0")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class PasswordPolicy(Base):
    __tablename__ = 'password_policies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    min_length = Column(Integer, default=8)
    max_length = Column(Integer, default=128)
    require_uppercase = Column(Boolean, default=True)
    require_lowercase = Column(Boolean, default=True)
    require_digits = Column(Boolean, default=True)
    require_special_chars = Column(Boolean, default=True)
    prevent_common_passwords = Column(Boolean, default=True)
    prevent_personal_info = Column(Boolean, default=True)
    max_age_days = Column(Integer, default=90)
    history_count = Column(Integer, default=5)
    lockout_threshold = Column(Integer, default=5)
    lockout_duration_minutes = Column(Integer, default=30)
    reset_token_expiry_hours = Column(Integer, default=24)
    two_factor_required = Column(Boolean, default=False)
    two_factor_methods = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class UserPassword(Base):
    __tablename__ = 'user_passwords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    password_hash = Column(String(500), nullable=False)
    salt = Column(String(100), nullable=False)
    algorithm = Column(String(50), default="bcrypt")
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    must_change = Column(Boolean, default=False)
    change_reason = Column(String(255))

    # Relationships
    user = relationship("Employee", back_populates="passwords")

class PasswordHistory(Base):
    __tablename__ = 'password_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    password_hash = Column(String(500), nullable=False)
    salt = Column(String(100), nullable=False)
    algorithm = Column(String(50), default="bcrypt")
    changed_at = Column(DateTime, default=datetime.utcnow)
    changed_by = Column(Integer, ForeignKey('employees.id'))
    change_reason = Column(String(255))

    # Relationships
    user = relationship("Employee", foreign_keys=[user_id])
    changed_by_employee = relationship("Employee", foreign_keys=[changed_by])

class AccessControl(Base):
    __tablename__ = 'access_controls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    control_type = Column(Enum(AccessControlType), nullable=False)
    resource_type = Column(String(50), nullable=False)  # table, api, file, function
    resource_name = Column(String(255), nullable=False)
    permissions = Column(JSON)
    conditions = Column(JSON)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=1)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    effective_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    version = Column(String(20), default="1.0")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class RolePermission(Base):
    __tablename__ = 'role_permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    conditions = Column(JSON)
    is_active = Column(Boolean, default=True)
    granted_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")
    granted_by_employee = relationship("Employee", foreign_keys=[granted_by])

class UserPermission(Base):
    __tablename__ = 'user_permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    conditions = Column(JSON)
    is_active = Column(Boolean, default=True)
    granted_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("Employee", back_populates="permissions")
    permission = relationship("Permission", back_populates="users")
    granted_by_employee = relationship("Employee", foreign_keys=[granted_by])

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    resource_type = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    scope = Column(String(50), default="global")  # global, university, faculty, department, personal
    is_system = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    roles = relationship("RolePermission", back_populates="permission")
    users = relationship("UserPermission", back_populates="permission")

class SecurityAudit(Base):
    __tablename__ = 'security_audits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(Enum(AuditAction), nullable=False)
    user_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    session_id = Column(Integer, ForeignKey('user_sessions.id'))
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    location = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    reason = Column(String(255))
    compliance_requirements = Column(JSON)
    risk_assessment = Column(JSON)

    # Relationships
    user = relationship("Employee", foreign_keys=[user_id])
    session = relationship("UserSession", foreign_keys=[session_id])

class EncryptionKey(Base):
    __tablename__ = 'encryption_keys'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key_name = Column(String(255), nullable=False)
    key_type = Column(String(50), nullable=False)  # symmetric, asymmetric, hash
    algorithm = Column(Enum(EncryptionAlgorithm), nullable=False)
    key_data = Column(Text, nullable=False)  # encrypted key data
    key_version = Column(String(20), default="1.0")
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    last_rotated_at = Column(DateTime)
    rotation_schedule = Column(JSON)
    usage_count = Column(Integer, default=0)
    max_usage_count = Column(Integer)
    compromised = Column(Boolean, default=False)
    compromise_date = Column(DateTime)
    compromise_reason = Column(Text)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class SecurityIncident(Base):
    __tablename__ = 'security_incidents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(String(20), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(SecurityAlertLevel), nullable=False)
    status = Column(String(20), default='open')  # open, investigating, resolved, closed
    incident_type = Column(String(50), nullable=False)
    affected_systems = Column(JSON)
    affected_users = Column(JSON)
    discovered_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    reported_at = Column(DateTime)
    assigned_to = Column(Integer, ForeignKey('employees.id'))
    assigned_at = Column(DateTime)
    resolved_by = Column(Integer, ForeignKey('employees.id'))
    resolved_at = Column(DateTime)
    resolution = Column(Text)
    evidence = Column(JSON)
    impact_assessment = Column(JSON)
    lessons_learned = Column(Text)
    prevention_measures = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    discovered_by_employee = relationship("Employee", foreign_keys=[discovered_by])
    assigned_to_employee = relationship("Employee", foreign_keys=[assigned_to])
    resolved_by_employee = relationship("Employee", foreign_keys=[resolved_by])

class ComplianceCheck(Base):
    __tablename__ = 'compliance_checks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    check_name = Column(String(255), nullable=False)
    check_name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    compliance_standard = Column(String(100), nullable=False)  # GDPR, HIPAA, ISO27001, etc.
    check_type = Column(String(50), nullable=False)  # automated, manual, hybrid
    frequency = Column(String(20), default='daily')  # hourly, daily, weekly, monthly
    query_definition = Column(JSON)
    threshold_values = Column(JSON)
    is_active = Column(Boolean, default=True)
    last_run_date = Column(DateTime)
    next_run_date = Column(DateTime)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class ComplianceResult(Base):
    __tablename__ = 'compliance_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    compliance_check_id = Column(Integer, ForeignKey('compliance_checks.id'), nullable=False)
    check_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), nullable=False)  # pass, fail, warning, error
    score = Column(Float)
    details = Column(JSON)
    violations = Column(JSON)
    recommendations = Column(JSON)
    executed_by = Column(Integer, ForeignKey('employees.id'))
    reviewed_by = Column(Integer, ForeignKey('employees.id'))
    review_date = Column(DateTime)
    review_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    compliance_check = relationship("ComplianceCheck", back_populates="results")
    executed_by_employee = relationship("Employee", foreign_keys=[executed_by])
    reviewed_by_employee = relationship("Employee", foreign_keys=[reviewed_by])

class TwoFactorToken(Base):
    __tablename__ = 'two_factor_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    token = Column(String(100), nullable=False)
    token_type = Column(String(20), nullable=False)  # TOTP, SMS, Email
    secret_key = Column(String(100))
    backup_codes = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    last_used_at = Column(DateTime)
    usage_count = Column(Integer, default=0)

    # Relationships
    user = relationship("Employee", back_populates="two_factor_tokens")

class SecurityAlert(Base):
    __tablename__ = 'security_alerts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_type = Column(String(50), nullable=False)
    severity = Column(Enum(SecurityAlertLevel), nullable=False)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    details = Column(JSON)
    affected_resources = Column(JSON)
    triggered_by = Column(Integer, ForeignKey('employees.id'))
    triggered_at = Column(DateTime, default=datetime.utcnow)
    acknowledged_by = Column(Integer, ForeignKey('employees.id'))
    acknowledged_at = Column(DateTime)
    resolved_by = Column(Integer, ForeignKey('employees.id'))
    resolved_at = Column(DateTime)
    resolution_notes = Column(Text)
    escalation_level = Column(Integer, default=1)
    notification_sent = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    triggered_by_employee = relationship("Employee", foreign_keys=[triggered_by])
    acknowledged_by_employee = relationship("Employee", foreign_keys=[acknowledged_by])
    resolved_by_employee = relationship("Employee", foreign_keys=[resolved_by])

class AccessLog(Base):
    __tablename__ = 'access_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('employees.id'))
    session_id = Column(Integer, ForeignKey('user_sessions.id'))
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(Integer)
    resource_name = Column(String(255))
    action = Column(Enum(AuditAction), nullable=False)
    method = Column(String(10))  # GET, POST, PUT, DELETE
    url = Column(String(500))
    parameters = Column(JSON)
    response_code = Column(Integer)
    response_time_ms = Column(Integer)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    location = Column(JSON)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("Employee", foreign_keys=[user_id])
    session = relationship("UserSession", foreign_keys=[session_id])
```

## Pydantic Schemas برای سیستم امنیتی

```python
# app/schemas/security.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class AuthenticationMethod(str, Enum):
    PASSWORD = "رمز عبور"
    TWO_FACTOR = "دو عاملی"
    BIOMETRIC = "بیومتریک"
    CERTIFICATE = "گواهی دیجیتال"
    SSO = "تک ورود"
    LDAP = "LDAP"
    OAUTH = "OAuth"

class SessionStatus(str, Enum):
    ACTIVE = "فعال"
    EXPIRED = "منقضی"
    TERMINATED = "پایان یافته"
    SUSPENDED = "معلق"

class SecurityEventType(str, Enum):
    LOGIN_SUCCESS = "ورود موفق"
    LOGIN_FAILURE = "ورود ناموفق"
    LOGOUT = "خروج"
    PASSWORD_CHANGE = "تغییر رمز عبور"
    PASSWORD_RESET = "بازنشانی رمز عبور"
    SESSION_TIMEOUT = "انقضای جلسه"
    UNAUTHORIZED_ACCESS = "دسترسی غیرمجاز"
    SUSPICIOUS_ACTIVITY = "فعالیت مشکوک"
    BRUTE_FORCE_ATTACK = "حمله brute force"
    SQL_INJECTION = "SQL injection"
    XSS_ATTACK = "حمله XSS"
    CSRF_ATTACK = "حمله CSRF"
    DATA_BREACH = "نقض داده"
    PRIVILEGE_ESCALATION = "ارتقای امتیاز"

class SecurityAlertLevel(str, Enum):
    LOW = "کم"
    MEDIUM = "متوسط"
    HIGH = "بالا"
    CRITICAL = "بحرانی"

class EncryptionAlgorithm(str, Enum):
    AES_256 = "AES-256"
    RSA_2048 = "RSA-2048"
    ECC = "ECC"
    SHA_256 = "SHA-256"

class AccessControlType(str, Enum):
    ROLE_BASED = "بر پایه نقش"
    ATTRIBUTE_BASED = "بر پایه ویژگی"
    POLICY_BASED = "بر پایه سیاست"
    CONTEXT_BASED = "بر پایه زمینه"

class AuditAction(str, Enum):
    CREATE = "ایجاد"
    READ = "خواندن"
    UPDATE = "به‌روزرسانی"
    DELETE = "حذف"
    EXECUTE = "اجرا"
    EXPORT = "صادرات"
    IMPORT = "واردات"
    LOGIN = "ورود"
    LOGOUT = "خروج"

# User Session schemas
class UserSessionBase(BaseModel):
    device_info: Optional[Dict[str, Any]] = None
    ip_address: str = Field(..., min_length=1, max_length=45)
    user_agent: Optional[str] = None
    location: Optional[Dict[str, Any]] = None
    authentication_method: AuthenticationMethod = AuthenticationMethod.PASSWORD
    two_factor_verified: bool = False

class UserSessionCreate(UserSessionBase):
    user_id: int
    session_token: str = Field(..., min_length=1, max_length=500)
    refresh_token: Optional[str] = None
    expiry_time: datetime

class UserSessionUpdate(BaseModel):
    status: Optional[SessionStatus] = None
    last_activity: Optional[datetime] = None
    expiry_time: Optional[datetime] = None
    is_secure: Optional[bool] = None

class UserSession(UserSessionBase):
    id: int
    user_id: int
    session_token: str
    refresh_token: Optional[str] = None
    status: SessionStatus
    login_time: datetime
    last_activity: datetime
    expiry_time: datetime
    is_secure: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserSessionWithDetails(UserSession):
    user: Optional[Dict[str, Any]] = None

# Security Event schemas
class SecurityEventBase(BaseModel):
    event_type: SecurityEventType
    severity: SecurityAlertLevel = SecurityAlertLevel.LOW
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    location: Optional[Dict[str, Any]] = None
    resource: Optional[str] = None
    action: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    is_suspicious: bool = False
    risk_score: float = 0.0
    response_taken: Optional[str] = None
    notes: Optional[str] = None

class SecurityEventCreate(SecurityEventBase):
    user_id: Optional[int] = None
    session_id: Optional[int] = None

class SecurityEventUpdate(BaseModel):
    severity: Optional[SecurityAlertLevel] = None
    is_suspicious: Optional[bool] = None
    risk_score: Optional[float] = None
    response_taken: Optional[str] = None
    investigated_by: Optional[int] = None
    investigation_date: Optional[datetime] = None
    notes: Optional[str] = None

class SecurityEvent(SecurityEventBase):
    id: int
    user_id: Optional[int] = None
    session_id: Optional[int] = None
    investigated_by: Optional[int] = None
    investigation_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SecurityEventWithDetails(SecurityEvent):
    user: Optional[Dict[str, Any]] = None
    session: Optional[Dict[str, Any]] = None
    investigator: Optional[Dict[str, Any]] = None

# Security Policy schemas
class SecurityPolicyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    policy_type: str = Field(..., min_length=1, max_length=50)
    rules: Optional[Dict[str, Any]] = None
    priority: int = 1
    effective_date: datetime = Field(default_factory=datetime.utcnow)
    expiry_date: Optional[datetime] = None
    version: str = "1.0"

class SecurityPolicyCreate(SecurityPolicyBase):
    pass

class SecurityPolicyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    policy_type: Optional[str] = Field(None, min_length=1, max_length=50)
    rules: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    version: Optional[str] = None

class SecurityPolicy(SecurityPolicyBase):
    id: int
    is_active: bool
    created_by: int
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SecurityPolicyWithDetails(SecurityPolicy):
    created_by_employee: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None

# Password Policy schemas
class PasswordPolicyBase(BaseModel):
    min_length: int = 8
    max_length: int = 128
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digits: bool = True
    require_special_chars: bool = True
    prevent_common_passwords: bool = True
    prevent_personal_info: bool = True
    max_age_days: int = 90
    history_count: int = 5
    lockout_threshold: int = 5
    lockout_duration_minutes: int = 30
    reset_token_expiry_hours: int = 24
    two_factor_required: bool = False
    two_factor_methods: Optional[Dict[str, Any]] = None

class PasswordPolicyCreate(PasswordPolicyBase):
    pass

class PasswordPolicyUpdate(BaseModel):
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    require_uppercase: Optional[bool] = None
    require_lowercase: Optional[bool] = None
    require_digits: Optional[bool] = None
    require_special_chars: Optional[bool] = None
    prevent_common_passwords: Optional[bool] = None
    prevent_personal_info: Optional[bool] = None
    max_age_days: Optional[int] = None
    history_count: Optional[int] = None
    lockout_threshold: Optional[int] = None
    lockout_duration_minutes: Optional[int] = None
    reset_token_expiry_hours: Optional[int] = None
    two_factor_required: Optional[bool] = None
    two_factor_methods: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class PasswordPolicy(PasswordPolicyBase):
    id: int
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PasswordPolicyWithDetails(PasswordPolicy):
    created_by_employee: Optional[Dict[str, Any]] = None

# Permission schemas
class PermissionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    resource_type: str = Field(..., min_length=1, max_length=50)
    action: str = Field(..., min_length=1, max_length=50)
    scope: str = "global"

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    resource_type: Optional[str] = Field(None, min_length=1, max_length=50)
    action: Optional[str] = Field(None, min_length=1, max_length=50)
    scope: Optional[str] = None
    is_active: Optional[bool] = None

class Permission(PermissionBase):
    id: int
    is_system: bool
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PermissionWithDetails(Permission):
    created_by_employee: Optional[Dict[str, Any]] = None
    roles_count: int = 0
    users_count: int = 0

# Role Permission schemas
class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    conditions: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermissionUpdate(BaseModel):
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    conditions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None

class RolePermission(RolePermissionBase):
    id: int
    is_active: bool
    granted_by: int
    granted_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class RolePermissionWithDetails(RolePermission):
    role: Optional[Dict[str, Any]] = None
    permission: Optional[Dict[str, Any]] = None
    granted_by_employee: Optional[Dict[str, Any]] = None

# User Permission schemas
class UserPermissionBase(BaseModel):
    user_id: int
    permission_id: int
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    conditions: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None

class UserPermissionCreate(UserPermissionBase):
    pass

class UserPermissionUpdate(BaseModel):
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    conditions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None

class UserPermission(UserPermissionBase):
    id: int
    is_active: bool
    granted_by: int
    granted_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class UserPermissionWithDetails(UserPermission):
    user: Optional[Dict[str, Any]] = None
    permission: Optional[Dict[str, Any]] = None
    granted_by_employee: Optional[Dict[str, Any]] = None

# Security Incident schemas
class SecurityIncidentBase(BaseModel):
    incident_id: str = Field(..., min_length=1, max_length=20)
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    severity: SecurityAlertLevel
    incident_type: str = Field(..., min_length=1, max_length=50)
    affected_systems: Optional[Dict[str, Any]] = None
    affected_users: Optional[Dict[str, Any]] = None
    reported_at: Optional[datetime] = None
    resolution: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None
    impact_assessment: Optional[Dict[str, Any]] = None
    lessons_learned: Optional[str] = None
    prevention_measures: Optional[Dict[str, Any]] = None

class SecurityIncidentCreate(SecurityIncidentBase):
    discovered_by: int

class SecurityIncidentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    severity: Optional[SecurityAlertLevel] = None
    status: Optional[str] = None
    incident_type: Optional[str] = Field(None, min_length=1, max_length=50)
    affected_systems: Optional[Dict[str, Any]] = None
    affected_users: Optional[Dict[str, Any]] = None
    reported_at: Optional[datetime] = None
    assigned_to: Optional[int] = None
    assigned_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    resolution: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None
    impact_assessment: Optional[Dict[str, Any]] = None
    lessons_learned: Optional[str] = None
    prevention_measures: Optional[Dict[str, Any]] = None

class SecurityIncident(SecurityIncidentBase):
    id: int
    status: str
    discovered_by: int
    discovered_at: datetime
    assigned_to: Optional[int] = None
    assigned_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SecurityIncidentWithDetails(SecurityIncident):
    discovered_by_employee: Optional[Dict[str, Any]] = None
    assigned_to_employee: Optional[Dict[str, Any]] = None
    resolved_by_employee: Optional[Dict[str, Any]] = None

# Two Factor Token schemas
class TwoFactorTokenBase(BaseModel):
    token: str = Field(..., min_length=1, max_length=100)
    token_type: str = Field(..., min_length=1, max_length=20)
    secret_key: Optional[str] = None
    backup_codes: Optional[Dict[str, Any]] = None

class TwoFactorTokenCreate(TwoFactorTokenBase):
    user_id: int
    expires_at: Optional[datetime] = None

class TwoFactorTokenUpdate(BaseModel):
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None

class TwoFactorToken(TwoFactorTokenBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    usage_count: int

    class Config:
        from_attributes = True

class TwoFactorTokenWithDetails(TwoFactorToken):
    user: Optional[Dict[str, Any]] = None

# Security Alert schemas
class SecurityAlertBase(BaseModel):
    alert_type: str = Field(..., min_length=1, max_length=50)
    severity: SecurityAlertLevel
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    details: Optional[Dict[str, Any]] = None
    affected_resources: Optional[Dict[str, Any]] = None
    escalation_level: int = 1

class SecurityAlertCreate(SecurityAlertBase):
    triggered_by: Optional[int] = None

class SecurityAlertUpdate(BaseModel):
    severity: Optional[SecurityAlertLevel] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    message: Optional[str] = Field(None, min_length=1)
    details: Optional[Dict[str, Any]] = None
    affected_resources: Optional[Dict[str, Any]] = None
    acknowledged_by: Optional[int] = None
    acknowledged_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    escalation_level: Optional[int] = None
    notification_sent: Optional[bool] = None
    is_active: Optional[bool] = None

class SecurityAlert(SecurityAlertBase):
    id: int
    triggered_by: Optional[int] = None
    triggered_at: datetime
    acknowledged_by: Optional[int] = None
    acknowledged_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    notification_sent: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class SecurityAlertWithDetails(SecurityAlert):
    triggered_by_employee: Optional[Dict[str, Any]] = None
    acknowledged_by_employee: Optional[Dict[str, Any]] = None
    resolved_by_employee: Optional[Dict[str, Any]] = None

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
class SecurityEventSearchFilters(BaseModel):
    event_type: Optional[SecurityEventType] = None
    severity: Optional[SecurityAlertLevel] = None
    user_id: Optional[int] = None
    session_id: Optional[int] = None
    is_suspicious: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    ip_address: Optional[str] = None
    search: Optional[str] = None

class SecurityIncidentSearchFilters(BaseModel):
    severity: Optional[SecurityAlertLevel] = None
    status: Optional[str] = None
    incident_type: Optional[str] = None
    discovered_by: Optional[int] = None
    assigned_to: Optional[int] = None
    resolved_by: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None

class SecurityAlertSearchFilters(BaseModel):
    alert_type: Optional[str] = None
    severity: Optional[SecurityAlertLevel] = None
    triggered_by: Optional[int] = None
    acknowledged_by: Optional[int] = None
    resolved_by: Optional[int] = None
    is_active: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

class PermissionSearchFilters(BaseModel):
    resource_type: Optional[str] = None
    action: Optional[str] = None
    scope: Optional[str] = None
    is_system: Optional[bool] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None

class AccessLogSearchFilters(BaseModel):
    user_id: Optional[int] = None
    session_id: Optional[int] = None
    resource_type: Optional[str] = None
    action: Optional[AuditAction] = None
    method: Optional[str] = None
    response_code: Optional[int] = None
    success: Optional[bool] = None
    ip_address: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

# Authentication schemas
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1)
    remember_me: bool = False
    two_factor_code: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]
    session_id: int

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., min_length=1)

class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=1)
    confirm_password: str = Field(..., min_length=1)

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    token: Optional[str] = None
    new_password: Optional[str] = None

class TwoFactorSetupResponse(BaseModel):
    secret_key: str
    qr_code_url: str
    backup_codes: List[str]

class TwoFactorVerifyRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=10)
    backup_code: Optional[str] = None
```

این پیاده‌سازی کامل مدل‌های امنیتی و دسترسی شامل تمام ویژگی‌های مورد نیاز برای سیستم احراز هویت، مجوزها، و مدیریت امنیت دانشگاهی ایران است.
