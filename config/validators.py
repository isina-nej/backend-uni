# ==============================================================================
# ADVANCED VALIDATORS FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

import re
from datetime import date, datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.users.models import User


def validate_national_id(value):
    """Validate Iranian national ID"""
    if not value:
        return

    # Remove any non-digit characters
    national_id = re.sub(r'\D', '', str(value))

    if len(national_id) != 10:
        raise ValidationError(_('National ID must be exactly 10 digits'))

    # Check if all digits are the same
    if len(set(national_id)) == 1:
        raise ValidationError(_('Invalid national ID format'))

    # Calculate checksum
    checksum = 0
    for i in range(9):
        checksum += int(national_id[i]) * (10 - i)

    remainder = checksum % 11
    control_digit = int(national_id[9])

    if remainder < 2:
        if control_digit != remainder:
            raise ValidationError(_('Invalid national ID checksum'))
    else:
        if control_digit != (11 - remainder):
            raise ValidationError(_('Invalid national ID checksum'))

    return national_id


def validate_phone_number(value):
    """Validate phone number format"""
    if not value:
        return

    # Remove spaces and hyphens
    phone = re.sub(r'[\s\-]', '', str(value))

    # Iranian mobile number patterns
    mobile_patterns = [
        r'^09\d{9}$',  # 09123456789
        r'^\+989\d{9}$',  # +989123456789
        r'^989\d{9}$',  # 989123456789
    ]

    # Iranian landline patterns
    landline_patterns = [
        r'^0[1-8]\d{9}$',  # 02112345678
        r'^\+98[1-8]\d{9}$',  # +982112345678
    ]

    is_valid = False
    for pattern in mobile_patterns + landline_patterns:
        if re.match(pattern, phone):
            is_valid = True
            break

    if not is_valid:
        raise ValidationError(_('Invalid phone number format'))

    return phone


def validate_email_domain(value):
    """Validate email domain for university emails"""
    if not value:
        return

    # University email domains
    allowed_domains = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
        'university.edu', 'uni.ac.ir', 'ut.ac.ir', 'sharif.edu',
        'tehran.ac.ir', 'iust.ac.ir', 'aut.ac.ir'
    ]

    domain = value.split('@')[-1].lower()

    if domain not in allowed_domains:
        # Allow any .ac.ir or .edu domain
        if not (domain.endswith('.ac.ir') or domain.endswith('.edu')):
            raise ValidationError(_('Email domain not allowed'))

    return value


def validate_birth_date(value):
    """Validate birth date"""
    if not value:
        return

    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if age < 15:
        raise ValidationError(_('User must be at least 15 years old'))

    if age > 100:
        raise ValidationError(_('Invalid birth date'))

    return value


def validate_course_capacity(current_students, max_capacity=50):
    """Validate course capacity"""
    if current_students > max_capacity:
        raise ValidationError(_(f'Course capacity exceeded. Maximum: {max_capacity}'))

    return current_students


def validate_unique_enrollment(student, course):
    """Validate unique enrollment"""
    if course.students.filter(id=student.id).exists():
        raise ValidationError(_('Student is already enrolled in this course'))

    return True


def validate_professor_qualification(professor, course):
    """Validate professor qualification for course"""
    if not professor.employee:
        raise ValidationError(_('Professor must have employee profile'))

    # Check if professor has required qualifications
    required_qualifications = ['PhD', 'Master', 'Bachelor']
    if professor.employee.highest_degree not in required_qualifications:
        raise ValidationError(_('Professor does not have required qualifications'))

    return True


def validate_schedule_conflict(user, new_schedule):
    """Validate schedule conflicts"""
    from apps.schedules.models import Schedule

    # Check for time conflicts
    conflicting_schedules = Schedule.objects.filter(
        user=user,
        day_of_week=new_schedule.day_of_week,
        start_time__lt=new_schedule.end_time,
        end_time__gt=new_schedule.start_time
    ).exclude(id=getattr(new_schedule, 'id', None))

    if conflicting_schedules.exists():
        raise ValidationError(_('Schedule conflict detected'))

    return True


def validate_exam_date(exam_date, course):
    """Validate exam date"""
    if exam_date < course.created_at.date():
        raise ValidationError(_('Exam date cannot be before course creation date'))

    # Exam should be within course duration
    if hasattr(course, 'end_date') and exam_date > course.end_date:
        raise ValidationError(_('Exam date cannot be after course end date'))

    return exam_date


def validate_grade_range(grade):
    """Validate grade range"""
    if not (0 <= grade <= 20):
        raise ValidationError(_('Grade must be between 0 and 20'))

    return grade


def validate_attendance_percentage(attendance_percentage):
    """Validate attendance percentage"""
    if not (0 <= attendance_percentage <= 100):
        raise ValidationError(_('Attendance percentage must be between 0 and 100'))

    return attendance_percentage


def validate_file_size(file, max_size_mb=10):
    """Validate file size"""
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(_(f'File size cannot exceed {max_size_mb}MB'))

    return file


def validate_file_extension(file, allowed_extensions):
    """Validate file extension"""
    extension = file.name.split('.')[-1].lower()
    if extension not in allowed_extensions:
        raise ValidationError(_(f'File extension .{extension} not allowed. Allowed: {", ".join(allowed_extensions)}'))

    return file


# Custom field validators for serializers
class AdvancedValidators:
    """Collection of advanced validation methods"""

    @staticmethod
    def validate_student_registration(data):
        """Validate student registration data"""
        errors = {}

        # Validate national ID
        try:
            validate_national_id(data.get('national_id'))
        except ValidationError as e:
            errors['national_id'] = str(e)

        # Validate phone
        try:
            validate_phone_number(data.get('phone'))
        except ValidationError as e:
            errors['phone'] = str(e)

        # Validate email
        try:
            validate_email_domain(data.get('email'))
        except ValidationError as e:
            errors['email'] = str(e)

        # Validate birth date
        try:
            validate_birth_date(data.get('birth_date'))
        except ValidationError as e:
            errors['birth_date'] = str(e)

        if errors:
            raise ValidationError(errors)

        return data

    @staticmethod
    def validate_course_enrollment(student, course):
        """Validate course enrollment"""
        errors = []

        # Check capacity
        try:
            validate_course_capacity(course.students.count() + 1)
        except ValidationError as e:
            errors.append(str(e))

        # Check unique enrollment
        try:
            validate_unique_enrollment(student, course)
        except ValidationError as e:
            errors.append(str(e))

        if errors:
            raise ValidationError(' '.join(errors))

        return True

    @staticmethod
    def validate_employee_assignment(employee, position):
        """Validate employee position assignment"""
        if not employee.user:
            raise ValidationError(_('Employee must be linked to a user'))

        # Check position requirements
        if hasattr(position, 'required_degree') and employee.highest_degree != position.required_degree:
            raise ValidationError(_('Employee does not meet position degree requirements'))

        return True
