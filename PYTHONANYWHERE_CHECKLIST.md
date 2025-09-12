# ==============================================================================
# چک‌لیست استقرار PythonAnywhere
# PythonAnywhere Deployment Checklist
# ==============================================================================

## قبل از استقرار (Pre-Deployment)

### ✅ آماده‌سازی محلی
- [ ] پروژه به‌درستی در محیط محلی کار می‌کند
- [ ] تمام tests پاس می‌شوند
- [ ] کد commit و push شده است
- [ ] فایل‌های حساس در .gitignore قرار دارند

### ✅ فایل‌های PythonAnywhere
- [ ] `requirements_pythonanywhere.txt` آماده است
- [ ] `config/settings_pythonanywhere.py` تنظیم شده
- [ ] `.env.pythonanywhere` با اطلاعات واقعی پر شده
- [ ] `pythonanywhere_wsgi.py` آماده است

## در PythonAnywhere (On PythonAnywhere)

### ✅ تنظیم اکانت
- [ ] اکانت PythonAnywhere ایجاد شده
- [ ] نوع subscription مناسب انتخاب شده
- [ ] Dashboard قابل دسترسی است

### ✅ دیتابیس MySQL
- [ ] دیتابیس MySQL ایجاد شده
- [ ] نام دیتابیس، کاربر و رمز یادداشت شده
- [ ] اطلاعات در `.env.pythonanywhere` به‌روزرسانی شده

### ✅ آپلود کد
- [ ] کد از طریق Git clone شده یا آپلود شده
- [ ] فایل‌ها در `/home/yourusername/backend-uni` قرار دارند
- [ ] دسترسی‌های فایل درست تنظیم شده

### ✅ نصب و راه‌اندازی
- [ ] Virtual environment ایجاد شده (اختیاری)
- [ ] `pip install -r requirements_pythonanywhere.txt` اجرا شده
- [ ] Migration ها اجرا شده: `python manage.py migrate`
- [ ] Static files جمع‌آوری شده: `python manage.py collectstatic`
- [ ] Superuser ایجاد شده: `python manage.py createsuperuser`

### ✅ تنظیم Web App
- [ ] Web app جدید ایجاد شده (Manual Configuration)
- [ ] Python 3.10 انتخاب شده
- [ ] WSGI file path تنظیم شده: `/var/www/yourusername_pythonanywhere_com_wsgi.py`
- [ ] محتوای WSGI file با `pythonanywhere_wsgi.py` جایگزین شده

### ✅ Static Files
- [ ] Static files URL: `/static/`
- [ ] Static files Directory: `/home/yourusername/yourusername.pythonanywhere.com/static`
- [ ] Media files URL: `/media/`
- [ ] Media files Directory: `/home/yourusername/yourusername.pythonanywhere.com/media`

### ✅ Security Settings
- [ ] `yourusername` در همه فایل‌ها جایگزین شده
- [ ] SECRET_KEY قوی تولید و تنظیم شده
- [ ] DEBUG=False تنظیم شده
- [ ] ALLOWED_HOSTS شامل domain PythonAnywhere است

## بعد از استقرار (Post-Deployment)

### ✅ تست عملکرد
- [ ] سایت در مرورگر باز می‌شود: `https://yourusername.pythonanywhere.com`
- [ ] Admin panel کار می‌کند: `/admin/`
- [ ] API endpoints پاسخ می‌دهند: `/api/`
- [ ] Swagger UI قابل دسترسی است: `/api/schema/swagger-ui/`

### ✅ تست API
- [ ] Authentication endpoints کار می‌کنند
- [ ] CRUD operations روی models اصلی تست شده
- [ ] File upload/download کار می‌کند
- [ ] Pagination درست عمل می‌کند

### ✅ Monitoring و Logs
- [ ] Error logs بررسی شده: Web App → Error log
- [ ] Access logs بررسی شده
- [ ] Performance قابل قبول است
- [ ] Memory usage مناسب است

### ✅ Final Steps
- [ ] Domain name (اختیاری) تنظیم شده
- [ ] SSL certificate فعال است
- [ ] CORS settings برای frontend تنظیم شده
- [ ] Backup strategy برنامه‌ریزی شده

## عیب‌یابی (Troubleshooting)

### 🔧 مشکلات رایج:
- [ ] **500 Error**: Log files و Django settings بررسی شود
- [ ] **Database Error**: اطلاعات MySQL و permissions بررسی شود  
- [ ] **Static Files**: collectstatic و مسیرها بررسی شود
- [ ] **Import Error**: Python path و installed packages بررسی شود

### 🛠️ ابزارهای کمکی:
- [ ] `health_check_pythonanywhere.sh` اجرا شده
- [ ] `validate_deployment.sh` اجرا شده
- [ ] `python manage.py check` بدون خطا پاس شده

## Performance Optimization

### ⚡ بهینه‌سازی
- [ ] Database queries بهینه‌سازی شده
- [ ] Static files compression فعال شده
- [ ] Caching strategy پیاده‌سازی شده (Redis)
- [ ] Image optimization انجام شده

## Security Checklist

### 🔒 امنیت
- [ ] همه secret keys تغییر کرده‌اند
- [ ] Debug mode خاموش است
- [ ] SQL injection protection فعال است
- [ ] HTTPS enforcement فعال است
- [ ] Security headers تنظیم شده‌اند

## Maintenance

### 🔄 نگهداری
- [ ] Backup strategy تعریف شده
- [ ] Update procedure مستند شده
- [ ] Monitoring alerts تنظیم شده
- [ ] Documentation به‌روزرسانی شده

---

## نکات مهم:

1. **هر تغییر کد:** Web app را reload کنید
2. **تغییر static files:** collectstatic اجرا کنید
3. **تغییر database:** migration اجرا کنید
4. **مشکلات:** ابتدا logs را بررسی کنید

## منابع کمکی:

- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- فایل: `PYTHONANYWHERE_DEPLOYMENT_GUIDE.md`

---

✅ **استقرار موفق!** 🚀

Date: ___________
Deployed by: ___________
Domain: https://____________.pythonanywhere.com
