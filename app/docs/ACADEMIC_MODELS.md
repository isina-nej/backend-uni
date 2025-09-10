# مدل‌های آموزشی - Academic Models

## مدل‌های SQLAlchemy برای سیستم آموزشی

```python
# app/models/academic.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class CourseType(str, enum.Enum):
    THEORETICAL = "نظری"
    PRACTICAL = "عملی"
    THEORETICAL_PRACTICAL = "نظری-عملی"
    SEMINAR = "سمینار"
    WORKSHOP = "کارگاه"
    PROJECT = "پروژه"
    THESIS = "پایان‌نامه"
    INTERNSHIP = "کارآموزی"

class CourseLevel(str, enum.Enum):
    UNDERGRADUATE = "کارشناسی"
    MASTER = "کارشناسی ارشد"
    PHD = "دکتری"
    POSTGRADUATE = "پسادکتری"

class SemesterType(str, enum.Enum):
    FALL = "پاییز"
    SPRING = "بهار"
    SUMMER = "تابستان"

class AssessmentType(str, enum.Enum):
    EXAM = "امتحان"
    QUIZ = "کوییز"
    ASSIGNMENT = "تکلیف"
    PROJECT = "پروژه"
    PRESENTATION = "ارائه"
    PARTICIPATION = "مشارکت"

class CourseStatus(str, enum.Enum):
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    CANCELLED = "لغو شده"
    ARCHIVED = "بایگانی شده"

class ProgramType(str, enum.Enum):
    UNDERGRADUATE = "کارشناسی"
    MASTER = "کارشناسی ارشد"
    PHD = "دکتری"
    ASSOCIATE = "کاردانی"
    PROFESSIONAL_CERTIFICATE = "گواهی حرفه‌ای"
    CONTINUING_EDUCATION = "آموزش مداوم"

class Curriculum(Base):
    __tablename__ = 'curricula'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    program_type = Column(Enum(ProgramType), nullable=False)
    academic_level = Column(String(50), nullable=False)
    total_credits_required = Column(Float, nullable=False)
    duration_years = Column(Integer, nullable=False)
    description = Column(Text)
    objectives = Column(JSON)
    learning_outcomes = Column(JSON)
    admission_requirements = Column(JSON)
    graduation_requirements = Column(JSON)
    is_active = Column(Boolean, default=True)
    version = Column(String(20), default="1.0")
    effective_date = Column(DateTime, nullable=False)
    review_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="curricula")
    courses = relationship("CurriculumCourse", back_populates="curriculum")

class CurriculumCourse(Base):
    __tablename__ = 'curriculum_courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    curriculum_id = Column(Integer, ForeignKey('curricula.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    semester_number = Column(Integer, nullable=False)
    is_required = Column(Boolean, default=True)
    is_elective = Column(Boolean, default=False)
    prerequisites = Column(JSON)  # List of prerequisite course IDs
    corequisites = Column(JSON)  # List of corequisite course IDs
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    curriculum = relationship("Curriculum", back_populates="courses")
    course = relationship("Course", back_populates="curricula")

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    course_type = Column(Enum(CourseType), nullable=False)
    course_level = Column(Enum(CourseLevel), nullable=False)
    credits = Column(Float, nullable=False)
    theoretical_hours = Column(Integer, default=0)
    practical_hours = Column(Integer, default=0)
    total_hours = Column(Integer, nullable=False)
    description = Column(Text)
    objectives = Column(JSON)
    learning_outcomes = Column(JSON)
    prerequisites = Column(JSON)
    textbooks = Column(JSON)
    references = Column(JSON)
    syllabus = Column(JSON)
    grading_criteria = Column(JSON)
    status = Column(Enum(CourseStatus), default=CourseStatus.ACTIVE)
    language = Column(String(50), default="فارسی")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="courses")
    curricula = relationship("CurriculumCourse", back_populates="course")
    offerings = relationship("CourseOffering", back_populates="course")
    enrollments = relationship("CourseEnrollment", back_populates="course")
    grades = relationship("Grade", back_populates="course")
    assessments = relationship("CourseAssessment", back_populates="course")

class CourseOffering(Base):
    __tablename__ = 'course_offerings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    semester = Column(String(20), nullable=False)  # 4001, 4002, etc.
    academic_year = Column(String(20), nullable=False)  # 1400-1401
    instructor_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    teaching_assistant_id = Column(Integer, ForeignKey('employees.id'))
    max_enrollment = Column(Integer, nullable=False)
    current_enrollment = Column(Integer, default=0)
    classroom = Column(String(100))
    schedule = Column(JSON)  # Weekly schedule
    exam_schedule = Column(JSON)
    status = Column(String(20), default='planned')  # planned, active, completed, cancelled
    enrollment_deadline = Column(DateTime)
    withdrawal_deadline = Column(DateTime)
    materials = Column(JSON)  # Course materials and resources
    announcements = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="offerings")
    instructor = relationship("Employee", foreign_keys=[instructor_id])
    teaching_assistant = relationship("Employee", foreign_keys=[teaching_assistant_id])
    enrollments = relationship("CourseEnrollment", back_populates="offering")

class CourseAssessment(Base):
    __tablename__ = 'course_assessments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    offering_id = Column(Integer, ForeignKey('course_offerings.id'))
    assessment_type = Column(Enum(AssessmentType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    weight_percentage = Column(Float, nullable=False)
    due_date = Column(DateTime)
    total_points = Column(Float)
    grading_rubric = Column(JSON)
    instructions = Column(Text)
    attachments = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="assessments")
    offering = relationship("CourseOffering", back_populates="assessments")
    submissions = relationship("AssessmentSubmission", back_populates="assessment")

class AssessmentSubmission(Base):
    __tablename__ = 'assessment_submissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(Integer, ForeignKey('course_assessments.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    submission_date = Column(DateTime, default=datetime.utcnow)
    submitted_files = Column(JSON)
    text_response = Column(Text)
    grade = Column(Float)
    feedback = Column(Text)
    graded_by = Column(Integer, ForeignKey('employees.id'))
    graded_at = Column(DateTime)
    status = Column(String(20), default='submitted')  # submitted, graded, late
    plagiarism_score = Column(Float)
    originality_report = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    assessment = relationship("CourseAssessment", back_populates="submissions")
    student = relationship("Student", foreign_keys=[student_id])
    graded_by_employee = relationship("Employee", foreign_keys=[graded_by])

class AcademicCalendar(Base):
    __tablename__ = 'academic_calendar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    academic_year = Column(String(20), nullable=False)  # 1400-1401
    semester = Column(String(20), nullable=False)  # 4001, 4002, etc.
    semester_type = Column(Enum(SemesterType), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    registration_start = Column(DateTime)
    registration_end = Column(DateTime)
    classes_start = Column(DateTime)
    classes_end = Column(DateTime)
    exam_start = Column(DateTime)
    exam_end = Column(DateTime)
    holidays = Column(JSON)
    important_dates = Column(JSON)
    is_current = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="academic_calendars")

class AcademicProgram(Base):
    __tablename__ = 'academic_programs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    program_type = Column(Enum(ProgramType), nullable=False)
    degree_awarded = Column(String(100), nullable=False)
    duration_years = Column(Integer, nullable=False)
    total_credits = Column(Float, nullable=False)
    curriculum_id = Column(Integer, ForeignKey('curricula.id'))
    admission_capacity = Column(Integer)
    current_enrollment = Column(Integer, default=0)
    tuition_fee = Column(Float)
    description = Column(Text)
    objectives = Column(JSON)
    career_prospects = Column(JSON)
    accreditation_status = Column(String(100))
    accreditation_body = Column(String(255))
    accreditation_date = Column(DateTime)
    next_accreditation_review = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="academic_programs")
    curriculum = relationship("Curriculum", back_populates="academic_program")

class CourseMaterial(Base):
    __tablename__ = 'course_materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    offering_id = Column(Integer, ForeignKey('course_offerings.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    material_type = Column(String(50), nullable=False)  # lecture, assignment, resource, etc.
    file_path = Column(String(500))
    file_url = Column(String(500))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    week_number = Column(Integer)
    is_required = Column(Boolean, default=False)
    is_downloadable = Column(Boolean, default=True)
    uploaded_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    view_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="materials")
    offering = relationship("CourseOffering", back_populates="materials")
    uploaded_by_employee = relationship("Employee", foreign_keys=[uploaded_by])

class CourseAnnouncement(Base):
    __tablename__ = 'course_announcements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    offering_id = Column(Integer, ForeignKey('course_offerings.id'))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(String(20), default='normal')  # low, normal, high, urgent
    attachments = Column(JSON)
    is_pinned = Column(Boolean, default=False)
    published_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    published_at = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="announcements")
    offering = relationship("CourseOffering", back_populates="announcements")
    published_by_employee = relationship("Employee", foreign_keys=[published_by])

class CourseEvaluation(Base):
    __tablename__ = 'course_evaluations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    offering_id = Column(Integer, ForeignKey('course_offerings.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    evaluation_date = Column(DateTime, default=datetime.utcnow)
    overall_rating = Column(Float)  # 1-5 scale
    content_quality = Column(Float)
    instructor_effectiveness = Column(Float)
    materials_quality = Column(Float)
    assessment_fairness = Column(Float)
    workload_appropriateness = Column(Float)
    learning_outcomes = Column(Float)
    comments = Column(Text)
    suggestions = Column(Text)
    is_anonymous = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="evaluations")
    offering = relationship("CourseOffering", back_populates="evaluations")
    student = relationship("Student", foreign_keys=[student_id])

class AcademicAdvising(Base):
    __tablename__ = 'academic_advising'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    advisor_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    advising_date = Column(DateTime, nullable=False)
    advising_type = Column(String(50), nullable=False)  # academic, career, personal
    topics_discussed = Column(JSON)
    recommendations = Column(JSON)
    action_items = Column(JSON)
    follow_up_date = Column(DateTime)
    notes = Column(Text)
    status = Column(String(20), default='completed')  # scheduled, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", foreign_keys=[student_id])
    advisor = relationship("Employee", foreign_keys=[advisor_id])

class ResearchProject(Base):
    __tablename__ = 'research_projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    abstract = Column(Text)
    keywords = Column(JSON)
    research_field = Column(String(255))
    principal_investigator_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    co_investigators = Column(JSON)  # List of co-investigator employee IDs
    research_center_id = Column(Integer, ForeignKey('research_centers.id'))
    department_id = Column(Integer, ForeignKey('departments.id'))
    funding_source = Column(String(255))
    funding_amount = Column(Float)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    expected_completion = Column(DateTime)
    status = Column(String(20), default='planning')  # planning, active, completed, suspended, cancelled
    progress_percentage = Column(Float, default=0)
    publications = Column(JSON)
    outcomes = Column(JSON)
    budget = Column(JSON)
    milestones = Column(JSON)
    deliverables = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    principal_investigator = relationship("Employee", foreign_keys=[principal_investigator_id])
    research_center = relationship("ResearchCenter", back_populates="projects")
    department = relationship("Department", back_populates="research_projects")

class ThesisDissertation(Base):
    __tablename__ = 'thesis_dissertations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    title_fa = Column(String(500), nullable=False)
    abstract = Column(Text)
    keywords = Column(JSON)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    supervisor_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    co_supervisor_id = Column(Integer, ForeignKey('employees.id'))
    advisor_id = Column(Integer, ForeignKey('employees.id'))
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    thesis_type = Column(String(50), nullable=False)  # thesis, dissertation, project
    submission_date = Column(DateTime)
    defense_date = Column(DateTime)
    grade = Column(String(5))
    status = Column(String(20), default='in_progress')  # in_progress, submitted, defended, approved, rejected
    defense_result = Column(String(20))  # passed, failed, conditional_pass
    revisions_required = Column(Boolean, default=False)
    final_submission_date = Column(DateTime)
    file_path = Column(String(500))
    file_url = Column(String(500))
    examiners = Column(JSON)  # List of examiner employee IDs
    defense_committee = Column(JSON)
    publications = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", foreign_keys=[student_id])
    supervisor = relationship("Employee", foreign_keys=[supervisor_id])
    co_supervisor = relationship("Employee", foreign_keys=[co_supervisor_id])
    advisor = relationship("Employee", foreign_keys=[advisor_id])
    department = relationship("Department", foreign_keys=[department_id])

class AcademicAward(Base):
    __tablename__ = 'academic_awards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    description = Column(Text)
    award_type = Column(String(50), nullable=False)  # academic, research, service, etc.
    recipient_type = Column(String(20), nullable=False)  # student, employee
    recipient_id = Column(Integer, nullable=False)  # Can be student or employee ID
    awarded_date = Column(DateTime, nullable=False)
    academic_year = Column(String(20))
    semester = Column(String(20))
    criteria = Column(JSON)
    value = Column(Float)  # Monetary value if applicable
    certificate_issued = Column(Boolean, default=True)
    certificate_path = Column(String(500))
    awarded_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    awarded_by_employee = relationship("Employee", foreign_keys=[awarded_by])
```

## Pydantic Schemas برای سیستم آموزشی

```python
# app/schemas/academic.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class CourseType(str, Enum):
    THEORETICAL = "نظری"
    PRACTICAL = "عملی"
    THEORETICAL_PRACTICAL = "نظری-عملی"
    SEMINAR = "سمینار"
    WORKSHOP = "کارگاه"
    PROJECT = "پروژه"
    THESIS = "پایان‌نامه"
    INTERNSHIP = "کارآموزی"

class CourseLevel(str, Enum):
    UNDERGRADUATE = "کارشناسی"
    MASTER = "کارشناسی ارشد"
    PHD = "دکتری"
    POSTGRADUATE = "پسادکتری"

class SemesterType(str, Enum):
    FALL = "پاییز"
    SPRING = "بهار"
    SUMMER = "تابستان"

class AssessmentType(str, Enum):
    EXAM = "امتحان"
    QUIZ = "کوییز"
    ASSIGNMENT = "تکلیف"
    PROJECT = "پروژه"
    PRESENTATION = "ارائه"
    PARTICIPATION = "مشارکت"

class CourseStatus(str, Enum):
    ACTIVE = "فعال"
    INACTIVE = "غیرفعال"
    CANCELLED = "لغو شده"
    ARCHIVED = "بایگانی شده"

class ProgramType(str, Enum):
    UNDERGRADUATE = "کارشناسی"
    MASTER = "کارشناسی ارشد"
    PHD = "دکتری"
    ASSOCIATE = "کاردانی"
    PROFESSIONAL_CERTIFICATE = "گواهی حرفه‌ای"
    CONTINUING_EDUCATION = "آموزش مداوم"

# Curriculum schemas
class CurriculumBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    program_type: ProgramType
    academic_level: str = Field(..., min_length=1, max_length=50)
    total_credits_required: float = Field(..., gt=0)
    duration_years: int = Field(..., gt=0)
    description: Optional[str] = None
    objectives: Optional[Dict[str, Any]] = None
    learning_outcomes: Optional[Dict[str, Any]] = None
    admission_requirements: Optional[Dict[str, Any]] = None
    graduation_requirements: Optional[Dict[str, Any]] = None
    version: str = "1.0"
    effective_date: datetime
    review_date: Optional[datetime] = None

class CurriculumCreate(CurriculumBase):
    department_id: int

class CurriculumUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    program_type: Optional[ProgramType] = None
    academic_level: Optional[str] = Field(None, min_length=1, max_length=50)
    total_credits_required: Optional[float] = Field(None, gt=0)
    duration_years: Optional[int] = Field(None, gt=0)
    description: Optional[str] = None
    objectives: Optional[Dict[str, Any]] = None
    learning_outcomes: Optional[Dict[str, Any]] = None
    admission_requirements: Optional[Dict[str, Any]] = None
    graduation_requirements: Optional[Dict[str, Any]] = None
    version: Optional[str] = None
    effective_date: Optional[datetime] = None
    review_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class Curriculum(CurriculumBase):
    id: int
    department_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CurriculumWithDetails(Curriculum):
    department: Optional[Dict[str, Any]] = None
    courses_count: int = 0

# Curriculum Course schemas
class CurriculumCourseBase(BaseModel):
    semester_number: int = Field(..., gt=0)
    is_required: bool = True
    is_elective: bool = False
    prerequisites: Optional[Dict[str, Any]] = None
    corequisites: Optional[Dict[str, Any]] = None

class CurriculumCourseCreate(CurriculumCourseBase):
    curriculum_id: int
    course_id: int

class CurriculumCourseUpdate(BaseModel):
    semester_number: Optional[int] = Field(None, gt=0)
    is_required: Optional[bool] = None
    is_elective: Optional[bool] = None
    prerequisites: Optional[Dict[str, Any]] = None
    corequisites: Optional[Dict[str, Any]] = None

class CurriculumCourse(CurriculumCourseBase):
    id: int
    curriculum_id: int
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CurriculumCourseWithDetails(CurriculumCourse):
    curriculum: Optional[Dict[str, Any]] = None
    course: Optional[Dict[str, Any]] = None

# Course schemas
class CourseBase(BaseModel):
    course_code: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    course_type: CourseType
    course_level: CourseLevel
    credits: float = Field(..., gt=0)
    theoretical_hours: int = 0
    practical_hours: int = 0
    total_hours: int = Field(..., gt=0)
    description: Optional[str] = None
    objectives: Optional[Dict[str, Any]] = None
    learning_outcomes: Optional[Dict[str, Any]] = None
    prerequisites: Optional[Dict[str, Any]] = None
    textbooks: Optional[Dict[str, Any]] = None
    references: Optional[Dict[str, Any]] = None
    syllabus: Optional[Dict[str, Any]] = None
    grading_criteria: Optional[Dict[str, Any]] = None
    language: str = "فارسی"

class CourseCreate(CourseBase):
    department_id: int

class CourseUpdate(BaseModel):
    course_code: Optional[str] = Field(None, min_length=1, max_length=20)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    course_type: Optional[CourseType] = None
    course_level: Optional[CourseLevel] = None
    credits: Optional[float] = Field(None, gt=0)
    theoretical_hours: Optional[int] = None
    practical_hours: Optional[int] = None
    total_hours: Optional[int] = Field(None, gt=0)
    description: Optional[str] = None
    objectives: Optional[Dict[str, Any]] = None
    learning_outcomes: Optional[Dict[str, Any]] = None
    prerequisites: Optional[Dict[str, Any]] = None
    textbooks: Optional[Dict[str, Any]] = None
    references: Optional[Dict[str, Any]] = None
    syllabus: Optional[Dict[str, Any]] = None
    grading_criteria: Optional[Dict[str, Any]] = None
    status: Optional[CourseStatus] = None
    language: Optional[str] = None
    is_active: Optional[bool] = None

class Course(CourseBase):
    id: int
    department_id: int
    status: CourseStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CourseWithDetails(Course):
    department: Optional[Dict[str, Any]] = None
    offerings_count: int = 0
    enrollments_count: int = 0
    average_grade: Optional[float] = None

# Course Offering schemas
class CourseOfferingBase(BaseModel):
    semester: str = Field(..., min_length=1, max_length=20)
    academic_year: str = Field(..., min_length=1, max_length=20)
    max_enrollment: int = Field(..., gt=0)
    classroom: Optional[str] = None
    schedule: Optional[Dict[str, Any]] = None
    exam_schedule: Optional[Dict[str, Any]] = None
    enrollment_deadline: Optional[datetime] = None
    withdrawal_deadline: Optional[datetime] = None
    materials: Optional[Dict[str, Any]] = None
    announcements: Optional[Dict[str, Any]] = None

class CourseOfferingCreate(CourseOfferingBase):
    course_id: int
    instructor_id: int
    teaching_assistant_id: Optional[int] = None

class CourseOfferingUpdate(BaseModel):
    semester: Optional[str] = Field(None, min_length=1, max_length=20)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    instructor_id: Optional[int] = None
    teaching_assistant_id: Optional[int] = None
    max_enrollment: Optional[int] = Field(None, gt=0)
    classroom: Optional[str] = None
    schedule: Optional[Dict[str, Any]] = None
    exam_schedule: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    enrollment_deadline: Optional[datetime] = None
    withdrawal_deadline: Optional[datetime] = None
    materials: Optional[Dict[str, Any]] = None
    announcements: Optional[Dict[str, Any]] = None

class CourseOffering(CourseOfferingBase):
    id: int
    course_id: int
    instructor_id: int
    teaching_assistant_id: Optional[int] = None
    current_enrollment: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CourseOfferingWithDetails(CourseOffering):
    course: Optional[Dict[str, Any]] = None
    instructor: Optional[Dict[str, Any]] = None
    teaching_assistant: Optional[Dict[str, Any]] = None
    enrollments_count: int = 0

# Course Assessment schemas
class CourseAssessmentBase(BaseModel):
    assessment_type: AssessmentType
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    weight_percentage: float = Field(..., ge=0, le=100)
    due_date: Optional[datetime] = None
    total_points: Optional[float] = None
    grading_rubric: Optional[Dict[str, Any]] = None
    instructions: Optional[str] = None
    attachments: Optional[Dict[str, Any]] = None

class CourseAssessmentCreate(CourseAssessmentBase):
    course_id: int
    offering_id: Optional[int] = None

class CourseAssessmentUpdate(BaseModel):
    assessment_type: Optional[AssessmentType] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    weight_percentage: Optional[float] = Field(None, ge=0, le=100)
    due_date: Optional[datetime] = None
    total_points: Optional[float] = None
    grading_rubric: Optional[Dict[str, Any]] = None
    instructions: Optional[str] = None
    attachments: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class CourseAssessment(CourseAssessmentBase):
    id: int
    course_id: int
    offering_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CourseAssessmentWithDetails(CourseAssessment):
    course: Optional[Dict[str, Any]] = None
    offering: Optional[Dict[str, Any]] = None
    submissions_count: int = 0

# Assessment Submission schemas
class AssessmentSubmissionBase(BaseModel):
    submission_date: datetime
    submitted_files: Optional[Dict[str, Any]] = None
    text_response: Optional[str] = None
    grade: Optional[float] = None
    feedback: Optional[str] = None
    status: str = "submitted"
    plagiarism_score: Optional[float] = None
    originality_report: Optional[Dict[str, Any]] = None

class AssessmentSubmissionCreate(AssessmentSubmissionBase):
    assessment_id: int
    student_id: int

class AssessmentSubmissionUpdate(BaseModel):
    submission_date: Optional[datetime] = None
    submitted_files: Optional[Dict[str, Any]] = None
    text_response: Optional[str] = None
    grade: Optional[float] = None
    feedback: Optional[str] = None
    graded_by: Optional[int] = None
    graded_at: Optional[datetime] = None
    status: Optional[str] = None
    plagiarism_score: Optional[float] = None
    originality_report: Optional[Dict[str, Any]] = None

class AssessmentSubmission(AssessmentSubmissionBase):
    id: int
    assessment_id: int
    student_id: int
    graded_by: Optional[int] = None
    graded_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AssessmentSubmissionWithDetails(AssessmentSubmission):
    assessment: Optional[Dict[str, Any]] = None
    student: Optional[Dict[str, Any]] = None
    graded_by_employee: Optional[Dict[str, Any]] = None

# Academic Calendar schemas
class AcademicCalendarBase(BaseModel):
    academic_year: str = Field(..., min_length=1, max_length=20)
    semester: str = Field(..., min_length=1, max_length=20)
    semester_type: SemesterType
    start_date: datetime
    end_date: datetime
    registration_start: Optional[datetime] = None
    registration_end: Optional[datetime] = None
    classes_start: Optional[datetime] = None
    classes_end: Optional[datetime] = None
    exam_start: Optional[datetime] = None
    exam_end: Optional[datetime] = None
    holidays: Optional[Dict[str, Any]] = None
    important_dates: Optional[Dict[str, Any]] = None
    is_current: bool = False

class AcademicCalendarCreate(AcademicCalendarBase):
    university_id: int

class AcademicCalendarUpdate(BaseModel):
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    semester: Optional[str] = Field(None, min_length=1, max_length=20)
    semester_type: Optional[SemesterType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    registration_start: Optional[datetime] = None
    registration_end: Optional[datetime] = None
    classes_start: Optional[datetime] = None
    classes_end: Optional[datetime] = None
    exam_start: Optional[datetime] = None
    exam_end: Optional[datetime] = None
    holidays: Optional[Dict[str, Any]] = None
    important_dates: Optional[Dict[str, Any]] = None
    is_current: Optional[bool] = None

class AcademicCalendar(AcademicCalendarBase):
    id: int
    university_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AcademicCalendarWithDetails(AcademicCalendar):
    university: Optional[Dict[str, Any]] = None

# Academic Program schemas
class AcademicProgramBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    program_type: ProgramType
    degree_awarded: str = Field(..., min_length=1, max_length=100)
    duration_years: int = Field(..., gt=0)
    total_credits: float = Field(..., gt=0)
    admission_capacity: Optional[int] = None
    tuition_fee: Optional[float] = None
    description: Optional[str] = None
    objectives: Optional[Dict[str, Any]] = None
    career_prospects: Optional[Dict[str, Any]] = None
    accreditation_status: Optional[str] = None
    accreditation_body: Optional[str] = None
    accreditation_date: Optional[datetime] = None
    next_accreditation_review: Optional[datetime] = None

class AcademicProgramCreate(AcademicProgramBase):
    department_id: int
    curriculum_id: Optional[int] = None

class AcademicProgramUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    program_type: Optional[ProgramType] = None
    degree_awarded: Optional[str] = Field(None, min_length=1, max_length=100)
    duration_years: Optional[int] = Field(None, gt=0)
    total_credits: Optional[float] = Field(None, gt=0)
    curriculum_id: Optional[int] = None
    admission_capacity: Optional[int] = None
    current_enrollment: Optional[int] = None
    tuition_fee: Optional[float] = None
    description: Optional[str] = None
    objectives: Optional[Dict[str, Any]] = None
    career_prospects: Optional[Dict[str, Any]] = None
    accreditation_status: Optional[str] = None
    accreditation_body: Optional[str] = None
    accreditation_date: Optional[datetime] = None
    next_accreditation_review: Optional[datetime] = None
    is_active: Optional[bool] = None

class AcademicProgram(AcademicProgramBase):
    id: int
    department_id: int
    curriculum_id: Optional[int] = None
    current_enrollment: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AcademicProgramWithDetails(AcademicProgram):
    department: Optional[Dict[str, Any]] = None
    curriculum: Optional[Dict[str, Any]] = None

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
class CurriculumSearchFilters(BaseModel):
    department_id: Optional[int] = None
    program_type: Optional[ProgramType] = None
    academic_level: Optional[str] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class CourseSearchFilters(BaseModel):
    department_id: Optional[int] = None
    course_type: Optional[CourseType] = None
    course_level: Optional[CourseLevel] = None
    status: Optional[CourseStatus] = None
    is_active: Optional[bool] = None
    credits_min: Optional[float] = None
    credits_max: Optional[float] = None
    search: Optional[str] = None

class CourseOfferingSearchFilters(BaseModel):
    course_id: Optional[int] = None
    instructor_id: Optional[int] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None
    status: Optional[str] = None
    enrollment_min: Optional[int] = None
    enrollment_max: Optional[int] = None

class AcademicCalendarSearchFilters(BaseModel):
    university_id: Optional[int] = None
    academic_year: Optional[str] = None
    semester: Optional[str] = None
    semester_type: Optional[SemesterType] = None
    is_current: Optional[bool] = None

class AcademicProgramSearchFilters(BaseModel):
    department_id: Optional[int] = None
    program_type: Optional[ProgramType] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None
```

این پیاده‌سازی کامل مدل‌های آموزشی شامل تمام ویژگی‌های مورد نیاز برای سیستم مدیریت آموزشی دانشگاهی ایران است.
