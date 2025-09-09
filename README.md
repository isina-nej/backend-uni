# 🎓 University Management System Backend

یک سیستم مدیریت دانشگاهی جامع و قدرتمند که با Django و Django REST Framework ساخته شده است.

## ✨ ویژگی‌های کلیدی

### 🏗️ آرکیتکچر مدولار
- **ساختار مدولار**: هر بخش به صورت جداگانه پیاده‌سازی شده
- **قابلیت توسعه**: آسان برای اضافه کردن ماژول‌های جدید
- **نگهداری آسان**: کد تمیز و قابل فهم

### 👥 مدیریت کاربران
- **نقش‌های مختلف**: دانشجو، استاد، کارمند، ادمین
- **احراز هویت قوی**: Token-based authentication
- **پروفایل کاربری**: مدیریت اطلاعات شخصی

### 📚 ماژول‌های اصلی

#### 🎯 هسته سیستم
- **کاربران** (Users): مدیریت دانشجویان، اساتید و کارمندان
- **درس‌ها** (Courses): مدیریت دروس و ثبت‌نام
- **اطلاع‌رسانی** (Notifications): سیستم اطلاع‌رسانی داخلی

#### 📊 آموزشی
- **نمرات** (Grades): مدیریت نمرات و ارزیابی
- **برنامه‌ریزی** (Schedules): برنامه کلاس‌ها و جلسات
- **امتحانات** (Exams): برنامه‌ریزی و مدیریت امتحانات
- **تکالیف** (Assignments): مدیریت تکالیف و پروژه‌ها

#### 🏛️ خدمات دانشگاه
- **کتابخانه** (Library): مدیریت کتاب‌ها و امانت
- **مالی** (Financial): مدیریت شهریه و پرداخت‌ها
- **حضور غیاب** (Attendance): ثبت حضور و غیاب
- **پژوهش** (Research): مدیریت پروژه‌های تحقیقاتی

#### 📢 ارتباطات
- **اعلان‌ها** (Announcements): اعلان‌های عمومی و اخبار
- **احراز هویت** (Authentication): ورود/خروج و مدیریت جلسات

#### 📈 گزارش‌گیری
- **داشبورد** (Dashboard): آمار کلی سیستم
- **گزارش دانشجو**: گزارش عملکرد فردی
- **گزارش درس**: تحلیل عملکرد کلاس

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.9+
- **MySQL 8.0+** یا **MariaDB 10.5+**
- Virtual Environment

> 📖 **راهنمای کامل تنظیم MySQL**: [MYSQL_SETUP.md](MYSQL_SETUP.md)
> 🌐 **راهنمای MySQL در PythonAnywhere**: [MYSQL_PYTHONANYWHERE.md](MYSQL_PYTHONANYWHERE.md)

### مراحل نصب

1. **کلون کردن پروژه**
```bash
git clone <repository-url>
cd backend
```

2. **ایجاد Virtual Environment**
```bash
python -m venv venv
venv\\Scripts\\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **نصب کتابخانه‌ها**
```bash
pip install -r requirements.txt
```

4. **تنظیمات دیتابیس**
- فایل `config/settings.py` را برای اتصال به PostgreSQL تنظیم کنید

5. **اجرای Migration ها**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **ایجاد Super User**
```bash
python manage.py createsuperuser
```

7. **راه‌اندازی سرور**
```bash
python manage.py runserver
```

## 🌐 API Endpoints

### احراز هویت
- `POST /api/auth/login/` - ورود به سیستم
- `POST /api/auth/logout/` - خروج از سیستم
- `GET /api/auth/profile/` - نمایش پروفایل
- `PUT /api/auth/profile/update/` - بروزرسانی پروفایل

### کاربران
- `GET/POST /api/users/users/` - لیست/ایجاد کاربران
- `GET/PUT/DELETE /api/users/users/{id}/` - عملیات روی کاربر

### دروس
- `GET/POST /api/courses/courses/` - لیست/ایجاد دروس
- `GET/PUT/DELETE /api/courses/courses/{id}/` - عملیات روی درس

### اعلان‌ها
- `GET/POST /api/announcements/announcements/` - لیست/ایجاد اعلان
- `GET/PUT/DELETE /api/announcements/announcements/{id}/` - عملیات روی اعلان

### تکالیف
- `GET/POST /api/assignments/assignments/` - لیست/ایجاد تکلیف
- `GET/POST /api/assignments/submissions/` - ارسال/نمایش پاسخ

### گزارش‌ها
- `GET /api/reports/dashboard/` - آمار کلی (فقط ادمین)
- `GET /api/reports/student/` - گزارش دانشجو
- `GET /api/reports/course/{id}/` - گزارش درس

## 🛠️ تکنولوژی‌های استفاده شده

### Backend Framework
- **Django 5.1**: فریمورک اصلی
- **Django REST Framework**: برای API
- **MySQL 8.0+**: دیتابیس production

### کتابخانه‌های اضافی
- **django-filter**: فیلترینگ پیشرفته
- **django-cors-headers**: پشتیبانی از CORS
- **mysqlclient**: اتصال به MySQL
- **loguru**: لاگ‌گیری پیشرفته
- **channels**: WebSocket support
- **pillow**: پردازش تصاویر

## 📱 سازگاری با پلتفرم‌ها

این API طراحی شده برای پشتیبانی از:
- **وب اپلیکیشن‌ها** (React, Vue, Angular)
- **موبایل اپ‌های فلاتر** (Flutter)
- **ربات‌ها** (Telegram, Discord)
- **اپلیکیشن‌های دسکتاپ**

## 🔐 امنیت

- **Token Authentication**: احراز هویت مبتنی بر توکن
- **Permission System**: کنترل دسترسی پیشرفته
- **CORS Protection**: محافظت در برابر Cross-Origin attacks
- **Data Validation**: اعتبارسنجی کامل داده‌ها

## 🎯 Admin Panel

دسترسی به پنل ادمین:
- URL: `http://127.0.0.1:8000/admin/`
- با حساب superuser وارد شوید

## 📊 مثال‌های استفاده

### ورود به سیستم
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \\
  -H "Content-Type: application/json" \\
  -d '{"username": "admin", "password": "your_password"}'
```

### دریافت لیست اعلان‌ها
```bash
curl -X GET http://127.0.0.1:8000/api/announcements/announcements/ \\
  -H "Authorization: Token your_token_here"
```

### ایجاد اعلان جدید
```bash
curl -X POST http://127.0.0.1:8000/api/announcements/announcements/ \\
  -H "Authorization: Token your_token_here" \\
  -H "Content-Type: application/json" \\
  -d '{
    "title": "اطلاعیه مهم",
    "content": "محتوای اطلاعیه",
    "target_audience": "students",
    "priority": "high"
  }'
```

## 🔄 توسعه و نگهداری

### اضافه کردن ماژول جدید
1. در پوشه `apps` یک اپلیکیشن جدید بسازید
2. مدل‌ها، سریالایزرها و ویوها را تعریف کنید
3. URL ها را به `config/api_urls.py` اضافه کنید
4. اپلیکیشن را به `INSTALLED_APPS` اضافه کنید

### Migration ها
```bash
python manage.py makemigrations app_name
python manage.py migrate
```

## 📞 پشتیبانی

برای سوالات و مشکلات:
- مستندات API: `/api/` endpoint
- Admin Panel: `/admin/`
- مشاهده لاگ‌ها در کنسول

## 🌟 ویژگی‌های آینده

- [ ] سیستم چت آنلاین
- [ ] پشتیبانی از فایل‌های چندرسانه‌ای
- [ ] ربات تلگرام
- [ ] اپلیکیشن موبایل
- [ ] Dashboard تحلیلی پیشرفته

---

**نوشته شده با ❤️ برای جامعه آکادمیک**
1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Set environment variables (SECRET_KEY, DB credentials, etc.)
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`

## Structure
- apps/: Modular Django apps (users, courses, notifications)
- config/: Settings and URL configurations
- logs/: Log files
- tests/: Unit and integration tests
- docs/: Documentation

## APIs
- /api/users/: User management
- /api/courses/: Course operations
- /api/notifications/: Notifications for bots/web

## Fault Tolerance
- Isolated apps prevent cascading failures.
- Logging captures errors without stopping the system.
- Use Celery for async tasks to avoid blocking.

## Updates
- Modular design allows easy addition of new apps.
- Version APIs for backward compatibility.
#   b a c k e n d - u n i 
 
 