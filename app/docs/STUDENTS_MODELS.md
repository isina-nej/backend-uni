# مدل‌های دانشجویی - Students Models

## مدل‌های SQLAlchemy برای دانشجویان

```python
# app/models/students.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class StudentType(str, enum.Enum):
    UNDERGRADUATE = "کارشناسی"
    MASTER = "کارشناسی ارشد"
    PHD = "دکتری"
    PHD_BY_RESEARCH = "دکتری پژوهشی"
    PROFESSIONAL_DOCTORATE = "دکترای حرفه‌ای"
    ASSOCIATE = "کاردانی"
    NON_DEGREE = "بدون مدرک"
    EXCHANGE = "تبادلی"
    VISITING = "میهمان"

class AcademicLevel(str, enum.Enum):
    ASSOCIATE = "کاردانی"
    BACHELOR = "کارشناسی"
    MASTER = "کارشناسی ارشد"
    PHD = "دکتری"
    POSTDOC = "پسادکتری"

class StudentStatus(str, enum.Enum):
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    GRADUATED = "فارغ‌التحصیل"
    SUSPENDED = "محرومیت"
    EXPELLED = "اخراج"
    TRANSFERRED = "انتقال"
    DECEASED = "فوت شده"
    WITHDRAWN = "انصراف"

class AdmissionType(str, enum.Enum):
    REGULAR = "معمولی"
    TALENTED = "برگزیده"
    INTERNATIONAL = "بین‌المللی"
    TRANSFER = "انتقالی"
    CONDITIONAL = "مشروط"
    SPECIAL = "ویژه"

class ScholarshipType(str, enum.Enum):
    MERIT = "برگزیده"
    NEED_BASED = "نیازمند"
    ATHLETIC = "ورزشی"
    RESEARCH = "پژوهشی"
    INTERNATIONAL = "بین‌المللی"
    EMPLOYEE_CHILD = "فرزند کارمند"
    DISABLED = "جانباز و ایثارگر"

class StudentCategory(Base):
    __tablename__ = 'student_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    student_type = Column(Enum(StudentType), nullable=False)
    academic_level = Column(Enum(AcademicLevel), nullable=False)
    admission_requirements = Column(JSON)
    tuition_fee = Column(Float)
    duration_years = Column(Integer)
    max_credits_per_semester = Column(Integer)
    min_gpa_required = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    students = relationship("Student", back_populates="category")

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_number = Column(String(20), unique=True, nullable=False)
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
    
    # Academic details
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('student_categories.id'), nullable=False)
    student_type = Column(Enum(StudentType), nullable=False)
    academic_level = Column(Enum(AcademicLevel), nullable=False)
    student_status = Column(Enum(StudentStatus), default=StudentStatus.ACTIVE)
    admission_type = Column(Enum(AdmissionType), nullable=False)
    
    # Academic progress
    admission_date = Column(DateTime, nullable=False)
    expected_graduation_date = Column(DateTime)
    actual_graduation_date = Column(DateTime)
    current_semester = Column(Integer, default=1)
    total_credits_earned = Column(Float, default=0)
    gpa = Column(Float, default=0)
    cgpa = Column(Float, default=0)
    
    # Financial details
    tuition_fee = Column(Float)
    scholarship_type = Column(Enum(ScholarshipType))
    scholarship_amount = Column(Float)
    outstanding_balance = Column(Float, default=0)
    
    # Education background
    high_school_name = Column(String(255))
    high_school_graduation_year = Column(Integer)
    diploma_grade = Column(Float)
    entrance_exam_score = Column(Float)
    previous_degree = Column(String(255))
    previous_university = Column(String(255))
    previous_gpa = Column(Float)
    
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
    university = relationship("University", back_populates="students")
    department = relationship("Department", back_populates="students")
    category = relationship("StudentCategory", back_populates="students")
    academic_records = relationship("AcademicRecord", back_populates="student")
    enrollments = relationship("CourseEnrollment", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    scholarships = relationship("StudentScholarship", back_populates="student")
    documents = relationship("StudentDocument", back_populates="student")
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    updated_by_employee = relationship("Employee", foreign_keys=[updated_by])

class AcademicRecord(Base):
    __tablename__ = 'academic_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    semester = Column(String(20), nullable=False)  # 4001, 4002, etc.
    academic_year = Column(String(20), nullable=False)  # 1400-1401
    semester_gpa = Column(Float)
    semester_credits = Column(Float)
    total_credits = Column(Float)
    cumulative_gpa = Column(Float)
    status = Column(String(20), default='active')  # active, probation, dismissed
    academic_advisor_id = Column(Integer, ForeignKey('employees.id'))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="academic_records")
    academic_advisor = relationship("Employee", foreign_keys=[academic_advisor_id])

class CourseEnrollment(Base):
    __tablename__ = 'course_enrollments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    semester = Column(String(20), nullable=False)
    academic_year = Column(String(20), nullable=False)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='enrolled')  # enrolled, dropped, completed
    drop_date = Column(DateTime)
    drop_reason = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    grade = relationship("Grade", back_populates="enrollment", uselist=False)

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_id = Column(Integer, ForeignKey('course_enrollments.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    semester = Column(String(20), nullable=False)
    academic_year = Column(String(20), nullable=False)
    grade_value = Column(String(5))  # A, B+, B, C+, C, D, F
    grade_point = Column(Float)  # 4.0, 3.5, 3.0, etc.
    credits = Column(Float)
    status = Column(String(20), default='final')  # final, incomplete, withdrawn
    graded_by = Column(Integer, ForeignKey('employees.id'))
    graded_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

    # Relationships
    enrollment = relationship("CourseEnrollment", back_populates="grade")
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")
    graded_by_employee = relationship("Employee", foreign_keys=[graded_by])

class StudentScholarship(Base):
    __tablename__ = 'student_scholarships'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    scholarship_type = Column(Enum(ScholarshipType), nullable=False)
    amount = Column(Float, nullable=False)
    academic_year = Column(String(20), nullable=False)
    semester = Column(String(20), nullable=False)
    awarded_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime)
    conditions = Column(JSON)
    status = Column(String(20), default='active')  # active, suspended, cancelled
    awarded_by = Column(Integer, ForeignKey('employees.id'))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="scholarships")
    awarded_by_employee = relationship("Employee", foreign_keys=[awarded_by])

class StudentDocument(Base):
    __tablename__ = 'student_documents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    document_type = Column(String(100), nullable=False)  # diploma, transcript, passport, etc.
    title = Column(String(255), nullable=False)
    file_path = Column(String(500))
    file_url = Column(String(500))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    uploaded_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_confidential = Column(Boolean, default=False)
    verification_status = Column(String(20), default='pending')  # pending, verified, rejected
    verified_by = Column(Integer, ForeignKey('employees.id'))
    verified_at = Column(DateTime)
    notes = Column(Text)

    # Relationships
    student = relationship("Student", back_populates="documents")
    uploaded_by_employee = relationship("Employee", foreign_keys=[uploaded_by])
    verified_by_employee = relationship("Employee", foreign_keys=[verified_by])

class StudentTransfer(Base):
    __tablename__ = 'student_transfers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    from_university_id = Column(Integer, ForeignKey('universities.id'))
    to_university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    from_department_id = Column(Integer, ForeignKey('departments.id'))
    to_department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    transfer_type = Column(String(50), nullable=False)  # internal, external
    transfer_date = Column(DateTime, nullable=False)
    effective_date = Column(DateTime, nullable=False)
    reason = Column(Text)
    status = Column(String(20), default='pending')  # pending, approved, completed, rejected
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approved_at = Column(DateTime)
    rejection_reason = Column(Text)
    transfer_credits = Column(Float, default=0)
    transfer_gpa = Column(Float)
    documents = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", foreign_keys=[student_id])
    from_university = relationship("University", foreign_keys=[from_university_id])
    to_university = relationship("University", foreign_keys=[to_university_id])
    from_department = relationship("Department", foreign_keys=[from_department_id])
    to_department = relationship("Department", foreign_keys=[to_department_id])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class StudentDisciplinary(Base):
    __tablename__ = 'student_disciplinary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    incident_type = Column(String(100), nullable=False)  # academic, behavioral, etc.
    incident_date = Column(DateTime, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False)  # minor, major, severe
    action_taken = Column(Text)
    sanction_type = Column(String(100))  # warning, suspension, expulsion, etc.
    sanction_duration = Column(String(100))  # days, weeks, semesters
    sanction_start_date = Column(DateTime)
    sanction_end_date = Column(DateTime)
    reported_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    reviewed_by = Column(Integer, ForeignKey('employees.id'))
    status = Column(String(20), default='active')  # active, resolved, appealed
    appeal_date = Column(DateTime)
    appeal_reason = Column(Text)
    appeal_status = Column(String(20))  # pending, approved, rejected
    appeal_reviewed_by = Column(Integer, ForeignKey('employees.id'))
    appeal_reviewed_at = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", foreign_keys=[student_id])
    reported_by_employee = relationship("Employee", foreign_keys=[reported_by])
    reviewed_by_employee = relationship("Employee", foreign_keys=[reviewed_by])
    appeal_reviewed_by_employee = relationship("Employee", foreign_keys=[appeal_reviewed_by])

class StudentAttendance(Base):
    __tablename__ = 'student_attendance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    semester = Column(String(20), nullable=False)
    academic_year = Column(String(20), nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)  # present, absent, late, excused
    minutes_late = Column(Integer, default=0)
    recorded_by = Column(Integer, ForeignKey('employees.id'))
    recorded_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

    # Relationships
    student = relationship("Student", foreign_keys=[student_id])
    course = relationship("Course", foreign_keys=[course_id])
    recorded_by_employee = relationship("Employee", foreign_keys=[recorded_by])

class StudentFinancialAid(Base):
    __tablename__ = 'student_financial_aid'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    aid_type = Column(String(100), nullable=False)  # loan, grant, work_study, etc.
    amount = Column(Float, nullable=False)
    academic_year = Column(String(20), nullable=False)
    semester = Column(String(20), nullable=False)
    awarded_date = Column(DateTime, nullable=False)
    disbursement_date = Column(DateTime)
    status = Column(String(20), default='awarded')  # awarded, disbursed, cancelled
    conditions = Column(JSON)
    repayment_terms = Column(JSON)
    awarded_by = Column(Integer, ForeignKey('employees.id'))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", foreign_keys=[student_id])
    awarded_by_employee = relationship("Employee", foreign_keys=[awarded_by])

class StudentHealthRecord(Base):
    __tablename__ = 'student_health_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    record_date = Column(DateTime, nullable=False)
    record_type = Column(String(100), nullable=False)  # checkup, illness, accident, etc.
    description = Column(Text)
    diagnosis = Column(Text)
    treatment = Column(Text)
    medications = Column(JSON)
    follow_up_date = Column(DateTime)
    physician_name = Column(String(255))
    physician_contact = Column(String(100))
    emergency_contact_used = Column(Boolean, default=False)
    confidential = Column(Boolean, default=False)
    recorded_by = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", foreign_keys=[student_id])
    recorded_by_employee = relationship("Employee", foreign_keys=[recorded_by])
```

## Pydantic Schemas برای دانشجویان

```python
# app/schemas/students.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class StudentType(str, Enum):
    UNDERGRADUATE = "کارشناسی"
    MASTER = "کارشناسی ارشد"
    PHD = "دکتری"
    PHD_BY_RESEARCH = "دکتری پژوهشی"
    PROFESSIONAL_DOCTORATE = "دکترای حرفه‌ای"
    ASSOCIATE = "کاردانی"
    NON_DEGREE = "بدون مدرک"
    EXCHANGE = "تبادلی"
    VISITING = "میهمان"

class AcademicLevel(str, Enum):
    ASSOCIATE = "کاردانی"
    BACHELOR = "کارشناسی"
    MASTER = "کارشناسی ارشد"
    PHD = "دکتری"
    POSTDOC = "پسادکتری"

class StudentStatus(str, Enum):
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    GRADUATED = "فارغ‌التحصیل"
    SUSPENDED = "محرومیت"
    EXPELLED = "اخراج"
    TRANSFERRED = "انتقال"
    DECEASED = "فوت شده"
    WITHDRAWN = "انصراف"

class AdmissionType(str, Enum):
    REGULAR = "معمولی"
    TALENTED = "برگزیده"
    INTERNATIONAL = "بین‌المللی"
    TRANSFER = "انتقالی"
    CONDITIONAL = "مشروط"
    SPECIAL = "ویژه"

class ScholarshipType(str, Enum):
    MERIT = "برگزیده"
    NEED_BASED = "نیازمند"
    ATHLETIC = "ورزشی"
    RESEARCH = "پژوهشی"
    INTERNATIONAL = "بین‌المللی"
    EMPLOYEE_CHILD = "فرزند کارمند"
    DISABLED = "جانباز و ایثارگر"

# Student Category schemas
class StudentCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    student_type: StudentType
    academic_level: AcademicLevel
    admission_requirements: Optional[Dict[str, Any]] = None
    tuition_fee: Optional[float] = None
    duration_years: Optional[int] = None
    max_credits_per_semester: Optional[int] = None
    min_gpa_required: Optional[float] = None

class StudentCategoryCreate(StudentCategoryBase):
    pass

class StudentCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    student_type: Optional[StudentType] = None
    academic_level: Optional[AcademicLevel] = None
    admission_requirements: Optional[Dict[str, Any]] = None
    tuition_fee: Optional[float] = None
    duration_years: Optional[int] = None
    max_credits_per_semester: Optional[int] = None
    min_gpa_required: Optional[float] = None
    is_active: Optional[bool] = None

class StudentCategory(StudentCategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StudentCategoryWithDetails(StudentCategory):
    students_count: int = 0

# Student schemas
class StudentBase(BaseModel):
    student_number: str = Field(..., min_length=1, max_length=20)
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
    student_type: StudentType
    academic_level: AcademicLevel
    admission_type: AdmissionType
    admission_date: datetime
    expected_graduation_date: Optional[datetime] = None
    tuition_fee: Optional[float] = None
    scholarship_type: Optional[ScholarshipType] = None
    scholarship_amount: Optional[float] = None
    high_school_name: Optional[str] = None
    high_school_graduation_year: Optional[int] = None
    diploma_grade: Optional[float] = None
    entrance_exam_score: Optional[float] = None
    previous_degree: Optional[str] = None
    previous_university: Optional[str] = None
    previous_gpa: Optional[float] = None

class StudentCreate(StudentBase):
    university_id: int
    department_id: int
    category_id: int
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)

class StudentUpdate(BaseModel):
    student_number: Optional[str] = Field(None, min_length=1, max_length=20)
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
    category_id: Optional[int] = None
    student_type: Optional[StudentType] = None
    academic_level: Optional[AcademicLevel] = None
    student_status: Optional[StudentStatus] = None
    admission_type: Optional[AdmissionType] = None
    expected_graduation_date: Optional[datetime] = None
    actual_graduation_date: Optional[datetime] = None
    current_semester: Optional[int] = None
    total_credits_earned: Optional[float] = None
    gpa: Optional[float] = None
    cgpa: Optional[float] = None
    tuition_fee: Optional[float] = None
    scholarship_type: Optional[ScholarshipType] = None
    scholarship_amount: Optional[float] = None
    outstanding_balance: Optional[float] = None
    high_school_name: Optional[str] = None
    high_school_graduation_year: Optional[int] = None
    diploma_grade: Optional[float] = None
    entrance_exam_score: Optional[float] = None
    previous_degree: Optional[str] = None
    previous_university: Optional[str] = None
    previous_gpa: Optional[float] = None
    is_active: Optional[bool] = None

class Student(StudentBase):
    id: int
    university_id: int
    department_id: int
    category_id: int
    student_status: StudentStatus
    current_semester: int
    total_credits_earned: float
    gpa: float
    cgpa: float
    outstanding_balance: float
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

class StudentWithDetails(Student):
    university: Optional[Dict[str, Any]] = None
    department: Optional[Dict[str, Any]] = None
    category: Optional[Dict[str, Any]] = None
    academic_records_count: int = 0
    current_enrollments_count: int = 0
    total_credits: float = 0
    scholarships_count: int = 0
    documents_count: int = 0

# Academic Record schemas
class AcademicRecordBase(BaseModel):
    semester: str = Field(..., min_length=1, max_length=20)
    academic_year: str = Field(..., min_length=1, max_length=20)
    semester_gpa: Optional[float] = None
    semester_credits: Optional[float] = None
    total_credits: Optional[float] = None
    cumulative_gpa: Optional[float] = None
    status: str = "active"
    notes: Optional[str] = None

class AcademicRecordCreate(AcademicRecordBase):
    student_id: int
    academic_advisor_id: Optional[int] = None

class AcademicRecordUpdate(BaseModel):
    semester: Optional[str] = Field(None, min_length=1, max_length=20)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    semester_gpa: Optional[float] = None
    semester_credits: Optional[float] = None
    total_credits: Optional[float] = None
    cumulative_gpa: Optional[float] = None
    status: Optional[str] = None
    academic_advisor_id: Optional[int] = None
    notes: Optional[str] = None

class AcademicRecord(AcademicRecordBase):
    id: int
    student_id: int
    academic_advisor_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AcademicRecordWithDetails(AcademicRecord):
    student: Optional[Dict[str, Any]] = None
    academic_advisor: Optional[Dict[str, Any]] = None

# Course Enrollment schemas
class CourseEnrollmentBase(BaseModel):
    semester: str = Field(..., min_length=1, max_length=20)
    academic_year: str = Field(..., min_length=1, max_length=20)
    status: str = "enrolled"
    drop_reason: Optional[str] = None

class CourseEnrollmentCreate(CourseEnrollmentBase):
    student_id: int
    course_id: int

class CourseEnrollmentUpdate(BaseModel):
    semester: Optional[str] = Field(None, min_length=1, max_length=20)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    status: Optional[str] = None
    drop_date: Optional[datetime] = None
    drop_reason: Optional[str] = None

class CourseEnrollment(CourseEnrollmentBase):
    id: int
    student_id: int
    course_id: int
    enrollment_date: datetime
    drop_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CourseEnrollmentWithDetails(CourseEnrollment):
    student: Optional[Dict[str, Any]] = None
    course: Optional[Dict[str, Any]] = None
    grade: Optional[Dict[str, Any]] = None

# Grade schemas
class GradeBase(BaseModel):
    semester: str = Field(..., min_length=1, max_length=20)
    academic_year: str = Field(..., min_length=1, max_length=20)
    grade_value: Optional[str] = Field(None, max_length=5)
    grade_point: Optional[float] = None
    credits: Optional[float] = None
    status: str = "final"
    notes: Optional[str] = None

class GradeCreate(GradeBase):
    enrollment_id: int
    student_id: int
    course_id: int

class GradeUpdate(BaseModel):
    semester: Optional[str] = Field(None, min_length=1, max_length=20)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    grade_value: Optional[str] = Field(None, max_length=5)
    grade_point: Optional[float] = None
    credits: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class Grade(GradeBase):
    id: int
    enrollment_id: int
    student_id: int
    course_id: int
    graded_by: Optional[int] = None
    graded_at: datetime

    class Config:
        from_attributes = True

class GradeWithDetails(Grade):
    enrollment: Optional[Dict[str, Any]] = None
    student: Optional[Dict[str, Any]] = None
    course: Optional[Dict[str, Any]] = None
    graded_by_employee: Optional[Dict[str, Any]] = None

# Student Scholarship schemas
class StudentScholarshipBase(BaseModel):
    scholarship_type: ScholarshipType
    amount: float = Field(..., gt=0)
    academic_year: str = Field(..., min_length=1, max_length=20)
    semester: str = Field(..., min_length=1, max_length=20)
    awarded_date: datetime
    expiry_date: Optional[datetime] = None
    conditions: Optional[Dict[str, Any]] = None
    status: str = "active"
    notes: Optional[str] = None

class StudentScholarshipCreate(StudentScholarshipBase):
    student_id: int

class StudentScholarshipUpdate(BaseModel):
    scholarship_type: Optional[ScholarshipType] = None
    amount: Optional[float] = Field(None, gt=0)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    semester: Optional[str] = Field(None, min_length=1, max_length=20)
    awarded_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    conditions: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class StudentScholarship(StudentScholarshipBase):
    id: int
    student_id: int
    awarded_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class StudentScholarshipWithDetails(StudentScholarship):
    student: Optional[Dict[str, Any]] = None
    awarded_by_employee: Optional[Dict[str, Any]] = None

# Student Document schemas
class StudentDocumentBase(BaseModel):
    document_type: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=255)
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_confidential: bool = False
    verification_status: str = "pending"
    notes: Optional[str] = None

class StudentDocumentCreate(StudentDocumentBase):
    student_id: int

class StudentDocumentUpdate(BaseModel):
    document_type: Optional[str] = Field(None, min_length=1, max_length=100)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_confidential: Optional[bool] = None
    verification_status: Optional[str] = None
    notes: Optional[str] = None

class StudentDocument(StudentDocumentBase):
    id: int
    student_id: int
    uploaded_by: int
    uploaded_at: datetime
    verified_by: Optional[int] = None
    verified_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class StudentDocumentWithDetails(StudentDocument):
    student: Optional[Dict[str, Any]] = None
    uploaded_by_employee: Optional[Dict[str, Any]] = None
    verified_by_employee: Optional[Dict[str, Any]] = None

# Student Transfer schemas
class StudentTransferBase(BaseModel):
    transfer_type: str = Field(..., min_length=1, max_length=50)
    transfer_date: datetime
    effective_date: datetime
    reason: Optional[str] = None
    transfer_credits: float = 0
    transfer_gpa: Optional[float] = None
    documents: Optional[Dict[str, Any]] = None

class StudentTransferCreate(StudentTransferBase):
    student_id: int
    from_university_id: Optional[int] = None
    to_university_id: int
    from_department_id: Optional[int] = None
    to_department_id: int

class StudentTransferUpdate(BaseModel):
    transfer_type: Optional[str] = Field(None, min_length=1, max_length=50)
    transfer_date: Optional[datetime] = None
    effective_date: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    rejection_reason: Optional[str] = None
    transfer_credits: Optional[float] = None
    transfer_gpa: Optional[float] = None
    documents: Optional[Dict[str, Any]] = None

class StudentTransfer(StudentTransferBase):
    id: int
    student_id: int
    from_university_id: Optional[int] = None
    to_university_id: int
    from_department_id: Optional[int] = None
    to_department_id: int
    status: str
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class StudentTransferWithDetails(StudentTransfer):
    student: Optional[Dict[str, Any]] = None
    from_university: Optional[Dict[str, Any]] = None
    to_university: Optional[Dict[str, Any]] = None
    from_department: Optional[Dict[str, Any]] = None
    to_department: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None

# Student Disciplinary schemas
class StudentDisciplinaryBase(BaseModel):
    incident_type: str = Field(..., min_length=1, max_length=100)
    incident_date: datetime
    description: str = Field(..., min_length=1)
    severity: str = Field(..., min_length=1, max_length=20)
    action_taken: Optional[str] = None
    sanction_type: Optional[str] = None
    sanction_duration: Optional[str] = None
    sanction_start_date: Optional[datetime] = None
    sanction_end_date: Optional[datetime] = None
    status: str = "active"
    appeal_reason: Optional[str] = None
    notes: Optional[str] = None

class StudentDisciplinaryCreate(StudentDisciplinaryBase):
    student_id: int

class StudentDisciplinaryUpdate(BaseModel):
    incident_type: Optional[str] = Field(None, min_length=1, max_length=100)
    incident_date: Optional[datetime] = None
    description: Optional[str] = Field(None, min_length=1)
    severity: Optional[str] = Field(None, min_length=1, max_length=20)
    action_taken: Optional[str] = None
    sanction_type: Optional[str] = None
    sanction_duration: Optional[str] = None
    sanction_start_date: Optional[datetime] = None
    sanction_end_date: Optional[datetime] = None
    status: Optional[str] = None
    appeal_date: Optional[datetime] = None
    appeal_reason: Optional[str] = None
    appeal_status: Optional[str] = None
    notes: Optional[str] = None

class StudentDisciplinary(StudentDisciplinaryBase):
    id: int
    student_id: int
    reported_by: int
    reviewed_by: Optional[int] = None
    appeal_reviewed_by: Optional[int] = None
    appeal_reviewed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class StudentDisciplinaryWithDetails(StudentDisciplinary):
    student: Optional[Dict[str, Any]] = None
    reported_by_employee: Optional[Dict[str, Any]] = None
    reviewed_by_employee: Optional[Dict[str, Any]] = None
    appeal_reviewed_by_employee: Optional[Dict[str, Any]] = None

# Student Attendance schemas
class StudentAttendanceBase(BaseModel):
    semester: str = Field(..., min_length=1, max_length=20)
    academic_year: str = Field(..., min_length=1, max_length=20)
    date: datetime
    status: str = Field(..., min_length=1, max_length=20)
    minutes_late: int = 0
    notes: Optional[str] = None

class StudentAttendanceCreate(StudentAttendanceBase):
    student_id: int
    course_id: int

class StudentAttendanceUpdate(BaseModel):
    semester: Optional[str] = Field(None, min_length=1, max_length=20)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    date: Optional[datetime] = None
    status: Optional[str] = Field(None, min_length=1, max_length=20)
    minutes_late: Optional[int] = None
    notes: Optional[str] = None

class StudentAttendance(StudentAttendanceBase):
    id: int
    student_id: int
    course_id: int
    recorded_by: Optional[int] = None
    recorded_at: datetime

    class Config:
        from_attributes = True

class StudentAttendanceWithDetails(StudentAttendance):
    student: Optional[Dict[str, Any]] = None
    course: Optional[Dict[str, Any]] = None
    recorded_by_employee: Optional[Dict[str, Any]] = None

# Student Financial Aid schemas
class StudentFinancialAidBase(BaseModel):
    aid_type: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    academic_year: str = Field(..., min_length=1, max_length=20)
    semester: str = Field(..., min_length=1, max_length=20)
    awarded_date: datetime
    disbursement_date: Optional[datetime] = None
    status: str = "awarded"
    conditions: Optional[Dict[str, Any]] = None
    repayment_terms: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class StudentFinancialAidCreate(StudentFinancialAidBase):
    student_id: int

class StudentFinancialAidUpdate(BaseModel):
    aid_type: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    semester: Optional[str] = Field(None, min_length=1, max_length=20)
    awarded_date: Optional[datetime] = None
    disbursement_date: Optional[datetime] = None
    status: Optional[str] = None
    conditions: Optional[Dict[str, Any]] = None
    repayment_terms: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class StudentFinancialAid(StudentFinancialAidBase):
    id: int
    student_id: int
    awarded_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class StudentFinancialAidWithDetails(StudentFinancialAid):
    student: Optional[Dict[str, Any]] = None
    awarded_by_employee: Optional[Dict[str, Any]] = None

# Student Health Record schemas
class StudentHealthRecordBase(BaseModel):
    record_date: datetime
    record_type: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    medications: Optional[Dict[str, Any]] = None
    follow_up_date: Optional[datetime] = None
    physician_name: Optional[str] = None
    physician_contact: Optional[str] = None
    emergency_contact_used: bool = False
    confidential: bool = False

class StudentHealthRecordCreate(StudentHealthRecordBase):
    student_id: int

class StudentHealthRecordUpdate(BaseModel):
    record_date: Optional[datetime] = None
    record_type: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    medications: Optional[Dict[str, Any]] = None
    follow_up_date: Optional[datetime] = None
    physician_name: Optional[str] = None
    physician_contact: Optional[str] = None
    emergency_contact_used: Optional[bool] = None
    confidential: Optional[bool] = None

class StudentHealthRecord(StudentHealthRecordBase):
    id: int
    student_id: int
    recorded_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class StudentHealthRecordWithDetails(StudentHealthRecord):
    student: Optional[Dict[str, Any]] = None
    recorded_by_employee: Optional[Dict[str, Any]] = None

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
class StudentSearchFilters(BaseModel):
    university_id: Optional[int] = None
    department_id: Optional[int] = None
    category_id: Optional[int] = None
    student_type: Optional[StudentType] = None
    academic_level: Optional[AcademicLevel] = None
    student_status: Optional[StudentStatus] = None
    admission_type: Optional[AdmissionType] = None
    admission_date_from: Optional[datetime] = None
    admission_date_to: Optional[datetime] = None
    graduation_date_from: Optional[datetime] = None
    graduation_date_to: Optional[datetime] = None
    gpa_min: Optional[float] = None
    gpa_max: Optional[float] = None
    scholarship_type: Optional[ScholarshipType] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None  # Search in name, email, student_number

class StudentCategorySearchFilters(BaseModel):
    student_type: Optional[StudentType] = None
    academic_level: Optional[AcademicLevel] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class AcademicRecordSearchFilters(BaseModel):
    student_id: Optional[int] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None
    status: Optional[str] = None
    gpa_min: Optional[float] = None
    gpa_max: Optional[float] = None

class CourseEnrollmentSearchFilters(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None
    status: Optional[str] = None

class GradeSearchFilters(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None
    grade_value: Optional[str] = None
    grade_point_min: Optional[float] = None
    grade_point_max: Optional[float] = None
    status: Optional[str] = None
```

این پیاده‌سازی کامل مدل‌های دانشجویی شامل تمام ویژگی‌های مورد نیاز برای سیستم مدیریت دانشجویی دانشگاهی ایران است.
