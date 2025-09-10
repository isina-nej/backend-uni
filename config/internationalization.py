# ==============================================================================
# INTERNATIONALIZATION CONFIGURATION FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os


# Language configurations
LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Persian')),
    ('ar', _('Arabic')),
]

LANGUAGE_CODE = 'fa'  # Default to Persian
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Locale paths
LOCALE_PATHS = [
    os.path.join(settings.BASE_DIR, 'locale'),
]

# Persian (Farsi) specific configurations
PERSIAN_CALENDAR = True
PERSIAN_DIGITS = True

# Date and time formats for Persian
if LANGUAGE_CODE == 'fa':
    DATE_FORMAT = 'Y/m/d'
    DATETIME_FORMAT = 'Y/m/d H:i'
    TIME_FORMAT = 'H:i'
    SHORT_DATE_FORMAT = 'Y/m/d'
    SHORT_DATETIME_FORMAT = 'Y/m/d H:i'


# Custom translation for university-specific terms
UNIVERSITY_TRANSLATIONS = {
    'en': {
        'student': 'Student',
        'professor': 'Professor',
        'course': 'Course',
        'grade': 'Grade',
        'attendance': 'Attendance',
        'schedule': 'Schedule',
        'exam': 'Exam',
        'faculty': 'Faculty',
        'department': 'Department',
        'university': 'University',
        'semester': 'Semester',
        'academic_year': 'Academic Year',
        'enrollment': 'Enrollment',
        'transcript': 'Transcript',
        'gpa': 'GPA',
        'credit': 'Credit',
        'prerequisite': 'Prerequisite',
        'thesis': 'Thesis',
        'research': 'Research',
        'library': 'Library',
        'dormitory': 'Dormitory',
        'tuition': 'Tuition Fee',
        'scholarship': 'Scholarship',
        'degree': 'Degree',
        'bachelor': 'Bachelor',
        'master': 'Master',
        'phd': 'PhD',
        'diploma': 'Diploma',
        'certificate': 'Certificate',
    },
    'fa': {
        'student': 'دانشجو',
        'professor': 'استاد',
        'course': 'درس',
        'grade': 'نمره',
        'attendance': 'حضور و غیاب',
        'schedule': 'برنامه زمانی',
        'exam': 'امتحان',
        'faculty': 'دانشکده',
        'department': 'گروه',
        'university': 'دانشگاه',
        'semester': 'ترم',
        'academic_year': 'سال تحصیلی',
        'enrollment': 'ثبت‌نام',
        'transcript': 'ریز نمرات',
        'gpa': 'معدل',
        'credit': 'واحد',
        'prerequisite': 'پیش‌نیاز',
        'thesis': 'پایان‌نامه',
        'research': 'پژوهش',
        'library': 'کتابخانه',
        'dormitory': 'خوابگاه',
        'tuition': 'شهریه',
        'scholarship': 'بورسیه',
        'degree': 'مدرک',
        'bachelor': 'کارشناسی',
        'master': 'کارشناسی ارشد',
        'phd': 'دکتری',
        'diploma': 'دیپلم',
        'certificate': 'گواهی‌نامه',
    },
    'ar': {
        'student': 'طالب',
        'professor': 'أستاذ',
        'course': 'مقرر',
        'grade': 'درجة',
        'attendance': 'الحضور',
        'schedule': 'جدول زمني',
        'exam': 'امتحان',
        'faculty': 'كلية',
        'department': 'قسم',
        'university': 'جامعة',
        'semester': 'فصل دراسي',
        'academic_year': 'السنة الأكاديمية',
        'enrollment': 'تسجيل',
        'transcript': 'كشف درجات',
        'gpa': 'المعدل التراكمي',
        'credit': 'ساعة معتمدة',
        'prerequisite': 'متطلب سابق',
        'thesis': 'أطروحة',
        'research': 'بحث',
        'library': 'مكتبة',
        'dormitory': 'سكن جامعي',
        'tuition': 'رسوم دراسية',
        'scholarship': 'منحة دراسية',
        'degree': 'شهادة',
        'bachelor': 'بكالوريوس',
        'master': 'ماجستير',
        'phd': 'دكتوراه',
        'diploma': 'دبلوم',
        'certificate': 'شهادة',
    }
}


def get_translation(key, language='fa'):
    """Get translation for a specific key and language"""
    return UNIVERSITY_TRANSLATIONS.get(language, {}).get(key, key)


# API response translations
API_MESSAGES = {
    'en': {
        'success': 'Operation completed successfully',
        'created': 'Resource created successfully',
        'updated': 'Resource updated successfully',
        'deleted': 'Resource deleted successfully',
        'not_found': 'Resource not found',
        'unauthorized': 'Authentication required',
        'forbidden': 'Access forbidden',
        'validation_error': 'Validation error',
        'server_error': 'Internal server error',
        'student_enrolled': 'Student enrolled successfully',
        'student_unenrolled': 'Student unenrolled successfully',
        'course_full': 'Course capacity is full',
        'already_enrolled': 'Student is already enrolled',
        'not_enrolled': 'Student is not enrolled in this course',
        'grade_submitted': 'Grade submitted successfully',
        'attendance_marked': 'Attendance marked successfully',
        'schedule_created': 'Schedule created successfully',
        'exam_scheduled': 'Exam scheduled successfully',
    },
    'fa': {
        'success': 'عملیات با موفقیت انجام شد',
        'created': 'منبع با موفقیت ایجاد شد',
        'updated': 'منبع با موفقیت به‌روزرسانی شد',
        'deleted': 'منبع با موفقیت حذف شد',
        'not_found': 'منبع مورد نظر یافت نشد',
        'unauthorized': 'احراز هویت مورد نیاز است',
        'forbidden': 'دسترسی ممنوع است',
        'validation_error': 'خطای اعتبارسنجی',
        'server_error': 'خطای داخلی سرور',
        'student_enrolled': 'دانشجو با موفقیت ثبت‌نام شد',
        'student_unenrolled': 'ثبت‌نام دانشجو با موفقیت لغو شد',
        'course_full': 'ظرفیت دوره تکمیل شده است',
        'already_enrolled': 'دانشجو قبلاً ثبت‌نام کرده است',
        'not_enrolled': 'دانشجو در این دوره ثبت‌نام نکرده است',
        'grade_submitted': 'نمره با موفقیت ثبت شد',
        'attendance_marked': 'حضور و غیاب با موفقیت ثبت شد',
        'schedule_created': 'برنامه زمانی با موفقیت ایجاد شد',
        'exam_scheduled': 'امتحان با موفقیت برنامه‌ریزی شد',
    },
    'ar': {
        'success': 'تمت العملية بنجاح',
        'created': 'تم إنشاء المورد بنجاح',
        'updated': 'تم تحديث المورد بنجاح',
        'deleted': 'تم حذف المورد بنجاح',
        'not_found': 'المورد غير موجود',
        'unauthorized': 'مطلوب تسجيل الدخول',
        'forbidden': 'الوصول محظور',
        'validation_error': 'خطأ في التحقق',
        'server_error': 'خطأ داخلي في الخادم',
        'student_enrolled': 'تم تسجيل الطالب بنجاح',
        'student_unenrolled': 'تم إلغاء تسجيل الطالب بنجاح',
        'course_full': 'المقرر ممتلئ',
        'already_enrolled': 'الطالب مسجل بالفعل',
        'not_enrolled': 'الطالب غير مسجل في هذا المقرر',
        'grade_submitted': 'تم تسجيل الدرجة بنجاح',
        'attendance_marked': 'تم تسجيل الحضور بنجاح',
        'schedule_created': 'تم إنشاء الجدول بنجاح',
        'exam_scheduled': 'تم جدولة الامتحان بنجاح',
    }
}


def get_api_message(key, language='fa'):
    """Get API message in specified language"""
    return API_MESSAGES.get(language, {}).get(key, key)


# Field labels for forms and API documentation
FIELD_LABELS = {
    'en': {
        'national_id': 'National ID',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'email': 'Email Address',
        'phone': 'Phone Number',
        'birth_date': 'Birth Date',
        'user_type': 'User Type',
        'course_title': 'Course Title',
        'course_code': 'Course Code',
        'course_description': 'Course Description',
        'professor': 'Professor',
        'students': 'Students',
        'grade_score': 'Score',
        'exam_date': 'Exam Date',
        'attendance_status': 'Attendance Status',
        'schedule_time': 'Schedule Time',
        'classroom': 'Classroom',
    },
    'fa': {
        'national_id': 'کد ملی',
        'first_name': 'نام',
        'last_name': 'نام خانوادگی',
        'email': 'آدرس ایمیل',
        'phone': 'شماره تلفن',
        'birth_date': 'تاریخ تولد',
        'user_type': 'نوع کاربر',
        'course_title': 'عنوان درس',
        'course_code': 'کد درس',
        'course_description': 'توضیحات درس',
        'professor': 'استاد',
        'students': 'دانشجویان',
        'grade_score': 'نمره',
        'exam_date': 'تاریخ امتحان',
        'attendance_status': 'وضعیت حضور',
        'schedule_time': 'زمان برنامه',
        'classroom': 'کلاس درس',
    }
}


def get_field_label(field, language='fa'):
    """Get field label in specified language"""
    return FIELD_LABELS.get(language, {}).get(field, field)


# Language detection utilities
def get_user_language(request):
    """Detect user's preferred language from request"""
    # 1. Check URL parameter
    if 'lang' in request.GET:
        lang = request.GET['lang']
        if lang in [code for code, name in LANGUAGES]:
            return lang
    
    # 2. Check user profile
    if hasattr(request, 'user') and request.user.is_authenticated:
        if hasattr(request.user, 'preferred_language'):
            return request.user.preferred_language
    
    # 3. Check Accept-Language header
    accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    for lang_code, _ in LANGUAGES:
        if lang_code in accept_language:
            return lang_code
    
    # 4. Default language
    return LANGUAGE_CODE


# Middleware for language detection
class LanguageMiddleware:
    """Middleware to set language based on user preference"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Set language for this request
        language = get_user_language(request)
        
        from django.utils import translation
        translation.activate(language)
        request.LANGUAGE_CODE = language
        
        response = self.get_response(request)
        
        # Add language info to response headers
        response['Content-Language'] = language
        
        return response


# Persian date utilities
class PersianDateUtils:
    """Utilities for Persian calendar and date formatting"""
    
    @staticmethod
    def to_persian_digits(text):
        """Convert English digits to Persian digits"""
        english_digits = '0123456789'
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        
        for eng, per in zip(english_digits, persian_digits):
            text = text.replace(eng, per)
        
        return text
    
    @staticmethod
    def format_persian_date(date_obj):
        """Format date for Persian locale"""
        if not date_obj:
            return ''
        
        # Convert to Persian calendar if needed
        formatted_date = date_obj.strftime('%Y/%m/%d')
        
        if PERSIAN_DIGITS:
            formatted_date = PersianDateUtils.to_persian_digits(formatted_date)
        
        return formatted_date
    
    @staticmethod
    def format_persian_datetime(datetime_obj):
        """Format datetime for Persian locale"""
        if not datetime_obj:
            return ''
        
        formatted_datetime = datetime_obj.strftime('%Y/%m/%d %H:%M')
        
        if PERSIAN_DIGITS:
            formatted_datetime = PersianDateUtils.to_persian_digits(formatted_datetime)
        
        return formatted_datetime


# Direction (RTL/LTR) configuration
def get_text_direction(language):
    """Get text direction for language"""
    rtl_languages = ['fa', 'ar', 'he']
    return 'rtl' if language in rtl_languages else 'ltr'


# Number formatting for different locales
def format_number(number, language='fa'):
    """Format number based on locale"""
    if language == 'fa' and PERSIAN_DIGITS:
        return PersianDateUtils.to_persian_digits(str(number))
    return str(number)
