# ==============================================================================
# خلاصه فایل‌های ایجاد شده برای PythonAnywhere
# PythonAnywhere Deployment Files Summary
# ==============================================================================

این فایل‌ها برای استقرار پروژه Django در PythonAnywhere ایجاد شده‌اند:

## فایل‌های اصلی تنظیمات:

### 1. requirements_pythonanywhere.txt
- پکیج‌های مورد نیاز برای PythonAnywhere
- شامل MySQL client و سایر ابزارهای ضروری
- بهینه‌سازی شده برای محیط PythonAnywhere

### 2. config/settings_pythonanywhere.py
- تنظیمات Django مخصوص PythonAnywhere
- پیکربندی MySQL database
- تنظیمات امنیتی production
- مسیرهای static و media files

### 3. .env.pythonanywhere
- متغیرهای محیطی برای production
- اطلاعات دیتابیس MySQL
- کلیدهای امنیتی

### 4. pythonanywhere_wsgi.py
- فایل WSGI برای PythonAnywhere
- تنظیم مسیر پروژه و settings module

## اسکریپت‌های کمکی:

### 5. deploy_pythonanywhere.sh
- اسکریپت خودکار استقرار
- نصب packages، migration، collectstatic

### 6. prepare_pythonanywhere.bat
- اسکریپت Windows برای آماده‌سازی
- ایجاد virtual environment و نصب requirements

### 7. setup_database_pythonanywhere.py
- اسکریپت Python برای راه‌اندازی دیتابیس
- ایجاد tables، superuser، sample data

### 8. health_check_pythonanywhere.sh
- بررسی سلامت استقرار
- تست database connection، static files

### 9. validate_deployment.sh
- تست endpoints و عملکرد
- بررسی SSL و response time

## فایل‌های مستندات:

### 10. PYTHONANYWHERE_DEPLOYMENT_GUIDE.md
- راهنمای کامل استقرار قدم به قدم
- عیب‌یابی مشکلات رایج
- نکات امنیتی و بهینه‌سازی

### 11. config/urls_pythonanywhere.py
- تنظیمات URL برای production
- Error handlers سفارشی

### 12. config/views.py
- Custom error handlers (404, 500)
- پشتیبانی از API و web responses

## مراحل استقرار:

### مرحله ۱: آماده‌سازی محلی
```bash
# Windows
prepare_pythonanywhere.bat

# Linux/Mac
chmod +x deploy_pythonanywhere.sh
```

### مرحله ۲: آپلود به PythonAnywhere
- استفاده از Git یا آپلود مستقیم فایل‌ها
- کپی کردن فایل‌ها به `/home/yourusername/backend-uni`

### مرحله ۳: تنظیم متغیرهای محیطی
- ویرایش `.env.pythonanywhere`
- تنظیم اطلاعات دیتابیس MySQL

### مرحله ۴: اجرای اسکریپت استقرار
```bash
cd /home/yourusername/backend-uni
chmod +x deploy_pythonanywhere.sh
./deploy_pythonanywhere.sh
```

### مرحله ۵: تنظیم Web App
- تنظیم WSGI file
- تنظیم static files mapping
- Reload web app

### مرحله ۶: تست و اعتبارسنجی
```bash
./health_check_pythonanywhere.sh
./validate_deployment.sh
```

## نکات مهم:

1. **جایگزینی نام کاربری:**
   - در همه فایل‌ها `yourusername` را با نام کاربری PythonAnywhere خود جایگزین کنید

2. **امنیت:**
   - SECRET_KEY قوی تولید کنید
   - DEBUG=False قرار دهید
   - اطلاعات حساس را در .env نگه دارید

3. **Database:**
   - MySQL credentials را از PythonAnywhere dashboard بگیرید
   - Migration ها را اجرا کنید

4. **Static Files:**
   - collectstatic را اجرا کنید
   - مسیرهای static را درست تنظیم کنید

5. **Monitoring:**
   - Log files را بررسی کنید
   - Error tracking را فعال کنید

## فایل‌های قابل حذف بعد از استقرار:

- `prepare_pythonanywhere.bat` (بعد از آماده‌سازی)
- فایل‌های test و development
- `.git` directory (اختیاری)

## پشتیبانی و عیب‌یابی:

در صورت بروز مشکل:
1. `PYTHONANYWHERE_DEPLOYMENT_GUIDE.md` را مطالعه کنید
2. Log files را بررسی کنید
3. `health_check_pythonanywhere.sh` را اجرا کنید
4. PythonAnywhere support با forums مراجعه کنید

---

موفق باشید! 🚀
