# مدل‌های اصلی دانشگاه - Main University Models

## مدل‌های SQLAlchemy برای سیستم دانشگاهی

```python
# app/models/__init__.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float, DECIMAL
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# Enums
class Gender(str, enum.Enum):
    MALE = "مرد"
    FEMALE = "زن"
    OTHER = "سایر"

class MaritalStatus(str, enum.Enum):
    SINGLE = "مجرد"
    MARRIED = "متاهل"
    DIVORCED = "طلاق گرفته"


class DegreeLevel(str, enum.Enum):
    ASSOCIATE = "کاردانی"
    BACHELOR = "کارشناسی"
    MASTER = "کارشناسی ارشد"
    DOCTORATE = "دکتری"
    POST_DOCTORATE = "فوق دکتری"

class EmploymentType(str, enum.Enum):
    FULL_TIME = "تمام وقت"
    PART_TIME = "پاره وقت"
    CONTRACT = "قراردادی"
    TEMPORARY = "موقت"

class StudentStatus(str, enum.Enum):
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    GRADUATED = "فارغ‌التحصیل"
    SUSPENDED = "محروم"
    TRANSFERRED = "انتقال یافته"

class CourseType(str, enum.Enum):
    THEORETICAL = "نظری"
    PRACTICAL = "عملی"
    THEORETICAL_PRACTICAL = "نظری-عملی"
    WORKSHOP = "کارگاه"
    SEMINAR = "سمینار"

class GradeScale(str, enum.Enum):
    FOUR_POINT = "چهار امتیازی"
    HUNDRED_POINT = "صد امتیازی"
    LETTER_GRADE = "حرفی"

# Core Models
class University(Base):
    __tablename__ = 'universities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    type = Column(String(50), nullable=False)  # دولتی، آزاد، پیام نور، etc.
    province = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    established_year = Column(Integer)
    accreditation_status = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    faculties = relationship("Faculty", back_populates="university")
    employees = relationship("Employee", back_populates="university")

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
    email = Column(String(255))
    established_year = Column(Integer)
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
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    head_id = Column(Integer, ForeignKey('employees.id'))
    phone = Column(String(20))
    email = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    faculty = relationship("Faculty", back_populates="departments")
    head = relationship("Employee", foreign_keys=[head_id])
    courses = relationship("Course", back_populates="department")

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    employee_number = Column(String(20), unique=True, nullable=False)
    national_id = Column(String(10), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    marital_status = Column(Enum(MaritalStatus))
    phone = Column(String(20))
    email = Column(String(255), unique=True, nullable=False)
    address = Column(Text)
    hire_date = Column(DateTime, nullable=False)
    employment_type = Column(Enum(EmploymentType), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    position = Column(String(100), nullable=False)
    salary = Column(DECIMAL(15, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="employees")
    department = relationship("Department", foreign_keys=[department_id])
    sessions = relationship("UserSession", back_populates="user")
    passwords = relationship("UserPassword", back_populates="user")
    two_factor_tokens = relationship("TwoFactorToken", back_populates="user")

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_number = Column(String(20), unique=True, nullable=False)
    national_id = Column(String(10), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    phone = Column(String(20))
    email = Column(String(255), unique=True, nullable=False)
    address = Column(Text)
    enrollment_date = Column(DateTime, nullable=False)
    graduation_date = Column(DateTime)
    status = Column(Enum(StudentStatus), default=StudentStatus.ACTIVE)
    gpa = Column(Float)
    total_credits = Column(Integer, default=0)
    major_id = Column(Integer, ForeignKey('departments.id'))
    advisor_id = Column(Integer, ForeignKey('employees.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    major = relationship("Department", foreign_keys=[major_id])
    advisor = relationship("Employee", foreign_keys=[advisor_id])
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    description = Column(Text)
    course_type = Column(Enum(CourseType), nullable=False)
    credits = Column(Integer, nullable=False)
    hours = Column(Integer, nullable=False)
    prerequisites = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    semester = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    grade = Column(String(5))
    grade_points = Column(Float)
    status = Column(String(20), default='enrolled')  # enrolled, completed, dropped, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

# User Management Models
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    name_fa = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    is_system = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    permissions = relationship("RolePermission", back_populates="role")

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    resource_type = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    scope = Column(String(50), default="global")
    is_system = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    roles = relationship("RolePermission", back_populates="permission")
    users = relationship("UserPermission", back_populates="permission")

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
    status = Column(String(20), default='active')
    login_time = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    expiry_time = Column(DateTime, nullable=False)
    is_secure = Column(Boolean, default=False)
    authentication_method = Column(String(50), default='password')
    two_factor_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("Employee", back_populates="sessions")

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

class TwoFactorToken(Base):
    __tablename__ = 'two_factor_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    token = Column(String(100), nullable=False)
    token_type = Column(String(20), nullable=False)
    secret_key = Column(String(100))
    backup_codes = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    last_used_at = Column(DateTime)
    usage_count = Column(Integer, default=0)

    # Relationships
    user = relationship("Employee", back_populates="two_factor_tokens")

# Add missing relationships to Employee
Employee.permissions = relationship("UserPermission", back_populates="user")
```

## Pydantic Schemas برای سیستم دانشگاهی

```python
# app/schemas/__init__.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class Gender(str, Enum):
    MALE = "مرد"
    FEMALE = "زن"
    OTHER = "سایر"

class MaritalStatus(str, Enum):
    SINGLE = "مجرد"
    MARRIED = "متاهل"
    DIVORCED = "طلاق گرفته"
    WIDOWED = "بیوه"

class DegreeLevel(str, Enum):
    ASSOCIATE = "کاردانی"
    BACHELOR = "کارشناسی"
    MASTER = "کارشناسی ارشد"
    DOCTORATE = "دکتری"
    POST_DOCTORATE = "پسادکتری"

class EmploymentType(str, Enum):
    FULL_TIME = "تمام وقت"
    PART_TIME = "پاره وقت"
    CONTRACT = "قراردادی"
    TEMPORARY = "موقت"

class StudentStatus(str, Enum):
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    GRADUATED = "فارغ‌التحصیل"
    SUSPENDED = "محروم"
    TRANSFERRED = "انتقال یافته"

class CourseType(str, Enum):
    THEORETICAL = "نظری"
    PRACTICAL = "عملی"
    THEORETICAL_PRACTICAL = "نظری-عملی"
    WORKSHOP = "کارگاه"
    SEMINAR = "سمینار"

class GradeScale(str, Enum):
    FOUR_POINT = "چهار امتیازی"
    HUNDRED_POINT = "صد امتیازی"
    LETTER_GRADE = "حرفی"

# University schemas
class UniversityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    type: str = Field(..., min_length=1, max_length=50)
    province: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=100)
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    established_year: Optional[int] = None
    accreditation_status: Optional[str] = None

class UniversityCreate(UniversityBase):
    pass

class UniversityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    province: Optional[str] = Field(None, min_length=1, max_length=100)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    established_year: Optional[int] = None
    accreditation_status: Optional[str] = None
    is_active: Optional[bool] = None

class University(UniversityBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UniversityWithDetails(University):
    faculties_count: int = 0
    employees_count: int = 0
    students_count: int = 0

# Faculty schemas
class FacultyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    established_year: Optional[int] = None

class FacultyCreate(FacultyBase):
    university_id: int

class FacultyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    dean_id: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    established_year: Optional[int] = None
    is_active: Optional[bool] = None

class Faculty(FacultyBase):
    id: int
    university_id: int
    dean_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FacultyWithDetails(Faculty):
    university: Optional[Dict[str, Any]] = None
    dean: Optional[Dict[str, Any]] = None
    departments_count: int = 0

# Department schemas
class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class DepartmentCreate(DepartmentBase):
    faculty_id: int

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    head_id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class Department(DepartmentBase):
    id: int
    faculty_id: int
    head_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DepartmentWithDetails(Department):
    faculty: Optional[Dict[str, Any]] = None
    head: Optional[Dict[str, Any]] = None
    courses_count: int = 0
    employees_count: int = 0
    students_count: int = 0

# Employee schemas
class EmployeeBase(BaseModel):
    employee_number: str = Field(..., min_length=1, max_length=20)
    national_id: str = Field(..., min_length=10, max_length=10)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    gender: Gender
    birth_date: datetime
    marital_status: Optional[MaritalStatus] = None
    phone: Optional[str] = None
    email: EmailStr
    address: Optional[str] = None
    hire_date: datetime
    employment_type: EmploymentType
    position: str = Field(..., min_length=1, max_length=100)
    salary: Optional[float] = None

class EmployeeCreate(EmployeeBase):
    university_id: int
    department_id: Optional[int] = None

class EmployeeUpdate(BaseModel):
    employee_number: Optional[str] = Field(None, min_length=1, max_length=20)
    national_id: Optional[str] = Field(None, min_length=10, max_length=10)
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    gender: Optional[Gender] = None
    birth_date: Optional[datetime] = None
    marital_status: Optional[MaritalStatus] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    hire_date: Optional[datetime] = None
    employment_type: Optional[EmploymentType] = None
    department_id: Optional[int] = None
    position: Optional[str] = Field(None, min_length=1, max_length=100)
    salary: Optional[float] = None
    is_active: Optional[bool] = None

class Employee(EmployeeBase):
    id: int
    university_id: int
    department_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EmployeeWithDetails(Employee):
    university: Optional[Dict[str, Any]] = None
    department: Optional[Dict[str, Any]] = None
    age: Optional[int] = None
    years_of_service: Optional[int] = None

# Student schemas
class StudentBase(BaseModel):
    student_number: str = Field(..., min_length=1, max_length=20)
    national_id: str = Field(..., min_length=10, max_length=10)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    gender: Gender
    birth_date: datetime
    phone: Optional[str] = None
    email: EmailStr
    address: Optional[str] = None
    enrollment_date: datetime
    graduation_date: Optional[datetime] = None
    status: StudentStatus = StudentStatus.ACTIVE
    gpa: Optional[float] = None
    total_credits: int = 0

class StudentCreate(StudentBase):
    major_id: Optional[int] = None
    advisor_id: Optional[int] = None

class StudentUpdate(BaseModel):
    student_number: Optional[str] = Field(None, min_length=1, max_length=20)
    national_id: Optional[str] = Field(None, min_length=10, max_length=10)
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    gender: Optional[Gender] = None
    birth_date: Optional[datetime] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    enrollment_date: Optional[datetime] = None
    graduation_date: Optional[datetime] = None
    status: Optional[StudentStatus] = None
    gpa: Optional[float] = None
    total_credits: Optional[int] = None
    major_id: Optional[int] = None
    advisor_id: Optional[int] = None
    is_active: Optional[bool] = None

class Student(StudentBase):
    id: int
    major_id: Optional[int] = None
    advisor_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StudentWithDetails(Student):
    major: Optional[Dict[str, Any]] = None
    advisor: Optional[Dict[str, Any]] = None
    age: Optional[int] = None
    current_semester: Optional[str] = None
    enrolled_courses_count: int = 0

# Course schemas
class CourseBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    course_type: CourseType
    credits: int = Field(..., gt=0)
    hours: int = Field(..., gt=0)
    prerequisites: Optional[Dict[str, Any]] = None

class CourseCreate(CourseBase):
    department_id: int

class CourseUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    course_type: Optional[CourseType] = None
    credits: Optional[int] = Field(None, gt=0)
    hours: Optional[int] = Field(None, gt=0)
    prerequisites: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class Course(CourseBase):
    id: int
    department_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CourseWithDetails(Course):
    department: Optional[Dict[str, Any]] = None
    enrolled_students_count: int = 0
    average_grade: Optional[float] = None

# Enrollment schemas
class EnrollmentBase(BaseModel):
    semester: str = Field(..., min_length=1, max_length=20)
    year: int = Field(..., gt=0)
    enrollment_date: datetime = Field(default_factory=datetime.utcnow)
    grade: Optional[str] = None
    grade_points: Optional[float] = None
    status: str = "enrolled"

class EnrollmentCreate(EnrollmentBase):
    student_id: int
    course_id: int

class EnrollmentUpdate(BaseModel):
    semester: Optional[str] = Field(None, min_length=1, max_length=20)
    year: Optional[int] = Field(None, gt=0)
    enrollment_date: Optional[datetime] = None
    grade: Optional[str] = None
    grade_points: Optional[float] = None
    status: Optional[str] = None

class Enrollment(EnrollmentBase):
    id: int
    student_id: int
    course_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EnrollmentWithDetails(Enrollment):
    student: Optional[Dict[str, Any]] = None
    course: Optional[Dict[str, Any]] = None

# Role schemas
class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    name_fa: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    is_active: Optional[bool] = None

class Role(RoleBase):
    id: int
    is_system: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RoleWithDetails(Role):
    permissions_count: int = 0
    users_count: int = 0

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
class UniversitySearchFilters(BaseModel):
    type: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class FacultySearchFilters(BaseModel):
    university_id: Optional[int] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class DepartmentSearchFilters(BaseModel):
    faculty_id: Optional[int] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class EmployeeSearchFilters(BaseModel):
    university_id: Optional[int] = None
    department_id: Optional[int] = None
    employment_type: Optional[EmploymentType] = None
    gender: Optional[Gender] = None
    is_active: Optional[bool] = None
    hire_date_from: Optional[datetime] = None
    hire_date_to: Optional[datetime] = None
    search: Optional[str] = None

class StudentSearchFilters(BaseModel):
    major_id: Optional[int] = None
    advisor_id: Optional[int] = None
    status: Optional[StudentStatus] = None
    gender: Optional[Gender] = None
    is_active: Optional[bool] = None
    enrollment_date_from: Optional[datetime] = None
    enrollment_date_to: Optional[datetime] = None
    gpa_min: Optional[float] = None
    gpa_max: Optional[float] = None
    search: Optional[str] = None

class CourseSearchFilters(BaseModel):
    department_id: Optional[int] = None
    course_type: Optional[CourseType] = None
    credits: Optional[int] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class EnrollmentSearchFilters(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    semester: Optional[str] = None
    year: Optional[int] = None
    status: Optional[str] = None
    grade: Optional[str] = None
    enrollment_date_from: Optional[datetime] = None
    enrollment_date_to: Optional[datetime] = None

class RoleSearchFilters(BaseModel):
    is_system: Optional[bool] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class PermissionSearchFilters(BaseModel):
    resource_type: Optional[str] = None
    action: Optional[str] = None
    scope: Optional[str] = None
    is_system: Optional[bool] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    search: Optional[str] = None

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
```

این پیاده‌سازی مدل‌های اصلی دانشگاه شامل تمام موجودیت‌های پایه و روابط بین آن‌ها است و پایه‌ای محکم برای توسعه سیستم دانشگاهی فراهم می‌کند.
