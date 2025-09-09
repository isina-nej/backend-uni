# 🚀 فایل‌های Collection برای Test API ها

دو فایل کامل و حرفه‌ای برای تست API های سیستم مدیریت دانشگاه آماده شده است:

## 📁 فایل‌های موجود

### 1. 🔥 APIdog Collection
**فایل**: `apidog_collection.json`
- ✨ **بهترین انتخاب برای APIdog**
- 📊 OpenAPI 3.0 استاندارد
- 🎯 Schema validation کامل
- 🔧 Mock server قدرتمند
- 📚 Documentation خودکار
- 🧪 Testing scenarios پیشرفته

### 2. 📮 Postman Collection  
**فایل**: `postman_collection.json`
- ✨ **برای کاربران Postman**
- 🔄 Pre/Post request scripts
- 📊 Environment variables
- 🧪 Automated testing
- 👥 Team collaboration

## 🎯 توصیه استفاده

### برای APIdog (پیشنهاد اول):
```bash
# import کردن فایل
File → Import → apidog_collection.json
```

**مزایای APIdog:**
- 🔥 Interface زیباتر و مدرن
- 📊 Documentation بهتر
- 🧪 Mock server قدرتمند
- 🎯 Schema validation دقیق‌تر
- 🚀 Performance بهتر

### برای Postman:
```bash
# import کردن فایل  
Import → Upload Files → postman_collection.json
```

**مزایای Postman:**
- 🏢 محبوب در شرکت‌ها
- 📚 جامعه کاربری بزرگ
- 🔧 Plugin های متنوع
- 💼 Enterprise features

## 📋 محتویات هر دو Collection

### 🔐 Authentication (احراز هویت)
- Login / Logout
- Profile management
- Token handling

### 👥 User Management (مدیریت کاربران)
- CRUD operations
- Role-based filtering
- Search functionality

### 📚 Academic Modules (ماژول‌های آموزشی)
- Courses (دروس)
- Grades (نمرات)  
- Schedules (برنامه‌ها)
- Exams (امتحانات)
- Assignments (تکالیف)

### 🏛️ University Services (خدمات دانشگاه)
- Library (کتابخانه)
- Financial (امور مالی)
- Attendance (حضور غیاب)
- Research (پژوهش)

### 📢 Communication (ارتباطات)
- Announcements (اعلان‌ها)
- Notifications (اطلاعیه‌ها)

### 📈 Reports (گزارش‌گیری)
- Dashboard analytics
- Student reports
- Course performance

## 🛠️ نحوه استفاده

### گام 1: Import Collection
- فایل مورد نظر را در APIdog یا Postman import کنید

### گام 2: Environment Setup
```json
{
  "base_url": "http://127.0.0.1:8000",
  "admin_username": "admin", 
  "admin_password": "admin123"
}
```

### گام 3: Login و دریافت Token
- ابتدا از endpoint `Login` استفاده کنید
- Token دریافتی خودکار ذخیره می‌شود

### گام 4: استفاده از سایر API ها
- تمام endpoint ها آماده تست هستند
- فیلترها و پارامترها پیش‌تنظیم شده‌اند

## 📊 ویژگی‌های خاص

### تست‌های خودکار:
- Response validation
- Status code checks  
- Performance monitoring
- Data structure validation

### مدیریت Token:
- Auto-login capability
- Token refresh handling
- Session management

### Environment Variables:
- Development/Production configs
- Dynamic parameter handling
- Reusable configurations

## 🎉 نتیجه

هر دو فایل کاملاً functional و production-ready هستند:

- ✅ **تمام 50+ API endpoint**
- ✅ **فولدربندی منطقی و منظم**
- ✅ **تست‌های خودکار**
- ✅ **مستندات کامل**
- ✅ **Environment management**
- ✅ **Error handling**

---

**توصیه**: اگر جدید هستید، از **APIdog** شروع کنید! 🚀
