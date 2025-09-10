# مدل‌های پیشرفته کتابخانه - Advanced Library Models

## مدل‌های SQLAlchemy پیشرفته برای سیستم کتابخانه

```python
# app/models/advanced_library.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float, DECIMAL
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# Enums
class BookStatus(str, enum.Enum):
    AVAILABLE = "موجود"
    BORROWED = "امانت داده شده"
    RESERVED = "رزرو شده"
    LOST = "گم شده"
    DAMAGED = "آسیب دیده"
    UNDER_MAINTENANCE = "در حال تعمیر"

class BookCondition(str, enum.Enum):
    EXCELLENT = "عالی"
    GOOD = "خوب"
    FAIR = "متوسط"
    POOR = "ضعیف"
    DAMAGED = "آسیب دیده"

class LoanStatus(str, enum.Enum):
    ACTIVE = "فعال"
    RETURNED = "بازگردانده شده"
    OVERDUE = "سررسید گذشته"
    LOST = "گم شده"
    EXTENDED = "تمدید شده"

class ReservationStatus(str, enum.Enum):
    PENDING = "در انتظار"
    READY = "آماده تحویل"
    EXPIRED = "منقضی شده"
    CANCELLED = "لغو شده"
    FULFILLED = "برآورده شده"

class MaterialType(str, enum.Enum):
    BOOK = "کتاب"
    JOURNAL = "مجله"
    THESIS = "پایان‌نامه"
    DISSERTATION = "رساله"
    CD_DVD = "سی‌دی/دی‌وی‌دی"
    E_BOOK = "کتاب الکترونیکی"
    AUDIO_BOOK = "کتاب صوتی"
    MAGAZINE = "نشریه"
    NEWSPAPER = "روزنامه"
    REFERENCE = "مرجع"

class AccessLevel(str, enum.Enum):
    PUBLIC = "عمومی"
    STUDENT = "دانشجویی"
    STAFF = "کارمندی"
    FACULTY = "هیات علمی"
    RESTRICTED = "محدود"

# Library Models
class Library(Base):
    __tablename__ = 'libraries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    opening_hours = Column(JSON)
    capacity = Column(Integer)
    librarian_id = Column(Integer, ForeignKey('employees.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="libraries")
    librarian = relationship("Employee", foreign_keys=[librarian_id])
    books = relationship("Book", back_populates="library")
    loans = relationship("Loan", back_populates="library")
    reservations = relationship("Reservation", back_populates="library")

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    isbn = Column(String(20), unique=True)
    title = Column(String(500), nullable=False)
    title_fa = Column(String(500), nullable=False)
    subtitle = Column(String(500))
    authors = Column(JSON, nullable=False)  # List of authors
    publisher = Column(String(255))
    publication_year = Column(Integer)
    edition = Column(String(50))
    pages = Column(Integer)
    language = Column(String(50), default='فارسی')
    description = Column(Text)
    material_type = Column(Enum(MaterialType), nullable=False)
    access_level = Column(Enum(AccessLevel), default=AccessLevel.PUBLIC)
    category_id = Column(Integer, ForeignKey('book_categories.id'))
    subject_area = Column(String(255))
    keywords = Column(JSON)
    cover_image_url = Column(String(500))
    digital_copy_url = Column(String(500))
    acquisition_date = Column(DateTime)
    acquisition_cost = Column(DECIMAL(10, 2))
    replacement_cost = Column(DECIMAL(10, 2))
    is_available = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="books")
    category = relationship("BookCategory", back_populates="books")
    copies = relationship("BookCopy", back_populates="book")
    loans = relationship("Loan", back_populates="book")
    reservations = relationship("Reservation", back_populates="book")

class BookCategory(Base):
    __tablename__ = 'book_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey('book_categories.id'))
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    parent = relationship("BookCategory", remote_side=[id])
    children = relationship("BookCategory")
    books = relationship("Book", back_populates="category")

class BookCopy(Base):
    __tablename__ = 'book_copies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    copy_number = Column(String(20), nullable=False)
    barcode = Column(String(50), unique=True, nullable=False)
    status = Column(Enum(BookStatus), default=BookStatus.AVAILABLE)
    condition = Column(Enum(BookCondition), default=BookCondition.GOOD)
    location = Column(String(255))
    shelf_number = Column(String(50))
    purchase_date = Column(DateTime)
    purchase_cost = Column(DECIMAL(10, 2))
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    book = relationship("Book", back_populates="copies")
    loans = relationship("Loan", back_populates="copy")

class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    copy_id = Column(Integer, ForeignKey('book_copies.id'), nullable=False)
    borrower_type = Column(String(20), nullable=False)  # student, employee
    borrower_id = Column(Integer, nullable=False)  # student_id or employee_id
    loan_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime)
    status = Column(Enum(LoanStatus), default=LoanStatus.ACTIVE)
    extension_count = Column(Integer, default=0)
    max_extensions = Column(Integer, default=3)
    fine_amount = Column(DECIMAL(8, 2), default=0)
    fine_paid = Column(Boolean, default=False)
    fine_payment_date = Column(DateTime)
    notes = Column(Text)
    issued_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    returned_to = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="loans")
    book = relationship("Book", back_populates="loans")
    copy = relationship("BookCopy", back_populates="loans")
    issued_by_employee = relationship("Employee", foreign_keys=[issued_by])
    returned_to_employee = relationship("Employee", foreign_keys=[returned_to])

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrower_type = Column(String(20), nullable=False)  # student, employee
    borrower_id = Column(Integer, nullable=False)  # student_id or employee_id
    reservation_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING)
    pickup_date = Column(DateTime)
    cancellation_date = Column(DateTime)
    cancellation_reason = Column(Text)
    notification_sent = Column(Boolean, default=False)
    queue_position = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="reservations")
    book = relationship("Book", back_populates="reservations")

class Fine(Base):
    __tablename__ = 'fines'

    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(Integer, ForeignKey('loans.id'), nullable=False)
    borrower_type = Column(String(20), nullable=False)  # student, employee
    borrower_id = Column(Integer, nullable=False)  # student_id or employee_id
    amount = Column(DECIMAL(8, 2), nullable=False)
    reason = Column(String(255), nullable=False)
    fine_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    payment_date = Column(DateTime)
    status = Column(String(20), default='unpaid')  # unpaid, paid, waived
    payment_method = Column(String(50))
    waived_by = Column(Integer, ForeignKey('employees.id'))
    waived_date = Column(DateTime)
    waiver_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    loan = relationship("Loan", back_populates="fines")
    waived_by_employee = relationship("Employee", foreign_keys=[waived_by])

class LibraryMembership(Base):
    __tablename__ = 'library_memberships'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    member_type = Column(String(20), nullable=False)  # student, employee
    member_id = Column(Integer, nullable=False)  # student_id or employee_id
    membership_number = Column(String(20), unique=True, nullable=False)
    join_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    status = Column(String(20), default='active')  # active, expired, suspended
    max_books = Column(Integer, default=5)
    max_loan_days = Column(Integer, default=14)
    max_reservations = Column(Integer, default=3)
    outstanding_fines = Column(DECIMAL(8, 2), default=0)
    is_blocked = Column(Boolean, default=False)
    block_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="memberships")

class LibraryEvent(Base):
    __tablename__ = 'library_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(Integer, ForeignKey('libraries.id'), nullable=False)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    description = Column(Text)
    event_type = Column(String(50), nullable=False)  # workshop, seminar, book_launch, etc.
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(255))
    capacity = Column(Integer)
    registered_count = Column(Integer, default=0)
    is_free = Column(Boolean, default=True)
    registration_fee = Column(DECIMAL(8, 2), default=0)
    organizer_id = Column(Integer, ForeignKey('employees.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    library = relationship("Library", back_populates="events")
    organizer = relationship("Employee", foreign_keys=[organizer_id])
    registrations = relationship("EventRegistration", back_populates="event")

class EventRegistration(Base):
    __tablename__ = 'event_registrations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('library_events.id'), nullable=False)
    registrant_type = Column(String(20), nullable=False)  # student, employee
    registrant_id = Column(Integer, nullable=False)  # student_id or employee_id
    registration_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='registered')  # registered, attended, cancelled
    attendance_date = Column(DateTime)
    feedback_rating = Column(Integer)
    feedback_comments = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    event = relationship("LibraryEvent", back_populates="registrations")

# Add missing relationships to main models
University.libraries = relationship("Library", back_populates="university")

Library.memberships = relationship("LibraryMembership", back_populates="library")
Library.events = relationship("LibraryEvent", back_populates="library")

Loan.fines = relationship("Fine", back_populates="loan")
```

## Pydantic Schemas پیشرفته برای سیستم کتابخانه

```python
# app/schemas/advanced_library.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class BookStatus(str, Enum):
    AVAILABLE = "موجود"
    BORROWED = "امانت داده شده"
    RESERVED = "رزرو شده"
    LOST = "گم شده"
    DAMAGED = "آسیب دیده"
    UNDER_MAINTENANCE = "در حال تعمیر"

class BookCondition(str, Enum):
    EXCELLENT = "عالی"
    GOOD = "خوب"
    FAIR = "متوسط"
    POOR = "ضعیف"
    DAMAGED = "آسیب دیده"

class LoanStatus(str, Enum):
    ACTIVE = "فعال"
    RETURNED = "بازگردانده شده"
    OVERDUE = "سررسید گذشته"
    LOST = "گم شده"
    EXTENDED = "تمدید شده"

class ReservationStatus(str, Enum):
    PENDING = "در انتظار"
    READY = "آماده تحویل"
    EXPIRED = "منقضی شده"
    CANCELLED = "لغو شده"
    FULFILLED = "برآورده شده"

class MaterialType(str, Enum):
    BOOK = "کتاب"
    JOURNAL = "مجله"
    THESIS = "پایان‌نامه"
    DISSERTATION = "رساله"
    CD_DVD = "سی‌دی/دی‌وی‌دی"
    E_BOOK = "کتاب الکترونیکی"
    AUDIO_BOOK = "کتاب صوتی"
    MAGAZINE = "نشریه"
    NEWSPAPER = "روزنامه"
    REFERENCE = "مرجع"

class AccessLevel(str, Enum):
    PUBLIC = "عمومی"
    STUDENT = "دانشجویی"
    STAFF = "کارمندی"
    FACULTY = "هیات علمی"
    RESTRICTED = "محدود"

# Library schemas
class LibraryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    opening_hours: Optional[Dict[str, Any]] = None
    capacity: Optional[int] = None

class LibraryCreate(LibraryBase):
    university_id: int

class LibraryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    opening_hours: Optional[Dict[str, Any]] = None
    capacity: Optional[int] = None
    librarian_id: Optional[int] = None
    is_active: Optional[bool] = None

class Library(LibraryBase):
    id: int
    university_id: int
    librarian_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LibraryWithDetails(Library):
    university: Optional[Dict[str, Any]] = None
    librarian: Optional[Dict[str, Any]] = None
    books_count: int = 0
    active_loans_count: int = 0
    overdue_loans_count: int = 0
    members_count: int = 0

# Book schemas
class BookBase(BaseModel):
    isbn: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=500)
    title_fa: str = Field(..., min_length=1, max_length=500)
    subtitle: Optional[str] = None
    authors: List[str] = Field(..., min_items=1)
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    edition: Optional[str] = None
    pages: Optional[int] = None
    language: str = "فارسی"
    description: Optional[str] = None
    material_type: MaterialType
    access_level: AccessLevel = AccessLevel.PUBLIC
    subject_area: Optional[str] = None
    keywords: Optional[List[str]] = None
    cover_image_url: Optional[str] = None
    digital_copy_url: Optional[str] = None
    acquisition_date: Optional[datetime] = None
    acquisition_cost: Optional[float] = None
    replacement_cost: Optional[float] = None

class BookCreate(BookBase):
    library_id: int
    category_id: Optional[int] = None

class BookUpdate(BaseModel):
    isbn: Optional[str] = None
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=500)
    subtitle: Optional[str] = None
    authors: Optional[List[str]] = Field(None, min_items=1)
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    edition: Optional[str] = None
    pages: Optional[int] = None
    language: Optional[str] = None
    description: Optional[str] = None
    material_type: Optional[MaterialType] = None
    access_level: Optional[AccessLevel] = None
    category_id: Optional[int] = None
    subject_area: Optional[str] = None
    keywords: Optional[List[str]] = None
    cover_image_url: Optional[str] = None
    digital_copy_url: Optional[str] = None
    acquisition_date: Optional[datetime] = None
    acquisition_cost: Optional[float] = None
    replacement_cost: Optional[float] = None
    is_available: Optional[bool] = None
    is_active: Optional[bool] = None

class Book(BookBase):
    id: int
    library_id: int
    category_id: Optional[int] = None
    is_available: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookWithDetails(Book):
    library: Optional[Dict[str, Any]] = None
    category: Optional[Dict[str, Any]] = None
    copies_count: int = 0
    available_copies_count: int = 0
    active_loans_count: int = 0
    reservations_count: int = 0

# Book Category schemas
class BookCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None

class BookCategoryCreate(BookCategoryBase):
    parent_id: Optional[int] = None

class BookCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    is_active: Optional[bool] = None

class BookCategory(BookCategoryBase):
    id: int
    parent_id: Optional[int] = None
    level: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookCategoryWithDetails(BookCategory):
    parent: Optional[Dict[str, Any]] = None
    children: List[Dict[str, Any]] = []
    books_count: int = 0

# Book Copy schemas
class BookCopyBase(BaseModel):
    copy_number: str = Field(..., min_length=1, max_length=20)
    barcode: str = Field(..., min_length=1, max_length=50)
    status: BookStatus = BookStatus.AVAILABLE
    condition: BookCondition = BookCondition.GOOD
    location: Optional[str] = None
    shelf_number: Optional[str] = None
    purchase_date: Optional[datetime] = None
    purchase_cost: Optional[float] = None
    notes: Optional[str] = None

class BookCopyCreate(BookCopyBase):
    book_id: int

class BookCopyUpdate(BaseModel):
    copy_number: Optional[str] = Field(None, min_length=1, max_length=20)
    barcode: Optional[str] = Field(None, min_length=1, max_length=50)
    status: Optional[BookStatus] = None
    condition: Optional[BookCondition] = None
    location: Optional[str] = None
    shelf_number: Optional[str] = None
    purchase_date: Optional[datetime] = None
    purchase_cost: Optional[float] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class BookCopy(BookCopyBase):
    id: int
    book_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookCopyWithDetails(BookCopy):
    book: Optional[Dict[str, Any]] = None
    current_loan: Optional[Dict[str, Any]] = None
    loan_history_count: int = 0

# Loan schemas
class LoanBase(BaseModel):
    loan_date: datetime
    due_date: datetime
    extension_count: int = 0
    max_extensions: int = 3
    notes: Optional[str] = None

class LoanCreate(LoanBase):
    library_id: int
    book_id: int
    copy_id: int
    borrower_type: str = Field(..., regex="^(student|employee)$")
    borrower_id: int

class LoanUpdate(BaseModel):
    loan_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    status: Optional[LoanStatus] = None
    extension_count: Optional[int] = None
    max_extensions: Optional[int] = None
    fine_amount: Optional[float] = None
    fine_paid: Optional[bool] = None
    fine_payment_date: Optional[datetime] = None
    notes: Optional[str] = None
    returned_to: Optional[int] = None

class Loan(LoanBase):
    id: int
    library_id: int
    book_id: int
    copy_id: int
    borrower_type: str
    borrower_id: int
    return_date: Optional[datetime] = None
    status: LoanStatus
    fine_amount: float
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
    book: Optional[Dict[str, Any]] = None
    copy: Optional[Dict[str, Any]] = None
    borrower: Optional[Dict[str, Any]] = None
    issued_by_employee: Optional[Dict[str, Any]] = None
    returned_to_employee: Optional[Dict[str, Any]] = None
    fines: List[Dict[str, Any]] = []
    days_overdue: int = 0

# Reservation schemas
class ReservationBase(BaseModel):
    reservation_date: datetime = Field(default_factory=datetime.utcnow)
    expiry_date: datetime

class ReservationCreate(ReservationBase):
    library_id: int
    book_id: int
    borrower_type: str = Field(..., regex="^(student|employee)$")
    borrower_id: int

class ReservationUpdate(BaseModel):
    reservation_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    status: Optional[ReservationStatus] = None
    pickup_date: Optional[datetime] = None
    cancellation_date: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    notification_sent: Optional[bool] = None

class Reservation(ReservationBase):
    id: int
    library_id: int
    book_id: int
    borrower_type: str
    borrower_id: int
    status: ReservationStatus
    pickup_date: Optional[datetime] = None
    cancellation_date: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    notification_sent: bool
    queue_position: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReservationWithDetails(Reservation):
    library: Optional[Dict[str, Any]] = None
    book: Optional[Dict[str, Any]] = None
    borrower: Optional[Dict[str, Any]] = None

# Fine schemas
class FineBase(BaseModel):
    amount: float = Field(..., gt=0)
    reason: str = Field(..., min_length=1, max_length=255)
    fine_date: datetime = Field(default_factory=datetime.utcnow)
    due_date: datetime

class FineCreate(FineBase):
    loan_id: int
    borrower_type: str = Field(..., regex="^(student|employee)$")
    borrower_id: int

class FineUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    reason: Optional[str] = Field(None, min_length=1, max_length=255)
    fine_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    payment_date: Optional[datetime] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    waived_by: Optional[int] = None
    waived_date: Optional[datetime] = None
    waiver_reason: Optional[str] = None

class Fine(FineBase):
    id: int
    loan_id: int
    borrower_type: str
    borrower_id: int
    payment_date: Optional[datetime] = None
    status: str
    payment_method: Optional[str] = None
    waived_by: Optional[int] = None
    waived_date: Optional[datetime] = None
    waiver_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FineWithDetails(Fine):
    loan: Optional[Dict[str, Any]] = None
    borrower: Optional[Dict[str, Any]] = None
    waived_by_employee: Optional[Dict[str, Any]] = None

# Library Membership schemas
class LibraryMembershipBase(BaseModel):
    membership_number: str = Field(..., min_length=1, max_length=20)
    join_date: datetime = Field(default_factory=datetime.utcnow)
    expiry_date: Optional[datetime] = None
    max_books: int = 5
    max_loan_days: int = 14
    max_reservations: int = 3

class LibraryMembershipCreate(LibraryMembershipBase):
    library_id: int
    member_type: str = Field(..., regex="^(student|employee)$")
    member_id: int

class LibraryMembershipUpdate(BaseModel):
    membership_number: Optional[str] = Field(None, min_length=1, max_length=20)
    join_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    status: Optional[str] = None
    max_books: Optional[int] = None
    max_loan_days: Optional[int] = None
    max_reservations: Optional[int] = None
    outstanding_fines: Optional[float] = None
    is_blocked: Optional[bool] = None
    block_reason: Optional[str] = None

class LibraryMembership(LibraryMembershipBase):
    id: int
    library_id: int
    member_type: str
    member_id: int
    status: str
    outstanding_fines: float
    is_blocked: bool
    block_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LibraryMembershipWithDetails(LibraryMembership):
    library: Optional[Dict[str, Any]] = None
    member: Optional[Dict[str, Any]] = None
    active_loans_count: int = 0
    active_reservations_count: int = 0

# Library Event schemas
class LibraryEventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    event_type: str = Field(..., min_length=1, max_length=50)
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None
    capacity: Optional[int] = None
    is_free: bool = True
    registration_fee: float = 0

class LibraryEventCreate(LibraryEventBase):
    library_id: int

class LibraryEventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    event_type: Optional[str] = Field(None, min_length=1, max_length=50)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    is_free: Optional[bool] = None
    registration_fee: Optional[float] = None
    organizer_id: Optional[int] = None
    is_active: Optional[bool] = None

class LibraryEvent(LibraryEventBase):
    id: int
    library_id: int
    registered_count: int
    organizer_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LibraryEventWithDetails(LibraryEvent):
    library: Optional[Dict[str, Any]] = None
    organizer: Optional[Dict[str, Any]] = None
    registrations: List[Dict[str, Any]] = []
    available_spots: Optional[int] = None

# Event Registration schemas
class EventRegistrationBase(BaseModel):
    registration_date: datetime = Field(default_factory=datetime.utcnow)

class EventRegistrationCreate(EventRegistrationBase):
    event_id: int
    registrant_type: str = Field(..., regex="^(student|employee)$")
    registrant_id: int

class EventRegistrationUpdate(BaseModel):
    registration_date: Optional[datetime] = None
    status: Optional[str] = None
    attendance_date: Optional[datetime] = None
    feedback_rating: Optional[int] = Field(None, ge=1, le=5)
    feedback_comments: Optional[str] = None

class EventRegistration(EventRegistrationBase):
    id: int
    event_id: int
    registrant_type: str
    registrant_id: int
    status: str
    attendance_date: Optional[datetime] = None
    feedback_rating: Optional[int] = None
    feedback_comments: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EventRegistrationWithDetails(EventRegistration):
    event: Optional[Dict[str, Any]] = None
    registrant: Optional[Dict[str, Any]] = None

# Search and filter schemas
class LibrarySearchFilters(BaseModel):
    university_id: Optional[int] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class BookSearchFilters(BaseModel):
    library_id: Optional[int] = None
    category_id: Optional[int] = None
    material_type: Optional[MaterialType] = None
    access_level: Optional[AccessLevel] = None
    is_available: Optional[bool] = None
    is_active: Optional[bool] = None
    publication_year_from: Optional[int] = None
    publication_year_to: Optional[int] = None
    search: Optional[str] = None

class LoanSearchFilters(BaseModel):
    library_id: Optional[int] = None
    book_id: Optional[int] = None
    copy_id: Optional[int] = None
    borrower_type: Optional[str] = None
    borrower_id: Optional[int] = None
    status: Optional[LoanStatus] = None
    issued_by: Optional[int] = None
    loan_date_from: Optional[datetime] = None
    loan_date_to: Optional[datetime] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    return_date_from: Optional[datetime] = None
    return_date_to: Optional[datetime] = None
    search: Optional[str] = None

class ReservationSearchFilters(BaseModel):
    library_id: Optional[int] = None
    book_id: Optional[int] = None
    borrower_type: Optional[str] = None
    borrower_id: Optional[int] = None
    status: Optional[ReservationStatus] = None
    reservation_date_from: Optional[datetime] = None
    reservation_date_to: Optional[datetime] = None
    expiry_date_from: Optional[datetime] = None
    expiry_date_to: Optional[datetime] = None
    search: Optional[str] = None

class FineSearchFilters(BaseModel):
    loan_id: Optional[int] = None
    borrower_type: Optional[str] = None
    borrower_id: Optional[int] = None
    status: Optional[str] = None
    waived_by: Optional[int] = None
    fine_date_from: Optional[datetime] = None
    fine_date_to: Optional[datetime] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    payment_date_from: Optional[datetime] = None
    payment_date_to: Optional[datetime] = None
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    search: Optional[str] = None

# Library dashboard schemas
class LibrarySummary(BaseModel):
    total_books: int
    available_books: int
    borrowed_books: int
    overdue_loans: int
    active_reservations: int
    total_members: int
    outstanding_fines: float
    monthly_loans: int
    monthly_returns: int

class BookStatistics(BaseModel):
    book_id: int
    title: str
    total_copies: int
    available_copies: int
    borrowed_copies: int
    reservations_count: int
    total_loans: int
    overdue_loans: int
    average_loan_duration: float

class MemberStatistics(BaseModel):
    member_id: int
    member_type: str
    member_name: str
    total_loans: int
    active_loans: int
    overdue_loans: int
    outstanding_fines: float
    reservations_count: int
    membership_status: str
```

این پیاده‌سازی مدل‌های پیشرفته کتابخانه شامل تمام جنبه‌های مدیریت کتابخانه دانشگاهی است و پایه‌ای محکم برای سیستم کتابخانه فراهم می‌کند.
