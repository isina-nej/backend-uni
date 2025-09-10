# مدل‌های پرسنلی - Personnel Models

## مدل‌های SQLAlchemy برای پرسنل دانشگاه

```python
# app/models/personnel.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class EmployeeType(str, enum.Enum):
    ACADEMIC = "آموزشی"
    ADMINISTRATIVE = "اداری"
    TECHNICAL = "فنی"
    SERVICE = "خدماتی"
    MEDICAL = "پزشکی"
    SECURITY = "امنیتی"

class AcademicRank(str, enum.Enum):
    INSTRUCTOR = "مربی"
    ASSISTANT_PROFESSOR = "استادیار"
    ASSOCIATE_PROFESSOR = "دانشیار"
    PROFESSOR = "استاد"
    EMERITUS_PROFESSOR = "استاد بازنشسته"

class EmploymentStatus(str, enum.Enum):
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    SUSPENDED = "معلق"
    TERMINATED = "فسخ شده"
    RETIRED = "بازنشسته"
    DECEASED = "فوت شده"

class ContractType(str, enum.Enum):
    PERMANENT = "رسمی"
    CONTRACTUAL = "قراردادی"
    TEMPORARY = "موقت"
    PART_TIME = "پاره وقت"
    VISITING = "میهمان"

class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    department_id = Column(Integer, ForeignKey('departments.id'))
    organizational_unit_id = Column(Integer, ForeignKey('administrative_units.id'))
    position_type = Column(Enum(EmployeeType), nullable=False)
    academic_rank = Column(Enum(AcademicRank))
    base_salary = Column(Float)
    benefits = Column(JSON)  # مزایا و حقوق
    responsibilities = Column(JSON)
    required_qualifications = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="positions")
    organizational_unit = relationship("AdministrativeUnit", back_populates="positions")
    employees = relationship("Employee", back_populates="position")

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    codename = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    module = Column(String(100))  # ماژول مربوطه (organization, personnel, academic, etc.)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employee_permissions = relationship("EmployeePermission", back_populates="permission")

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_number = Column(String(20), unique=True, nullable=False)
    national_id = Column(String(10), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    first_name_fa = Column(String(100), nullable=False)
    last_name_fa = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    mobile = Column(String(20))
    birth_date = Column(DateTime)
    gender = Column(String(10))
    marital_status = Column(String(20))
    address = Column(Text)
    emergency_contact = Column(JSON)
    
    # Employment details
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)
    admin_unit_id = Column(Integer, ForeignKey('administrative_units.id'))
    employee_type = Column(Enum(EmployeeType), nullable=False)
    employment_status = Column(Enum(EmploymentStatus), default=EmploymentStatus.ACTIVE)
    contract_type = Column(Enum(ContractType), nullable=False)
    academic_rank = Column(Enum(AcademicRank))
    
    # Employment dates
    hire_date = Column(DateTime, nullable=False)
    contract_start_date = Column(DateTime)
    contract_end_date = Column(DateTime)
    termination_date = Column(DateTime)
    
    # Salary and benefits
    base_salary = Column(Float)
    current_salary = Column(Float)
    benefits = Column(JSON)
    deductions = Column(JSON)
    
    # Education and qualifications
    education_level = Column(String(100))
    field_of_study = Column(String(255))
    university_graduated = Column(String(255))
    degrees = Column(JSON)
    certifications = Column(JSON)
    skills = Column(JSON)
    
    # Work experience
    previous_positions = Column(JSON)
    years_of_experience = Column(Integer)
    
    # System access
    username = Column(String(100), unique=True)
    password_hash = Column(String(255))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    
    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('employees.id'))
    updated_by = Column(Integer, ForeignKey('employees.id'))

    # Relationships
    university = relationship("University", back_populates="employees")
    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    admin_unit = relationship("AdministrativeUnit", back_populates="employees")
    permissions = relationship("EmployeePermission", back_populates="employee")
    created_by_employee = relationship("Employee", foreign_keys=[created_by], remote_side=[id])
    updated_by_employee = relationship("Employee", foreign_keys=[updated_by], remote_side=[id])

class EmployeePermission(Base):
    __tablename__ = 'employee_permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)
    granted_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    notes = Column(Text)

    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="permissions")
    permission = relationship("Permission", back_populates="employee_permissions")
    granted_by_employee = relationship("Employee", foreign_keys=[granted_by])

class EmployeeHistory(Base):
    __tablename__ = 'employee_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    change_type = Column(String(50), nullable=False)  # position_change, salary_change, status_change, etc.
    old_value = Column(JSON)
    new_value = Column(JSON)
    change_reason = Column(Text)
    effective_date = Column(DateTime, nullable=False)
    changed_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    changed_by_employee = relationship("Employee", foreign_keys=[changed_by])

class EmployeeDocument(Base):
    __tablename__ = 'employee_documents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    document_type = Column(String(100), nullable=False)  # contract, degree, certification, etc.
    title = Column(String(255), nullable=False)
    file_path = Column(String(500))
    file_url = Column(String(500))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    uploaded_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_confidential = Column(Boolean, default=False)
    notes = Column(Text)

    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    uploaded_by_employee = relationship("Employee", foreign_keys=[uploaded_by])

class EmployeeAttendance(Base):
    __tablename__ = 'employee_attendance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    check_in_time = Column(DateTime)
    check_out_time = Column(DateTime)
    work_hours = Column(Float)
    overtime_hours = Column(Float)
    absence_reason = Column(String(255))
    is_present = Column(Boolean, default=True)
    is_late = Column(Boolean, default=False)
    late_minutes = Column(Integer, default=0)
    recorded_by = Column(Integer, ForeignKey('employees.id'))
    recorded_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    recorded_by_employee = relationship("Employee", foreign_keys=[recorded_by])

class EmployeeLeave(Base):
    __tablename__ = 'employee_leaves'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    leave_type = Column(String(50), nullable=False)  # annual, sick, maternity, etc.
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    days_count = Column(Float, nullable=False)
    reason = Column(Text)
    status = Column(String(20), default='pending')  # pending, approved, rejected
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approved_at = Column(DateTime)
    rejection_reason = Column(Text)
    applied_at = Column(DateTime, default=datetime.utcnow)
    documents = Column(JSON)  # فایل‌های ضمیمه شده

    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class EmployeeEvaluation(Base):
    __tablename__ = 'employee_evaluations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    evaluation_period = Column(String(20), nullable=False)  # monthly, quarterly, annual
    evaluation_date = Column(DateTime, nullable=False)
    evaluator_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    overall_rating = Column(Float)  # 1-5 scale
    categories = Column(JSON)  # ارزیابی در دسته‌های مختلف
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    goals = Column(JSON)
    development_plan = Column(Text)
    comments = Column(Text)
    next_evaluation_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    evaluator = relationship("Employee", foreign_keys=[evaluator_id])

class EmployeeTraining(Base):
    __tablename__ = 'employee_trainings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    training_title = Column(String(255), nullable=False)
    training_type = Column(String(100), nullable=False)  # internal, external, online, etc.
    provider = Column(String(255))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    duration_hours = Column(Float)
    cost = Column(Float)
    certificate_issued = Column(Boolean, default=False)
    certificate_path = Column(String(500))
    status = Column(String(20), default='planned')  # planned, in_progress, completed, cancelled
    evaluation_score = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
```

## Pydantic Schemas برای پرسنل

```python
# app/schemas/personnel.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class EmployeeType(str, Enum):
    ACADEMIC = "آموزشی"
    ADMINISTRATIVE = "اداری"
    TECHNICAL = "فنی"
    SERVICE = "خدماتی"
    MEDICAL = "پزشکی"
    SECURITY = "امنیتی"

class AcademicRank(str, Enum):
    INSTRUCTOR = "مربی"
    ASSISTANT_PROFESSOR = "استادیار"
    ASSOCIATE_PROFESSOR = "دانشیار"
    PROFESSOR = "استاد"
    EMERITUS_PROFESSOR = "استاد بازنشسته"

class EmploymentStatus(str, Enum):
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    SUSPENDED = "معلق"
    TERMINATED = "فسخ شده"
    RETIRED = "بازنشسته"
    DECEASED = "فوت شده"

class ContractType(str, Enum):
    PERMANENT = "رسمی"
    CONTRACTUAL = "قراردادی"
    TEMPORARY = "موقت"
    PART_TIME = "پاره وقت"
    VISITING = "میهمان"

# Position schemas
class PositionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    position_type: EmployeeType
    academic_rank: Optional[AcademicRank] = None
    base_salary: Optional[float] = None
    benefits: Optional[Dict[str, Any]] = None
    responsibilities: Optional[Dict[str, Any]] = None
    required_qualifications: Optional[Dict[str, Any]] = None

class PositionCreate(PositionBase):
    department_id: Optional[int] = None
    organizational_unit_id: Optional[int] = None

class PositionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    department_id: Optional[int] = None
    organizational_unit_id: Optional[int] = None
    position_type: Optional[EmployeeType] = None
    academic_rank: Optional[AcademicRank] = None
    base_salary: Optional[float] = None
    benefits: Optional[Dict[str, Any]] = None
    responsibilities: Optional[Dict[str, Any]] = None
    required_qualifications: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class Position(PositionBase):
    id: int
    department_id: Optional[int] = None
    organizational_unit_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PositionWithDetails(Position):
    department: Optional[Dict[str, Any]] = None
    organizational_unit: Optional[Dict[str, Any]] = None
    employees_count: int = 0

# Permission schemas
class PermissionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    codename: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    module: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    codename: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    module: Optional[str] = None
    is_active: Optional[bool] = None

class Permission(PermissionBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Employee schemas
class EmployeeBase(BaseModel):
    employee_number: str = Field(..., min_length=1, max_length=20)
    national_id: str = Field(..., min_length=10, max_length=10)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    first_name_fa: str = Field(..., min_length=1, max_length=100)
    last_name_fa: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    mobile: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[Dict[str, Any]] = None
    employee_type: EmployeeType
    contract_type: ContractType
    academic_rank: Optional[AcademicRank] = None
    hire_date: datetime
    contract_start_date: Optional[datetime] = None
    contract_end_date: Optional[datetime] = None
    base_salary: Optional[float] = None
    benefits: Optional[Dict[str, Any]] = None
    education_level: Optional[str] = None
    field_of_study: Optional[str] = None
    university_graduated: Optional[str] = None
    degrees: Optional[Dict[str, Any]] = None
    certifications: Optional[Dict[str, Any]] = None
    skills: Optional[Dict[str, Any]] = None
    previous_positions: Optional[Dict[str, Any]] = None
    years_of_experience: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    university_id: int
    position_id: int
    department_id: Optional[int] = None
    admin_unit_id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)

class EmployeeUpdate(BaseModel):
    employee_number: Optional[str] = Field(None, min_length=1, max_length=20)
    national_id: Optional[str] = Field(None, min_length=10, max_length=10)
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    first_name_fa: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name_fa: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[Dict[str, Any]] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    admin_unit_id: Optional[int] = None
    employee_type: Optional[EmployeeType] = None
    employment_status: Optional[EmploymentStatus] = None
    contract_type: Optional[ContractType] = None
    academic_rank: Optional[AcademicRank] = None
    contract_start_date: Optional[datetime] = None
    contract_end_date: Optional[datetime] = None
    termination_date: Optional[datetime] = None
    base_salary: Optional[float] = None
    current_salary: Optional[float] = None
    benefits: Optional[Dict[str, Any]] = None
    deductions: Optional[Dict[str, Any]] = None
    education_level: Optional[str] = None
    field_of_study: Optional[str] = None
    university_graduated: Optional[str] = None
    degrees: Optional[Dict[str, Any]] = None
    certifications: Optional[Dict[str, Any]] = None
    skills: Optional[Dict[str, Any]] = None
    previous_positions: Optional[Dict[str, Any]] = None
    years_of_experience: Optional[int] = None
    is_active: Optional[bool] = None

class Employee(EmployeeBase):
    id: int
    university_id: int
    department_id: Optional[int] = None
    position_id: int
    admin_unit_id: Optional[int] = None
    employment_status: EmploymentStatus
    current_salary: Optional[float] = None
    deductions: Optional[Dict[str, Any]] = None
    username: Optional[str] = None
    is_active: bool
    last_login: Optional[datetime] = None
    login_attempts: int
    locked_until: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        from_attributes = True

class EmployeeWithDetails(Employee):
    university: Optional[Dict[str, Any]] = None
    department: Optional[Dict[str, Any]] = None
    position: Optional[Dict[str, Any]] = None
    admin_unit: Optional[Dict[str, Any]] = None
    permissions: List[Dict[str, Any]] = []
    documents_count: int = 0
    evaluations_count: int = 0
    trainings_count: int = 0

# Employee Permission schemas
class EmployeePermissionBase(BaseModel):
    permission_id: int
    expires_at: Optional[datetime] = None
    notes: Optional[str] = None

class EmployeePermissionCreate(EmployeePermissionBase):
    employee_id: int

class EmployeePermissionUpdate(BaseModel):
    permission_id: Optional[int] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None

class EmployeePermission(EmployeePermissionBase):
    id: int
    employee_id: int
    granted_by: int
    granted_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class EmployeePermissionWithDetails(EmployeePermission):
    employee: Optional[Dict[str, Any]] = None
    permission: Optional[Dict[str, Any]] = None
    granted_by_employee: Optional[Dict[str, Any]] = None

# Employee History schemas
class EmployeeHistoryBase(BaseModel):
    change_type: str = Field(..., min_length=1, max_length=50)
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    change_reason: Optional[str] = None
    effective_date: datetime

class EmployeeHistoryCreate(EmployeeHistoryBase):
    employee_id: int

class EmployeeHistory(EmployeeHistoryBase):
    id: int
    employee_id: int
    changed_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class EmployeeHistoryWithDetails(EmployeeHistory):
    employee: Optional[Dict[str, Any]] = None
    changed_by_employee: Optional[Dict[str, Any]] = None

# Employee Document schemas
class EmployeeDocumentBase(BaseModel):
    document_type: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=255)
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_confidential: bool = False
    notes: Optional[str] = None

class EmployeeDocumentCreate(EmployeeDocumentBase):
    employee_id: int

class EmployeeDocumentUpdate(BaseModel):
    document_type: Optional[str] = Field(None, min_length=1, max_length=100)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_confidential: Optional[bool] = None
    notes: Optional[str] = None

class EmployeeDocument(EmployeeDocumentBase):
    id: int
    employee_id: int
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

class EmployeeDocumentWithDetails(EmployeeDocument):
    employee: Optional[Dict[str, Any]] = None
    uploaded_by_employee: Optional[Dict[str, Any]] = None

# Employee Attendance schemas
class EmployeeAttendanceBase(BaseModel):
    date: datetime
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    work_hours: Optional[float] = None
    overtime_hours: Optional[float] = None
    absence_reason: Optional[str] = None
    is_present: bool = True
    is_late: bool = False
    late_minutes: int = 0
    notes: Optional[str] = None

class EmployeeAttendanceCreate(EmployeeAttendanceBase):
    employee_id: int

class EmployeeAttendanceUpdate(BaseModel):
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    work_hours: Optional[float] = None
    overtime_hours: Optional[float] = None
    absence_reason: Optional[str] = None
    is_present: Optional[bool] = None
    is_late: Optional[bool] = None
    late_minutes: Optional[int] = None
    notes: Optional[str] = None

class EmployeeAttendance(EmployeeAttendanceBase):
    id: int
    employee_id: int
    recorded_by: Optional[int] = None
    recorded_at: datetime

    class Config:
        from_attributes = True

class EmployeeAttendanceWithDetails(EmployeeAttendance):
    employee: Optional[Dict[str, Any]] = None
    recorded_by_employee: Optional[Dict[str, Any]] = None

# Employee Leave schemas
class EmployeeLeaveBase(BaseModel):
    leave_type: str = Field(..., min_length=1, max_length=50)
    start_date: datetime
    end_date: datetime
    days_count: float = Field(..., gt=0)
    reason: Optional[str] = None
    documents: Optional[Dict[str, Any]] = None

class EmployeeLeaveCreate(EmployeeLeaveBase):
    employee_id: int

class EmployeeLeaveUpdate(BaseModel):
    leave_type: Optional[str] = Field(None, min_length=1, max_length=50)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    days_count: Optional[float] = Field(None, gt=0)
    reason: Optional[str] = None
    status: Optional[str] = None
    rejection_reason: Optional[str] = None
    documents: Optional[Dict[str, Any]] = None

class EmployeeLeave(EmployeeLeaveBase):
    id: int
    employee_id: int
    status: str
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    applied_at: datetime

    class Config:
        from_attributes = True

class EmployeeLeaveWithDetails(EmployeeLeave):
    employee: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None

# Employee Evaluation schemas
class EmployeeEvaluationBase(BaseModel):
    evaluation_period: str = Field(..., min_length=1, max_length=20)
    evaluation_date: datetime
    evaluator_id: int
    overall_rating: Optional[float] = Field(None, ge=1, le=5)
    categories: Optional[Dict[str, Any]] = None
    strengths: Optional[Dict[str, Any]] = None
    weaknesses: Optional[Dict[str, Any]] = None
    goals: Optional[Dict[str, Any]] = None
    development_plan: Optional[str] = None
    comments: Optional[str] = None
    next_evaluation_date: Optional[datetime] = None

class EmployeeEvaluationCreate(EmployeeEvaluationBase):
    employee_id: int

class EmployeeEvaluationUpdate(BaseModel):
    evaluation_period: Optional[str] = Field(None, min_length=1, max_length=20)
    evaluation_date: Optional[datetime] = None
    evaluator_id: Optional[int] = None
    overall_rating: Optional[float] = Field(None, ge=1, le=5)
    categories: Optional[Dict[str, Any]] = None
    strengths: Optional[Dict[str, Any]] = None
    weaknesses: Optional[Dict[str, Any]] = None
    goals: Optional[Dict[str, Any]] = None
    development_plan: Optional[str] = None
    comments: Optional[str] = None
    next_evaluation_date: Optional[datetime] = None

class EmployeeEvaluation(EmployeeEvaluationBase):
    id: int
    employee_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class EmployeeEvaluationWithDetails(EmployeeEvaluation):
    employee: Optional[Dict[str, Any]] = None
    evaluator: Optional[Dict[str, Any]] = None

# Employee Training schemas
class EmployeeTrainingBase(BaseModel):
    training_title: str = Field(..., min_length=1, max_length=255)
    training_type: str = Field(..., min_length=1, max_length=100)
    provider: Optional[str] = None
    start_date: datetime
    end_date: datetime
    duration_hours: Optional[float] = None
    cost: Optional[float] = None
    certificate_issued: bool = False
    certificate_path: Optional[str] = None
    evaluation_score: Optional[float] = None
    notes: Optional[str] = None

class EmployeeTrainingCreate(EmployeeTrainingBase):
    employee_id: int

class EmployeeTrainingUpdate(BaseModel):
    training_title: Optional[str] = Field(None, min_length=1, max_length=255)
    training_type: Optional[str] = Field(None, min_length=1, max_length=100)
    provider: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    duration_hours: Optional[float] = None
    cost: Optional[float] = None
    certificate_issued: Optional[bool] = None
    certificate_path: Optional[str] = None
    status: Optional[str] = None
    evaluation_score: Optional[float] = None
    notes: Optional[str] = None

class EmployeeTraining(EmployeeTrainingBase):
    id: int
    employee_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class EmployeeTrainingWithDetails(EmployeeTraining):
    employee: Optional[Dict[str, Any]] = None

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
class EmployeeSearchFilters(BaseModel):
    university_id: Optional[int] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    employee_type: Optional[EmployeeType] = None
    employment_status: Optional[EmploymentStatus] = None
    contract_type: Optional[ContractType] = None
    academic_rank: Optional[AcademicRank] = None
    hire_date_from: Optional[datetime] = None
    hire_date_to: Optional[datetime] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None  # Search in name, email, employee_number

class PositionSearchFilters(BaseModel):
    department_id: Optional[int] = None
    organizational_unit_id: Optional[int] = None
    position_type: Optional[EmployeeType] = None
    academic_rank: Optional[AcademicRank] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class PermissionSearchFilters(BaseModel):
    module: Optional[str] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None
```

## API Endpoints برای پرسنل

```python
# app/api/v1/personnel.py
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db_session
from app.schemas.personnel import *
from app.services.personnel_service import PersonnelService
from app.auth.permissions import require_permission
from app.cache.redis_cache import RedisCache
from app.utils.pagination import paginate
from app.tasks.celery_app import celery_app

router = APIRouter()
cache = RedisCache()

# Employee endpoints
@router.post("/employees/", response_model=Employee, dependencies=[Depends(require_permission("create_employee"))])
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db_session)
):
    """Create a new employee"""
    service = PersonnelService(db)
    return await service.create_employee(employee)

@router.get("/employees/", response_model=PaginatedResponse)
async def list_employees(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    filters: EmployeeSearchFilters = Depends(),
    db: Session = Depends(get_db_session)
):
    """List employees with pagination and filtering"""
    cache_key = f"employees:{page}:{size}:{filters.dict()}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return cached_result
    
    service = PersonnelService(db)
    result = await service.list_employees(
        page=page,
        size=size,
        filters=filters
    )
    
    await cache.set(cache_key, result, ttl=300)
    return result

@router.get("/employees/{employee_id}", response_model=EmployeeWithDetails)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db_session)
):
    """Get employee by ID with details"""
    cache_key = f"employee:{employee_id}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return cached_result
    
    service = PersonnelService(db)
    employee = await service.get_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    await cache.set(cache_key, employee, ttl=300)
    return employee

@router.put("/employees/{employee_id}", response_model=Employee, dependencies=[Depends(require_permission("update_employee"))])
async def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    current_employee_id: int = Depends(require_permission("update_employee")),
    db: Session = Depends(get_db_session)
):
    """Update employee"""
    service = PersonnelService(db)
    employee = await service.update_employee(employee_id, employee_update, current_employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    await cache.delete_pattern(f"employee:{employee_id}")
    await cache.delete_pattern("employees:*")
    
    return employee

@router.delete("/employees/{employee_id}", dependencies=[Depends(require_permission("delete_employee"))])
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete employee"""
    service = PersonnelService(db)
    success = await service.delete_employee(employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    await cache.delete_pattern(f"employee:{employee_id}")
    await cache.delete_pattern("employees:*")
    
    return {"message": "Employee deleted successfully"}

# Position endpoints
@router.post("/positions/", response_model=Position, dependencies=[Depends(require_permission("create_position"))])
async def create_position(
    position: PositionCreate,
    db: Session = Depends(get_db_session)
):
    """Create a new position"""
    service = PersonnelService(db)
    return await service.create_position(position)

@router.get("/positions/", response_model=PaginatedResponse)
async def list_positions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    filters: PositionSearchFilters = Depends(),
    db: Session = Depends(get_db_session)
):
    """List positions with pagination and filtering"""
    cache_key = f"positions:{page}:{size}:{filters.dict()}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return cached_result
    
    service = PersonnelService(db)
    result = await service.list_positions(
        page=page,
        size=size,
        filters=filters
    )
    
    await cache.set(cache_key, result, ttl=300)
    return result

@router.get("/positions/{position_id}", response_model=PositionWithDetails)
async def get_position(
    position_id: int,
    db: Session = Depends(get_db_session)
):
    """Get position by ID with details"""
    cache_key = f"position:{position_id}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return cached_result
    
    service = PersonnelService(db)
    position = await service.get_position(position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    
    await cache.set(cache_key, position, ttl=300)
    return position

@router.put("/positions/{position_id}", response_model=Position, dependencies=[Depends(require_permission("update_position"))])
async def update_position(
    position_id: int,
    position_update: PositionUpdate,
    db: Session = Depends(get_db_session)
):
    """Update position"""
    service = PersonnelService(db)
    position = await service.update_position(position_id, position_update)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    
    await cache.delete_pattern(f"position:{position_id}")
    await cache.delete_pattern("positions:*")
    
    return position

@router.delete("/positions/{position_id}", dependencies=[Depends(require_permission("delete_position"))])
async def delete_position(
    position_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete position"""
    service = PersonnelService(db)
    success = await service.delete_position(position_id)
    if not success:
        raise HTTPException(status_code=404, detail="Position not found")
    
    await cache.delete_pattern(f"position:{position_id}")
    await cache.delete_pattern("positions:*")
    
    return {"message": "Position deleted successfully"}

# Permission endpoints
@router.post("/permissions/", response_model=Permission, dependencies=[Depends(require_permission("create_permission"))])
async def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db_session)
):
    """Create a new permission"""
    service = PersonnelService(db)
    return await service.create_permission(permission)

@router.get("/permissions/", response_model=PaginatedResponse)
async def list_permissions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    filters: PermissionSearchFilters = Depends(),
    db: Session = Depends(get_db_session)
):
    """List permissions with pagination and filtering"""
    cache_key = f"permissions:{page}:{size}:{filters.dict()}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return cached_result
    
    service = PersonnelService(db)
    result = await service.list_permissions(
        page=page,
        size=size,
        filters=filters
    )
    
    await cache.set(cache_key, result, ttl=300)
    return result

@router.get("/permissions/{permission_id}", response_model=Permission)
async def get_permission(
    permission_id: int,
    db: Session = Depends(get_db_session)
):
    """Get permission by ID"""
    service = PersonnelService(db)
    permission = await service.get_permission(permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    return permission

@router.put("/permissions/{permission_id}", response_model=Permission, dependencies=[Depends(require_permission("update_permission"))])
async def update_permission(
    permission_id: int,
    permission_update: PermissionUpdate,
    db: Session = Depends(get_db_session)
):
    """Update permission"""
    service = PersonnelService(db)
    permission = await service.update_permission(permission_id, permission_update)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    await cache.delete_pattern(f"permission:{permission_id}")
    await cache.delete_pattern("permissions:*")
    
    return permission

@router.delete("/permissions/{permission_id}", dependencies=[Depends(require_permission("delete_permission"))])
async def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete permission"""
    service = PersonnelService(db)
    success = await service.delete_permission(permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    await cache.delete_pattern(f"permission:{permission_id}")
    await cache.delete_pattern("permissions:*")
    
    return {"message": "Permission deleted successfully"}

# Employee Permission endpoints
@router.post("/employee-permissions/", response_model=EmployeePermission, dependencies=[Depends(require_permission("grant_permission"))])
async def grant_permission(
    permission_data: EmployeePermissionCreate,
    current_employee_id: int = Depends(require_permission("grant_permission")),
    db: Session = Depends(get_db_session)
):
    """Grant permission to employee"""
    service = PersonnelService(db)
    return await service.grant_permission(permission_data, current_employee_id)

@router.get("/employee-permissions/", response_model=PaginatedResponse)
async def list_employee_permissions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    employee_id: Optional[int] = None,
    permission_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db_session)
):
    """List employee permissions with pagination and filtering"""
    cache_key = f"employee_permissions:{page}:{size}:{employee_id}:{permission_id}:{is_active}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return cached_result
    
    service = PersonnelService(db)
    result = await service.list_employee_permissions(
        page=page,
        size=size,
        employee_id=employee_id,
        permission_id=permission_id,
        is_active=is_active
    )
    
    await cache.set(cache_key, result, ttl=300)
    return result

@router.put("/employee-permissions/{permission_id}/revoke", dependencies=[Depends(require_permission("revoke_permission"))])
async def revoke_permission(
    permission_id: int,
    current_employee_id: int = Depends(require_permission("revoke_permission")),
    db: Session = Depends(get_db_session)
):
    """Revoke employee permission"""
    service = PersonnelService(db)
    success = await service.revoke_permission(permission_id, current_employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee permission not found")
    
    await cache.delete_pattern("employee_permissions:*")
    
    return {"message": "Permission revoked successfully"}

# Employee Attendance endpoints
@router.post("/attendance/", response_model=EmployeeAttendance, dependencies=[Depends(require_permission("record_attendance"))])
async def record_attendance(
    attendance: EmployeeAttendanceCreate,
    current_employee_id: int = Depends(require_permission("record_attendance")),
    db: Session = Depends(get_db_session)
):
    """Record employee attendance"""
    service = PersonnelService(db)
    return await service.record_attendance(attendance, current_employee_id)

@router.get("/attendance/", response_model=PaginatedResponse)
async def list_attendance(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    employee_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    is_present: Optional[bool] = None,
    db: Session = Depends(get_db_session)
):
    """List attendance records with pagination and filtering"""
    service = PersonnelService(db)
    result = await service.list_attendance(
        page=page,
        size=size,
        employee_id=employee_id,
        date_from=date_from,
        date_to=date_to,
        is_present=is_present
    )
    
    return result

@router.put("/attendance/{attendance_id}", response_model=EmployeeAttendance, dependencies=[Depends(require_permission("update_attendance"))])
async def update_attendance(
    attendance_id: int,
    attendance_update: EmployeeAttendanceUpdate,
    current_employee_id: int = Depends(require_permission("update_attendance")),
    db: Session = Depends(get_db_session)
):
    """Update attendance record"""
    service = PersonnelService(db)
    attendance = await service.update_attendance(attendance_id, attendance_update, current_employee_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    return attendance

# Employee Leave endpoints
@router.post("/leaves/", response_model=EmployeeLeave, dependencies=[Depends(require_permission("request_leave"))])
async def request_leave(
    leave: EmployeeLeaveCreate,
    db: Session = Depends(get_db_session)
):
    """Request employee leave"""
    service = PersonnelService(db)
    return await service.request_leave(leave)

@router.get("/leaves/", response_model=PaginatedResponse)
async def list_leaves(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    employee_id: Optional[int] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db_session)
):
    """List leave requests with pagination and filtering"""
    service = PersonnelService(db)
    result = await service.list_leaves(
        page=page,
        size=size,
        employee_id=employee_id,
        leave_type=leave_type,
        status=status,
        date_from=date_from,
        date_to=date_to
    )
    
    return result

@router.put("/leaves/{leave_id}/approve", response_model=EmployeeLeave, dependencies=[Depends(require_permission("approve_leave"))])
async def approve_leave(
    leave_id: int,
    current_employee_id: int = Depends(require_permission("approve_leave")),
    db: Session = Depends(get_db_session)
):
    """Approve leave request"""
    service = PersonnelService(db)
    leave = await service.approve_leave(leave_id, current_employee_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    return leave

@router.put("/leaves/{leave_id}/reject", response_model=EmployeeLeave, dependencies=[Depends(require_permission("reject_leave"))])
async def reject_leave(
    leave_id: int,
    rejection_reason: str,
    current_employee_id: int = Depends(require_permission("reject_leave")),
    db: Session = Depends(get_db_session)
):
    """Reject leave request"""
    service = PersonnelService(db)
    leave = await service.reject_leave(leave_id, rejection_reason, current_employee_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    return leave

# Employee Evaluation endpoints
@router.post("/evaluations/", response_model=EmployeeEvaluation, dependencies=[Depends(require_permission("create_evaluation"))])
async def create_evaluation(
    evaluation: EmployeeEvaluationCreate,
    db: Session = Depends(get_db_session)
):
    """Create employee evaluation"""
    service = PersonnelService(db)
    return await service.create_evaluation(evaluation)

@router.get("/evaluations/", response_model=PaginatedResponse)
async def list_evaluations(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    employee_id: Optional[int] = None,
    evaluator_id: Optional[int] = None,
    evaluation_period: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db_session)
):
    """List evaluations with pagination and filtering"""
    service = PersonnelService(db)
    result = await service.list_evaluations(
        page=page,
        size=size,
        employee_id=employee_id,
        evaluator_id=evaluator_id,
        evaluation_period=evaluation_period,
        date_from=date_from,
        date_to=date_to
    )
    
    return result

@router.get("/evaluations/{evaluation_id}", response_model=EmployeeEvaluationWithDetails)
async def get_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db_session)
):
    """Get evaluation by ID with details"""
    service = PersonnelService(db)
    evaluation = await service.get_evaluation(evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    return evaluation

# Employee Training endpoints
@router.post("/trainings/", response_model=EmployeeTraining, dependencies=[Depends(require_permission("create_training"))])
async def create_training(
    training: EmployeeTrainingCreate,
    db: Session = Depends(get_db_session)
):
    """Create employee training"""
    service = PersonnelService(db)
    return await service.create_training(training)

@router.get("/trainings/", response_model=PaginatedResponse)
async def list_trainings(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    employee_id: Optional[int] = None,
    training_type: Optional[str] = None,
    status: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db_session)
):
    """List trainings with pagination and filtering"""
    service = PersonnelService(db)
    result = await service.list_trainings(
        page=page,
        size=size,
        employee_id=employee_id,
        training_type=training_type,
        status=status,
        date_from=date_from,
        date_to=date_to
    )
    
    return result

@router.put("/trainings/{training_id}", response_model=EmployeeTraining, dependencies=[Depends(require_permission("update_training"))])
async def update_training(
    training_id: int,
    training_update: EmployeeTrainingUpdate,
    db: Session = Depends(get_db_session)
):
    """Update training"""
    service = PersonnelService(db)
    training = await service.update_training(training_id, training_update)
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    
    return training

# Employee Document endpoints
@router.post("/documents/", response_model=EmployeeDocument, dependencies=[Depends(require_permission("upload_document"))])
async def upload_document(
    document: EmployeeDocumentCreate,
    file: UploadFile = File(...),
    current_employee_id: int = Depends(require_permission("upload_document")),
    db: Session = Depends(get_db_session)
):
    """Upload employee document"""
    service = PersonnelService(db)
    return await service.upload_document(document, file, current_employee_id)

@router.get("/documents/", response_model=PaginatedResponse)
async def list_documents(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    employee_id: Optional[int] = None,
    document_type: Optional[str] = None,
    is_confidential: Optional[bool] = None,
    db: Session = Depends(get_db_session)
):
    """List documents with pagination and filtering"""
    service = PersonnelService(db)
    result = await service.list_documents(
        page=page,
        size=size,
        employee_id=employee_id,
        document_type=document_type,
        is_confidential=is_confidential
    )
    
    return result

@router.get("/documents/{document_id}/download")
async def download_document(
    document_id: int,
    db: Session = Depends(get_db_session)
):
    """Download employee document"""
    service = PersonnelService(db)
    return await service.download_document(document_id)

# Statistics and reports
@router.get("/statistics/{university_id}")
async def get_personnel_statistics(
    university_id: int,
    db: Session = Depends(get_db_session)
):
    """Get personnel statistics for university"""
    cache_key = f"personnel_stats:{university_id}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return cached_result
    
    service = PersonnelService(db)
    stats = await service.get_personnel_statistics(university_id)
    
    await cache.set(cache_key, stats, ttl=600)  # 10 minutes
    return stats

@router.get("/reports/attendance/{university_id}")
async def get_attendance_report(
    university_id: int,
    month: int,
    year: int,
    db: Session = Depends(get_db_session)
):
    """Generate attendance report"""
    service = PersonnelService(db)
    report = await service.generate_attendance_report(university_id, month, year)
    return report

@router.get("/reports/salary/{university_id}")
async def get_salary_report(
    university_id: int,
    month: int,
    year: int,
    db: Session = Depends(get_db_session)
):
    """Generate salary report"""
    service = PersonnelService(db)
    report = await service.generate_salary_report(university_id, month, year)
    return report

# Bulk operations
@router.post("/bulk-import/employees")
async def bulk_import_employees(
    file: UploadFile = File(...),
    current_employee_id: int = Depends(require_permission("bulk_import_employees")),
    db: Session = Depends(get_db_session)
):
    """Bulk import employees from CSV/Excel"""
    service = PersonnelService(db)
    result = await service.bulk_import_employees(file, current_employee_id)
    return result

@router.post("/bulk-update/salary")
async def bulk_update_salary(
    salary_updates: List[dict],
    current_employee_id: int = Depends(require_permission("bulk_update_salary")),
    db: Session = Depends(get_db_session)
):
    """Bulk update employee salaries"""
    service = PersonnelService(db)
    result = await service.bulk_update_salary(salary_updates, current_employee_id)
    return result
```

## Business Logic Service برای پرسنل

```python
# app/services/personnel_service.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.models.personnel import *
from app.schemas.personnel import *
from app.utils.pagination import paginate
from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PersonnelService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        """Create a new employee"""
        # Check if employee number already exists
        existing = self.db.query(Employee).filter(Employee.employee_number == employee_data.employee_number).first()
        if existing:
            raise ValueError("Employee number already exists")
        
        # Check if national ID already exists
        existing = self.db.query(Employee).filter(Employee.national_id == employee_data.national_id).first()
        if existing:
            raise ValueError("National ID already exists")
        
        # Check if email already exists
        existing = self.db.query(Employee).filter(Employee.email == employee_data.email).first()
        if existing:
            raise ValueError("Email already exists")
        
        # Check if username already exists
        if employee_data.username:
            existing = self.db.query(Employee).filter(Employee.username == employee_data.username).first()
            if existing:
                raise ValueError("Username already exists")
        
        # Hash password
        hashed_password = pwd_context.hash(employee_data.password)
        
        employee = Employee(
            **employee_data.dict(exclude={'password'}),
            password_hash=hashed_password,
            current_salary=employee_data.base_salary
        )
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        
        # Create initial history record
        await self._create_history_record(
            employee.id,
            "employee_created",
            None,
            employee.__dict__,
            "Initial employee creation"
        )
        
        # Send notification
        await self._send_notification("employee.created", employee.dict())
        
        return employee
    
    async def list_employees(
        self,
        page: int = 1,
        size: int = 10,
        filters: EmployeeSearchFilters = None
    ) -> PaginatedResponse:
        """List employees with pagination and filtering"""
        query = self.db.query(Employee)
        
        # Apply filters
        if filters:
            if filters.university_id:
                query = query.filter(Employee.university_id == filters.university_id)
            
            if filters.department_id:
                query = query.filter(Employee.department_id == filters.department_id)
            
            if filters.position_id:
                query = query.filter(Employee.position_id == filters.position_id)
            
            if filters.employee_type:
                query = query.filter(Employee.employee_type == filters.employee_type)
            
            if filters.employment_status:
                query = query.filter(Employee.employment_status == filters.employment_status)
            
            if filters.contract_type:
                query = query.filter(Employee.contract_type == filters.contract_type)
            
            if filters.academic_rank:
                query = query.filter(Employee.academic_rank == filters.academic_rank)
            
            if filters.hire_date_from:
                query = query.filter(Employee.hire_date >= filters.hire_date_from)
            
            if filters.hire_date_to:
                query = query.filter(Employee.hire_date <= filters.hire_date_to)
            
            if filters.is_active is not None:
                query = query.filter(Employee.is_active == filters.is_active)
            
            if filters.search:
                search_term = f"%{filters.search}%"
                query = query.filter(
                    or_(
                        Employee.first_name_fa.ilike(search_term),
                        Employee.last_name_fa.ilike(search_term),
                        Employee.first_name.ilike(search_term),
                        Employee.last_name.ilike(search_term),
                        Employee.email.ilike(search_term),
                        Employee.employee_number.ilike(search_term)
                    )
                )
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        employees = query.offset((page - 1) * size).limit(size).all()
        
        # Convert to response format
        items = [Employee.from_orm(emp) for emp in employees]
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size,
            has_next=page * size < total,
            has_prev=page > 1
        )
    
    async def get_employee(self, employee_id: int) -> Optional[EmployeeWithDetails]:
        """Get employee by ID with details"""
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            return None
        
        # Get related data
        permissions = self.db.query(EmployeePermission).filter(
            and_(
                EmployeePermission.employee_id == employee_id,
                EmployeePermission.is_active == True
            )
        ).all()
        
        documents_count = self.db.query(func.count(EmployeeDocument.id)).filter(
            EmployeeDocument.employee_id == employee_id
        ).scalar()
        
        evaluations_count = self.db.query(func.count(EmployeeEvaluation.id)).filter(
            EmployeeEvaluation.employee_id == employee_id
        ).scalar()
        
        trainings_count = self.db.query(func.count(EmployeeTraining.id)).filter(
            EmployeeTraining.employee_id == employee_id
        ).scalar()
        
        # Get related objects
        university = employee.university
        department = employee.department
        position = employee.position
        admin_unit = employee.admin_unit
        
        return EmployeeWithDetails(
            **employee.__dict__,
            university={
                "id": university.id,
                "name": university.name_fa,
                "code": university.code
            } if university else None,
            department={
                "id": department.id,
                "name": department.name_fa,
                "code": department.code
            } if department else None,
            position={
                "id": position.id,
                "title": position.title_fa,
                "code": position.code
            } if position else None,
            admin_unit={
                "id": admin_unit.id,
                "name": admin_unit.name_fa,
                "code": admin_unit.code
            } if admin_unit else None,
            permissions=[
                {
                    "id": perm.id,
                    "permission": {
                        "id": perm.permission.id,
                        "name": perm.permission.name_fa,
                        "codename": perm.permission.codename
                    },
                    "granted_at": perm.granted_at,
                    "expires_at": perm.expires_at
                } for perm in permissions
            ],
            documents_count=documents_count,
            evaluations_count=evaluations_count,
            trainings_count=trainings_count
        )
    
    async def update_employee(
        self,
        employee_id: int,
        update_data: EmployeeUpdate,
        current_employee_id: int
    ) -> Optional[Employee]:
        """Update employee"""
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            return None
        
        old_values = employee.__dict__.copy()
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            if field == 'password' and value:
                value = pwd_context.hash(value)
                field = 'password_hash'
            setattr(employee, field, value)
        
        employee.updated_at = datetime.utcnow()
        employee.updated_by = current_employee_id
        
        self.db.commit()
        self.db.refresh(employee)
        
        # Create history record
        await self._create_history_record(
            employee.id,
            "employee_updated",
            old_values,
            employee.__dict__,
            "Employee information updated"
        )
        
        return employee
    
    async def delete_employee(self, employee_id: int) -> bool:
        """Delete employee"""
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            return False
        
        # Check for dependencies
        has_dependents = self.db.query(Employee).filter(Employee.created_by == employee_id).first()
        if has_dependents:
            raise ValueError("Cannot delete employee with dependent records")
        
        self.db.delete(employee)
        self.db.commit()
        
        return True
    
    async def create_position(self, position_data: PositionCreate) -> Position:
        """Create a new position"""
        # Check if code already exists
        existing = self.db.query(Position).filter(Position.code == position_data.code).first()
        if existing:
            raise ValueError("Position code already exists")
        
        position = Position(**position_data.dict())
        self.db.add(position)
        self.db.commit()
        self.db.refresh(position)
        
        return position
    
    async def list_positions(
        self,
        page: int = 1,
        size: int = 10,
        filters: PositionSearchFilters = None
    ) -> PaginatedResponse:
        """List positions with pagination and filtering"""
        query = self.db.query(Position)
        
        # Apply filters
        if filters:
            if filters.department_id:
                query = query.filter(Position.department_id == filters.department_id)
            
            if filters.organizational_unit_id:
                query = query.filter(Position.organizational_unit_id == filters.organizational_unit_id)
            
            if filters.position_type:
                query = query.filter(Position.position_type == filters.position_type)
            
            if filters.academic_rank:
                query = query.filter(Position.academic_rank == filters.academic_rank)
            
            if filters.is_active is not None:
                query = query.filter(Position.is_active == filters.is_active)
            
            if filters.search:
                search_term = f"%{filters.search}%"
                query = query.filter(
                    or_(
                        Position.title.ilike(search_term),
                        Position.title_fa.ilike(search_term),
                        Position.code.ilike(search_term)
                    )
                )
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        positions = query.offset((page - 1) * size).limit(size).all()
        
        # Convert to response format
        items = [Position.from_orm(pos) for pos in positions]
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size,
            has_next=page * size < total,
            has_prev=page > 1
        )
    
    async def get_position(self, position_id: int) -> Optional[PositionWithDetails]:
        """Get position by ID with details"""
        position = self.db.query(Position).filter(Position.id == position_id).first()
        if not position:
            return None
        
        # Get related counts
        employees_count = self.db.query(func.count(Employee.id)).filter(
            Employee.position_id == position_id
        ).scalar()
        
        # Get related objects
        department = position.department
        organizational_unit = position.organizational_unit
        
        return PositionWithDetails(
            **position.__dict__,
            department={
                "id": department.id,
                "name": department.name_fa,
                "code": department.code
            } if department else None,
            organizational_unit={
                "id": organizational_unit.id,
                "name": organizational_unit.name_fa,
                "code": organizational_unit.code
            } if organizational_unit else None,
            employees_count=employees_count
        )
    
    async def grant_permission(
        self,
        permission_data: EmployeePermissionCreate,
        current_employee_id: int
    ) -> EmployeePermission:
        """Grant permission to employee"""
        # Check if permission already exists and is active
        existing = self.db.query(EmployeePermission).filter(
            and_(
                EmployeePermission.employee_id == permission_data.employee_id,
                EmployeePermission.permission_id == permission_data.permission_id,
                EmployeePermission.is_active == True
            )
        ).first()
        
        if existing:
            raise ValueError("Employee already has this permission")
        
        permission = EmployeePermission(
            **permission_data.dict(),
            granted_by=current_employee_id
        )
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        
        return permission
    
    async def revoke_permission(
        self,
        permission_id: int,
        current_employee_id: int
    ) -> bool:
        """Revoke employee permission"""
        permission = self.db.query(EmployeePermission).filter(
            EmployeePermission.id == permission_id
        ).first()
        
        if not permission:
            return False
        
        permission.is_active = False
        permission.updated_at = datetime.utcnow()
        
        self.db.commit()
        
        return True
    
    async def record_attendance(
        self,
        attendance_data: EmployeeAttendanceCreate,
        current_employee_id: int
    ) -> EmployeeAttendance:
        """Record employee attendance"""
        # Check if attendance already exists for this date
        existing = self.db.query(EmployeeAttendance).filter(
            and_(
                EmployeeAttendance.employee_id == attendance_data.employee_id,
                func.date(EmployeeAttendance.date) == attendance_data.date.date()
            )
        ).first()
        
        if existing:
            raise ValueError("Attendance already recorded for this date")
        
        attendance = EmployeeAttendance(
            **attendance_data.dict(),
            recorded_by=current_employee_id
        )
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        
        return attendance
    
    async def request_leave(
        self,
        leave_data: EmployeeLeaveCreate
    ) -> EmployeeLeave:
        """Request employee leave"""
        # Validate leave dates
        if leave_data.end_date < leave_data.start_date:
            raise ValueError("End date cannot be before start date")
        
        # Calculate days count
        days_count = (leave_data.end_date - leave_data.start_date).days + 1
        
        leave = EmployeeLeave(
            **leave_data.dict(),
            days_count=days_count
        )
        self.db.add(leave)
        self.db.commit()
        self.db.refresh(leave)
        
        return leave
    
    async def approve_leave(
        self,
        leave_id: int,
        current_employee_id: int
    ) -> Optional[EmployeeLeave]:
        """Approve leave request"""
        leave = self.db.query(EmployeeLeave).filter(EmployeeLeave.id == leave_id).first()
        if not leave:
            return None
        
        if leave.status != 'pending':
            raise ValueError("Leave request is not in pending status")
        
        leave.status = 'approved'
        leave.approved_by = current_employee_id
        leave.approved_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(leave)
        
        return leave
    
    async def reject_leave(
        self,
        leave_id: int,
        rejection_reason: str,
        current_employee_id: int
    ) -> Optional[EmployeeLeave]:
        """Reject leave request"""
        leave = self.db.query(EmployeeLeave).filter(EmployeeLeave.id == leave_id).first()
        if not leave:
            return None
        
        if leave.status != 'pending':
            raise ValueError("Leave request is not in pending status")
        
        leave.status = 'rejected'
        leave.rejection_reason = rejection_reason
        leave.approved_by = current_employee_id
        leave.approved_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(leave)
        
        return leave
    
    async def create_evaluation(
        self,
        evaluation_data: EmployeeEvaluationCreate
    ) -> EmployeeEvaluation:
        """Create employee evaluation"""
        evaluation = EmployeeEvaluation(**evaluation_data.dict())
        self.db.add(evaluation)
        self.db.commit()
        self.db.refresh(evaluation)
        
        return evaluation
    
    async def create_training(
        self,
        training_data: EmployeeTrainingCreate
    ) -> EmployeeTraining:
        """Create employee training"""
        training = EmployeeTraining(**training_data.dict())
        self.db.add(training)
        self.db.commit()
        self.db.refresh(training)
        
        return training
    
    async def get_personnel_statistics(self, university_id: int) -> Dict[str, Any]:
        """Get personnel statistics for university"""
        # Employee statistics by type
        employee_stats = self.db.query(
            Employee.employee_type,
            func.count(Employee.id).label('count')
        ).filter(
            and_(
                Employee.university_id == university_id,
                Employee.is_active == True
            )
        ).group_by(Employee.employee_type).all()
        
        # Employee statistics by status
        status_stats = self.db.query(
            Employee.employment_status,
            func.count(Employee.id).label('count')
        ).filter(
            and_(
                Employee.university_id == university_id,
                Employee.is_active == True
            )
        ).group_by(Employee.employment_status).all()
        
        # Position statistics
        position_stats = self.db.query(
            Position.position_type,
            func.count(Position.id).label('count')
        ).join(Employee, Position.id == Employee.position_id).filter(
            Employee.university_id == university_id
        ).group_by(Position.position_type).all()
        
        # Attendance statistics (current month)
        current_month = datetime.utcnow().replace(day=1)
        next_month = (current_month + timedelta(days=32)).replace(day=1)
        
        attendance_stats = self.db.query(
            func.count(EmployeeAttendance.id).label('total_records'),
            func.sum(EmployeeAttendance.work_hours).label('total_hours'),
            func.avg(EmployeeAttendance.work_hours).label('avg_hours'),
            func.count(EmployeeAttendance.id).filter(EmployeeAttendance.is_late == True).label('late_count')
        ).join(Employee, EmployeeAttendance.employee_id == Employee.id).filter(
            and_(
                Employee.university_id == university_id,
                EmployeeAttendance.date >= current_month,
                EmployeeAttendance.date < next_month
            )
        ).first()
        
        return {
            "employees_by_type": {
                emp_type.value: count for emp_type, count in employee_stats
            },
            "employees_by_status": {
                status.value: count for status, count in status_stats
            },
            "positions_by_type": {
                pos_type.value: count for pos_type, count in position_stats
            },
            "current_month_attendance": {
                "total_records": attendance_stats.total_records or 0,
                "total_hours": float(attendance_stats.total_hours or 0),
                "avg_hours": float(attendance_stats.avg_hours or 0),
                "late_count": attendance_stats.late_count or 0
            }
        }
    
    async def _create_history_record(
        self,
        employee_id: int,
        change_type: str,
        old_value: Dict[str, Any],
        new_value: Dict[str, Any],
        reason: str
    ):
        """Create employee history record"""
        history = EmployeeHistory(
            employee_id=employee_id,
            change_type=change_type,
            old_value=old_value,
            new_value=new_value,
            change_reason=reason,
            effective_date=datetime.utcnow()
        )
        self.db.add(history)
        self.db.commit()
    
    async def _send_notification(self, event_type: str, data: Dict[str, Any]):
        """Send notification for personnel events"""
        # Implementation would send to Kafka/Redis pubsub
        pass
```

این پیاده‌سازی کامل مدل‌های پرسنلی شامل تمام ویژگی‌های مورد نیاز برای سیستم مدیریت پرسنل دانشگاهی ایران است.
