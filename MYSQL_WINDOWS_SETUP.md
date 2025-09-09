# 🚀 راهنمای سریع نصب MySQL روی Windows

## مرحله 1: دانلود MySQL Installer
1. برو به: https://dev.mysql.com/downloads/installer/
2. دانلود **MySQL Installer for Windows**
3. فایل را اجرا کن

## مرحله 2: نصب MySQL Server
1. در نصب کننده، گزینه **"Developer Default"** رو انتخاب کن
2. منتظر بمون تا دانلود و نصب کامل بشه
3. در مرحله **"Type and Networking"**:
   - **Config Type**: Development Computer
   - **Connectivity**: TCP/IP
   - **Port**: 3306
   - **Open Firewall**: ✅ Yes

## مرحله 3: تنظیم Root Password
1. در مرحله **"Accounts and Roles"**:
   - **Root Password**: یک پسورد قوی انتخاب کن (مثل: `MySQL2025!`)
   - یادت باشه این پسورد رو

## مرحله 4: تکمیل نصب
1. روی **"Execute"** کلیک کن تا نصب کامل بشه
2. در پایان، **"Finish"** رو بزن

---

# 🔧 تنظیمات بعد از نصب

## مرحله 1: اضافه کردن MySQL به PATH
1. **Win + R** بزن و `sysdm.cpl` تایپ کن
2. تب **"Advanced"** → **"Environment Variables"**
3. در **"System Variables"**، **"Path"** رو پیدا کن
4. **"Edit"** → **"New"** → مسیر MySQL bin رو اضافه کن:
   ```
   C:\Program Files\MySQL\MySQL Server 8.0\bin
   ```

## مرحله 2: راه‌اندازی MySQL Service
1. **Win + R** → `services.msc`
2. **"MySQL80"** رو پیدا کن
3. راست کلیک → **"Start"**
4. اگر می‌خوای همیشه اجرا بشه: راست کلیک → **"Properties"** → **"Startup type"** → **"Automatic"**

---

# 🧪 تست اتصال MySQL

## مرحله 1: باز کردن Command Prompt
```cmd
mysql -u root -p
```

## مرحله 2: اگر خطا گرفتی:
```cmd
# اگر MySQL در PATH نیست:
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

## مرحله 3: ایجاد دیتابیس
```sql
CREATE DATABASE backend_uni_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
EXIT;
```

---

# ⚙️ بروزرسانی تنظیمات Django

## مرحله 1: ویرایش settings.py
فایل `config/settings.py` رو باز کن و قسمت DATABASES رو تغییر بده:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'backend_uni_db',
        'USER': 'root',
        'PASSWORD': 'MySQL2025!',  # پسورد خودت رو بذار
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

## مرحله 2: تست اتصال Django
```bash
cd d:\project\uni\backend
python test_mysql.py
```

## مرحله 3: اجرای Migration
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

# 🔍 عیب‌یابی مشکلات رایج

## خطای "Can't connect to server"
```bash
# بررسی وضعیت سرویس MySQL
net start mysql80

# یا در PowerShell:
Get-Service -Name mysql80
Start-Service -Name mysql80
```

## خطای "Access denied"
```sql
-- در MySQL shell:
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
```

## خطای "Port already in use"
```bash
# بررسی پورت
netstat -ano | findstr :3306

# تغییر پورت در my.ini
[mysqld]
port=3307
```

---

# 📱 گزینه‌های جایگزین (اگر نصب MySQL سخت بود)

## گزینه 1: XAMPP
1. دانلود از: https://www.apachefriends.org/
2. فقط MySQL رو فعال کن
3. تنظیمات مشابه بالا

## گزینه 2: MySQL Docker
```bash
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=MySQL2025! -e MYSQL_DATABASE=backend_uni_db -p 3306:3306 -d mysql:8.0
```

---

# ✅ چک لیست نهایی

- [ ] MySQL Server نصب شده
- [ ] MySQL Service اجرا می‌شود
- [ ] دیتابیس `backend_uni_db` ایجاد شده
- [ ] تنظیمات Django بروزرسانی شده
- [ ] اتصال تست شده
- [ ] Migration اجرا شده

اگر همه مراحل رو درست انجام بدی، مشکل حل می‌شه! 🎉
