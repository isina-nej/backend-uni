# MySQL Setup for PythonAnywhere

## 📋 تنظیم MySQL در PythonAnywhere

### مرحله 1: فعال کردن MySQL
1. برو به [PythonAnywhere Dashboard](https://www.pythonanywhere.com/user/sinanej2/)
2. روی تب **"Databases"** کلیک کن
3. در بخش **"MySQL"** روی **"Create a database"** کلیک کن
4. نام دیتابیس: `backend_uni_db`
5. پسورد رو یادداشت کن

### مرحله 2: بروزرسانی تنظیمات
در فایل `config/settings_production.py` قسمت DATABASES رو تغییر بده:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sinanej2$backend_uni_db',  # نام دیتابیس PythonAnywhere
        'USER': 'sinanej2',  # یوزرنیم PythonAnywhere
        'PASSWORD': 'YOUR_MYSQL_PASSWORD',  # پسورد دیتابیس
        'HOST': 'sinanej2.mysql.pythonanywhere-services.com',  # هاست MySQL
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### مرحله 3: بروزرسانی requirements.txt
در PythonAnywhere console:

```bash
cd /home/sinanej2/backend-uni
workon backend-uni-env
pip uninstall psycopg2-binary
pip install mysqlclient
```

### مرحله 4: اجرای Migration
```bash
python manage.py migrate --settings=config.settings_production
```

### مرحله 5: ایجاد Superuser
```bash
python manage.py createsuperuser --settings=config.settings_production
```

## 🔧 عیب‌یابی

### اگر mysqlclient نصب نشد:
```bash
pip install pymysql
```

سپس در `settings_production.py` اضافه کنید:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### بررسی اتصال دیتابیس:
```bash
python manage.py dbshell --settings=config.settings_production
```

### اگر مشکل داشتید:
1. اطلاعات دیتابیس رو از تب Databases چک کنید
2. مطمئن شوید virtual environment فعال است
3. لاگ‌های error رو چک کنید
