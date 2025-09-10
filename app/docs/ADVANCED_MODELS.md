# 🏛️ سیستم جامع مدیریت دانشگاهی ایران - معماری پیشرفته

## 📋 نمای کلی سیستم

این سیستم بر اساس ساختار کامل دانشگاه‌های ایران طراحی شده و شامل تمامی سطوح سازمانی، نقش‌ها، دسترسی‌ها و دسته‌بندی‌های موجود در نظام آموزش عالی کشور است.

## 🏗️ معماری سیستم

### لایه‌های اصلی
```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  React/Vue.js + TypeScript                        │    │
│  │  - Admin Dashboard                                 │    │
│  │  - Student Portal                                  │    │
│  │  - Faculty Portal                                  │    │
│  │  - Staff Portal                                    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                   API Gateway Layer                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  FastAPI + Nginx                                   │    │
│  │  - Load Balancing                                   │    │
│  │  - Rate Limiting                                    │    │
│  │  - Authentication Middleware                        │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                 Business Logic Layer                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  FastAPI Services                                 │    │
│  │  - User Management                                 │    │
│  │  - Academic Management                             │    │
│  │  - Financial Management                            │    │
│  │  - Research Management                             │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                 Data Layer                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  CockroachDB (OLTP)                               │    │
│  │  - Distributed SQL Database                        │    │
│  │  - ACID Transactions                               │    │
│  │  - Horizontal Scaling                              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Redis (Cache & Session)                           │    │
│  │  - Session Storage                                 │    │
│  │  - API Response Cache                              │    │
│  │  - Rate Limiting                                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  MinIO (Object Storage)                            │    │
│  │  - Document Storage                                │    │
│  │  - Media Files                                     │    │
│  │  - Backup Storage                                  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                 Streaming & Analytics Layer                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Apache Kafka                                       │    │
│  │  - Event Streaming                                  │    │
│  │  - Message Queue                                    │    │
│  │  - Real-time Analytics                              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  ClickHouse (OLAP)                                 │    │
│  │  - Analytical Queries                               │    │
│  │  - Real-time Reports                                │    │
│  │  - Data Warehousing                                 │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                 Orchestration Layer                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Apache Airflow                                     │    │
│  │  - ETL Pipelines                                    │    │
│  │  - Scheduled Tasks                                  │    │
│  │  - Data Processing                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Kubernetes                                         │    │
│  │  - Container Orchestration                          │    │
│  │  - Auto Scaling                                     │    │
│  │  - Service Discovery                                │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 📊 مدل‌های داده پیشرفته

### 1. ساختار سازمانی (Organizational Structure)

```python
# models/organization.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class UniversityType(enum.Enum):
    STATE = "دولتی"
    AZAD = "آزاد اسلامی"
    PAYAM_NOOR = "پیام نور"
    NON_PROFIT = "غیرانتفاعی"
    MEDICAL_SCIENCES = "علوم پزشکی"
    TECHNICAL = "فنی و حرفه‌ای"
    RESEARCH_INSTITUTE = "پژوهشگاه"

class OrganizationalUnitType(enum.Enum):
    MINISTRY = "وزارت"
    UNIVERSITY = "دانشگاه"
    FACULTY = "دانشکده"
    DEPARTMENT = "گروه آموزشی"
    RESEARCH_CENTER = "پژوهشکده"
    ADMIN_UNIT = "واحد اداری"
    SERVICE_CENTER = "مرکز خدماتی"
    HOSPITAL = "بیمارستان"
    CLINIC = "کلینیک"

class University(Base):
    __tablename__ = 'universities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    type = Column(Enum(UniversityType), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    address = Column(Text)
    website = Column(String(255))
    phone = Column(String(20))
    establishment_year = Column(Integer)
    president_id = Column(Integer, ForeignKey('employees.id'))
    social_media_links = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    president = relationship("Employee", foreign_keys=[president_id])
    faculties = relationship("Faculty", back_populates="university")
    departments = relationship("Department", back_populates="university")
    research_centers = relationship("ResearchCenter", back_populates="university")
    admin_units = relationship("AdministrativeUnit", back_populates="university")
    employees = relationship("Employee", back_populates="university")
    students = relationship("Student", back_populates="university")

class Faculty(Base):
    __tablename__ = 'faculties'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    dean_id = Column(Integer, ForeignKey('employees.id'))
    address = Column(Text)
    phone = Column(String(20))
    website = Column(String(255))
    establishment_year = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="faculties")
    dean = relationship("Employee", foreign_keys=[dean_id])
    departments = relationship("Department", back_populates="faculty")

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    faculty_id = Column(Integer, ForeignKey('faculties.id'), nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    head_id = Column(Integer, ForeignKey('employees.id'))
    field_of_study = Column(String(255))
    degree_levels = Column(JSON)  # ["کارشناسی", "کارشناسی ارشد", "دکتری"]
    capacity = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    faculty = relationship("Faculty", back_populates="departments")
    university = relationship("University", back_populates="departments")
    head = relationship("Employee", foreign_keys=[head_id])
    students = relationship("Student", back_populates="department")
    courses = relationship("Course", back_populates="department")

class ResearchCenter(Base):
    __tablename__ = 'research_centers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    director_id = Column(Integer, ForeignKey('employees.id'))
    research_field = Column(String(255))
    address = Column(Text)
    phone = Column(String(20))
    website = Column(String(255))
    budget = Column(JSON)  # سالانه بودجه
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="research_centers")
    director = relationship("Employee", foreign_keys=[director_id])
    projects = relationship("ResearchProject", back_populates="research_center")

class AdministrativeUnit(Base):
    __tablename__ = 'administrative_units'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    unit_type = Column(Enum(OrganizationalUnitType), nullable=False)
    manager_id = Column(Integer, ForeignKey('employees.id'))
    parent_id = Column(Integer, ForeignKey('administrative_units.id'))
    responsibilities = Column(JSON)
    address = Column(Text)
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="admin_units")
    manager = relationship("Employee", foreign_keys=[manager_id])
    parent = relationship("AdministrativeUnit", remote_side=[id])
    children = relationship("AdministrativeUnit", back_populates="parent")
    employees = relationship("Employee", back_populates="admin_unit")
```

### 2. مدل‌های پرسنلی (Personnel Models)

```python
# models/personnel.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

class EmployeeType(enum.Enum):
    ACADEMIC = "هیأت علمی"
    ADMINISTRATIVE = "اداری"
    TECHNICAL = "فنی"
    SERVICE = "خدماتی"
    MEDICAL = "درمانی"
    RESEARCH = "پژوهشی"

class AcademicRank(enum.Enum):
    INSTRUCTOR = "مربی"
    ASSISTANT_PROFESSOR = "استادیار"
    ASSOCIATE_PROFESSOR = "دانشیار"
    PROFESSOR = "استاد"
    EMERITUS_PROFESSOR = "استاد بازنشسته"
    VISITING_PROFESSOR = "استاد مدعو"

class EmploymentType(enum.Enum):
    PERMANENT = "رسمی"
    CONTRACT = "قراردادی"
    PROJECT = "پروژه‌ای"
    HOURLY = "ساعتی"
    VISITING = "مهمان"
    RETIRED = "بازنشسته"

class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    employee_type = Column(Enum(EmployeeType), nullable=False)
    level = Column(String(50))  # اجرایی، ارشد، میانی، پایه
    authority_level = Column(Integer, default=1)  # 1-5
    base_salary = Column(Float)
    responsibilities = Column(JSON)
    requirements = Column(JSON)
    organizational_unit_id = Column(Integer, ForeignKey('organizational_units.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organizational_unit = relationship("OrganizationalUnit", back_populates="positions")
    employees = relationship("Employee", back_populates="position")

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    national_id = Column(String(10), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    first_name_fa = Column(String(100), nullable=False)
    last_name_fa = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    address = Column(Text)
    birth_date = Column(DateTime)
    gender = Column(Enum('MALE', 'FEMALE', name='gender_enum'))
    avatar = Column(String(500))

    # Employment Info
    employee_type = Column(Enum(EmployeeType), nullable=False)
    position_id = Column(Integer, ForeignKey('positions.id'))
    employment_type = Column(Enum(EmploymentType), nullable=False)
    hire_date = Column(DateTime)
    contract_end_date = Column(DateTime)
    base_salary = Column(Float)
    allowances = Column(JSON)  # فوق‌العاده‌ها
    deductions = Column(JSON)  # کسورات

    # Academic Info (for faculty)
    academic_rank = Column(Enum(AcademicRank))
    field_of_study = Column(String(255))
    education_level = Column(String(100))
    university_of_study = Column(String(255))
    graduation_year = Column(Integer)

    # Organizational Info
    university_id = Column(Integer, ForeignKey('universities.id'))
    faculty_id = Column(Integer, ForeignKey('faculties.id'))
    department_id = Column(Integer, ForeignKey('departments.id'))
    admin_unit_id = Column(Integer, ForeignKey('administrative_units.id'))
    research_center_id = Column(Integer, ForeignKey('research_centers.id'))

    # Status
    is_active = Column(Boolean, default=True)
    status = Column(String(50), default='ACTIVE')  # ACTIVE, INACTIVE, ON_LEAVE, RETIRED
    last_login = Column(DateTime)
    last_login_ip = Column(String(45))

    # Additional Info
    bio = Column(Text)
    skills = Column(JSON)
    languages = Column(JSON)
    certifications = Column(JSON)
    work_experience = Column(JSON)
    emergency_contact = Column(JSON)
    preferences = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    position = relationship("Position", back_populates="employees")
    university = relationship("University", back_populates="employees")
    faculty = relationship("Faculty")
    department = relationship("Department")
    admin_unit = relationship("AdministrativeUnit", back_populates="employees")
    research_center = relationship("ResearchCenter")
    user_positions = relationship("UserPosition", back_populates="employee")
    permissions = relationship("EmployeePermission", back_populates="employee")
    access_logs = relationship("AccessLog", back_populates="employee")

class UserPosition(Base):
    __tablename__ = 'user_positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)
    organizational_unit_id = Column(Integer, ForeignKey('organizational_units.id'))
    is_primary = Column(Boolean, default=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    appointment_letter = Column(String(500))  # مسیر فایل
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="user_positions")
    position = relationship("Position")
    organizational_unit = relationship("OrganizationalUnit")

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    name_fa = Column(String(255), nullable=False)
    codename = Column(String(100), unique=True, nullable=False)
    category = Column(String(100))  # ACADEMIC, ADMINISTRATIVE, FINANCIAL, etc.
    description = Column(Text)
    module = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class EmployeePermission(Base):
    __tablename__ = 'employee_permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)
    organizational_unit_id = Column(Integer, ForeignKey('organizational_units.id'))
    granted_by_id = Column(Integer, ForeignKey('employees.id'))
    granted_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    reason = Column(Text)
    restrictions = Column(JSON)
    is_active = Column(Boolean, default=True)

    # Relationships
    employee = relationship("Employee", back_populates="permissions")
    permission = relationship("Permission")
    organizational_unit = relationship("OrganizationalUnit")
    granted_by = relationship("Employee", foreign_keys=[granted_by_id])

class AccessLog(Base):
    __tablename__ = 'access_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    action = Column(String(100), nullable=False)
    resource = Column(String(255), nullable=False)
    method = Column(String(10))  # GET, POST, PUT, DELETE
    status_code = Column(Integer)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    session_id = Column(String(255))
    request_data = Column(JSON)
    response_data = Column(JSON)
    execution_time = Column(Float)  # milliseconds
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="access_logs")
```

### 3. مدل‌های دانشجویی (Student Models)

```python
# models/students.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

class StudentType(enum.Enum):
    REGULAR = "روزانه"
    EVENING = "شبانه"
    SELF_SUPPORTED = "پردیس خودگردان"
    VIRTUAL = "مجازی"
    PAYAM_NOOR = "پیام نور"
    NON_PROFIT = "غیرانتفاعی"
    AZAD = "آزاد اسلامی"
    INTERNATIONAL = "بین‌المللی"

class AcademicLevel(enum.Enum):
    BACHELOR = "کارشناسی"
    MASTER = "کارشناسی ارشد"
    PHD = "دکتری تخصصی"
    PROFESSIONAL_DOCTORATE = "دکتری حرفه‌ای"
    POSTDOC = "فوق دکتری"

class AcademicStatus(enum.Enum):
    ACTIVE = "فعال"
    ON_LEAVE = "مرخصی تحصیلی"
    CONDITIONAL = "مشروط"
    GUEST = "مهمان"
    TRANSFERRED = "انتقالی"
    GRADUATED = "فارغ‌التحصیل"
    WITHDRAWN = "انصرافی"
    SUSPENDED = "اخراج"

class FinancialStatus(enum.Enum):
    REGULAR = "عادی"
    SCHOLARSHIP = "بورسیه"
    LOAN_RECIPIENT = "وام‌گیرنده"
    TUITION_DISCOUNT = "تخفیف شهریه"
    TUITION_EXEMPT = "معافیت شهریه"

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    national_id = Column(String(10), unique=True, nullable=False)
    student_id = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    first_name_fa = Column(String(100), nullable=False)
    last_name_fa = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    address = Column(Text)
    birth_date = Column(DateTime)
    gender = Column(Enum('MALE', 'FEMALE', name='gender_enum'))
    avatar = Column(String(500))

    # Academic Info
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculties.id'))
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    academic_level = Column(Enum(AcademicLevel), nullable=False)
    student_type = Column(Enum(StudentType), nullable=False)
    entrance_year = Column(Integer, nullable=False)
    expected_graduation_year = Column(Integer)
    field_of_study = Column(String(255))
    major = Column(String(255))
    minor = Column(String(255))
    gpa = Column(Float)
    total_credits = Column(Float, default=0)
    completed_credits = Column(Float, default=0)

    # Status
    academic_status = Column(Enum(AcademicStatus), default=AcademicStatus.ACTIVE)
    financial_status = Column(Enum(FinancialStatus), default=FinancialStatus.REGULAR)
    is_active = Column(Boolean, default=True)

    # Financial Info
    tuition_fee = Column(Float)
    scholarships = Column(JSON)
    loans = Column(JSON)
    payments = Column(JSON)

    # Special Categories
    is_international = Column(Boolean, default=False)
    is_talented = Column(Boolean, default=False)
    is_martyr_family = Column(Boolean, default=False)
    is_disabled = Column(Boolean, default=False)
    is_athlete = Column(Boolean, default=False)
    is_married = Column(Boolean, default=False)
    is_employed = Column(Boolean, default=False)

    # Additional Info
    emergency_contact = Column(JSON)
    medical_info = Column(JSON)
    special_needs = Column(JSON)
    achievements = Column(JSON)
    activities = Column(JSON)
    languages = Column(JSON)
    skills = Column(JSON)

    # System Info
    last_login = Column(DateTime)
    last_login_ip = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="students")
    faculty = relationship("Faculty")
    department = relationship("Department", back_populates="students")
    enrollments = relationship("CourseEnrollment", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    access_logs = relationship("StudentAccessLog", back_populates="student")

class StudentSpecialCategory(Base):
    __tablename__ = 'student_special_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    description = Column(Text)
    benefits = Column(JSON)
    requirements = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class StudentCategoryAssignment(Base):
    __tablename__ = 'student_category_assignments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('student_special_categories.id'), nullable=False)
    assigned_by_id = Column(Integer, ForeignKey('employees.id'))
    assigned_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    notes = Column(Text)
    is_active = Column(Boolean, default=True)

    # Relationships
    student = relationship("Student")
    category = relationship("StudentSpecialCategory")
    assigned_by = relationship("Employee")

class StudentAccessLog(Base):
    __tablename__ = 'student_access_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    action = Column(String(100), nullable=False)
    resource = Column(String(255), nullable=False)
    method = Column(String(10))
    status_code = Column(Integer)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    session_id = Column(String(255))
    request_data = Column(JSON)
    response_data = Column(JSON)
    execution_time = Column(Float)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="access_logs")
```

### 4. مدل‌های آموزشی (Academic Models)

```python
# models/academic.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

class CourseType(enum.Enum):
    THEORETICAL = "نظری"
    PRACTICAL = "عملی"
    THEORETICAL_PRACTICAL = "نظری-عملی"
    WORKSHOP = "کارگاه"
    SEMINAR = "سمینار"
    PROJECT = "پروژه"

class CourseStatus(enum.Enum):
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    CANCELLED = "لغو شده"

class Semester(Base):
    __tablename__ = 'semesters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)  # 1402-01
    name_fa = Column(String(100), nullable=False)  # بهار ۱۴۰۲
    year = Column(Integer, nullable=False)
    season = Column(Enum('SPRING', 'SUMMER', 'FALL', 'WINTER', name='season_enum'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    registration_start = Column(DateTime)
    registration_end = Column(DateTime)
    withdrawal_deadline = Column(DateTime)
    is_active = Column(Boolean, default=False)
    is_current = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    course_type = Column(Enum(CourseType), nullable=False)
    credits = Column(Float, nullable=False)
    hours = Column(Integer, nullable=False)  # تعداد ساعات
    prerequisites = Column(JSON)  # پیش‌نیازها
    description = Column(Text)
    objectives = Column(JSON)
    syllabus = Column(JSON)
    status = Column(Enum(CourseStatus), default=CourseStatus.ACTIVE)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="courses")
    offerings = relationship("CourseOffering", back_populates="course")

class CourseOffering(Base):
    __tablename__ = 'course_offerings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    semester_id = Column(Integer, ForeignKey('semesters.id'), nullable=False)
    instructor_id = Column(Integer, ForeignKey('employees.id'))
    capacity = Column(Integer, nullable=False)
    enrolled_count = Column(Integer, default=0)
    classroom = Column(String(100))
    schedule = Column(JSON)  # زمان‌بندی کلاس
    exam_date = Column(DateTime)
    exam_location = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="offerings")
    semester = relationship("Semester")
    instructor = relationship("Employee")
    enrollments = relationship("CourseEnrollment", back_populates="offering")

class CourseEnrollment(Base):
    __tablename__ = 'course_enrollments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    offering_id = Column(Integer, ForeignKey('course_offerings.id'), nullable=False)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum('ENROLLED', 'DROPPED', 'COMPLETED', 'FAILED', name='enrollment_status'))
    grade = Column(String(5))
    grade_points = Column(Float)
    is_active = Column(Boolean, default=True)

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    offering = relationship("CourseOffering", back_populates="enrollments")

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    semester_id = Column(Integer, ForeignKey('semesters.id'), nullable=False)
    grade = Column(String(5), nullable=False)
    grade_points = Column(Float, nullable=False)
    status = Column(Enum('FINAL', 'MIDTERM', 'PROVISIONAL', name='grade_status'))
    entered_by_id = Column(Integer, ForeignKey('employees.id'))
    entered_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

    # Relationships
    student = relationship("Student", back_populates="grades")
    course = relationship("Course")
    semester = relationship("Semester")
    entered_by = relationship("Employee")
```

این مدل‌های پیشرفته شامل تمامی جنبه‌های ساختار دانشگاهی ایران هستند و برای مقیاس بالا طراحی شده‌اند.
