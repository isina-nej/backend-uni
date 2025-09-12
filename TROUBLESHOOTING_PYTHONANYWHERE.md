# ==============================================================================
# راهنمای حل مشکلات استقرار PythonAnywhere
# PythonAnywhere Troubleshooting Guide
# ==============================================================================

## مشکلات شناسایی شده:

### 1. Disk Quota Exceeded
**علت:** فضای دیسک اکانت رایگان PythonAnywhere تمام شده
**راه‌حل:**
```bash
# پاک کردن cache files
rm -rf ~/.cache/pip/*
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# استفاده از requirements کمتر
pip3.10 install --user -r requirements_minimal_pythonanywhere.txt --no-cache-dir
```

### 2. Log Directory Missing
**علت:** مسیر `/home/yourusername/logs/django.log` وجود ندارد
**راه‌حل:** تنظیمات logging در `settings_pythonanywhere.py` تغییر کرده تا فقط از console استفاده کند

### 3. Wrong Username in Paths
**علت:** هنوز `yourusername` در فایل‌ها جایگزین نشده
**راه‌حل:** همه فایل‌ها به‌روزرسانی شده‌اند برای `sinanej2`

## مراحل حل مشکل:

### مرحله ۱: پاکسازی فضا
```bash
cd /home/sinanej2/backend-uni/backend-uni
chmod +x recovery_pythonanywhere.sh
./recovery_pythonanywhere.sh
```

### مرحله ۲: ایجاد دیتابیس MySQL
1. در PythonAnywhere Dashboard → Databases بروید
2. یک دیتابیس MySQL جدید ایجاد کنید
3. نام دیتابیس، کاربر و رمز را یادداشت کنید

### مرحله ۳: به‌روزرسانی .env
فایل `.env.pythonanywhere` را ویرایش کنید:
```env
SECRET_KEY=your-generated-secret-key
DEBUG=False
DB_NAME=sinanej2$your_actual_database_name
DB_USER=sinanej2
DB_PASSWORD=your_actual_database_password
DB_HOST=sinanej2.mysql.pythonanywhere-services.com
```

### مرحله ۴: تست کردن
```bash
# بررسی تنظیمات
python3.10 manage.py check --settings=config.settings_pythonanywhere

# اجرای مایگریشن
python3.10 manage.py migrate --settings=config.settings_pythonanywhere

# جمع‌آوری static files
python3.10 manage.py collectstatic --noinput --settings=config.settings_pythonanywhere
```

### مرحله ۵: تنظیم Web App
1. در PythonAnywhere Dashboard → Web بروید
2. اگر Web App وجود ندارد، ایجاد کنید
3. تنظیمات:
   - **WSGI file:** `/var/www/sinanej2_pythonanywhere_com_wsgi.py`
   - محتوای فایل را با `pythonanywhere_wsgi.py` جایگزین کنید
   - **Static files:**
     - URL: `/static/`
     - Directory: `/home/sinanej2/sinanej2.pythonanywhere.com/static`
   - **Media files:**
     - URL: `/media/`
     - Directory: `/home/sinanej2/sinanej2.pythonanywhere.com/media`

### مرحله ۶: Reload Web App
در Web tab، روی "Reload" کلیک کنید

## نکات مهم:

### حل مشکل Disk Quota:
- از `--no-cache-dir` در pip install استفاده کنید
- فقط پکیج‌های ضروری نصب کنید
- فایل‌های غیرضروری را حذف کنید
- در نظر بگیرید اکانت پولی تهیه کنید

### بهینه‌سازی فضا:
```bash
# پاک کردن فایل‌های اضافی
rm -rf .git  # اگر نیاز به git ندارید
rm -rf tests/
rm -rf docs/
find . -name "*.md" -not -name "README.md" -delete
```

### تست عملکرد:
```bash
# تست اتصال به دیتابیس
python3.10 -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_pythonanywhere')
import django
django.setup()
from django.db import connection
print('Database connection:', connection.ensure_connection())
"
```

## آدرس‌های مهم:

- **Site URL:** https://sinanej2.pythonanywhere.com
- **Admin Panel:** https://sinanej2.pythonanywhere.com/admin/
- **API Root:** https://sinanej2.pythonanywhere.com/api/
- **Swagger UI:** https://sinanej2.pythonanywhere.com/api/schema/swagger-ui/

## در صورت ادامه مشکل:

1. **Error Logs:** در Web tab → Error log را بررسی کنید
2. **Access Logs:** در Web tab → Access log را بررسی کنید
3. **Console Testing:** در Bash console تست کنید
4. **Support:** از PythonAnywhere forums کمک بگیرید

## Command های کمکی:

```bash
# بررسی فضای دیسک
du -sh ~/*

# بررسی installed packages
pip3.10 list --user

# تست Django
python3.10 manage.py shell --settings=config.settings_pythonanywhere

# بررسی error logs
tail -f /var/log/sinanej2.pythonanywhere.com.error.log
```

---

**موفق باشید!** 🚀
