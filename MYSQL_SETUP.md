# MySQL Setup Guide for Backend Project

## 📋 پیش‌نیازها

### Windows
1. **MySQL Server** را دانلود و نصب کنید:
   - از [MySQL Official Website](https://dev.mysql.com/downloads/mysql/) دانلود کنید
   - یا از [XAMPP](https://www.apachefriends.org/) استفاده کنید

2. **MySQL Workbench** (اختیاری اما توصیه می‌شود):
   - از [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) دانلود کنید

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

### macOS
```bash
brew install mysql
brew services start mysql
```

## 🔧 تنظیمات اولیه MySQL

### 1. ورود به MySQL
```bash
mysql -u root -p
```

### 2. ایجاد دیتابیس
```sql
CREATE DATABASE backend_uni_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. ایجاد کاربر (اختیاری)
```sql
CREATE USER 'backend_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON backend_uni_db.* TO 'backend_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. تنظیمات امنیتی (توصیه می‌شود)
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_secure_password';
```

## ⚙️ تنظیمات پروژه

### 1. بروزرسانی فایل settings.py
فایل `config/settings.py` را باز کنید و قسمت DATABASES را پیدا کنید:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'backend_uni_db',
        'USER': 'root',  # یا نام کاربری که ایجاد کردید
        'PASSWORD': 'your_password',  # پسورد MySQL
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### 2. نصب mysqlclient
```bash
pip install mysqlclient
```

### 3. اجرای Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. ایجاد Superuser
```bash
python manage.py createsuperuser
```

## 🔍 عیب‌یابی مشکلات رایج

### خطای "mysqlclient not found"
```bash
# Windows
pip install mysqlclient

# اگر مشکل داشتید:
pip install pymysql
# سپس در settings.py اضافه کنید:
import pymysql
pymysql.install_as_MySQLdb()
```

### خطای اتصال
- مطمئن شوید MySQL Server اجرا می‌شود
- پورت 3306 باز است
- نام کاربری و پسورد درست است

### خطای Character Set
```sql
ALTER DATABASE backend_uni_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### خطای Authentication
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
```

## 🚀 راه‌اندازی سرور

```bash
python manage.py runserver
```

## 📊 مدیریت دیتابیس

### با MySQL Workbench
1. اتصال به localhost:3306
2. انتخاب دیتابیس backend_uni_db
3. مشاهده جداول و داده‌ها

### با Command Line
```bash
mysql -u root -p backend_uni_db
SHOW TABLES;
DESCRIBE users_user;  # مثال
```

## 🔄 تغییر از PostgreSQL به MySQL

اگر قبلاً از PostgreSQL استفاده می‌کردید:

1. **پشتیبان‌گیری** از داده‌های فعلی (اگر لازم است)
2. تنظیمات DATABASES را تغییر دهید
3. `pip install mysqlclient` و `pip uninstall psycopg2-binary`
4. `python manage.py migrate --run-syncdb` برای ایجاد جداول جدید
5. اگر داده دارید، از ابزارهای migration استفاده کنید

## 📝 نکات مهم

- **Backup**: همیشه از دیتابیس پشتیبان‌گیری کنید
- **Security**: از پسوردهای قوی استفاده کنید
- **Performance**: MySQL برای read-heavy workloads بهتر است
- **Compatibility**: مطمئن شوید همه فیلدهای مدل‌ها با MySQL سازگار هستند

## 🆘 پشتیبانی

اگر مشکل داشتید:
1. لاگ‌های Django را چک کنید: `python manage.py check`
2. اتصال MySQL را تست کنید: `mysql -u root -p`
3. تنظیمات DATABASES را دوباره چک کنید
