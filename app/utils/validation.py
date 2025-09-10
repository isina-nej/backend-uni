# app/utils/validation.py
import re
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from pydantic import BaseModel, validator, ValidationError
import logging

logger = logging.getLogger(__name__)

class ValidationResult(BaseModel):
    """Result of validation"""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []

    def add_error(self, error: str):
        """Add validation error"""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str):
        """Add validation warning"""
        self.warnings.append(warning)

class EmailValidator:
    """Email validation utilities"""

    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        return re.match(EmailValidator.EMAIL_REGEX, email) is not None

    @staticmethod
    def validate_university_email(email: str, university_domain: Optional[str] = None) -> ValidationResult:
        """Validate university email"""
        result = ValidationResult(is_valid=True)

        if not EmailValidator.is_valid_email(email):
            result.add_error("Invalid email format")
            return result

        if university_domain and not email.endswith(f"@{university_domain}"):
            result.add_warning(f"Email domain does not match university domain: {university_domain}")

        return result

class PhoneValidator:
    """Phone number validation utilities"""

    IRAN_PHONE_REGEX = r'^(\+98|0)?9\d{9}$'
    INTERNATIONAL_PHONE_REGEX = r'^\+?[1-9]\d{1,14}$'

    @staticmethod
    def is_valid_iranian_phone(phone: str) -> bool:
        """Validate Iranian phone number"""
        # Remove spaces and hyphens
        clean_phone = re.sub(r'[\s\-]', '', phone)
        return re.match(PhoneValidator.IRAN_PHONE_REGEX, clean_phone) is not None

    @staticmethod
    def is_valid_international_phone(phone: str) -> bool:
        """Validate international phone number"""
        return re.match(PhoneValidator.INTERNATIONAL_PHONE_REGEX, phone) is not None

    @staticmethod
    def normalize_phone(phone: str) -> str:
        """Normalize phone number"""
        # Remove spaces and hyphens
        clean_phone = re.sub(r'[\s\-]', '', phone)

        # Add +98 prefix for Iranian numbers if missing
        if clean_phone.startswith('9') and len(clean_phone) == 10:
            clean_phone = f"+98{clean_phone}"
        elif clean_phone.startswith('09') and len(clean_phone) == 11:
            clean_phone = f"+98{clean_phone[1:]}"

        return clean_phone

class NationalIdValidator:
    """Iranian national ID validation utilities"""

    @staticmethod
    def is_valid_national_id(national_id: str) -> bool:
        """Validate Iranian national ID"""
        if not national_id or len(national_id) != 10:
            return False

        if not national_id.isdigit():
            return False

        # Check for repeated digits
        if national_id == national_id[0] * 10:
            return False

        # Calculate checksum
        checksum = 0
        for i in range(9):
            checksum += int(national_id[i]) * (10 - i)

        remainder = checksum % 11
        if remainder < 2:
            expected_check = remainder
        else:
            expected_check = 11 - remainder

        return int(national_id[9]) == expected_check

class PasswordValidator:
    """Password validation utilities"""

    @staticmethod
    def validate_password_strength(password: str) -> ValidationResult:
        """Validate password strength"""
        result = ValidationResult(is_valid=True)

        if len(password) < 8:
            result.add_error("Password must be at least 8 characters long")

        if not re.search(r'[A-Z]', password):
            result.add_error("Password must contain at least one uppercase letter")

        if not re.search(r'[a-z]', password):
            result.add_error("Password must contain at least one lowercase letter")

        if not re.search(r'\d', password):
            result.add_error("Password must contain at least one digit")

        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
            result.add_warning("Password should contain at least one special character")

        # Calculate strength score
        strength_score = 0
        checks = [
            len(password) >= 8,
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'[a-z]', password)),
            bool(re.search(r'\d', password)),
            bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password))
        ]

        strength_score = sum(checks)

        if strength_score < 3:
            result.add_warning("Password strength is weak")
        elif strength_score < 4:
            result.add_warning("Password strength is medium")

        return result

class DateValidator:
    """Date validation utilities"""

    @staticmethod
    def is_valid_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
        """Validate date string"""
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_adult(birth_date: date, adult_age: int = 18) -> bool:
        """Check if person is adult"""
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age >= adult_age

    @staticmethod
    def validate_academic_year(academic_year: str) -> ValidationResult:
        """Validate academic year format"""
        result = ValidationResult(is_valid=True)

        # Expected format: YYYY-YYYY (e.g., 2023-2024)
        if not re.match(r'^\d{4}-\d{4}$', academic_year):
            result.add_error("Academic year must be in format YYYY-YYYY")
            return result

        start_year, end_year = map(int, academic_year.split('-'))

        if end_year != start_year + 1:
            result.add_error("Academic year end must be start year + 1")

        if start_year > datetime.now().year:
            result.add_warning("Academic year start is in the future")

        return result

class FileValidator:
    """File validation utilities"""

    ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    ALLOWED_DOCUMENT_TYPES = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain'
    ]
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    @staticmethod
    def validate_image_file(file_content: bytes, filename: str, max_size: int = MAX_FILE_SIZE) -> ValidationResult:
        """Validate image file"""
        result = ValidationResult(is_valid=True)

        if len(file_content) > max_size:
            result.add_error(f"File size exceeds maximum allowed size of {max_size} bytes")

        # Check file extension
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            result.add_error("Invalid image file extension")

        return result

    @staticmethod
    def validate_document_file(file_content: bytes, filename: str, max_size: int = MAX_FILE_SIZE) -> ValidationResult:
        """Validate document file"""
        result = ValidationResult(is_valid=True)

        if len(file_content) > max_size:
            result.add_error(f"File size exceeds maximum allowed size of {max_size} bytes")

        # Check file extension
        if not filename.lower().endswith(('.pdf', '.doc', '.docx', '.txt')):
            result.add_error("Invalid document file extension")

        return result

class DataValidator:
    """General data validation utilities"""

    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> ValidationResult:
        """Validate required fields"""
        result = ValidationResult(is_valid=True)

        for field in required_fields:
            if field not in data or data[field] is None or str(data[field]).strip() == "":
                result.add_error(f"Field '{field}' is required")

        return result

    @staticmethod
    def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
        """Sanitize string input"""
        if not text:
            return ""

        # Remove leading/trailing whitespace
        sanitized = text.strip()

        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>]', '', sanitized)

        # Truncate if max_length specified
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized

    @staticmethod
    def validate_range(value: float, min_value: Optional[float] = None, max_value: Optional[float] = None) -> ValidationResult:
        """Validate numeric range"""
        result = ValidationResult(is_valid=True)

        if min_value is not None and value < min_value:
            result.add_error(f"Value must be greater than or equal to {min_value}")

        if max_value is not None and value > max_value:
            result.add_error(f"Value must be less than or equal to {max_value}")

        return result

# Common validation functions
def validate_user_data(user_data: Dict[str, Any]) -> ValidationResult:
    """Validate user data"""
    result = ValidationResult(is_valid=True)

    # Email validation
    if 'email' in user_data:
        email_result = EmailValidator.validate_university_email(user_data['email'])
        result.errors.extend(email_result.errors)
        result.warnings.extend(email_result.warnings)
        if not email_result.is_valid:
            result.is_valid = False

    # Phone validation
    if 'phone' in user_data:
        if not PhoneValidator.is_valid_international_phone(user_data['phone']):
            result.add_error("Invalid phone number format")

    # National ID validation
    if 'national_id' in user_data:
        if not NationalIdValidator.is_valid_national_id(user_data['national_id']):
            result.add_error("Invalid national ID")

    # Password validation
    if 'password' in user_data:
        password_result = PasswordValidator.validate_password_strength(user_data['password'])
        result.errors.extend(password_result.errors)
        result.warnings.extend(password_result.warnings)
        if not password_result.is_valid:
            result.is_valid = False

    return result

def validate_student_data(student_data: Dict[str, Any]) -> ValidationResult:
    """Validate student data"""
    result = ValidationResult(is_valid=True)

    # Basic user validation
    user_result = validate_user_data(student_data)
    result.errors.extend(user_result.errors)
    result.warnings.extend(user_result.warnings)
    if not user_result.is_valid:
        result.is_valid = False

    # Student-specific validations
    if 'student_id' in student_data:
        if not re.match(r'^\d{8,10}$', str(student_data['student_id'])):
            result.add_error("Invalid student ID format")

    if 'enrollment_date' in student_data:
        if not DateValidator.is_valid_date(student_data['enrollment_date']):
            result.add_error("Invalid enrollment date")

    if 'gpa' in student_data:
        gpa_result = DataValidator.validate_range(student_data['gpa'], 0.0, 4.0)
        result.errors.extend(gpa_result.errors)
        if not gpa_result.is_valid:
            result.is_valid = False

    return result
