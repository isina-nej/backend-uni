# راهنمای کامل دیپلوی Django روی PythonAnywhere

## مرحله 1: آماده‌سازی کد (در کامپیوتر شما)

1. تغییرات را commit و push کنید:
```bash
git add .
git commit -m "Prepare for PythonAnywhere deployment"
git push origin main
```

## مرحله 2: تنظیم PythonAnywhere

### 2.1: ایجاد دیتابیس MySQL
1. وارد PythonAnywhere شوید
2. برو به تب "Databases"
3. یک دیتابیس MySQL جدید بساز
4. نام دیتابیس: `sinanej2$default` (خودکار ایجاد می‌شود)
5. رمز دیتابیس را یادداشت کن

### 2.2: کلون کردن پروژه
1. برو به تب "Consoles"
2. یک "Bash" کنسول جدید باز کن
3. دستورات زیر را اجرا کن:

```bash
# کلون کردن پروژه
cd ~
git clone https://github.com/isina-nej/backend-uni.git

# ایجاد virtual environment
python3.10 -m venv venv

# فعال کردن virtual environment
source venv/bin/activate

# نصب requirements
cd backend-uni
pip install --upgrade pip
pip install -r requirements.txt

# ایجاد secret key
SECRET_KEY=$(python generate_secret_key.py)
echo "Your secret key: $SECRET_KEY"

# ایجاد فایل .env
cat > .env << EOF
SECRET_KEY=$SECRET_KEY
DEBUG=False
DB_NAME=sinanej2\$default
DB_USER=sinanej2
DB_PASSWORD=YOUR_MYSQL_PASSWORD_HERE
DB_HOST=sinanej2.mysql.pythonanywhere-services.com
DB_PORT=3306
EOF

# ویرایش فایل .env و جایگذاری رمز واقعی دیتابیس
nano .env
# جایگزین کن: YOUR_MYSQL_PASSWORD_HERE با رمز واقعی MySQL

# تست تنظیمات
python manage.py check --settings=config.settings_production

# اجرای migration ها
python manage.py migrate --settings=config.settings_production

# ایجاد superuser
python manage.py createsuperuser --settings=config.settings_production

# جمع‌آوری فایل‌های static
python manage.py collectstatic --noinput --settings=config.settings_production
```

## مرحله 3: تنظیم Web App

### 3.1: ایجاد Web App
1. برو به تب "Web"
2. کلیک کن روی "Add a new web app"
3. Django را انتخاب کن
4. Python 3.10 را انتخاب کن
5. مسیر پروژه: `/home/sinanej2/backend-uni`

### 3.2: تنظیم WSGI File
1. در تب "Web"، روی لینک WSGI file کلیک کن
2. محتوای فایل را پاک کن و این کد را جایگذاری کن:

```python
import os
import sys

# Add your project directory to sys.path
project_home = '/home/sinanej2/backend-uni'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = '/home/sinanej2/venv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 3.3: تنظیم Static و Media Files
در تب "Web"، بخش "Static files":

1. **Static files**:
   - URL: `/static/`
   - Directory: `/home/sinanej2/static/`

2. **Media files** (اختیاری):
   - URL: `/media/`
   - Directory: `/home/sinanej2/media/`

## مرحله 4: راه‌اندازی نهایی

1. در تب "Web"، روی "Reload" کلیک کن
2. منتظر بمان تا وب‌اپ reload شود
3. برو به آدرس: https://sinanej2.pythonanywhere.com
4. باید صفحه Django را ببینی

## مرحله 5: تست API

برای تست API:
- Admin panel: https://sinanej2.pythonanywhere.com/admin/
- API root: https://sinanej2.pythonanywhere.com/api/

## رفع مشکلات رایج

### مشکل 1: ImportError
اگر خطای ImportError دیدی:
1. برو به Error logs در تب "Web"
2. بررسی کن که تمام packages نصب شده باشند
3. virtual environment درست فعال شده باشد

### مشکل 2: Database Connection Error
1. بررسی کن رمز MySQL در فایل .env درست باشد
2. نام دیتابیس باید `sinanej2$default` باشد
3. HOST باید `sinanej2.mysql.pythonanywhere-services.com` باشد

### مشکل 3: Static Files
اگر CSS/JS load نمی‌شود:
1. دوباره collectstatic اجرا کن:
```bash
cd ~/backend-uni
source ~/venv/bin/activate
python manage.py collectstatic --noinput --settings=config.settings_production
```

## بروزرسانی پروژه

برای بروزرسانی‌های آینده:
```bash
cd ~/backend-uni
source ~/venv/bin/activate
bash deploy.sh
```

سپس در تب "Web" روی "Reload" کلیک کن.

## نکات مهم

1. **همیشه** از `config.settings_production` استفاده کن
2. **هرگز** DEBUG=True در production قرار نده
3. رمز SECRET_KEY و دیتابیس را ایمن نگهدار
4. Log files در `/var/log/` قابل مشاهده هستند
5. برای troubleshooting از Error logs در تب "Web" استفاده کن
