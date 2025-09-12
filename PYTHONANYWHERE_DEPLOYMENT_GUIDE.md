# ==============================================================================
# راهنمای استقرار پروژه در PythonAnywhere
# PythonAnywhere Deployment Guide
# ==============================================================================

## مرحله ۱: آماده‌سازی اکانت PythonAnywhere

1. در سایت [PythonAnywhere](https://www.pythonanywhere.com) ثبت‌نام کنید
2. یک اکانت رایگان یا پولی ایجاد کنید
3. وارد Dashboard شوید

## مرحله ۲: آپلود کردن کد

### روش ۱: استفاده از Git (توصیه شده)
```bash
# در Bash Console در PythonAnywhere
git clone https://github.com/yourusername/backend-uni.git
cd backend-uni
```

### روش ۲: آپلود مستقیم فایل‌ها
- فایل‌های پروژه را زیپ کنید
- در Files tab آپلود کنید
- آنزیپ کنید

## مرحله ۳: تنظیم دیتابیس MySQL

1. در Dashboard، به بخش Databases بروید
2. یک دیتابیس MySQL جدید ایجاد کنید
3. نام دیتابیس، نام کاربری و رمز عبور را یادداشت کنید

## مرحله ۴: تنظیم متغیرهای محیطی

فایل `.env.pythonanywhere` را ویرایش کنید:

```env
# جایگزین کنید با اطلاعات واقعی خود
SECRET_KEY=your-actual-secret-key-here
DEBUG=False

DB_NAME=yourusername$yourdatabase
DB_USER=yourusername  
DB_PASSWORD=your-database-password
DB_HOST=yourusername.mysql.pythonanywhere-services.com

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

## مرحله ۵: نصب پکیج‌ها و راه‌اندازی

در Bash Console اجرا کنید:

```bash
cd /home/yourusername/backend-uni

# نصب پکیج‌ها
pip3.10 install --user -r requirements_pythonanywhere.txt

# اجرای مایگریشن‌ها
python3.10 manage.py migrate --settings=config.settings_pythonanywhere

# جمع‌آوری فایل‌های استاتیک
python3.10 manage.py collectstatic --noinput --settings=config.settings_pythonanywhere

# ایجاد سوپریوزر
python3.10 manage.py createsuperuser --settings=config.settings_pythonanywhere
```

## مرحله ۶: تنظیم Web App

1. در Dashboard به Web بروید
2. Add a new web app کلیک کنید
3. Manual configuration را انتخاب کنید
4. Python 3.10 را انتخاب کنید

### تنظیمات WSGI:
- WSGI configuration file: `/var/www/yourusername_pythonanywhere_com_wsgi.py`
- محتوای فایل را با `pythonanywhere_wsgi.py` جایگزین کنید

### تنظیمات Static Files:
- URL: `/static/`
- Directory: `/home/yourusername/yourusername.pythonanywhere.com/static`

- URL: `/media/`
- Directory: `/home/yourusername/yourusername.pythonanywhere.com/media`

## مرحله ۷: آخرین تنظیمات

1. فایل‌های زیر را ویرایش کنید و `yourusername` را با نام کاربری خود جایگزین کنید:
   - `config/settings_pythonanywhere.py`
   - `pythonanywhere_wsgi.py`
   - `.env.pythonanywhere`

2. در Web App Configuration:
   - Reload بزنید

## مرحله ۸: تست

1. به آدرس `https://yourusername.pythonanywhere.com` بروید
2. API endpoints را تست کنید:
   - `/admin/` - پنل ادمین
   - `/api/` - API endpoints
   - `/api/schema/swagger-ui/` - مستندات API

## نکات مهم

### امنیت:
- `DEBUG=False` قرار دهید
- SECRET_KEY قوی استفاده کنید
- رمزهای دیتابیس را محفوظ نگه دارید

### Performance:
- از Redis caching استفاده کنید (در پلان‌های پولی)
- فایل‌های استاتیک را بهینه کنید

### Monitoring:
- Log files را بررسی کنید: `/home/yourusername/logs/`
- Error logs را در Web tab مشاهده کنید

## عیب‌یابی

### مشکلات رایج:

1. **خطای Database Connection:**
   - اطلاعات دیتابیس را بررسی کنید
   - فایروال MySQL را چک کنید

2. **خطای Static Files:**
   - مسیر STATIC_ROOT را بررسی کنید
   - collectstatic را دوباره اجرا کنید

3. **خطای Import:**
   - Python path را بررسی کنید
   - پکیج‌های مورد نیاز نصب شده باشند

### Commands مفید:

```bash
# مشاهده logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log

# ری‌استارت web app
# از Web tab در Dashboard

# بررسی Python packages
pip3.10 list --user

# تست settings
python3.10 manage.py check --settings=config.settings_pythonanywhere
```

## پشتیبانی

در صورت بروز مشکل:
1. Log files را بررسی کنید
2. PythonAnywhere Help & Support مراجعه کنید
3. Forums آنها را چک کنید

## بروزرسانی

برای بروزرسانی پروژه:

```bash
git pull origin main
pip3.10 install --user -r requirements_pythonanywhere.txt
python3.10 manage.py migrate --settings=config.settings_pythonanywhere
python3.10 manage.py collectstatic --noinput --settings=config.settings_pythonanywhere
# از Web tab، Reload کنید
```
