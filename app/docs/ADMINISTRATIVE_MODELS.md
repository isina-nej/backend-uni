# مدل‌های اداری و مدیریتی - Administrative Models

## مدل‌های SQLAlchemy برای سیستم اداری

```python
# app/models/administrative.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class AdministrativeUnitType(str, enum.Enum):
    OFFICE = "دفتر"
    DEPARTMENT = "اداره"
    DIVISION = "بخش"
    CENTER = "مرکز"
    UNIT = "واحد"
    DIRECTORATE = "مدیریت"
    BUREAU = "اداره کل"

class AdministrativeRole(str, enum.Enum):
    DIRECTOR = "مدیر"
    DEPUTY_DIRECTOR = "معاون مدیر"
    HEAD = "رئیس"
    VICE_HEAD = "معاون"
    MANAGER = "مدیر"
    ASSISTANT_MANAGER = "معاون مدیر"
    SUPERVISOR = "سرپرست"
    COORDINATOR = "هماهنگ کننده"
    SPECIALIST = "کارشناس"
    ASSISTANT = "معاون"
    CLERK = "کارمند"

class BudgetCategory(str, enum.Enum):
    PERSONNEL = "پرسنلی"
    OPERATIONAL = "عملیاتی"
    CAPITAL = "سرمایه‌ای"
    RESEARCH = "پژوهشی"
    EDUCATIONAL = "آموزشی"
    ADMINISTRATIVE = "اداری"
    MAINTENANCE = "تعمیر و نگهداری"
    OTHER = "سایر"

class ProcurementType(str, enum.Enum):
    GOODS = "کالا"
    SERVICES = "خدمات"
    WORKS = "کارها"
    CONSULTANCY = "مشاوره"

class ContractType(str, enum.Enum):
    PERMANENT = "قراردادی دائمی"
    TEMPORARY = "قراردادی موقت"
    PROJECT_BASED = "پروژه‌ای"
    CONSULTANT = "مشاور"
    SERVICE_PROVIDER = "ارائه دهنده خدمات"

class AdministrativeUnit(Base):
    __tablename__ = 'administrative_units'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    unit_type = Column(Enum(AdministrativeUnitType), nullable=False)
    parent_unit_id = Column(Integer, ForeignKey('administrative_units.id'))
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    head_employee_id = Column(Integer, ForeignKey('employees.id'))
    deputy_head_employee_id = Column(Integer, ForeignKey('employees.id'))
    description = Column(Text)
    responsibilities = Column(JSON)
    contact_info = Column(JSON)
    location = Column(String(255))
    floor = Column(String(50))
    room_number = Column(String(50))
    phone_extension = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    establishment_date = Column(DateTime)
    budget_code = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    parent_unit = relationship("AdministrativeUnit", remote_side=[id], back_populates="sub_units")
    sub_units = relationship("AdministrativeUnit", back_populates="parent_unit")
    university = relationship("University", back_populates="administrative_units")
    head_employee = relationship("Employee", foreign_keys=[head_employee_id])
    deputy_head_employee = relationship("Employee", foreign_keys=[deputy_head_employee_id])
    employees = relationship("Employee", back_populates="administrative_unit")
    budget_items = relationship("BudgetItem", back_populates="administrative_unit")
    procurements = relationship("Procurement", back_populates="administrative_unit")

class AdministrativePosition(Base):
    __tablename__ = 'administrative_positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    administrative_unit_id = Column(Integer, ForeignKey('administrative_units.id'), nullable=False)
    role = Column(Enum(AdministrativeRole), nullable=False)
    grade = Column(String(20))
    salary_scale = Column(String(20))
    responsibilities = Column(JSON)
    requirements = Column(JSON)
    reporting_to = Column(Integer, ForeignKey('administrative_positions.id'))
    is_vacant = Column(Boolean, default=True)
    current_employee_id = Column(Integer, ForeignKey('employees.id'))
    appointment_date = Column(DateTime)
    contract_type = Column(Enum(ContractType))
    contract_start_date = Column(DateTime)
    contract_end_date = Column(DateTime)
    probation_period_months = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    administrative_unit = relationship("AdministrativeUnit", back_populates="positions")
    current_employee = relationship("Employee", foreign_keys=[current_employee_id])
    reports_to_position = relationship("AdministrativePosition", remote_side=[id], back_populates="subordinates")
    subordinates = relationship("AdministrativePosition", back_populates="reports_to_position")
    position_history = relationship("PositionHistory", back_populates="position")

class PositionHistory(Base):
    __tablename__ = 'position_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    position_id = Column(Integer, ForeignKey('administrative_positions.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    appointment_type = Column(String(50))
    contract_type = Column(Enum(ContractType))
    salary = Column(Float)
    benefits = Column(JSON)
    performance_rating = Column(Float)
    reason_for_leaving = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    position = relationship("AdministrativePosition", back_populates="position_history")
    employee = relationship("Employee", foreign_keys=[employee_id])

class BudgetItem(Base):
    __tablename__ = 'budget_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    administrative_unit_id = Column(Integer, ForeignKey('administrative_units.id'), nullable=False)
    budget_category = Column(Enum(BudgetCategory), nullable=False)
    item_code = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    description_fa = Column(Text, nullable=False)
    fiscal_year = Column(String(20), nullable=False)  # 1400-1401
    allocated_amount = Column(Float, nullable=False)
    spent_amount = Column(Float, default=0)
    remaining_amount = Column(Float, nullable=False)
    currency = Column(String(3), default='IRR')
    approval_status = Column(String(20), default='pending')  # pending, approved, rejected, revised
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    justification = Column(Text)
    priority_level = Column(String(20), default='medium')  # low, medium, high, critical
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    administrative_unit = relationship("AdministrativeUnit", back_populates="budget_items")
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    expenditures = relationship("BudgetExpenditure", back_populates="budget_item")

class BudgetExpenditure(Base):
    __tablename__ = 'budget_expenditures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    budget_item_id = Column(Integer, ForeignKey('budget_items.id'), nullable=False)
    amount = Column(Float, nullable=False)
    expenditure_date = Column(DateTime, nullable=False)
    description = Column(Text, nullable=False)
    vendor_supplier = Column(String(255))
    invoice_number = Column(String(50))
    payment_method = Column(String(50))
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    receipt_path = Column(String(500))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    budget_item = relationship("BudgetItem", back_populates="expenditures")
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class Procurement(Base):
    __tablename__ = 'procurements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    administrative_unit_id = Column(Integer, ForeignKey('administrative_units.id'), nullable=False)
    procurement_type = Column(Enum(ProcurementType), nullable=False)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    description = Column(Text)
    estimated_value = Column(Float)
    currency = Column(String(3), default='IRR')
    procurement_method = Column(String(50))  # tender, quotation, direct purchase, etc.
    status = Column(String(20), default='planning')  # planning, tendering, evaluation, awarded, completed, cancelled
    priority_level = Column(String(20), default='medium')
    required_date = Column(DateTime)
    budget_item_id = Column(Integer, ForeignKey('budget_items.id'))
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    tender_start_date = Column(DateTime)
    tender_end_date = Column(DateTime)
    evaluation_date = Column(DateTime)
    award_date = Column(DateTime)
    contract_signed_date = Column(DateTime)
    completion_date = Column(DateTime)
    awarded_to = Column(String(255))
    awarded_amount = Column(Float)
    contract_number = Column(String(50))
    contract_path = Column(String(500))
    evaluation_criteria = Column(JSON)
    bidders = Column(JSON)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    administrative_unit = relationship("AdministrativeUnit", back_populates="procurements")
    budget_item = relationship("BudgetItem", foreign_keys=[budget_item_id])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class Asset(Base):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    description = Column(Text)
    asset_type = Column(String(50), nullable=False)  # equipment, furniture, vehicle, software, etc.
    category = Column(String(100))
    subcategory = Column(String(100))
    manufacturer = Column(String(255))
    model = Column(String(255))
    serial_number = Column(String(100))
    purchase_date = Column(DateTime)
    purchase_price = Column(Float)
    currency = Column(String(3), default='IRR')
    supplier = Column(String(255))
    warranty_period_months = Column(Integer)
    warranty_expiry_date = Column(DateTime)
    location = Column(String(255))
    administrative_unit_id = Column(Integer, ForeignKey('administrative_units.id'))
    custodian_employee_id = Column(Integer, ForeignKey('employees.id'))
    condition = Column(String(20), default='good')  # excellent, good, fair, poor, damaged
    maintenance_schedule = Column(JSON)
    last_maintenance_date = Column(DateTime)
    next_maintenance_date = Column(DateTime)
    depreciation_method = Column(String(50))
    useful_life_years = Column(Integer)
    salvage_value = Column(Float)
    current_value = Column(Float)
    insurance_policy = Column(String(100))
    insurance_expiry_date = Column(DateTime)
    disposal_date = Column(DateTime)
    disposal_method = Column(String(50))
    disposal_value = Column(Float)
    status = Column(String(20), default='active')  # active, maintenance, disposed, lost, stolen
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    administrative_unit = relationship("AdministrativeUnit", back_populates="assets")
    custodian_employee = relationship("Employee", foreign_keys=[custodian_employee_id])
    maintenance_records = relationship("AssetMaintenance", back_populates="asset")

class AssetMaintenance(Base):
    __tablename__ = 'asset_maintenance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    maintenance_type = Column(String(50), nullable=False)  # preventive, corrective, predictive
    description = Column(Text, nullable=False)
    maintenance_date = Column(DateTime, nullable=False)
    performed_by = Column(String(255))
    cost = Column(Float)
    currency = Column(String(3), default='IRR')
    vendor = Column(String(255))
    next_maintenance_date = Column(DateTime)
    parts_replaced = Column(JSON)
    work_order_number = Column(String(50))
    technician_notes = Column(Text)
    status = Column(String(20), default='completed')  # scheduled, in_progress, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    asset = relationship("Asset", back_populates="maintenance_records")

class Committee(Base):
    __tablename__ = 'committees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    committee_type = Column(String(50), nullable=False)  # academic, administrative, disciplinary, etc.
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    chairperson_employee_id = Column(Integer, ForeignKey('employees.id'))
    secretary_employee_id = Column(Integer, ForeignKey('employees.id'))
    description = Column(Text)
    objectives = Column(JSON)
    authority = Column(JSON)
    meeting_frequency = Column(String(50))
    quorum_requirement = Column(String(50))
    term_years = Column(Integer)
    establishment_date = Column(DateTime)
    dissolution_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="committees")
    chairperson = relationship("Employee", foreign_keys=[chairperson_employee_id])
    secretary = relationship("Employee", foreign_keys=[secretary_employee_id])
    members = relationship("CommitteeMember", back_populates="committee")
    meetings = relationship("CommitteeMeeting", back_populates="committee")

class CommitteeMember(Base):
    __tablename__ = 'committee_members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    committee_id = Column(Integer, ForeignKey('committees.id'), nullable=False)
    member_type = Column(String(20), nullable=False)  # employee, student, external
    employee_id = Column(Integer, ForeignKey('employees.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    external_member_name = Column(String(255))
    external_member_affiliation = Column(String(255))
    role = Column(String(50), default='member')  # chairperson, secretary, member
    appointment_date = Column(DateTime, nullable=False)
    term_end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    committee = relationship("Committee", back_populates="members")
    employee = relationship("Employee", foreign_keys=[employee_id])
    student = relationship("Student", foreign_keys=[student_id])

class CommitteeMeeting(Base):
    __tablename__ = 'committee_meetings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    committee_id = Column(Integer, ForeignKey('committees.id'), nullable=False)
    meeting_number = Column(String(20))
    title = Column(String(255), nullable=False)
    meeting_date = Column(DateTime, nullable=False)
    start_time = Column(String(20))
    end_time = Column(String(20))
    location = Column(String(255))
    agenda = Column(JSON)
    minutes = Column(Text)
    decisions = Column(JSON)
    attendees = Column(JSON)
    absentees = Column(JSON)
    next_meeting_date = Column(DateTime)
    status = Column(String(20), default='scheduled')  # scheduled, held, cancelled, postponed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    committee = relationship("Committee", back_populates="meetings")

class Policy(Base):
    __tablename__ = 'policies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    category = Column(String(50), nullable=False)  # academic, administrative, financial, hr, etc.
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    administrative_unit_id = Column(Integer, ForeignKey('administrative_units.id'))
    description = Column(Text)
    content = Column(Text, nullable=False)
    effective_date = Column(DateTime, nullable=False)
    review_date = Column(DateTime)
    expiry_date = Column(DateTime)
    approval_status = Column(String(20), default='draft')  # draft, under_review, approved, rejected, expired
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    version = Column(String(20), default="1.0")
    previous_version_id = Column(Integer, ForeignKey('policies.id'))
    keywords = Column(JSON)
    attachments = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="policies")
    administrative_unit = relationship("AdministrativeUnit", foreign_keys=[administrative_unit_id])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    previous_version = relationship("Policy", remote_side=[id], back_populates="next_versions")
    next_versions = relationship("Policy", back_populates="previous_version")

class Regulation(Base):
    __tablename__ = 'regulations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    category = Column(String(50), nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    administrative_unit_id = Column(Integer, ForeignKey('administrative_units.id'))
    description = Column(Text)
    content = Column(Text, nullable=False)
    effective_date = Column(DateTime, nullable=False)
    review_date = Column(DateTime)
    expiry_date = Column(DateTime)
    approval_status = Column(String(20), default='draft')
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    version = Column(String(20), default="1.0")
    previous_version_id = Column(Integer, ForeignKey('regulations.id'))
    keywords = Column(JSON)
    attachments = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="regulations")
    administrative_unit = relationship("AdministrativeUnit", foreign_keys=[administrative_unit_id])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    previous_version = relationship("Regulation", remote_side=[id], back_populates="next_versions")
    next_versions = relationship("Regulation", back_populates="previous_version")

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    document_number = Column(String(50), unique=True, nullable=False)
    document_type = Column(String(50), nullable=False)  # policy, regulation, procedure, form, etc.
    category = Column(String(50))
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    administrative_unit_id = Column(Integer, ForeignKey('administrative_units.id'))
    author_employee_id = Column(Integer, ForeignKey('employees.id'))
    description = Column(Text)
    content = Column(Text)
    file_path = Column(String(500))
    file_url = Column(String(500))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    version = Column(String(20), default="1.0")
    status = Column(String(20), default='draft')  # draft, review, approved, published, archived
    approval_required = Column(Boolean, default=True)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    publication_date = Column(DateTime)
    expiry_date = Column(DateTime)
    keywords = Column(JSON)
    access_level = Column(String(20), default='internal')  # public, internal, confidential, restricted
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="documents")
    administrative_unit = relationship("AdministrativeUnit", foreign_keys=[administrative_unit_id])
    author_employee = relationship("Employee", foreign_keys=[author_employee_id])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class Workflow(Base):
    __tablename__ = 'workflows'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    workflow_type = Column(String(50), nullable=False)  # approval, review, procurement, etc.
    description = Column(Text)
    steps = Column(JSON)
    triggers = Column(JSON)
    conditions = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    instances = relationship("WorkflowInstance", back_populates="workflow")

class WorkflowInstance(Base):
    __tablename__ = 'workflow_instances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    workflow_id = Column(Integer, ForeignKey('workflows.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    initiator_employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    current_step = Column(String(50))
    status = Column(String(20), default='pending')  # pending, in_progress, approved, rejected, cancelled
    priority = Column(String(20), default='medium')
    due_date = Column(DateTime)
    completed_date = Column(DateTime)
    data = Column(JSON)
    attachments = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    workflow = relationship("Workflow", back_populates="instances")
    initiator_employee = relationship("Employee", foreign_keys=[initiator_employee_id])
    steps = relationship("WorkflowStep", back_populates="workflow_instance")

class WorkflowStep(Base):
    __tablename__ = 'workflow_steps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    workflow_instance_id = Column(Integer, ForeignKey('workflow_instances.id'), nullable=False)
    step_name = Column(String(100), nullable=False)
    assigned_to_employee_id = Column(Integer, ForeignKey('employees.id'))
    assigned_to_role = Column(String(50))
    status = Column(String(20), default='pending')  # pending, in_progress, completed, skipped
    action_taken = Column(String(50))  # approve, reject, review, etc.
    comments = Column(Text)
    action_date = Column(DateTime)
    due_date = Column(DateTime)
    sequence_number = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    workflow_instance = relationship("WorkflowInstance", back_populates="steps")
    assigned_to_employee = relationship("Employee", foreign_keys=[assigned_to_employee_id])
```

## Pydantic Schemas برای سیستم اداری

```python
# app/schemas/administrative.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class AdministrativeUnitType(str, Enum):
    OFFICE = "دفتر"
    DEPARTMENT = "اداره"
    DIVISION = "بخش"
    CENTER = "مرکز"
    UNIT = "واحد"
    DIRECTORATE = "مدیریت"
    BUREAU = "اداره کل"

class AdministrativeRole(str, Enum):
    DIRECTOR = "مدیر"
    DEPUTY_DIRECTOR = "معاون مدیر"
    HEAD = "رئیس"
    VICE_HEAD = "معاون"
    MANAGER = "مدیر"
    ASSISTANT_MANAGER = "معاون مدیر"
    SUPERVISOR = "سرپرست"
    COORDINATOR = "هماهنگ کننده"
    SPECIALIST = "کارشناس"
    ASSISTANT = "معاون"
    CLERK = "کارمند"

class BudgetCategory(str, Enum):
    PERSONNEL = "پرسنلی"
    OPERATIONAL = "عملیاتی"
    CAPITAL = "سرمایه‌ای"
    RESEARCH = "پژوهشی"
    EDUCATIONAL = "آموزشی"
    ADMINISTRATIVE = "اداری"
    MAINTENANCE = "تعمیر و نگهداری"
    OTHER = "سایر"

class ProcurementType(str, Enum):
    GOODS = "کالا"
    SERVICES = "خدمات"
    WORKS = "کارها"
    CONSULTANCY = "مشاوره"

class ContractType(str, Enum):
    PERMANENT = "قراردادی دائمی"
    TEMPORARY = "قراردادی موقت"
    PROJECT_BASED = "پروژه‌ای"
    CONSULTANT = "مشاور"
    SERVICE_PROVIDER = "ارائه دهنده خدمات"

# Administrative Unit schemas
class AdministrativeUnitBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    unit_type: AdministrativeUnitType
    description: Optional[str] = None
    responsibilities: Optional[Dict[str, Any]] = None
    contact_info: Optional[Dict[str, Any]] = None
    location: Optional[str] = None
    floor: Optional[str] = None
    room_number: Optional[str] = None
    phone_extension: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    establishment_date: Optional[datetime] = None
    budget_code: Optional[str] = None

class AdministrativeUnitCreate(AdministrativeUnitBase):
    parent_unit_id: Optional[int] = None
    university_id: int
    head_employee_id: Optional[int] = None
    deputy_head_employee_id: Optional[int] = None

class AdministrativeUnitUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    unit_type: Optional[AdministrativeUnitType] = None
    parent_unit_id: Optional[int] = None
    head_employee_id: Optional[int] = None
    deputy_head_employee_id: Optional[int] = None
    description: Optional[str] = None
    responsibilities: Optional[Dict[str, Any]] = None
    contact_info: Optional[Dict[str, Any]] = None
    location: Optional[str] = None
    floor: Optional[str] = None
    room_number: Optional[str] = None
    phone_extension: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    establishment_date: Optional[datetime] = None
    budget_code: Optional[str] = None
    is_active: Optional[bool] = None

class AdministrativeUnit(AdministrativeUnitBase):
    id: int
    parent_unit_id: Optional[int] = None
    university_id: int
    head_employee_id: Optional[int] = None
    deputy_head_employee_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AdministrativeUnitWithDetails(AdministrativeUnit):
    parent_unit: Optional[Dict[str, Any]] = None
    sub_units: List[Dict[str, Any]] = []
    university: Optional[Dict[str, Any]] = None
    head_employee: Optional[Dict[str, Any]] = None
    deputy_head_employee: Optional[Dict[str, Any]] = None
    employees_count: int = 0
    positions_count: int = 0

# Administrative Position schemas
class AdministrativePositionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    role: AdministrativeRole
    grade: Optional[str] = None
    salary_scale: Optional[str] = None
    responsibilities: Optional[Dict[str, Any]] = None
    requirements: Optional[Dict[str, Any]] = None
    contract_type: Optional[ContractType] = None
    contract_start_date: Optional[datetime] = None
    contract_end_date: Optional[datetime] = None
    probation_period_months: Optional[int] = None

class AdministrativePositionCreate(AdministrativePositionBase):
    administrative_unit_id: int
    reporting_to: Optional[int] = None
    current_employee_id: Optional[int] = None
    appointment_date: Optional[datetime] = None

class AdministrativePositionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    role: Optional[AdministrativeRole] = None
    grade: Optional[str] = None
    salary_scale: Optional[str] = None
    responsibilities: Optional[Dict[str, Any]] = None
    requirements: Optional[Dict[str, Any]] = None
    reporting_to: Optional[int] = None
    is_vacant: Optional[bool] = None
    current_employee_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    contract_type: Optional[ContractType] = None
    contract_start_date: Optional[datetime] = None
    contract_end_date: Optional[datetime] = None
    probation_period_months: Optional[int] = None
    is_active: Optional[bool] = None

class AdministrativePosition(AdministrativePositionBase):
    id: int
    administrative_unit_id: int
    reporting_to: Optional[int] = None
    is_vacant: bool
    current_employee_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AdministrativePositionWithDetails(AdministrativePosition):
    administrative_unit: Optional[Dict[str, Any]] = None
    current_employee: Optional[Dict[str, Any]] = None
    reports_to_position: Optional[Dict[str, Any]] = None
    subordinates: List[Dict[str, Any]] = []

# Budget Item schemas
class BudgetItemBase(BaseModel):
    budget_category: BudgetCategory
    item_code: str = Field(..., min_length=1, max_length=20)
    description: str = Field(..., min_length=1)
    description_fa: str = Field(..., min_length=1)
    fiscal_year: str = Field(..., min_length=1, max_length=20)
    allocated_amount: float = Field(..., gt=0)
    currency: str = "IRR"
    justification: Optional[str] = None
    priority_level: str = "medium"

class BudgetItemCreate(BudgetItemBase):
    administrative_unit_id: int

class BudgetItemUpdate(BaseModel):
    budget_category: Optional[BudgetCategory] = None
    item_code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = Field(None, min_length=1)
    description_fa: Optional[str] = Field(None, min_length=1)
    fiscal_year: Optional[str] = Field(None, min_length=1, max_length=20)
    allocated_amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = None
    approval_status: Optional[str] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    justification: Optional[str] = None
    priority_level: Optional[str] = None
    is_active: Optional[bool] = None

class BudgetItem(BudgetItemBase):
    id: int
    administrative_unit_id: int
    spent_amount: float
    remaining_amount: float
    approval_status: str
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BudgetItemWithDetails(BudgetItem):
    administrative_unit: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None
    expenditures_count: int = 0

# Procurement schemas
class ProcurementBase(BaseModel):
    procurement_type: ProcurementType
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    estimated_value: Optional[float] = None
    currency: str = "IRR"
    procurement_method: Optional[str] = None
    priority_level: str = "medium"
    required_date: Optional[datetime] = None
    tender_start_date: Optional[datetime] = None
    tender_end_date: Optional[datetime] = None
    evaluation_date: Optional[datetime] = None
    award_date: Optional[datetime] = None
    contract_signed_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    awarded_to: Optional[str] = None
    awarded_amount: Optional[float] = None
    contract_number: Optional[str] = None
    contract_path: Optional[str] = None
    evaluation_criteria: Optional[Dict[str, Any]] = None
    bidders: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class ProcurementCreate(ProcurementBase):
    administrative_unit_id: int
    budget_item_id: Optional[int] = None

class ProcurementUpdate(BaseModel):
    procurement_type: Optional[ProcurementType] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    estimated_value: Optional[float] = None
    currency: Optional[str] = None
    procurement_method: Optional[str] = None
    status: Optional[str] = None
    priority_level: Optional[str] = None
    required_date: Optional[datetime] = None
    budget_item_id: Optional[int] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    tender_start_date: Optional[datetime] = None
    tender_end_date: Optional[datetime] = None
    evaluation_date: Optional[datetime] = None
    award_date: Optional[datetime] = None
    contract_signed_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    awarded_to: Optional[str] = None
    awarded_amount: Optional[float] = None
    contract_number: Optional[str] = None
    contract_path: Optional[str] = None
    evaluation_criteria: Optional[Dict[str, Any]] = None
    bidders: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class Procurement(ProcurementBase):
    id: int
    administrative_unit_id: int
    budget_item_id: Optional[int] = None
    status: str
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProcurementWithDetails(Procurement):
    administrative_unit: Optional[Dict[str, Any]] = None
    budget_item: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None

# Asset schemas
class AssetBase(BaseModel):
    asset_code: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    asset_type: str = Field(..., min_length=1, max_length=50)
    category: Optional[str] = None
    subcategory: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = None
    currency: str = "IRR"
    supplier: Optional[str] = None
    warranty_period_months: Optional[int] = None
    warranty_expiry_date: Optional[datetime] = None
    location: Optional[str] = None
    condition: str = "good"
    maintenance_schedule: Optional[Dict[str, Any]] = None
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_date: Optional[datetime] = None
    depreciation_method: Optional[str] = None
    useful_life_years: Optional[int] = None
    salvage_value: Optional[float] = None
    current_value: Optional[float] = None
    insurance_policy: Optional[str] = None
    insurance_expiry_date: Optional[datetime] = None
    disposal_date: Optional[datetime] = None
    disposal_method: Optional[str] = None
    disposal_value: Optional[float] = None
    notes: Optional[str] = None

class AssetCreate(AssetBase):
    administrative_unit_id: Optional[int] = None
    custodian_employee_id: Optional[int] = None

class AssetUpdate(BaseModel):
    asset_code: Optional[str] = Field(None, min_length=1, max_length=20)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    asset_type: Optional[str] = Field(None, min_length=1, max_length=50)
    category: Optional[str] = None
    subcategory: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[float] = None
    currency: Optional[str] = None
    supplier: Optional[str] = None
    warranty_period_months: Optional[int] = None
    warranty_expiry_date: Optional[datetime] = None
    location: Optional[str] = None
    administrative_unit_id: Optional[int] = None
    custodian_employee_id: Optional[int] = None
    condition: Optional[str] = None
    maintenance_schedule: Optional[Dict[str, Any]] = None
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_date: Optional[datetime] = None
    depreciation_method: Optional[str] = None
    useful_life_years: Optional[int] = None
    salvage_value: Optional[float] = None
    current_value: Optional[float] = None
    insurance_policy: Optional[str] = None
    insurance_expiry_date: Optional[datetime] = None
    disposal_date: Optional[datetime] = None
    disposal_method: Optional[str] = None
    disposal_value: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class Asset(AssetBase):
    id: int
    administrative_unit_id: Optional[int] = None
    custodian_employee_id: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AssetWithDetails(Asset):
    administrative_unit: Optional[Dict[str, Any]] = None
    custodian_employee: Optional[Dict[str, Any]] = None
    maintenance_records_count: int = 0

# Committee schemas
class CommitteeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    committee_type: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    objectives: Optional[Dict[str, Any]] = None
    authority: Optional[Dict[str, Any]] = None
    meeting_frequency: Optional[str] = None
    quorum_requirement: Optional[str] = None
    term_years: Optional[int] = None
    establishment_date: Optional[datetime] = None
    dissolution_date: Optional[datetime] = None

class CommitteeCreate(CommitteeBase):
    university_id: int
    chairperson_employee_id: Optional[int] = None
    secretary_employee_id: Optional[int] = None

class CommitteeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    committee_type: Optional[str] = Field(None, min_length=1, max_length=50)
    chairperson_employee_id: Optional[int] = None
    secretary_employee_id: Optional[int] = None
    description: Optional[str] = None
    objectives: Optional[Dict[str, Any]] = None
    authority: Optional[Dict[str, Any]] = None
    meeting_frequency: Optional[str] = None
    quorum_requirement: Optional[str] = None
    term_years: Optional[int] = None
    establishment_date: Optional[datetime] = None
    dissolution_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class Committee(CommitteeBase):
    id: int
    university_id: int
    chairperson_employee_id: Optional[int] = None
    secretary_employee_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CommitteeWithDetails(Committee):
    university: Optional[Dict[str, Any]] = None
    chairperson: Optional[Dict[str, Any]] = None
    secretary: Optional[Dict[str, Any]] = None
    members_count: int = 0
    meetings_count: int = 0

# Policy schemas
class PolicyBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    category: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    content: str = Field(..., min_length=1)
    effective_date: datetime
    review_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    version: str = "1.0"
    keywords: Optional[Dict[str, Any]] = None
    attachments: Optional[Dict[str, Any]] = None

class PolicyCreate(PolicyBase):
    university_id: int
    administrative_unit_id: Optional[int] = None

class PolicyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    administrative_unit_id: Optional[int] = None
    description: Optional[str] = None
    content: Optional[str] = Field(None, min_length=1)
    effective_date: Optional[datetime] = None
    review_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    approval_status: Optional[str] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    version: Optional[str] = None
    previous_version_id: Optional[int] = None
    keywords: Optional[Dict[str, Any]] = None
    attachments: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class Policy(PolicyBase):
    id: int
    university_id: int
    administrative_unit_id: Optional[int] = None
    approval_status: str
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    previous_version_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PolicyWithDetails(Policy):
    university: Optional[Dict[str, Any]] = None
    administrative_unit: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None
    previous_version: Optional[Dict[str, Any]] = None

# Document schemas
class DocumentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    document_number: str = Field(..., min_length=1, max_length=50)
    document_type: str = Field(..., min_length=1, max_length=50)
    category: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    version: str = "1.0"
    approval_required: bool = True
    publication_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    keywords: Optional[Dict[str, Any]] = None
    access_level: str = "internal"

class DocumentCreate(DocumentBase):
    university_id: int
    administrative_unit_id: Optional[int] = None
    author_employee_id: Optional[int] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    document_number: Optional[str] = Field(None, min_length=1, max_length=50)
    document_type: Optional[str] = Field(None, min_length=1, max_length=50)
    category: Optional[str] = None
    administrative_unit_id: Optional[int] = None
    author_employee_id: Optional[int] = None
    description: Optional[str] = None
    content: Optional[str] = None
    file_path: Optional[str] = None
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    version: Optional[str] = None
    status: Optional[str] = None
    approval_required: Optional[bool] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    publication_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    keywords: Optional[Dict[str, Any]] = None
    access_level: Optional[str] = None
    is_active: Optional[bool] = None

class Document(DocumentBase):
    id: int
    university_id: int
    administrative_unit_id: Optional[int] = None
    author_employee_id: Optional[int] = None
    status: str
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DocumentWithDetails(Document):
    university: Optional[Dict[str, Any]] = None
    administrative_unit: Optional[Dict[str, Any]] = None
    author_employee: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None

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
class AdministrativeUnitSearchFilters(BaseModel):
    university_id: Optional[int] = None
    unit_type: Optional[AdministrativeUnitType] = None
    parent_unit_id: Optional[int] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class BudgetItemSearchFilters(BaseModel):
    administrative_unit_id: Optional[int] = None
    budget_category: Optional[BudgetCategory] = None
    fiscal_year: Optional[str] = None
    approval_status: Optional[str] = None
    is_active: Optional[bool] = None
    allocated_amount_min: Optional[float] = None
    allocated_amount_max: Optional[float] = None

class ProcurementSearchFilters(BaseModel):
    administrative_unit_id: Optional[int] = None
    procurement_type: Optional[ProcurementType] = None
    status: Optional[str] = None
    priority_level: Optional[str] = None
    estimated_value_min: Optional[float] = None
    estimated_value_max: Optional[float] = None
    search: Optional[str] = None

class AssetSearchFilters(BaseModel):
    administrative_unit_id: Optional[int] = None
    asset_type: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    condition: Optional[str] = None
    custodian_employee_id: Optional[int] = None
    purchase_price_min: Optional[float] = None
    purchase_price_max: Optional[float] = None

class CommitteeSearchFilters(BaseModel):
    university_id: Optional[int] = None
    committee_type: Optional[str] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class PolicySearchFilters(BaseModel):
    university_id: Optional[int] = None
    category: Optional[str] = None
    approval_status: Optional[str] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class DocumentSearchFilters(BaseModel):
    university_id: Optional[int] = None
    document_type: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    access_level: Optional[str] = None
    author_employee_id: Optional[int] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None
```

این پیاده‌سازی کامل مدل‌های اداری و مدیریتی شامل تمام ویژگی‌های مورد نیاز برای سیستم مدیریت اداری دانشگاهی ایران است.
