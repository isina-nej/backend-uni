# 🌐 راهنمای کامل API - سیستم مدیریت دانشگاهی

## 🚀 مقدمه

این مستند شامل تمامی endpoint های موجود در سیستم مدیریت دانشگاهی است. تمامی API ها بر اساس استاندارد REST طراحی شده‌اند.

## 🔑 احراز هویت

### Token Authentication
```http
POST /api/auth/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "role": "SUPER_ADMIN"
    }
}
```

### استفاده از Token
```http
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## 👥 Users API

### 📋 لیست کاربران
```http
GET /api/users/
Authorization: Token your_token
```

**پارامترهای فیلتر:**
- `role` - نقش کاربر
- `organizational_unit` - واحد سازمانی
- `is_active` - وضعیت فعال
- `search` - جستجو در نام، نام کاربری، ایمیل

**نمونه درخواست:**
```http
GET /api/users/?role=FACULTY&organizational_unit=5&search=احمد
```

**Response:**
```json
{
    "count": 150,
    "next": "http://api/users/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "prof.ahmadi",
            "email": "ahmadi@university.ac.ir",
            "first_name": "احمد",
            "last_name": "احمدی",
            "first_name_fa": "احمد",
            "last_name_fa": "احمدی",
            "role": "FACULTY",
            "national_id": "1234567890",
            "phone": "09123456789",
            "organizational_unit": {
                "id": 5,
                "name": "Computer Science",
                "name_fa": "علوم کامپیوتر"
            },
            "academic_rank": "ASSOCIATE_PROFESSOR",
            "is_active": true,
            "avatar": "/media/avatars/prof_ahmadi.jpg"
        }
    ]
}
```

### 👤 جزئیات کاربر
```http
GET /api/users/{id}/
Authorization: Token your_token
```

**Response:**
```json
{
    "id": 1,
    "username": "prof.ahmadi",
    "email": "ahmadi@university.ac.ir",
    "first_name": "احمد",
    "last_name": "احمدی",
    "first_name_fa": "احمد", 
    "last_name_fa": "احمدی",
    "role": "FACULTY",
    "national_id": "1234567890",
    "birth_date": "1975-05-15",
    "gender": "MALE",
    "phone": "09123456789",
    "address": "تهران، خیابان انقلاب",
    "avatar": "/media/avatars/prof_ahmadi.jpg",
    "academic_rank": "ASSOCIATE_PROFESSOR",
    "education_level": "PhD",
    "field_of_study": "Computer Science",
    "employee_id": "EMP001",
    "employment_type": "PERMANENT",
    "hire_date": "2010-09-01",
    "organizational_unit": {
        "id": 5,
        "name": "Computer Science Department",
        "name_fa": "گروه علوم کامپیوتر",
        "type": "DEPARTMENT"
    },
    "positions": [
        {
            "id": 1,
            "title": "Department Head",
            "title_fa": "رئیس گروه",
            "is_primary": true,
            "start_date": "2020-01-01",
            "is_active": true
        }
    ],
    "permissions": [
        {
            "id": 1,
            "permission": {
                "name": "manage_courses",
                "name_fa": "مدیریت دروس"
            },
            "organizational_unit": {
                "name": "Computer Science Department"
            },
            "granted_at": "2020-01-01T10:00:00Z",
            "expires_at": "2024-01-01T10:00:00Z"
        }
    ],
    "bio": "استاد مهندسی کامپیوتر با تخصص در هوش مصنوعی",
    "social_links": {
        "linkedin": "https://linkedin.com/in/ahmadi",
        "researchgate": "https://researchgate.net/profile/ahmadi"
    },
    "achievements": [
        {
            "title": "برترین استاد سال",
            "year": 2022,
            "organization": "دانشگاه تهران"
        }
    ],
    "skills": ["Python", "Machine Learning", "Data Science"],
    "languages": [
        {"name": "فارسی", "level": "Native"},
        {"name": "English", "level": "Fluent"}
    ],
    "is_active": true,
    "last_login": "2024-01-15T09:30:00Z",
    "date_joined": "2010-09-01T00:00:00Z"
}
```

### 🆕 ایجاد کاربر جدید
```http
POST /api/users/
Authorization: Token your_token
Content-Type: application/json

{
    "username": "new_student",
    "email": "student@university.ac.ir",
    "password": "secure_password123",
    "first_name": "علی",
    "last_name": "محمدی",
    "first_name_fa": "علی",
    "last_name_fa": "محمدی",
    "role": "STUDENT",
    "national_id": "0987654321",
    "phone": "09123456789",
    "organizational_unit": 5,
    "student_id": "98123456",
    "field_of_study": "Computer Science"
}
```

### ✏️ ویرایش کاربر
```http
PUT /api/users/{id}/
Authorization: Token your_token
Content-Type: application/json

{
    "phone": "09123456788",
    "address": "تهران، خیابان ولی‌عصر",
    "bio": "دانشجوی کارشناسی ارشد علوم کامپیوتر"
}
```

### 🗑️ حذف کاربر
```http
DELETE /api/users/{id}/
Authorization: Token your_token
```

### 👤 اطلاعات کاربر فعلی
```http
GET /api/users/me/
Authorization: Token your_token
```

### 📊 آمار کاربران
```http
GET /api/users/statistics/
Authorization: Token your_token
```

**Response:**
```json
{
    "total_users": 1500,
    "active_users": 1350,
    "role_distribution": [
        {"role": "STUDENT", "count": 1000, "percentage": 66.67},
        {"role": "FACULTY", "count": 200, "percentage": 13.33},
        {"role": "STAFF", "count": 250, "percentage": 16.67},
        {"role": "ADMIN", "count": 50, "percentage": 3.33}
    ],
    "unit_distribution": [
        {"unit": "Computer Science", "count": 300},
        {"unit": "Mathematics", "count": 250},
        {"unit": "Physics", "count": 200}
    ],
    "recent_registrations": 25,
    "active_sessions": 145
}
```

### 👔 تخصیص سمت
```http
POST /api/users/{id}/assign_position/
Authorization: Token your_token
Content-Type: application/json

{
    "position_id": 3,
    "is_primary": false,
    "start_date": "2024-01-01",
    "description": "مسئولیت موقت پروژه"
}
```

### 🔑 اعطای مجوز
```http
POST /api/users/{id}/grant_permission/
Authorization: Token your_token
Content-Type: application/json

{
    "permission_id": 5,
    "organizational_unit_id": 3,
    "expires_at": "2024-12-31T23:59:59Z",
    "reason": "نیاز به دسترسی برای پروژه جدید"
}
```

## 🏛️ Organizational Units API

### 📋 لیست واحدهای سازمانی
```http
GET /api/users/organizational-units/
Authorization: Token your_token
```

**پارامترهای فیلتر:**
- `type` - نوع واحد
- `parent` - واحد والد
- `is_active` - وضعیت فعال
- `search` - جستجو در نام

**Response:**
```json
{
    "count": 50,
    "results": [
        {
            "id": 1,
            "name": "University of Tehran",
            "name_fa": "دانشگاه تهران",
            "type": "UNIVERSITY",
            "code": "UT",
            "description": "دانشگاه تهران، قدیمی‌ترین دانشگاه مدرن ایران",
            "parent": null,
            "is_active": true,
            "website": "https://ut.ac.ir",
            "phone": "021-61111111",
            "email": "info@ut.ac.ir",
            "address": "تهران، خیابان انقلاب، دانشگاه تهران",
            "children_count": 15,
            "members_count": 25000
        }
    ]
}
```

### 🌳 ساختار درختی
```http
GET /api/users/organizational-units/tree/
Authorization: Token your_token
```

**Response:**
```json
[
    {
        "id": 1,
        "name": "University of Tehran",
        "name_fa": "دانشگاه تهران",
        "type": "UNIVERSITY",
        "children": [
            {
                "id": 2,
                "name": "Faculty of Engineering",
                "name_fa": "دانشکده مهندسی",
                "type": "FACULTY",
                "children": [
                    {
                        "id": 5,
                        "name": "Computer Science Department",
                        "name_fa": "گروه علوم کامپیوتر",
                        "type": "DEPARTMENT",
                        "children": []
                    }
                ]
            }
        ]
    }
]
```

### 👥 اعضای واحد
```http
GET /api/users/organizational-units/{id}/members/
Authorization: Token your_token
```

**پارامترهای اضافی:**
- `include_descendants=true` - شامل زیرواحدها
- `role` - فیلتر بر اساس نقش

## 💼 Positions API

### 📋 لیست سمت‌ها
```http
GET /api/users/positions/
Authorization: Token your_token
```

**Response:**
```json
{
    "count": 20,
    "results": [
        {
            "id": 1,
            "title": "Department Head",
            "title_fa": "رئیس گروه",
            "description": "مسئولیت کلی اداره گروه آموزشی",
            "level": "SENIOR",
            "authority_level": 4,
            "organizational_unit": {
                "id": 5,
                "name": "Computer Science Department"
            },
            "is_active": true,
            "created_at": "2023-01-01T00:00:00Z"
        }
    ]
}
```

### 👥 سمت‌های کاربران
```http
GET /api/users/user-positions/
Authorization: Token your_token
```

**پارامترهای فیلتر:**
- `user` - کاربر خاص
- `position` - سمت خاص
- `is_primary` - سمت اصلی
- `is_active` - فعال

## 🔑 Permissions API

### 📋 لیست مجوزها
```http
GET /api/users/permissions/
Authorization: Token your_token
```

**Response:**
```json
{
    "count": 30,
    "results": [
        {
            "id": 1,
            "name": "manage_courses",
            "name_fa": "مدیریت دروس",
            "description": "قابلیت ایجاد، ویرایش و حذف دروس",
            "category": "ACADEMIC",
            "is_active": true,
            "created_at": "2023-01-01T00:00:00Z"
        }
    ]
}
```

### 👥 مجوزهای کاربران
```http
GET /api/users/user-permissions/
Authorization: Token your_token
```

**پارامترهای فیلتر:**
- `user` - کاربر خاص
- `permission` - مجوز خاص
- `organizational_unit` - واحد سازمانی
- `is_active` - فعال
- `expires_soon` - منقضی شدن نزدیک

## 📊 Access Logs API

### 📋 لاگ دسترسی‌ها
```http
GET /api/users/access-logs/
Authorization: Token your_token
```

**پارامترهای فیلتر:**
- `user` - کاربر خاص
- `action` - نوع عملیات
- `success` - موفق/ناموفق
- `date_from` - از تاریخ
- `date_to` - تا تاریخ

**Response:**
```json
{
    "count": 10000,
    "results": [
        {
            "id": 1,
            "user": {
                "id": 1,
                "username": "prof.ahmadi",
                "full_name": "احمد احمدی"
            },
            "action": "LOGIN",
            "resource": "/api/auth/token/",
            "timestamp": "2024-01-15T09:30:00Z",
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0...",
            "success": true,
            "details": {
                "login_method": "username_password",
                "session_duration": 3600
            },
            "session_id": "abc123xyz789"
        }
    ]
}
```

## 🔍 جستجو و فیلترینگ

### 🔤 جستجوی متنی
```http
GET /api/users/?search=احمد
GET /api/users/organizational-units/?search=مهندسی
```

### 📊 فیلترهای پیشرفته
```http
# ترکیب چندین فیلتر
GET /api/users/?role=FACULTY&organizational_unit=5&is_active=true

# فیلتر تاریخی
GET /api/users/access-logs/?date_from=2024-01-01&date_to=2024-01-31

# فیلتر JSON
GET /api/users/?skills__contains=Python
```

### 📄 صفحه‌بندی
```http
GET /api/users/?page=2&page_size=20
```

**Response:**
```json
{
    "count": 1500,
    "next": "http://api/users/?page=3",
    "previous": "http://api/users/?page=1",
    "page_size": 20,
    "total_pages": 75,
    "current_page": 2,
    "results": [...]
}
```

### 📈 مرتب‌سازی
```http
GET /api/users/?ordering=last_name
GET /api/users/?ordering=-date_joined,first_name
```

## 📦 Bulk Operations

### 👥 عملیات دسته‌جمعی روی کاربران
```http
POST /api/users/bulk_update/
Authorization: Token your_token
Content-Type: application/json

{
    "user_ids": [1, 2, 3, 4, 5],
    "data": {
        "is_active": false,
        "organizational_unit": 10
    }
}
```

### 🔑 اعطای مجوز دسته‌جمعی
```http
POST /api/users/bulk_grant_permission/
Authorization: Token your_token
Content-Type: application/json

{
    "user_ids": [1, 2, 3],
    "permission_id": 5,
    "organizational_unit_id": 3,
    "expires_at": "2024-12-31T23:59:59Z"
}
```

## 📤 Export/Import

### 📊 خروجی Excel
```http
GET /api/users/export/?format=xlsx
Authorization: Token your_token
```

### 📁 خروجی CSV
```http
GET /api/users/export/?format=csv&fields=username,email,role
Authorization: Token your_token
```

### 📤 ورودی از فایل
```http
POST /api/users/import/
Authorization: Token your_token
Content-Type: multipart/form-data

file: [Excel/CSV file]
```

## ⚠️ خطاها و پاسخ‌ها

### 🔑 خطای احراز هویت
```json
{
    "detail": "Invalid token.",
    "error_code": "INVALID_TOKEN"
}
```

### 🚫 خطای دسترسی
```json
{
    "detail": "You do not have permission to perform this action.",
    "error_code": "PERMISSION_DENIED"
}
```

### ❌ خطای اعتبارسنجی
```json
{
    "username": ["This field is required."],
    "email": ["Enter a valid email address."],
    "national_id": ["National ID already exists."]
}
```

### 🔍 خطای یافت نشدن
```json
{
    "detail": "Not found.",
    "error_code": "NOT_FOUND"
}
```

## 🔧 تنظیمات پیشرفته

### 📊 محدودیت درخواست (Rate Limiting)
- **Anonymous**: 100 درخواست در ساعت
- **Authenticated**: 1000 درخواست در ساعت
- **Admin**: 5000 درخواست در ساعت

### 🎯 Caching
- لیست واحدهای سازمانی: 1 ساعت
- اطلاعات کاربری: 30 دقیقه
- آمار عمومی: 15 دقیقه

### 🔒 امنیت
- تمام API ها نیازمند Token هستند
- HTTPS اجباری در Production
- CORS محدود به domain های مجاز
- Rate limiting برای جلوگیری از سوءاستفاده

## 🧪 تست API

### 📋 نمونه تست با cURL
```bash
# احراز هویت
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# دریافت لیست کاربران
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Token YOUR_TOKEN"

# ایجاد کاربر جدید
curl -X POST http://localhost:8000/api/users/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "password": "password123",
    "first_name": "تست",
    "last_name": "کاربر",
    "role": "STUDENT"
  }'
```

### 🧪 نمونه تست با Postman
1. Set Environment Variable: `base_url = http://localhost:8000/api`
2. Authentication: Token YOUR_TOKEN
3. Import Collection از فایل: `docs/postman_collection.json`

این راهنما شامل تمامی endpoint ها و قابلیت‌های API سیستم مدیریت دانشگاهی است. برای اطلاعات بیشتر یا مثال‌های خاص، با تیم توسعه تماس بگیرید.
