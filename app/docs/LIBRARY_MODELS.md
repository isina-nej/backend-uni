# مدل‌های کتابخانه‌ای و منابع - Library Models

## مدل‌های SQLAlchemy برای سیستم کتابخانه

```python
# app/models/library.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class MaterialType(str, enum.Enum):
    BOOK = "کتاب"
    JOURNAL = "نشریه"
    MAGAZINE = "مجله"
    NEWSPAPER = "روزنامه"
    THESIS = "پایان‌نامه"
    DISSERTATION = "رساله"
    CONFERENCE_PAPER = "مقاله کنفرانس"
    REPORT = "گزارش"
    AUDIOVISUAL = "صوتی تصویری"
    ELECTRONIC_RESOURCE = "منبع الکترونیکی"
    MANUSCRIPT = "نسخه خطی"
    MAP = "نقشه"
    MICROFORM = "میکروفیلم"

class MaterialFormat(str, enum.Enum):
    PRINT = "چاپی"
    DIGITAL = "دیجیتال"
    AUDIO = "صوتی"
    VIDEO = "تصویری"
    MICROFILM = "میکروفیلم"
    CD_DVD = "سی‌دی/دی‌وی‌دی"
    ONLINE = "آنلاین"

class Language(str, enum.Enum):
    PERSIAN = "فارسی"
    ENGLISH = "انگلیسی"
    ARABIC = "عربی"
    FRENCH = "فرانسه"
    GERMAN = "آلمانی"
    SPANISH = "اسپانیایی"
    RUSSIAN = "روسی"
    CHINESE = "چینی"
    JAPANESE = "ژاپنی"
    OTHER = "سایر"

class AvailabilityStatus(str, enum.Enum):
    AVAILABLE = "موجود"
    CHECKED_OUT = "امانت داده شده"
    RESERVED = "رزرو شده"
    IN_TRANSIT = "در حال انتقال"
    LOST = "گم شده"
    DAMAGED = "آسیب دیده"
    UNDER_REPAIR = "در حال تعمیر"
    WITHDRAWN = "منسوخ شده"
    ON_ORDER = "در حال سفارش"

class LoanStatus(str, enum.Enum):
    ACTIVE = "فعال"
    RETURNED = "بازگردانده شده"
    OVERDUE = "سررسید گذشته"
    LOST = "گم شده"
    RENEWED = "تمدید شده"

class ReservationStatus(str, enum.Enum):
    PENDING = "در انتظار"
    READY = "آماده"
    EXPIRED = "منقضی شده"
    CANCELLED = "لغو شده"
    FULFILLED = "برآورده شده"

class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    contact_person = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    materials = relationship("LibraryMaterial", back_populates="publisher")

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    first_name_fa = Column(String(100))
    last_name_fa = Column(String(100))
    email = Column(String(255))
    affiliation = Column(String(255))
    biography = Column(Text)
    orcid_id = Column(String(50))
    google_scholar_id = Column(String(100))
    researchgate_id = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    material_authors = relationship("MaterialAuthor", back_populates="author")

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    parent_subject_id = Column(Integer, ForeignKey('subjects.id'))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    parent_subject = relationship("Subject", remote_side=[id], back_populates="sub_subjects")
    sub_subjects = relationship("Subject", back_populates="parent_subject")
    material_subjects = relationship("MaterialSubject", back_populates="subject")

class Library(Base):
    __tablename__ = 'libraries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    location = Column(String(255))
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    operating_hours = Column(JSON)
    librarian_id = Column(Integer, ForeignKey('employees.id'))
    description = Column(Text)
    total_capacity = Column(Integer)
    current_collection_size = Column(Integer, default=0)
    annual_budget = Column(Float)
    membership_fee = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="libraries")
    librarian = relationship("Employee", foreign_keys=[librarian_id])
    materials = relationship("LibraryMaterial", back_populates="library")
    loans = relationship("Loan", back_populates="library")
    reservations = relationship("Reservation", back_populates="library")

class LibraryMaterial(Base):
    __tablename__ = 'library_materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    material_type = Column(Enum(MaterialType), nullable=False)
    format = Column(Enum(MaterialFormat), nullable=False)
    title = Column(String(500), nullable=False)
    title_fa = Column(String(500))
    subtitle = Column(String(500))
    subtitle_fa = Column(String(500))
    edition = Column(String(50))
    volume = Column(String(50))
    issue = Column(String(50))
    isbn = Column(String(20))
    issn = Column(String(20))
    doi = Column(String(100))
    call_number = Column(String(50), unique=True, nullable=False)
    accession_number = Column(String(50), unique=True, nullable=False)
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    publication_year = Column(Integer)
    publication_place = Column(String(100))
    language = Column(Enum(Language), default=Language.PERSIAN)
    page_count = Column(Integer)
    description = Column(Text)
    abstract = Column(Text)
    keywords = Column(JSON)
    table_of_contents = Column(JSON)
    bibliography = Column(JSON)
    physical_location = Column(String(255))
    digital_url = Column(String(500))
    file_path = Column(String(500))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    availability_status = Column(Enum(AvailabilityStatus), default=AvailabilityStatus.AVAILABLE)
    acquisition_date = Column(DateTime)
    acquisition_cost = Column(Float)
    currency = Column(String(3), default='IRR')
    condition = Column(String(20), default='good')  # excellent, good, fair, poor
    replacement_cost = Column(Float)
    insurance_value = Column(Float)
    last_inventory_date = Column(DateTime)
    inventory_count = Column(Integer, default=1)
    is_reference_only = Column(Boolean, default=False)
    is_lendable = Column(Boolean, default=True)
    max_loan_period_days = Column(Integer, default=14)
    max_renewals = Column(Integer, default=2)
    overdue_fine_per_day = Column(Float, default=1000)
    replacement_fine = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="materials")
    publisher = relationship("Publisher", back_populates="materials")
    material_authors = relationship("MaterialAuthor", back_populates="material")
    material_subjects = relationship("MaterialSubject", back_populates="material")
    loans = relationship("Loan", back_populates="material")
    reservations = relationship("Reservation", back_populates="material")
    reviews = relationship("MaterialReview", back_populates="material")

class MaterialAuthor(Base):
    __tablename__ = 'material_authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('library_materials.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author_order = Column(Integer, nullable=False)
    contribution_type = Column(String(50))  # author, editor, translator, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    material = relationship("LibraryMaterial", back_populates="material_authors")
    author = relationship("Author", back_populates="material_authors")

class MaterialSubject(Base):
    __tablename__ = 'material_subjects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('library_materials.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    material = relationship("LibraryMaterial", back_populates="material_subjects")
    subject = relationship("Subject", back_populates="material_subjects")

class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    material_id = Column(Integer, ForeignKey('library_materials.id'), nullable=False)
    borrower_type = Column(String(20), nullable=False)  # student, employee, external
    student_id = Column(Integer, ForeignKey('students.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    external_borrower_name = Column(String(255))
    external_borrower_id = Column(String(50))
    loan_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime)
    status = Column(Enum(LoanStatus), default=LoanStatus.ACTIVE)
    renewal_count = Column(Integer, default=0)
    max_renewals_allowed = Column(Integer, default=2)
    overdue_days = Column(Integer, default=0)
    overdue_fine = Column(Float, default=0)
    damage_fine = Column(Float, default=0)
    lost_fine = Column(Float, default=0)
    total_fine = Column(Float, default=0)
    fine_paid = Column(Boolean, default=False)
    fine_payment_date = Column(DateTime)
    issued_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    returned_to = Column(Integer, ForeignKey('employees.id'))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="loans")
    material = relationship("LibraryMaterial", back_populates="loans")
    student = relationship("Student", foreign_keys=[student_id])
    employee = relationship("Employee", foreign_keys=[employee_id])
    issued_by_employee = relationship("Employee", foreign_keys=[issued_by])
    returned_to_employee = relationship("Employee", foreign_keys=[returned_to])

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    material_id = Column(Integer, ForeignKey('library_materials.id'), nullable=False)
    borrower_type = Column(String(20), nullable=False)  # student, employee, external
    student_id = Column(Integer, ForeignKey('students.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    external_borrower_name = Column(String(255))
    external_borrower_id = Column(String(50))
    reservation_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING)
    queue_position = Column(Integer)
    notification_sent = Column(Boolean, default=False)
    pickup_date = Column(DateTime)
    cancelled_date = Column(DateTime)
    cancellation_reason = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="reservations")
    material = relationship("LibraryMaterial", back_populates="reservations")
    student = relationship("Student", foreign_keys=[student_id])
    employee = relationship("Employee", foreign_keys=[employee_id])

class MaterialReview(Base):
    __tablename__ = 'material_reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('library_materials.id'), nullable=False)
    reviewer_type = Column(String(20), nullable=False)  # student, employee, external
    student_id = Column(Integer, ForeignKey('students.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    external_reviewer_name = Column(String(255))
    rating = Column(Float)  # 1-5 scale
    review_text = Column(Text)
    review_date = Column(DateTime, default=datetime.utcnow)
    is_approved = Column(Boolean, default=True)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    helpful_votes = Column(Integer, default=0)
    total_votes = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    material = relationship("LibraryMaterial", back_populates="reviews")
    student = relationship("Student", foreign_keys=[student_id])
    employee = relationship("Employee", foreign_keys=[employee_id])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class LibraryMembership(Base):
    __tablename__ = 'library_memberships'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    member_type = Column(String(20), nullable=False)  # student, employee, external
    student_id = Column(Integer, ForeignKey('students.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    external_member_name = Column(String(255))
    external_member_id = Column(String(50))
    membership_number = Column(String(50), unique=True, nullable=False)
    membership_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime)
    status = Column(String(20), default='active')  # active, expired, suspended, cancelled
    membership_fee = Column(Float, default=0)
    fee_paid = Column(Boolean, default=True)
    max_books_allowed = Column(Integer, default=5)
    max_loan_period_days = Column(Integer, default=14)
    max_renewals = Column(Integer, default=2)
    overdue_fine_limit = Column(Float, default=50000)
    suspension_start_date = Column(DateTime)
    suspension_end_date = Column(DateTime)
    suspension_reason = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="memberships")
    student = relationship("Student", foreign_keys=[student_id])
    employee = relationship("Employee", foreign_keys=[employee_id])

class InterLibraryLoan(Base):
    __tablename__ = 'inter_library_loans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    requesting_library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    providing_library_id = Column(Integer, ForeignKey('libraries.id'))
    material_title = Column(String(500), nullable=False)
    material_author = Column(String(255))
    material_type = Column(Enum(MaterialType))
    isbn_issn = Column(String(20))
    borrower_type = Column(String(20), nullable=False)  # student, employee, external
    student_id = Column(Integer, ForeignKey('students.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    external_borrower_name = Column(String(255))
    request_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    return_date = Column(DateTime)
    status = Column(String(20), default='requested')  # requested, approved, shipped, received, returned, cancelled
    shipping_method = Column(String(50))
    tracking_number = Column(String(100))
    shipping_cost = Column(Float)
    processing_fee = Column(Float)
    total_cost = Column(Float)
    payment_status = Column(String(20), default='pending')  # pending, paid, waived
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    requesting_library = relationship("Library", foreign_keys=[requesting_library_id])
    providing_library = relationship("Library", foreign_keys=[providing_library_id])
    student = relationship("Student", foreign_keys=[student_id])
    employee = relationship("Employee", foreign_keys=[employee_id])

class DigitalResource(Base):
    __tablename__ = 'digital_resources'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    title = Column(String(500), nullable=False)
    title_fa = Column(String(500))
    description = Column(Text)
    resource_type = Column(String(50), nullable=False)  # database, e-book, e-journal, video, audio, etc.
    provider = Column(String(255))
    url = Column(String(500), nullable=False)
    access_method = Column(String(50))  # open_access, subscription, licensed
    license_type = Column(String(100))
    license_expiry_date = Column(DateTime)
    username = Column(String(100))
    password = Column(String(100))
    ip_restrictions = Column(JSON)
    concurrent_users = Column(Integer)
    download_limit = Column(Integer)
    print_limit = Column(Integer)
    cost_per_access = Column(Float)
    annual_subscription_cost = Column(Float)
    currency = Column(String(3), default='IRR')
    subjects = Column(JSON)
    keywords = Column(JSON)
    is_active = Column(Boolean, default=True)
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="digital_resources")

class LibraryEvent(Base):
    __tablename__ = 'library_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    description = Column(Text)
    event_type = Column(String(50), nullable=False)  # workshop, seminar, book_launch, exhibition, etc.
    event_date = Column(DateTime, nullable=False)
    start_time = Column(String(20))
    end_time = Column(String(20))
    location = Column(String(255))
    capacity = Column(Integer)
    registered_count = Column(Integer, default=0)
    instructor_presenter = Column(String(255))
    cost = Column(Float, default=0)
    currency = Column(String(3), default='IRR')
    registration_required = Column(Boolean, default=False)
    registration_deadline = Column(DateTime)
    materials = Column(JSON)
    status = Column(String(20), default='planned')  # planned, confirmed, cancelled, completed
    feedback_rating = Column(Float)
    feedback_comments = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="events")
    registrations = relationship("EventRegistration", back_populates="event")

class EventRegistration(Base):
    __tablename__ = 'event_registrations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('library_events.id'), nullable=False)
    registrant_type = Column(String(20), nullable=False)  # student, employee, external
    student_id = Column(Integer, ForeignKey('students.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    external_registrant_name = Column(String(255))
    external_registrant_email = Column(String(255))
    registration_date = Column(DateTime, default=datetime.utcnow)
    attendance_status = Column(String(20), default='registered')  # registered, attended, no_show
    feedback_provided = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    event = relationship("LibraryEvent", back_populates="registrations")
    student = relationship("Student", foreign_keys=[student_id])
    employee = relationship("Employee", foreign_keys=[employee_id])

class LibraryStatistics(Base):
    __tablename__ = 'library_statistics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    statistic_date = Column(DateTime, nullable=False)
    period = Column(String(20), nullable=False)  # daily, weekly, monthly, yearly
    total_materials = Column(Integer)
    active_loans = Column(Integer)
    overdue_loans = Column(Integer)
    total_loans = Column(Integer)
    total_returns = Column(Integer)
    total_reservations = Column(Integer)
    active_reservations = Column(Integer)
    new_memberships = Column(Integer)
    total_members = Column(Integer)
    total_visitors = Column(Integer)
    digital_resource_accesses = Column(Integer)
    inter_library_loans = Column(Integer)
    events_held = Column(Integer)
    event_attendees = Column(Integer)
    budget_utilized = Column(Float)
    fines_collected = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="statistics")
```

## Pydantic Schemas برای سیستم کتابخانه

```python
# app/schemas/library.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MaterialType(str, Enum):
    BOOK = "کتاب"
    JOURNAL = "نشریه"
    MAGAZINE = "مجله"
    NEWSPAPER = "روزنامه"
    THESIS = "پایان‌نامه"
    DISSERTATION = "رساله"
    CONFERENCE_PAPER = "مقاله کنفرانس"
    REPORT = "گزارش"
    AUDIOVISUAL = "صوتی تصویری"
    ELECTRONIC_RESOURCE = "منبع الکترونیکی"
    MANUSCRIPT = "نسخه خطی"
    MAP = "نقشه"
    MICROFORM = "میکروفیلم"

class MaterialFormat(str, Enum):
    PRINT = "چاپی"
    DIGITAL = "دیجیتال"
    AUDIO = "صوتی"
    VIDEO = "تصویری"
    MICROFILM = "میکروفیلم"
    CD_DVD = "سی‌دی/دی‌وی‌دی"
    ONLINE = "آنلاین"

class Language(str, Enum):
    PERSIAN = "فارسی"
    ENGLISH = "انگلیسی"
    ARABIC = "عربی"
    FRENCH = "فرانسه"
    GERMAN = "آلمانی"
    SPANISH = "اسپانیایی"
    RUSSIAN = "روسی"
    CHINESE = "چینی"
    JAPANESE = "ژاپنی"
    OTHER = "سایر"

class AvailabilityStatus(str, Enum):
    AVAILABLE = "موجود"
    CHECKED_OUT = "امانت داده شده"
    RESERVED = "رزرو شده"
    IN_TRANSIT = "در حال انتقال"
    LOST = "گم شده"
    DAMAGED = "آسیب دیده"
    UNDER_REPAIR = "در حال تعمیر"
    WITHDRAWN = "منسوخ شده"
    ON_ORDER = "در حال سفارش"

class LoanStatus(str, Enum):
    ACTIVE = "فعال"
    RETURNED = "بازگردانده شده"
    OVERDUE = "سررسید گذشته"
    LOST = "گم شده"
    RENEWED = "تمدید شده"

class ReservationStatus(str, Enum):
    PENDING = "در انتظار"
    READY = "آماده"
    EXPIRED = "منقضی شده"
    CANCELLED = "لغو شده"
    FULFILLED = "برآورده شده"

# Publisher schemas
class PublisherBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    contact_person: Optional[str] = None

class PublisherCreate(PublisherBase):
    pass

class PublisherUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    contact_person: Optional[str] = None
    is_active: Optional[bool] = None

class Publisher(PublisherBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PublisherWithDetails(Publisher):
    materials_count: int = 0

# Author schemas
class AuthorBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    first_name_fa: Optional[str] = None
    last_name_fa: Optional[str] = None
    email: Optional[EmailStr] = None
    affiliation: Optional[str] = None
    biography: Optional[str] = None
    orcid_id: Optional[str] = None
    google_scholar_id: Optional[str] = None
    researchgate_id: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    first_name_fa: Optional[str] = None
    last_name_fa: Optional[str] = None
    email: Optional[EmailStr] = None
    affiliation: Optional[str] = None
    biography: Optional[str] = None
    orcid_id: Optional[str] = None
    google_scholar_id: Optional[str] = None
    researchgate_id: Optional[str] = None
    is_active: Optional[bool] = None

class Author(AuthorBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AuthorWithDetails(Author):
    materials_count: int = 0

# Subject schemas
class SubjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    parent_subject_id: Optional[int] = None

class SubjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    parent_subject_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class Subject(SubjectBase):
    id: int
    parent_subject_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SubjectWithDetails(Subject):
    parent_subject: Optional[Dict[str, Any]] = None
    sub_subjects: List[Dict[str, Any]] = []
    materials_count: int = 0

# Library schemas
class LibraryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    location: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    operating_hours: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    total_capacity: Optional[int] = None
    annual_budget: Optional[float] = None
    membership_fee: Optional[float] = None

class LibraryCreate(LibraryBase):
    university_id: int
    librarian_id: Optional[int] = None

class LibraryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    location: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    operating_hours: Optional[Dict[str, Any]] = None
    librarian_id: Optional[int] = None
    description: Optional[str] = None
    total_capacity: Optional[int] = None
    annual_budget: Optional[float] = None
    membership_fee: Optional[float] = None
    is_active: Optional[bool] = None

class Library(LibraryBase):
    id: int
    university_id: int
    librarian_id: Optional[int] = None
    current_collection_size: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LibraryWithDetails(Library):
    university: Optional[Dict[str, Any]] = None
    librarian: Optional[Dict[str, Any]] = None
    materials_count: int = 0
    active_loans_count: int = 0
    members_count: int = 0

# Library Material schemas
class LibraryMaterialBase(BaseModel):
    material_type: MaterialType
    format: MaterialFormat
    title: str = Field(..., min_length=1, max_length=500)
    title_fa: Optional[str] = None
    subtitle: Optional[str] = None
    subtitle_fa: Optional[str] = None
    edition: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    isbn: Optional[str] = None
    issn: Optional[str] = None
    doi: Optional[str] = None
    call_number: str = Field(..., min_length=1, max_length=50)
    accession_number: str = Field(..., min_length=1, max_length=50)
    publication_year: Optional[int] = None
    publication_place: Optional[str] = None
    language: Language = Language.PERSIAN
    page_count: Optional[int] = None
    description: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[Dict[str, Any]] = None
    table_of_contents: Optional[Dict[str, Any]] = None
    bibliography: Optional[Dict[str, Any]] = None
    physical_location: Optional[str] = None
    digital_url: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    acquisition_date: Optional[datetime] = None
    acquisition_cost: Optional[float] = None
    currency: str = "IRR"
    condition: str = "good"
    replacement_cost: Optional[float] = None
    insurance_value: Optional[float] = None
    last_inventory_date: Optional[datetime] = None
    inventory_count: int = 1
    is_reference_only: bool = False
    is_lendable: bool = True
    max_loan_period_days: int = 14
    max_renewals: int = 2
    overdue_fine_per_day: float = 1000
    replacement_fine: Optional[float] = None

class LibraryMaterialCreate(LibraryMaterialBase):
    library_id: int
    publisher_id: Optional[int] = None

class LibraryMaterialUpdate(BaseModel):
    material_type: Optional[MaterialType] = None
    format: Optional[MaterialFormat] = None
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    title_fa: Optional[str] = None
    subtitle: Optional[str] = None
    subtitle_fa: Optional[str] = None
    edition: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    isbn: Optional[str] = None
    issn: Optional[str] = None
    doi: Optional[str] = None
    call_number: Optional[str] = Field(None, min_length=1, max_length=50)
    accession_number: Optional[str] = Field(None, min_length=1, max_length=50)
    publisher_id: Optional[int] = None
    publication_year: Optional[int] = None
    publication_place: Optional[str] = None
    language: Optional[Language] = None
    page_count: Optional[int] = None
    description: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[Dict[str, Any]] = None
    table_of_contents: Optional[Dict[str, Any]] = None
    bibliography: Optional[Dict[str, Any]] = None
    physical_location: Optional[str] = None
    digital_url: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    availability_status: Optional[AvailabilityStatus] = None
    acquisition_date: Optional[datetime] = None
    acquisition_cost: Optional[float] = None
    currency: Optional[str] = None
    condition: Optional[str] = None
    replacement_cost: Optional[float] = None
    insurance_value: Optional[float] = None
    last_inventory_date: Optional[datetime] = None
    inventory_count: Optional[int] = None
    is_reference_only: Optional[bool] = None
    is_lendable: Optional[bool] = None
    max_loan_period_days: Optional[int] = None
    max_renewals: Optional[int] = None
    overdue_fine_per_day: Optional[float] = None
    replacement_fine: Optional[float] = None
    is_active: Optional[bool] = None

class LibraryMaterial(LibraryMaterialBase):
    id: int
    library_id: int
    publisher_id: Optional[int] = None
    availability_status: AvailabilityStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LibraryMaterialWithDetails(LibraryMaterial):
    library: Optional[Dict[str, Any]] = None
    publisher: Optional[Dict[str, Any]] = None
    authors: List[Dict[str, Any]] = []
    subjects: List[Dict[str, Any]] = []
    current_loans_count: int = 0
    reservations_count: int = 0
    average_rating: Optional[float] = None

# Loan schemas
class LoanBase(BaseModel):
    borrower_type: str = Field(..., min_length=1, max_length=20)
    loan_date: datetime
    due_date: datetime
    renewal_count: int = 0
    max_renewals_allowed: int = 2
    notes: Optional[str] = None

class LoanCreate(LoanBase):
    library_id: int
    material_id: int
    student_id: Optional[int] = None
    employee_id: Optional[int] = None
    external_borrower_name: Optional[str] = None
    external_borrower_id: Optional[str] = None

class LoanUpdate(BaseModel):
    borrower_type: Optional[str] = Field(None, min_length=1, max_length=20)
    loan_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    status: Optional[LoanStatus] = None
    renewal_count: Optional[int] = None
    max_renewals_allowed: Optional[int] = None
    overdue_days: Optional[int] = None
    overdue_fine: Optional[float] = None
    damage_fine: Optional[float] = None
    lost_fine: Optional[float] = None
    total_fine: Optional[float] = None
    fine_paid: Optional[bool] = None
    fine_payment_date: Optional[datetime] = None
    returned_to: Optional[int] = None
    notes: Optional[str] = None

class Loan(LoanBase):
    id: int
    library_id: int
    material_id: int
    student_id: Optional[int] = None
    employee_id: Optional[int] = None
    external_borrower_name: Optional[str] = None
    external_borrower_id: Optional[str] = None
    return_date: Optional[datetime] = None
    status: LoanStatus
    overdue_days: int
    overdue_fine: float
    damage_fine: float
    lost_fine: float
    total_fine: float
    fine_paid: bool
    fine_payment_date: Optional[datetime] = None
    issued_by: int
    returned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LoanWithDetails(Loan):
    library: Optional[Dict[str, Any]] = None
    material: Optional[Dict[str, Any]] = None
    student: Optional[Dict[str, Any]] = None
    employee: Optional[Dict[str, Any]] = None
    issued_by_employee: Optional[Dict[str, Any]] = None
    returned_to_employee: Optional[Dict[str, Any]] = None

# Reservation schemas
class ReservationBase(BaseModel):
    borrower_type: str = Field(..., min_length=1, max_length=20)
    reservation_date: datetime
    expiry_date: datetime
    notes: Optional[str] = None

class ReservationCreate(ReservationBase):
    library_id: int
    material_id: int
    student_id: Optional[int] = None
    employee_id: Optional[int] = None
    external_borrower_name: Optional[str] = None
    external_borrower_id: Optional[str] = None

class ReservationUpdate(BaseModel):
    borrower_type: Optional[str] = Field(None, min_length=1, max_length=20)
    reservation_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    status: Optional[ReservationStatus] = None
    queue_position: Optional[int] = None
    notification_sent: Optional[bool] = None
    pickup_date: Optional[datetime] = None
    cancelled_date: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    notes: Optional[str] = None

class Reservation(ReservationBase):
    id: int
    library_id: int
    material_id: int
    student_id: Optional[int] = None
    employee_id: Optional[int] = None
    external_borrower_name: Optional[str] = None
    external_borrower_id: Optional[str] = None
    status: ReservationStatus
    queue_position: Optional[int] = None
    notification_sent: bool
    pickup_date: Optional[datetime] = None
    cancelled_date: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReservationWithDetails(Reservation):
    library: Optional[Dict[str, Any]] = None
    material: Optional[Dict[str, Any]] = None
    student: Optional[Dict[str, Any]] = None
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
class LibraryMaterialSearchFilters(BaseModel):
    library_id: Optional[int] = None
    material_type: Optional[MaterialType] = None
    format: Optional[MaterialFormat] = None
    language: Optional[Language] = None
    availability_status: Optional[AvailabilityStatus] = None
    publisher_id: Optional[int] = None
    publication_year_from: Optional[int] = None
    publication_year_to: Optional[int] = None
    is_lendable: Optional[bool] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class LoanSearchFilters(BaseModel):
    library_id: Optional[int] = None
    material_id: Optional[int] = None
    borrower_type: Optional[str] = None
    student_id: Optional[int] = None
    employee_id: Optional[int] = None
    status: Optional[LoanStatus] = None
    issued_by: Optional[int] = None
    returned_to: Optional[int] = None
    loan_date_from: Optional[datetime] = None
    loan_date_to: Optional[datetime] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    overdue_only: Optional[bool] = None

class ReservationSearchFilters(BaseModel):
    library_id: Optional[int] = None
    material_id: Optional[int] = None
    borrower_type: Optional[str] = None
    student_id: Optional[int] = None
    employee_id: Optional[int] = None
    status: Optional[ReservationStatus] = None
    reservation_date_from: Optional[datetime] = None
    reservation_date_to: Optional[datetime] = None
    expiry_date_from: Optional[datetime] = None
    expiry_date_to: Optional[datetime] = None

class LibrarySearchFilters(BaseModel):
    university_id: Optional[int] = None
    librarian_id: Optional[int] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class PublisherSearchFilters(BaseModel):
    is_active: Optional[bool] = None
    search: Optional[str] = None

class AuthorSearchFilters(BaseModel):
    is_active: Optional[bool] = None
    search: Optional[str] = None

class SubjectSearchFilters(BaseModel):
    parent_subject_id: Optional[int] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None
```

این پیاده‌سازی کامل مدل‌های کتابخانه‌ای و منابع شامل تمام ویژگی‌های مورد نیاز برای سیستم کتابخانه دانشگاهی ایران است.
