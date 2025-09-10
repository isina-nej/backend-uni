# مدل‌های پیشرفته مالی - Advanced Financial Models

## مدل‌های SQLAlchemy پیشرفته برای حوزه مالی

```python
# app/models/advanced_financial.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float, DECIMAL
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# Enums
class BudgetType(str, enum.Enum):
    OPERATIONAL = "عملیاتی"
    CAPITAL = "سرمایه‌ای"
    RESEARCH = "پژوهشی"
    STUDENT_AID = "کمک هزینه تحصیلی"
    FACILITY_MAINTENANCE = "نگهداری تاسیسات"

class BudgetStatus(str, enum.Enum):
    DRAFT = "پیش‌نویس"
    SUBMITTED = "ارسال شده"
    APPROVED = "تایید شده"
    REJECTED = "رد شده"
    ACTIVE = "فعال"
    CLOSED = "بسته شده"

class TransactionType(str, enum.Enum):
    INCOME = "درآمد"
    EXPENSE = "هزینه"
    TRANSFER = "انتقال"

class PaymentMethod(str, enum.Enum):
    CASH = "نقدی"
    CHECK = "چک"
    BANK_TRANSFER = "انتقال بانکی"
    CREDIT_CARD = "کارت اعتباری"
    ONLINE_PAYMENT = "پرداخت آنلاین"

class InvoiceStatus(str, enum.Enum):
    DRAFT = "پیش‌نویس"
    SENT = "ارسال شده"
    PAID = "پرداخت شده"
    OVERDUE = "سررسید گذشته"
    CANCELLED = "لغو شده"

class ScholarshipType(str, enum.Enum):
    MERIT_BASED = "بر اساس شایستگی"
    NEED_BASED = "بر اساس نیاز"
    ATHLETIC = "ورزشی"
    RESEARCH = "پژوهشی"
    INTERNATIONAL = "بین‌المللی"

# Budget Models
class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    fiscal_year = Column(String(10), nullable=False)  # e.g., "1402-1403"
    budget_type = Column(Enum(BudgetType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    total_amount = Column(DECIMAL(20, 2), nullable=False)
    allocated_amount = Column(DECIMAL(20, 2), default=0)
    spent_amount = Column(DECIMAL(20, 2), default=0)
    status = Column(Enum(BudgetStatus), default=BudgetStatus.DRAFT)
    submitted_by = Column(Integer, ForeignKey('employees.id'))
    submitted_at = Column(DateTime)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approved_at = Column(DateTime)
    approval_notes = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="budgets")
    submitted_by_employee = relationship("Employee", foreign_keys=[submitted_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    categories = relationship("BudgetCategory", back_populates="budget")
    transactions = relationship("Transaction", back_populates="budget")

class BudgetCategory(Base):
    __tablename__ = 'budget_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    budget_id = Column(Integer, ForeignKey('budgets.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('budget_categories.id'))
    code = Column(String(20), nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    description = Column(Text)
    allocated_amount = Column(DECIMAL(15, 2), nullable=False)
    spent_amount = Column(DECIMAL(15, 2), default=0)
    level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    budget = relationship("Budget", back_populates="categories")
    parent = relationship("BudgetCategory", remote_side=[id])
    children = relationship("BudgetCategory")
    transactions = relationship("Transaction", back_populates="category")

# Transaction Models
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    budget_id = Column(Integer, ForeignKey('budgets.id'))
    category_id = Column(Integer, ForeignKey('budget_categories.id'))
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    description = Column(Text, nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    payment_method = Column(Enum(PaymentMethod))
    reference_number = Column(String(100))
    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    receipt_number = Column(String(100))
    attachments = Column(JSON)
    status = Column(String(20), default='completed')
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approved_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    budget = relationship("Budget", back_populates="transactions")
    category = relationship("BudgetCategory", back_populates="transactions")
    vendor = relationship("Vendor", back_populates="transactions")
    employee = relationship("Employee", foreign_keys=[employee_id])
    student = relationship("Student", foreign_keys=[student_id])
    invoice = relationship("Invoice", back_populates="transactions")
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    created_by_employee = relationship("Employee", foreign_keys=[created_by])

class Vendor(Base):
    __tablename__ = 'vendors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    vendor_type = Column(String(50), nullable=False)  # supplier, contractor, service_provider
    national_id = Column(String(20))
    registration_number = Column(String(50))
    tax_id = Column(String(20))
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    contact_person = Column(String(100))
    contact_phone = Column(String(20))
    bank_account = Column(String(50))
    bank_name = Column(String(100))
    rating = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transactions = relationship("Transaction", back_populates="vendor")
    invoices = relationship("Invoice", back_populates="vendor")

# Invoice Models
class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)
    budget_id = Column(Integer, ForeignKey('budgets.id'))
    category_id = Column(Integer, ForeignKey('budget_categories.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    total_amount = Column(DECIMAL(15, 2), nullable=False)
    tax_amount = Column(DECIMAL(15, 2), default=0)
    discount_amount = Column(DECIMAL(15, 2), default=0)
    net_amount = Column(DECIMAL(15, 2), nullable=False)
    currency = Column(String(3), default='IRR')
    issue_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    payment_date = Column(DateTime)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    payment_terms = Column(String(255))
    notes = Column(Text)
    attachments = Column(JSON)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    vendor = relationship("Vendor", back_populates="invoices")
    budget = relationship("Budget", back_populates="invoices")
    category = relationship("BudgetCategory", back_populates="invoices")
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    transactions = relationship("Transaction", back_populates="invoice")
    items = relationship("InvoiceItem", back_populates="invoice")

class InvoiceItem(Base):
    __tablename__ = 'invoice_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    item_number = Column(String(20))
    description = Column(Text, nullable=False)
    quantity = Column(DECIMAL(10, 2), nullable=False)
    unit_price = Column(DECIMAL(15, 2), nullable=False)
    total_price = Column(DECIMAL(15, 2), nullable=False)
    tax_rate = Column(DECIMAL(5, 2), default=0)
    tax_amount = Column(DECIMAL(15, 2), default=0)
    discount_rate = Column(DECIMAL(5, 2), default=0)
    discount_amount = Column(DECIMAL(15, 2), default=0)
    net_amount = Column(DECIMAL(15, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    invoice = relationship("Invoice", back_populates="items")

# Scholarship Models
class Scholarship(Base):
    __tablename__ = 'scholarships'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    scholarship_type = Column(Enum(ScholarshipType), nullable=False)
    description = Column(Text)
    eligibility_criteria = Column(JSON)
    amount = Column(DECIMAL(15, 2), nullable=False)
    currency = Column(String(3), default='IRR')
    duration_months = Column(Integer)
    is_renewable = Column(Boolean, default=False)
    max_recipients = Column(Integer)
    application_deadline = Column(DateTime)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    funding_source = Column(String(255))
    sponsor_id = Column(Integer, ForeignKey('vendors.id'))
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="scholarships")
    sponsor = relationship("Vendor", foreign_keys=[sponsor_id])
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    applications = relationship("ScholarshipApplication", back_populates="scholarship")

class ScholarshipApplication(Base):
    __tablename__ = 'scholarship_applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    scholarship_id = Column(Integer, ForeignKey('scholarships.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    application_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='pending')  # pending, approved, rejected, awarded
    gpa = Column(Float)
    financial_need_level = Column(String(20))
    supporting_documents = Column(JSON)
    review_notes = Column(Text)
    awarded_amount = Column(DECIMAL(15, 2))
    award_date = Column(DateTime)
    reviewed_by = Column(Integer, ForeignKey('employees.id'))
    reviewed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    scholarship = relationship("Scholarship", back_populates="applications")
    student = relationship("Student", back_populates="scholarship_applications")
    reviewed_by_employee = relationship("Employee", foreign_keys=[reviewed_by])

# Financial Reports Models
class FinancialReport(Base):
    __tablename__ = 'financial_reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    report_type = Column(String(50), nullable=False)  # budget, expense, revenue, balance_sheet
    fiscal_year = Column(String(10), nullable=False)
    period = Column(String(20), nullable=False)  # monthly, quarterly, annually
    title = Column(String(255), nullable=False)
    description = Column(Text)
    report_data = Column(JSON)
    generated_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approved_at = Column(DateTime)
    is_final = Column(Boolean, default=False)
    attachments = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="financial_reports")
    generated_by_employee = relationship("Employee", foreign_keys=[generated_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

# Add missing relationships to main models
University.budgets = relationship("Budget", back_populates="university")
University.scholarships = relationship("Scholarship", back_populates="university")
University.financial_reports = relationship("FinancialReport", back_populates="university")

Budget.invoices = relationship("Invoice", back_populates="budget")
BudgetCategory.invoices = relationship("Invoice", back_populates="category")

Student.scholarship_applications = relationship("ScholarshipApplication", back_populates="student")
```

## Pydantic Schemas پیشرفته برای حوزه مالی

```python
# app/schemas/advanced_financial.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class BudgetType(str, Enum):
    OPERATIONAL = "عملیاتی"
    CAPITAL = "سرمایه‌ای"
    RESEARCH = "پژوهشی"
    STUDENT_AID = "کمک هزینه تحصیلی"
    FACILITY_MAINTENANCE = "نگهداری تاسیسات"

class BudgetStatus(str, Enum):
    DRAFT = "پیش‌نویس"
    SUBMITTED = "ارسال شده"
    APPROVED = "تایید شده"
    REJECTED = "رد شده"
    ACTIVE = "فعال"
    CLOSED = "بسته شده"

class TransactionType(str, Enum):
    INCOME = "درآمد"
    EXPENSE = "هزینه"
    TRANSFER = "انتقال"

class PaymentMethod(str, Enum):
    CASH = "نقدی"
    CHECK = "چک"
    BANK_TRANSFER = "انتقال بانکی"
    CREDIT_CARD = "کارت اعتباری"
    ONLINE_PAYMENT = "پرداخت آنلاین"

class InvoiceStatus(str, Enum):
    DRAFT = "پیش‌نویس"
    SENT = "ارسال شده"
    PAID = "پرداخت شده"
    OVERDUE = "سررسید گذشته"
    CANCELLED = "لغو شده"

class ScholarshipType(str, Enum):
    MERIT_BASED = "بر اساس شایستگی"
    NEED_BASED = "بر اساس نیاز"
    ATHLETIC = "ورزشی"
    RESEARCH = "پژوهشی"
    INTERNATIONAL = "بین‌المللی"

# Budget schemas
class BudgetBase(BaseModel):
    fiscal_year: str = Field(..., min_length=1, max_length=10)
    budget_type: BudgetType
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    total_amount: float = Field(..., gt=0)
    start_date: datetime
    end_date: datetime

class BudgetCreate(BudgetBase):
    university_id: int

class BudgetUpdate(BaseModel):
    fiscal_year: Optional[str] = Field(None, min_length=1, max_length=10)
    budget_type: Optional[BudgetType] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    total_amount: Optional[float] = Field(None, gt=0)
    status: Optional[BudgetStatus] = None
    submitted_by: Optional[int] = None
    submitted_at: Optional[datetime] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    approval_notes: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class Budget(BudgetBase):
    id: int
    university_id: int
    allocated_amount: float
    spent_amount: float
    status: BudgetStatus
    submitted_by: Optional[int] = None
    submitted_at: Optional[datetime] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    approval_notes: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BudgetWithDetails(Budget):
    university: Optional[Dict[str, Any]] = None
    submitted_by_employee: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None
    categories_count: int = 0
    transactions_count: int = 0
    remaining_amount: float = 0
    utilization_percentage: float = 0

# Budget Category schemas
class BudgetCategoryBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    allocated_amount: float = Field(..., gt=0)

class BudgetCategoryCreate(BudgetCategoryBase):
    budget_id: int
    parent_id: Optional[int] = None

class BudgetCategoryUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    allocated_amount: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None

class BudgetCategory(BudgetCategoryBase):
    id: int
    budget_id: int
    parent_id: Optional[int] = None
    spent_amount: float
    level: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BudgetCategoryWithDetails(BudgetCategory):
    budget: Optional[Dict[str, Any]] = None
    parent: Optional[Dict[str, Any]] = None
    children: List[Dict[str, Any]] = []
    transactions_count: int = 0
    remaining_amount: float = 0
    utilization_percentage: float = 0

# Transaction schemas
class TransactionBase(BaseModel):
    transaction_type: TransactionType
    amount: float = Field(..., gt=0)
    description: str = Field(..., min_length=1)
    transaction_date: datetime
    payment_method: Optional[PaymentMethod] = None
    reference_number: Optional[str] = None
    receipt_number: Optional[str] = None
    attachments: Optional[Dict[str, Any]] = None

class TransactionCreate(TransactionBase):
    budget_id: Optional[int] = None
    category_id: Optional[int] = None
    vendor_id: Optional[int] = None
    employee_id: Optional[int] = None
    student_id: Optional[int] = None
    invoice_id: Optional[int] = None

class TransactionUpdate(BaseModel):
    transaction_type: Optional[TransactionType] = None
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, min_length=1)
    transaction_date: Optional[datetime] = None
    payment_method: Optional[PaymentMethod] = None
    reference_number: Optional[str] = None
    receipt_number: Optional[str] = None
    attachments: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None

class Transaction(TransactionBase):
    id: int
    budget_id: Optional[int] = None
    category_id: Optional[int] = None
    vendor_id: Optional[int] = None
    employee_id: Optional[int] = None
    student_id: Optional[int] = None
    invoice_id: Optional[int] = None
    status: str
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TransactionWithDetails(Transaction):
    budget: Optional[Dict[str, Any]] = None
    category: Optional[Dict[str, Any]] = None
    vendor: Optional[Dict[str, Any]] = None
    employee: Optional[Dict[str, Any]] = None
    student: Optional[Dict[str, Any]] = None
    invoice: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None
    created_by_employee: Optional[Dict[str, Any]] = None

# Vendor schemas
class VendorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    vendor_type: str = Field(..., min_length=1, max_length=50)
    national_id: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    bank_account: Optional[str] = None
    bank_name: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    vendor_type: Optional[str] = Field(None, min_length=1, max_length=50)
    national_id: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    bank_account: Optional[str] = None
    bank_name: Optional[str] = None
    rating: Optional[float] = None
    is_active: Optional[bool] = None

class Vendor(VendorBase):
    id: int
    rating: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VendorWithDetails(Vendor):
    transactions_count: int = 0
    total_transaction_amount: float = 0
    invoices_count: int = 0
    total_invoice_amount: float = 0

# Invoice schemas
class InvoiceBase(BaseModel):
    invoice_number: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    total_amount: float = Field(..., gt=0)
    tax_amount: float = 0
    discount_amount: float = 0
    currency: str = "IRR"
    issue_date: datetime
    due_date: datetime
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    attachments: Optional[Dict[str, Any]] = None

class InvoiceCreate(InvoiceBase):
    vendor_id: int
    budget_id: Optional[int] = None
    category_id: Optional[int] = None

class InvoiceUpdate(BaseModel):
    invoice_number: Optional[str] = Field(None, min_length=1, max_length=50)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    total_amount: Optional[float] = Field(None, gt=0)
    tax_amount: Optional[float] = None
    discount_amount: Optional[float] = None
    currency: Optional[str] = None
    issue_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    payment_date: Optional[datetime] = None
    status: Optional[InvoiceStatus] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    attachments: Optional[Dict[str, Any]] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None

class Invoice(InvoiceBase):
    id: int
    vendor_id: int
    budget_id: Optional[int] = None
    category_id: Optional[int] = None
    net_amount: float
    payment_date: Optional[datetime] = None
    status: InvoiceStatus
    created_by: int
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InvoiceWithDetails(Invoice):
    vendor: Optional[Dict[str, Any]] = None
    budget: Optional[Dict[str, Any]] = None
    category: Optional[Dict[str, Any]] = None
    created_by_employee: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None
    transactions: List[Dict[str, Any]] = []
    items: List[Dict[str, Any]] = []
    days_overdue: int = 0

# Invoice Item schemas
class InvoiceItemBase(BaseModel):
    item_number: Optional[str] = None
    description: str = Field(..., min_length=1)
    quantity: float = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    tax_rate: float = 0
    discount_rate: float = 0

class InvoiceItemCreate(InvoiceItemBase):
    invoice_id: int

class InvoiceItemUpdate(BaseModel):
    item_number: Optional[str] = None
    description: Optional[str] = Field(None, min_length=1)
    quantity: Optional[float] = Field(None, gt=0)
    unit_price: Optional[float] = Field(None, gt=0)
    tax_rate: Optional[float] = None
    discount_rate: Optional[float] = None

class InvoiceItem(InvoiceItemBase):
    id: int
    invoice_id: int
    total_price: float
    tax_amount: float
    discount_amount: float
    net_amount: float
    created_at: datetime

    class Config:
        from_attributes = True

# Scholarship schemas
class ScholarshipBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    scholarship_type: ScholarshipType
    description: Optional[str] = None
    eligibility_criteria: Optional[Dict[str, Any]] = None
    amount: float = Field(..., gt=0)
    currency: str = "IRR"
    duration_months: Optional[int] = None
    is_renewable: bool = False
    max_recipients: Optional[int] = None
    application_deadline: Optional[datetime] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    funding_source: Optional[str] = None

class ScholarshipCreate(ScholarshipBase):
    university_id: int
    sponsor_id: Optional[int] = None

class ScholarshipUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    scholarship_type: Optional[ScholarshipType] = None
    description: Optional[str] = None
    eligibility_criteria: Optional[Dict[str, Any]] = None
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = None
    duration_months: Optional[int] = None
    is_renewable: Optional[bool] = None
    max_recipients: Optional[int] = None
    application_deadline: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    funding_source: Optional[str] = None
    sponsor_id: Optional[int] = None
    is_active: Optional[bool] = None

class Scholarship(ScholarshipBase):
    id: int
    university_id: int
    sponsor_id: Optional[int] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ScholarshipWithDetails(Scholarship):
    university: Optional[Dict[str, Any]] = None
    sponsor: Optional[Dict[str, Any]] = None
    created_by_employee: Optional[Dict[str, Any]] = None
    applications_count: int = 0
    awarded_count: int = 0
    total_awarded_amount: float = 0

# Scholarship Application schemas
class ScholarshipApplicationBase(BaseModel):
    application_date: datetime = Field(default_factory=datetime.utcnow)
    gpa: Optional[float] = None
    financial_need_level: Optional[str] = None
    supporting_documents: Optional[Dict[str, Any]] = None

class ScholarshipApplicationCreate(ScholarshipApplicationBase):
    scholarship_id: int
    student_id: int

class ScholarshipApplicationUpdate(BaseModel):
    application_date: Optional[datetime] = None
    status: Optional[str] = None
    gpa: Optional[float] = None
    financial_need_level: Optional[str] = None
    supporting_documents: Optional[Dict[str, Any]] = None
    review_notes: Optional[str] = None
    awarded_amount: Optional[float] = None
    award_date: Optional[datetime] = None
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None

class ScholarshipApplication(ScholarshipApplicationBase):
    id: int
    scholarship_id: int
    student_id: int
    status: str
    review_notes: Optional[str] = None
    awarded_amount: Optional[float] = None
    award_date: Optional[datetime] = None
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ScholarshipApplicationWithDetails(ScholarshipApplication):
    scholarship: Optional[Dict[str, Any]] = None
    student: Optional[Dict[str, Any]] = None
    reviewed_by_employee: Optional[Dict[str, Any]] = None

# Financial Report schemas
class FinancialReportBase(BaseModel):
    report_type: str = Field(..., min_length=1, max_length=50)
    fiscal_year: str = Field(..., min_length=1, max_length=10)
    period: str = Field(..., min_length=1, max_length=20)
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    report_data: Optional[Dict[str, Any]] = None
    attachments: Optional[Dict[str, Any]] = None

class FinancialReportCreate(FinancialReportBase):
    university_id: int

class FinancialReportUpdate(BaseModel):
    report_type: Optional[str] = Field(None, min_length=1, max_length=50)
    fiscal_year: Optional[str] = Field(None, min_length=1, max_length=10)
    period: Optional[str] = Field(None, min_length=1, max_length=20)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    report_data: Optional[Dict[str, Any]] = None
    attachments: Optional[Dict[str, Any]] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    is_final: Optional[bool] = None

class FinancialReport(FinancialReportBase):
    id: int
    university_id: int
    generated_by: int
    generated_at: datetime
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    is_final: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FinancialReportWithDetails(FinancialReport):
    university: Optional[Dict[str, Any]] = None
    generated_by_employee: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None

# Search and filter schemas
class BudgetSearchFilters(BaseModel):
    university_id: Optional[int] = None
    fiscal_year: Optional[str] = None
    budget_type: Optional[BudgetType] = None
    status: Optional[BudgetStatus] = None
    submitted_by: Optional[int] = None
    approved_by: Optional[int] = None
    is_active: Optional[bool] = None
    start_date_from: Optional[datetime] = None
    start_date_to: Optional[datetime] = None
    end_date_from: Optional[datetime] = None
    end_date_to: Optional[datetime] = None
    search: Optional[str] = None

class TransactionSearchFilters(BaseModel):
    budget_id: Optional[int] = None
    category_id: Optional[int] = None
    transaction_type: Optional[TransactionType] = None
    payment_method: Optional[PaymentMethod] = None
    vendor_id: Optional[int] = None
    employee_id: Optional[int] = None
    student_id: Optional[int] = None
    invoice_id: Optional[int] = None
    status: Optional[str] = None
    approved_by: Optional[int] = None
    created_by: Optional[int] = None
    transaction_date_from: Optional[datetime] = None
    transaction_date_to: Optional[datetime] = None
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    search: Optional[str] = None

class InvoiceSearchFilters(BaseModel):
    vendor_id: Optional[int] = None
    budget_id: Optional[int] = None
    category_id: Optional[int] = None
    status: Optional[InvoiceStatus] = None
    created_by: Optional[int] = None
    approved_by: Optional[int] = None
    issue_date_from: Optional[datetime] = None
    issue_date_to: Optional[datetime] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    payment_date_from: Optional[datetime] = None
    payment_date_to: Optional[datetime] = None
    total_amount_min: Optional[float] = None
    total_amount_max: Optional[float] = None
    search: Optional[str] = None

class ScholarshipSearchFilters(BaseModel):
    university_id: Optional[int] = None
    scholarship_type: Optional[ScholarshipType] = None
    sponsor_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_renewable: Optional[bool] = None
    start_date_from: Optional[datetime] = None
    start_date_to: Optional[datetime] = None
    end_date_from: Optional[datetime] = None
    end_date_to: Optional[datetime] = None
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    search: Optional[str] = None

class VendorSearchFilters(BaseModel):
    vendor_type: Optional[str] = None
    rating_min: Optional[float] = None
    rating_max: Optional[float] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

# Financial dashboard schemas
class FinancialSummary(BaseModel):
    total_budget: float
    allocated_budget: float
    spent_budget: float
    remaining_budget: float
    budget_utilization_percentage: float
    total_income: float
    total_expenses: float
    net_income: float
    pending_invoices_count: int
    overdue_invoices_count: int
    active_scholarships_count: int
    total_scholarship_amount: float

class BudgetSummary(BaseModel):
    budget_id: int
    budget_title: str
    total_amount: float
    allocated_amount: float
    spent_amount: float
    remaining_amount: float
    utilization_percentage: float
    categories_count: int
    transactions_count: int

class MonthlyFinancialData(BaseModel):
    month: str
    year: int
    income: float
    expenses: float
    net: float
    budget_spent: float
    invoices_paid: float
    scholarships_awarded: float
```

این پیاده‌سازی مدل‌های پیشرفته مالی شامل تمام جنبه‌های بودجه‌بندی، تراکنش‌ها، فاکتورها، بورسیه‌ها و گزارش‌های مالی است و پایه‌ای محکم برای مدیریت مالی دانشگاه فراهم می‌کند.
