# مدل‌های مالی و بودجه‌ای - Financial Models

## مدل‌های SQLAlchemy برای سیستم مالی

```python
# app/models/financial.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class Currency(str, enum.Enum):
    IRR = "ریال"
    USD = "دلار آمریکا"
    EUR = "یورو"
    GBP = "پوند انگلیس"
    AED = "درهم امارات"

class PaymentMethod(str, enum.Enum):
    CASH = "نقدی"
    CHECK = "چک"
    BANK_TRANSFER = "انتقال بانکی"
    CREDIT_CARD = "کارت اعتباری"
    ONLINE_PAYMENT = "پرداخت آنلاین"
    WIRE_TRANSFER = "انتقال سیمی"

class TransactionType(str, enum.Enum):
    INCOME = "درآمد"
    EXPENSE = "هزینه"
    TRANSFER = "انتقال"
    ADJUSTMENT = "تطبیق"

class BudgetStatus(str, enum.Enum):
    DRAFT = "پیش‌نویس"
    SUBMITTED = "ارائه شده"
    APPROVED = "تایید شده"
    REJECTED = "رد شده"
    ACTIVE = "فعال"
    CLOSED = "بسته شده"

class InvoiceStatus(str, enum.Enum):
    DRAFT = "پیش‌نویس"
    SENT = "ارسال شده"
    PAID = "پرداخت شده"
    OVERDUE = "سررسید گذشته"
    CANCELLED = "لغو شده"

class SalaryComponentType(str, enum.Enum):
    BASIC_SALARY = "حقوق پایه"
    HOUSING_ALLOWANCE = "کمک مسکن"
    TRANSPORT_ALLOWANCE = "کمک حمل و نقل"
    MEAL_ALLOWANCE = "کمک تغذیه"
    OVERTIME = "اضافه کاری"
    BONUS = "پاداش"
    COMMISSION = "کمیسیون"
    TAX_DEDUCTION = "کسر مالیات"
    INSURANCE_DEDUCTION = "کسر بیمه"
    LOAN_DEDUCTION = "کسر وام"
    OTHER_ALLOWANCE = "سایر کمک‌ها"
    OTHER_DEDUCTION = "سایر کسورات"

class ScholarshipType(str, enum.Enum):
    MERIT_BASED = "بر اساس شایستگی"
    NEED_BASED = "بر اساس نیاز"
    ATHLETIC = "ورزشی"
    RESEARCH = "پژوهشی"
    INTERNATIONAL = "بین‌المللی"
    SPECIAL_PROGRAM = "برنامه ویژه"

class FeeType(str, enum.Enum):
    TUITION_FEE = "شهریه"
    REGISTRATION_FEE = "هزینه ثبت نام"
    EXAMINATION_FEE = "هزینه آزمون"
    LATE_PAYMENT_FEE = "جریمه تأخیر"
    LIBRARY_FEE = "هزینه کتابخانه"
    LABORATORY_FEE = "هزینه آزمایشگاه"
    SPORTS_FEE = "هزینه ورزشی"
    HEALTH_FEE = "هزینه بهداشتی"
    STUDENT_ACTIVITY_FEE = "هزینه فعالیت‌های دانشجویی"
    OTHER_FEE = "سایر هزینه‌ها"

class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    fiscal_year = Column(String(20), nullable=False)  # 1400-1401
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    description = Column(Text)
    total_budget = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    status = Column(Enum(BudgetStatus), default=BudgetStatus.DRAFT)
    prepared_by = Column(Integer, ForeignKey('employees.id'))
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    revision_number = Column(Integer, default=1)
    parent_budget_id = Column(Integer, ForeignKey('budgets.id'))
    budget_categories = Column(JSON)
    assumptions = Column(JSON)
    constraints = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="budgets")
    prepared_by_employee = relationship("Employee", foreign_keys=[prepared_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    parent_budget = relationship("Budget", remote_side=[id], back_populates="revisions")
    revisions = relationship("Budget", back_populates="parent_budget")
    budget_lines = relationship("BudgetLine", back_populates="budget")

class BudgetLine(Base):
    __tablename__ = 'budget_lines'

    id = Column(Integer, primary_key=True, autoincrement=True)
    budget_id = Column(Integer, ForeignKey('budgets.id'), nullable=False)
    administrative_unit_id = Column(Integer, ForeignKey('administrative_units.id'))
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100))
    description = Column(Text, nullable=False)
    description_fa = Column(Text, nullable=False)
    budgeted_amount = Column(Float, nullable=False)
    allocated_amount = Column(Float, default=0)
    spent_amount = Column(Float, default=0)
    remaining_amount = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    priority_level = Column(String(20), default='medium')  # low, medium, high, critical
    justification = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    budget = relationship("Budget", back_populates="budget_lines")
    administrative_unit = relationship("AdministrativeUnit", back_populates="budget_lines")
    transactions = relationship("Transaction", back_populates="budget_line")

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    budget_line_id = Column(Integer, ForeignKey('budget_lines.id'))
    administrative_unit_id = Column(Integer, ForeignKey('administrative_units.id'), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    exchange_rate = Column(Float, default=1.0)
    amount_irr = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    description_fa = Column(Text, nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    payment_method = Column(Enum(PaymentMethod))
    reference_number = Column(String(100))
    vendor_supplier = Column(String(255))
    invoice_number = Column(String(100))
    receipt_path = Column(String(500))
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    recorded_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    fiscal_year = Column(String(20))
    fiscal_period = Column(String(20))
    tags = Column(JSON)
    is_reconciled = Column(Boolean, default=False)
    reconciliation_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    budget_line = relationship("BudgetLine", back_populates="transactions")
    administrative_unit = relationship("AdministrativeUnit", back_populates="transactions")
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    recorded_by_employee = relationship("Employee", foreign_keys=[recorded_by])

class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    invoice_type = Column(String(50), nullable=False)  # tuition, service, penalty, etc.
    title = Column(String(255), nullable=False)
    description = Column(Text)
    issue_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    total_amount = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    tax_amount = Column(Float, default=0)
    discount_amount = Column(Float, default=0)
    paid_amount = Column(Float, default=0)
    outstanding_amount = Column(Float, nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    payment_terms = Column(String(255))
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    sent_date = Column(DateTime)
    reminder_count = Column(Integer, default=0)
    last_reminder_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="invoices")
    student = relationship("Student", foreign_keys=[student_id])
    employee = relationship("Employee", foreign_keys=[employee_id])
    created_by_employee = relationship("Employee", foreign_keys=[created_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])
    invoice_items = relationship("InvoiceItem", back_populates="invoice")
    payments = relationship("Payment", back_populates="invoice")

class InvoiceItem(Base):
    __tablename__ = 'invoice_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    item_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    quantity = Column(Float, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0)
    tax_amount = Column(Float, default=0)
    discount_rate = Column(Float, default=0)
    discount_amount = Column(Float, default=0)
    net_amount = Column(Float, nullable=False)
    reference_id = Column(Integer)  # Could reference course, service, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    invoice = relationship("Invoice", back_populates="invoice_items")

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    payment_number = Column(String(50), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    payment_date = Column(DateTime, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    reference_number = Column(String(100))
    bank_name = Column(String(255))
    account_number = Column(String(50))
    transaction_id = Column(String(100))
    receipt_path = Column(String(500))
    notes = Column(Text)
    recorded_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    verified_by = Column(Integer, ForeignKey('employees.id'))
    verification_date = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    is_reconciled = Column(Boolean, default=False)
    reconciliation_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
    student = relationship("Student", foreign_keys=[student_id])
    employee = relationship("Employee", foreign_keys=[employee_id])
    recorded_by_employee = relationship("Employee", foreign_keys=[recorded_by])
    verified_by_employee = relationship("Employee", foreign_keys=[verified_by])

class SalaryStructure(Base):
    __tablename__ = 'salary_structures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    title = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=False)
    grade = Column(String(20), nullable=False)
    level = Column(String(20))
    basic_salary = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    effective_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime)
    components = Column(JSON)
    benefits = Column(JSON)
    deductions = Column(JSON)
    total_gross = Column(Float, nullable=False)
    total_deductions = Column(Float, nullable=False)
    net_salary = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="salary_structures")
    employee_salaries = relationship("EmployeeSalary", back_populates="salary_structure")

class EmployeeSalary(Base):
    __tablename__ = 'employee_salaries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    salary_structure_id = Column(Integer, ForeignKey('salary_structures.id'), nullable=False)
    effective_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    basic_salary = Column(Float, nullable=False)
    components = Column(JSON)
    allowances = Column(JSON)
    deductions = Column(JSON)
    gross_salary = Column(Float, nullable=False)
    total_deductions = Column(Float, nullable=False)
    net_salary = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    payment_frequency = Column(String(20), default='monthly')  # monthly, bi-weekly, weekly
    bank_account = Column(String(50))
    bank_name = Column(String(255))
    tax_number = Column(String(50))
    insurance_number = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="salary")
    salary_structure = relationship("SalaryStructure", back_populates="employee_salaries")
    salary_components = relationship("SalaryComponent", back_populates="employee_salary")
    payroll_entries = relationship("PayrollEntry", back_populates="employee_salary")

class SalaryComponent(Base):
    __tablename__ = 'salary_components'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_salary_id = Column(Integer, ForeignKey('employee_salaries.id'), nullable=False)
    component_type = Column(Enum(SalaryComponentType), nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    is_taxable = Column(Boolean, default=True)
    is_deductible = Column(Boolean, default=False)
    calculation_method = Column(String(50))  # fixed, percentage, formula
    calculation_basis = Column(String(50))
    effective_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employee_salary = relationship("EmployeeSalary", back_populates="salary_components")

class PayrollEntry(Base):
    __tablename__ = 'payroll_entries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_salary_id = Column(Integer, ForeignKey('employee_salaries.id'), nullable=False)
    payroll_period = Column(String(20), nullable=False)  # 1400-01, 1400-02, etc.
    pay_date = Column(DateTime, nullable=False)
    basic_salary = Column(Float, nullable=False)
    total_allowances = Column(Float, default=0)
    total_deductions = Column(Float, default=0)
    gross_pay = Column(Float, nullable=False)
    net_pay = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    payment_method = Column(Enum(PaymentMethod))
    payment_reference = Column(String(100))
    status = Column(String(20), default='pending')  # pending, processed, paid, cancelled
    processed_by = Column(Integer, ForeignKey('employees.id'))
    processed_date = Column(DateTime)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee_salary = relationship("EmployeeSalary", back_populates="payroll_entries")
    processed_by_employee = relationship("Employee", foreign_keys=[processed_by])
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class Scholarship(Base):
    __tablename__ = 'scholarships'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    scholarship_type = Column(Enum(ScholarshipType), nullable=False)
    description = Column(Text)
    eligibility_criteria = Column(JSON)
    award_amount = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    coverage_type = Column(String(50))  # full, partial, specific_fees
    coverage_percentage = Column(Float)
    maximum_awards = Column(Integer)
    application_deadline = Column(DateTime)
    award_period_months = Column(Integer)
    renewal_criteria = Column(JSON)
    sponsoring_organization = Column(String(255))
    funding_source = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="scholarships")
    applications = relationship("ScholarshipApplication", back_populates="scholarship")
    awards = relationship("ScholarshipAward", back_populates="scholarship")

class ScholarshipApplication(Base):
    __tablename__ = 'scholarship_applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    scholarship_id = Column(Integer, ForeignKey('scholarships.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    application_date = Column(DateTime, default=datetime.utcnow)
    academic_year = Column(String(20))
    semester = Column(String(20))
    gpa = Column(Float)
    financial_need_level = Column(String(20))
    supporting_documents = Column(JSON)
    essay_response = Column(Text)
    recommendation_letters = Column(JSON)
    status = Column(String(20), default='submitted')  # submitted, under_review, approved, rejected, awarded
    review_date = Column(DateTime)
    reviewed_by = Column(Integer, ForeignKey('employees.id'))
    review_notes = Column(Text)
    award_amount = Column(Float)
    award_start_date = Column(DateTime)
    award_end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    scholarship = relationship("Scholarship", back_populates="applications")
    student = relationship("Student", foreign_keys=[student_id])
    reviewed_by_employee = relationship("Employee", foreign_keys=[reviewed_by])

class ScholarshipAward(Base):
    __tablename__ = 'scholarship_awards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    scholarship_id = Column(Integer, ForeignKey('scholarships.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    application_id = Column(Integer, ForeignKey('scholarship_applications.id'))
    award_date = Column(DateTime, nullable=False)
    award_amount = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    award_period_start = Column(DateTime, nullable=False)
    award_period_end = Column(DateTime, nullable=False)
    payment_schedule = Column(JSON)
    disbursement_method = Column(String(50))
    conditions = Column(JSON)
    renewal_required = Column(Boolean, default=False)
    renewal_date = Column(DateTime)
    status = Column(String(20), default='active')  # active, suspended, terminated, completed
    termination_reason = Column(String(255))
    total_disbursed = Column(Float, default=0)
    remaining_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    scholarship = relationship("Scholarship", back_populates="awards")
    student = relationship("Student", foreign_keys=[student_id])
    application = relationship("ScholarshipApplication", foreign_keys=[application_id])
    disbursements = relationship("ScholarshipDisbursement", back_populates="award")

class ScholarshipDisbursement(Base):
    __tablename__ = 'scholarship_disbursements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    award_id = Column(Integer, ForeignKey('scholarship_awards.id'), nullable=False)
    disbursement_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    payment_method = Column(Enum(PaymentMethod))
    reference_number = Column(String(100))
    academic_year = Column(String(20))
    semester = Column(String(20))
    purpose = Column(String(255))
    approved_by = Column(Integer, ForeignKey('employees.id'))
    approval_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    award = relationship("ScholarshipAward", back_populates="disbursements")
    approved_by_employee = relationship("Employee", foreign_keys=[approved_by])

class FeeStructure(Base):
    __tablename__ = 'fee_structures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    academic_program_id = Column(Integer, ForeignKey('academic_programs.id'))
    fee_type = Column(Enum(FeeType), nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    academic_year = Column(String(20), nullable=False)
    semester = Column(String(20))
    payment_deadline = Column(DateTime)
    late_payment_penalty = Column(Float, default=0)
    installment_allowed = Column(Boolean, default=False)
    max_installments = Column(Integer)
    installment_schedule = Column(JSON)
    discount_eligible = Column(Boolean, default=False)
    discount_criteria = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="fee_structures")
    academic_program = relationship("AcademicProgram", back_populates="fee_structures")

class StudentFee(Base):
    __tablename__ = 'student_fees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey('fee_structures.id'), nullable=False)
    academic_year = Column(String(20), nullable=False)
    semester = Column(String(20))
    amount_due = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0)
    outstanding_amount = Column(Float, nullable=False)
    currency = Column(Enum(Currency), default=Currency.IRR)
    due_date = Column(DateTime, nullable=False)
    payment_deadline = Column(DateTime)
    late_payment_penalty = Column(Float, default=0)
    discount_applied = Column(Float, default=0)
    discount_reason = Column(String(255))
    installment_plan = Column(JSON)
    status = Column(String(20), default='unpaid')  # unpaid, partially_paid, paid, overdue, waived
    waiver_reason = Column(String(255))
    waiver_approved_by = Column(Integer, ForeignKey('employees.id'))
    waiver_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="fees")
    fee_structure = relationship("FeeStructure", back_populates="student_fees")
    waiver_approved_by_employee = relationship("Employee", foreign_keys=[waiver_approved_by])

class FinancialAid(Base):
    __tablename__ = 'financial_aid'

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.id'), nullable=False)
    name = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    aid_type = Column(String(50), nullable=False)  # grant, loan, work_study, etc.
    description = Column(Text)
    eligibility_criteria = Column(JSON)
    maximum_amount = Column(Float)
    currency = Column(Enum(Currency), default=Currency.IRR)
    application_deadline = Column(DateTime)
    award_period_months = Column(Integer)
    repayment_required = Column(Boolean, default=False)
    repayment_terms = Column(JSON)
    sponsoring_organization = Column(String(255))
    funding_source = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    university = relationship("University", back_populates="financial_aid")
    applications = relationship("FinancialAidApplication", back_populates="financial_aid")

class FinancialAidApplication(Base):
    __tablename__ = 'financial_aid_applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    financial_aid_id = Column(Integer, ForeignKey('financial_aid.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    application_date = Column(DateTime, default=datetime.utcnow)
    academic_year = Column(String(20))
    financial_need_level = Column(String(20))
    household_income = Column(Float)
    supporting_documents = Column(JSON)
    status = Column(String(20), default='submitted')  # submitted, under_review, approved, rejected, awarded
    review_date = Column(DateTime)
    reviewed_by = Column(Integer, ForeignKey('employees.id'))
    review_notes = Column(Text)
    award_amount = Column(Float)
    award_start_date = Column(DateTime)
    award_end_date = Column(DateTime)
    disbursement_schedule = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    financial_aid = relationship("FinancialAid", back_populates="applications")
    student = relationship("Student", foreign_keys=[student_id])
    reviewed_by_employee = relationship("Employee", foreign_keys=[reviewed_by])

class TaxRecord(Base):
    __tablename__ = 'tax_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    tax_year = Column(String(20), nullable=False)  # 1400
    taxable_income = Column(Float, nullable=False)
    tax_paid = Column(Float, default=0)
    tax_owed = Column(Float, default=0)
    tax_refund = Column(Float, default=0)
    currency = Column(Enum(Currency), default=Currency.IRR)
    tax_brackets = Column(JSON)
    deductions = Column(JSON)
    credits = Column(JSON)
    filing_date = Column(DateTime)
    filing_status = Column(String(20), default='pending')  # pending, filed, processed, amended
    tax_authority_reference = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="tax_records")

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(String(20), nullable=False)  # INSERT, UPDATE, DELETE
    old_values = Column(JSON)
    new_values = Column(JSON)
    changed_by = Column(Integer, ForeignKey('employees.id'), nullable=False)
    change_reason = Column(String(255))
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    changed_by_employee = relationship("Employee", foreign_keys=[changed_by])
```

## Pydantic Schemas برای سیستم مالی

```python
# app/schemas/financial.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class Currency(str, Enum):
    IRR = "ریال"
    USD = "دلار آمریکا"
    EUR = "یورو"
    GBP = "پوند انگلیس"
    AED = "درهم امارات"

class PaymentMethod(str, Enum):
    CASH = "نقدی"
    CHECK = "چک"
    BANK_TRANSFER = "انتقال بانکی"
    CREDIT_CARD = "کارت اعتباری"
    ONLINE_PAYMENT = "پرداخت آنلاین"
    WIRE_TRANSFER = "انتقال سیمی"

class TransactionType(str, Enum):
    INCOME = "درآمد"
    EXPENSE = "هزینه"
    TRANSFER = "انتقال"
    ADJUSTMENT = "تطبیق"

class BudgetStatus(str, Enum):
    DRAFT = "پیش‌نویس"
    SUBMITTED = "ارائه شده"
    APPROVED = "تایید شده"
    REJECTED = "رد شده"
    ACTIVE = "فعال"
    CLOSED = "بسته شده"

class InvoiceStatus(str, Enum):
    DRAFT = "پیش‌نویس"
    SENT = "ارسال شده"
    PAID = "پرداخت شده"
    OVERDUE = "سررسید گذشته"
    CANCELLED = "لغو شده"

class SalaryComponentType(str, Enum):
    BASIC_SALARY = "حقوق پایه"
    HOUSING_ALLOWANCE = "کمک مسکن"
    TRANSPORT_ALLOWANCE = "کمک حمل و نقل"
    MEAL_ALLOWANCE = "کمک تغذیه"
    OVERTIME = "اضافه کاری"
    BONUS = "پاداش"
    COMMISSION = "کمیسیون"
    TAX_DEDUCTION = "کسر مالیات"
    INSURANCE_DEDUCTION = "کسر بیمه"
    LOAN_DEDUCTION = "کسر وام"
    OTHER_ALLOWANCE = "سایر کمک‌ها"
    OTHER_DEDUCTION = "سایر کسورات"

class ScholarshipType(str, Enum):
    MERIT_BASED = "بر اساس شایستگی"
    NEED_BASED = "بر اساس نیاز"
    ATHLETIC = "ورزشی"
    RESEARCH = "پژوهشی"
    INTERNATIONAL = "بین‌المللی"
    SPECIAL_PROGRAM = "برنامه ویژه"

class FeeType(str, Enum):
    TUITION_FEE = "شهریه"
    REGISTRATION_FEE = "هزینه ثبت نام"
    EXAMINATION_FEE = "هزینه آزمون"
    LATE_PAYMENT_FEE = "جریمه تأخیر"
    LIBRARY_FEE = "هزینه کتابخانه"
    LABORATORY_FEE = "هزینه آزمایشگاه"
    SPORTS_FEE = "هزینه ورزشی"
    HEALTH_FEE = "هزینه بهداشتی"
    STUDENT_ACTIVITY_FEE = "هزینه فعالیت‌های دانشجویی"
    OTHER_FEE = "سایر هزینه‌ها"

# Budget schemas
class BudgetBase(BaseModel):
    fiscal_year: str = Field(..., min_length=1, max_length=20)
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    total_budget: float = Field(..., gt=0)
    currency: Currency = Currency.IRR
    start_date: datetime
    end_date: datetime
    budget_categories: Optional[Dict[str, Any]] = None
    assumptions: Optional[Dict[str, Any]] = None
    constraints: Optional[Dict[str, Any]] = None

class BudgetCreate(BudgetBase):
    university_id: int

class BudgetUpdate(BaseModel):
    fiscal_year: Optional[str] = Field(None, min_length=1, max_length=20)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    total_budget: Optional[float] = Field(None, gt=0)
    currency: Optional[Currency] = None
    status: Optional[BudgetStatus] = None
    prepared_by: Optional[int] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    revision_number: Optional[int] = None
    parent_budget_id: Optional[int] = None
    budget_categories: Optional[Dict[str, Any]] = None
    assumptions: Optional[Dict[str, Any]] = None
    constraints: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class Budget(BudgetBase):
    id: int
    university_id: int
    status: BudgetStatus
    prepared_by: Optional[int] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    revision_number: int
    parent_budget_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BudgetWithDetails(Budget):
    university: Optional[Dict[str, Any]] = None
    prepared_by_employee: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None
    budget_lines_count: int = 0
    total_allocated: float = 0
    total_spent: float = 0

# Transaction schemas
class TransactionBase(BaseModel):
    transaction_type: TransactionType
    amount: float = Field(..., gt=0)
    currency: Currency = Currency.IRR
    exchange_rate: float = 1.0
    description: str = Field(..., min_length=1)
    description_fa: str = Field(..., min_length=1)
    transaction_date: datetime
    payment_method: Optional[PaymentMethod] = None
    reference_number: Optional[str] = None
    vendor_supplier: Optional[str] = None
    invoice_number: Optional[str] = None
    receipt_path: Optional[str] = None
    fiscal_year: Optional[str] = None
    fiscal_period: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    administrative_unit_id: int
    budget_line_id: Optional[int] = None

class TransactionUpdate(BaseModel):
    transaction_type: Optional[TransactionType] = None
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[Currency] = None
    exchange_rate: Optional[float] = None
    description: Optional[str] = Field(None, min_length=1)
    description_fa: Optional[str] = Field(None, min_length=1)
    transaction_date: Optional[datetime] = None
    payment_method: Optional[PaymentMethod] = None
    reference_number: Optional[str] = None
    vendor_supplier: Optional[str] = None
    invoice_number: Optional[str] = None
    receipt_path: Optional[str] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    fiscal_year: Optional[str] = None
    fiscal_period: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None
    is_reconciled: Optional[bool] = None
    reconciliation_date: Optional[datetime] = None
    notes: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    administrative_unit_id: int
    budget_line_id: Optional[int] = None
    amount_irr: float
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    recorded_by: int
    is_reconciled: bool
    reconciliation_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TransactionWithDetails(Transaction):
    administrative_unit: Optional[Dict[str, Any]] = None
    budget_line: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None
    recorded_by_employee: Optional[Dict[str, Any]] = None

# Invoice schemas
class InvoiceBase(BaseModel):
    invoice_number: str = Field(..., min_length=1, max_length=50)
    invoice_type: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    issue_date: datetime
    due_date: datetime
    total_amount: float = Field(..., ge=0)
    currency: Currency = Currency.IRR
    tax_amount: float = 0
    discount_amount: float = 0
    payment_terms: Optional[str] = None
    notes: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    university_id: int
    student_id: Optional[int] = None
    employee_id: Optional[int] = None

class InvoiceUpdate(BaseModel):
    invoice_number: Optional[str] = Field(None, min_length=1, max_length=50)
    invoice_type: Optional[str] = Field(None, min_length=1, max_length=50)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    issue_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    total_amount: Optional[float] = Field(None, ge=0)
    currency: Optional[Currency] = None
    tax_amount: Optional[float] = None
    discount_amount: Optional[float] = None
    status: Optional[InvoiceStatus] = None
    payment_terms: Optional[str] = None
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    sent_date: Optional[datetime] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class Invoice(InvoiceBase):
    id: int
    university_id: int
    student_id: Optional[int] = None
    employee_id: Optional[int] = None
    paid_amount: float
    outstanding_amount: float
    status: InvoiceStatus
    created_by: int
    approved_by: Optional[int] = None
    approval_date: Optional[datetime] = None
    sent_date: Optional[datetime] = None
    reminder_count: int
    last_reminder_date: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InvoiceWithDetails(Invoice):
    university: Optional[Dict[str, Any]] = None
    student: Optional[Dict[str, Any]] = None
    employee: Optional[Dict[str, Any]] = None
    created_by_employee: Optional[Dict[str, Any]] = None
    approved_by_employee: Optional[Dict[str, Any]] = None
    items_count: int = 0
    payments_count: int = 0

# Payment schemas
class PaymentBase(BaseModel):
    payment_number: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    currency: Currency = Currency.IRR
    payment_date: datetime
    payment_method: PaymentMethod
    reference_number: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    transaction_id: Optional[str] = None
    receipt_path: Optional[str] = None
    notes: Optional[str] = None

class PaymentCreate(PaymentBase):
    invoice_id: Optional[int] = None
    student_id: Optional[int] = None
    employee_id: Optional[int] = None

class PaymentUpdate(BaseModel):
    payment_number: Optional[str] = Field(None, min_length=1, max_length=50)
    amount: Optional[float] = Field(None, gt=0)
    currency: Optional[Currency] = None
    payment_date: Optional[datetime] = None
    payment_method: Optional[PaymentMethod] = None
    reference_number: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    transaction_id: Optional[str] = None
    receipt_path: Optional[str] = None
    verified_by: Optional[int] = None
    verification_date: Optional[datetime] = None
    is_verified: Optional[bool] = None
    is_reconciled: Optional[bool] = None
    reconciliation_date: Optional[datetime] = None
    notes: Optional[str] = None

class Payment(PaymentBase):
    id: int
    invoice_id: Optional[int] = None
    student_id: Optional[int] = None
    employee_id: Optional[int] = None
    recorded_by: int
    verified_by: Optional[int] = None
    verification_date: Optional[datetime] = None
    is_verified: bool
    is_reconciled: bool
    reconciliation_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaymentWithDetails(Payment):
    invoice: Optional[Dict[str, Any]] = None
    student: Optional[Dict[str, Any]] = None
    employee: Optional[Dict[str, Any]] = None
    recorded_by_employee: Optional[Dict[str, Any]] = None
    verified_by_employee: Optional[Dict[str, Any]] = None

# Salary Structure schemas
class SalaryStructureBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    title_fa: str = Field(..., min_length=1, max_length=255)
    grade: str = Field(..., min_length=1, max_length=20)
    level: Optional[str] = None
    basic_salary: float = Field(..., gt=0)
    currency: Currency = Currency.IRR
    effective_date: datetime
    expiry_date: Optional[datetime] = None
    components: Optional[Dict[str, Any]] = None
    benefits: Optional[Dict[str, Any]] = None
    deductions: Optional[Dict[str, Any]] = None

class SalaryStructureCreate(SalaryStructureBase):
    university_id: int

class SalaryStructureUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    title_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    grade: Optional[str] = Field(None, min_length=1, max_length=20)
    level: Optional[str] = None
    basic_salary: Optional[float] = Field(None, gt=0)
    currency: Optional[Currency] = None
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    components: Optional[Dict[str, Any]] = None
    benefits: Optional[Dict[str, Any]] = None
    deductions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class SalaryStructure(SalaryStructureBase):
    id: int
    university_id: int
    total_gross: float
    total_deductions: float
    net_salary: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SalaryStructureWithDetails(SalaryStructure):
    university: Optional[Dict[str, Any]] = None
    employee_count: int = 0

# Scholarship schemas
class ScholarshipBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    scholarship_type: ScholarshipType
    description: Optional[str] = None
    eligibility_criteria: Optional[Dict[str, Any]] = None
    award_amount: float = Field(..., gt=0)
    currency: Currency = Currency.IRR
    coverage_type: Optional[str] = None
    coverage_percentage: Optional[float] = None
    maximum_awards: Optional[int] = None
    application_deadline: Optional[datetime] = None
    award_period_months: Optional[int] = None
    renewal_criteria: Optional[Dict[str, Any]] = None
    sponsoring_organization: Optional[str] = None
    funding_source: Optional[str] = None

class ScholarshipCreate(ScholarshipBase):
    university_id: int

class ScholarshipUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    scholarship_type: Optional[ScholarshipType] = None
    description: Optional[str] = None
    eligibility_criteria: Optional[Dict[str, Any]] = None
    award_amount: Optional[float] = Field(None, gt=0)
    currency: Optional[Currency] = None
    coverage_type: Optional[str] = None
    coverage_percentage: Optional[float] = None
    maximum_awards: Optional[int] = None
    application_deadline: Optional[datetime] = None
    award_period_months: Optional[int] = None
    renewal_criteria: Optional[Dict[str, Any]] = None
    sponsoring_organization: Optional[str] = None
    funding_source: Optional[str] = None
    is_active: Optional[bool] = None

class Scholarship(ScholarshipBase):
    id: int
    university_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ScholarshipWithDetails(Scholarship):
    university: Optional[Dict[str, Any]] = None
    applications_count: int = 0
    awards_count: int = 0

# Fee Structure schemas
class FeeStructureBase(BaseModel):
    fee_type: FeeType
    name: str = Field(..., min_length=1, max_length=255)
    name_fa: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., ge=0)
    currency: Currency = Currency.IRR
    academic_year: str = Field(..., min_length=1, max_length=20)
    semester: Optional[str] = None
    payment_deadline: Optional[datetime] = None
    late_payment_penalty: float = 0
    installment_allowed: bool = False
    max_installments: Optional[int] = None
    installment_schedule: Optional[Dict[str, Any]] = None
    discount_eligible: bool = False
    discount_criteria: Optional[Dict[str, Any]] = None

class FeeStructureCreate(FeeStructureBase):
    university_id: int
    academic_program_id: Optional[int] = None

class FeeStructureUpdate(BaseModel):
    fee_type: Optional[FeeType] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    name_fa: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[float] = Field(None, ge=0)
    currency: Optional[Currency] = None
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    semester: Optional[str] = None
    payment_deadline: Optional[datetime] = None
    late_payment_penalty: Optional[float] = None
    installment_allowed: Optional[bool] = None
    max_installments: Optional[int] = None
    installment_schedule: Optional[Dict[str, Any]] = None
    discount_eligible: Optional[bool] = None
    discount_criteria: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class FeeStructure(FeeStructureBase):
    id: int
    university_id: int
    academic_program_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FeeStructureWithDetails(FeeStructure):
    university: Optional[Dict[str, Any]] = None
    academic_program: Optional[Dict[str, Any]] = None

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
class BudgetSearchFilters(BaseModel):
    university_id: Optional[int] = None
    fiscal_year: Optional[str] = None
    status: Optional[BudgetStatus] = None
    prepared_by: Optional[int] = None
    approved_by: Optional[int] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

class TransactionSearchFilters(BaseModel):
    administrative_unit_id: Optional[int] = None
    budget_line_id: Optional[int] = None
    transaction_type: Optional[TransactionType] = None
    payment_method: Optional[PaymentMethod] = None
    recorded_by: Optional[int] = None
    approved_by: Optional[int] = None
    fiscal_year: Optional[str] = None
    fiscal_period: Optional[str] = None
    is_reconciled: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    search: Optional[str] = None

class InvoiceSearchFilters(BaseModel):
    university_id: Optional[int] = None
    student_id: Optional[int] = None
    employee_id: Optional[int] = None
    status: Optional[InvoiceStatus] = None
    invoice_type: Optional[str] = None
    created_by: Optional[int] = None
    approved_by: Optional[int] = None
    is_active: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    search: Optional[str] = None

class PaymentSearchFilters(BaseModel):
    invoice_id: Optional[int] = None
    student_id: Optional[int] = None
    employee_id: Optional[int] = None
    payment_method: Optional[PaymentMethod] = None
    recorded_by: Optional[int] = None
    verified_by: Optional[int] = None
    is_verified: Optional[bool] = None
    is_reconciled: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    search: Optional[str] = None

class ScholarshipSearchFilters(BaseModel):
    university_id: Optional[int] = None
    scholarship_type: Optional[ScholarshipType] = None
    is_active: Optional[bool] = None
    award_amount_min: Optional[float] = None
    award_amount_max: Optional[float] = None
    search: Optional[str] = None

class FeeStructureSearchFilters(BaseModel):
    university_id: Optional[int] = None
    academic_program_id: Optional[int] = None
    fee_type: Optional[FeeType] = None
    academic_year: Optional[str] = None
    semester: Optional[str] = None
    is_active: Optional[bool] = None
    amount_min: Optional[float] = None
    amount_max: Optional[float] = None
    search: Optional[str] = None
```

این پیاده‌سازی کامل مدل‌های مالی و بودجه‌ای شامل تمام ویژگی‌های مورد نیاز برای سیستم مالی دانشگاهی ایران است.
