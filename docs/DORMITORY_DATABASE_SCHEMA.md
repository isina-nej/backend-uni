# 🏠 سیستم مدیریت خوابگاه - مستندات ساختار دیتابیس

## 🏗️ نمای کلی ساختار

سیستم مدیریت خوابگاه شامل 7 مدل اصلی است که به صورت سلسله‌مراتبی طراحی شده‌اند:

```
دانشگاه
  └── مجموعه خوابگاهی (DormitoryComplex) - جداسازی برادران/خواهران
      └── ساختمان (DormitoryBuilding) - چندین ساختمان در هر مجموعه
          └── طبقه (DormitoryFloor) - چندین طبقه در هر ساختمان
              └── اتاق (DormitoryRoom) - چندین اتاق در هر طبقه
                  └── اسکان (DormitoryAccommodation) - اسکان دانشجویان
```

---

## 📊 جداول اصلی

### 1️⃣ **DormitoryComplex** (مجموعه خوابگاهی)
**هدف**: مدیریت مجموعه‌های خوابگاهی جداگانه برای برادران و خواهران

**فیلدهای کلیدی**:
```python
- id (UUID, PK)
- name (varchar) - نام مجموعه خوابگاهی
- code (varchar, unique) - کد مجموعه
- gender (choice) - MALE/FEMALE (جداسازی اجباری)
- address (text) - آدرس کامل
- manager (FK to User) - مدیر مجموعه خوابگاهی
- facilities (JSON) - امکانات کلی
- rules (JSON) - قوانین مجموعه
- is_active (boolean)
```

**ویژگی‌های مهم**:
- ✅ جداسازی کامل برادران و خواهران
- ✅ هر مجموعه یک مدیر دارد
- ✅ امکانات و قوانین قابل تنظیم

### 2️⃣ **DormitoryBuilding** (ساختمان خوابگاه)
**هدف**: مدیریت ساختمان‌های مختلف در هر مجموعه

**فیلدهای کلیدی**:
```python
- id (UUID, PK)
- complex (FK to DormitoryComplex)
- name (varchar) - نام ساختمان
- code (varchar) - کد ساختمان (منحصر به فرد در مجموعه)
- floor_count (int) - تعداد طبقات
- supervisor (FK to User) - سرپرست ساختمان
- maintenance_status (choice) - وضعیت نگهداری
- has_elevator, has_laundry, has_kitchen, etc. - امکانات
- construction_year (int) - سال ساخت
- total_area (int) - مساحت کل
```

**قابلیت‌ها**:
- 🏢 تا 20 طبقه پشتیبانی می‌شود
- 🔧 ردیابی وضعیت نگهداری
- 👥 سرپرست اختصاصی برای هر ساختمان

### 3️⃣ **DormitoryFloor** (طبقه خوابگاه)
**هدف**: مدیریت طبقات در هر ساختمان

**فیلدهای کلیدی**:
```python
- id (UUID, PK)
- building (FK to DormitoryBuilding)
- floor_number (int) - شماره طبقه
- name (varchar) - نام اختیاری طبقه
- supervisor (FK to User) - سرپرست طبقه
- has_common_room, has_kitchen, has_bathroom - امکانات طبقه
```

**خصوصیات**:
- 🔢 شماره‌گذاری خودکار طبقات
- 👤 سرپرست اختیاری برای هر طبقه
- 🏠 امکانات مشترک قابل تعریف

### 4️⃣ **DormitoryRoom** (اتاق خوابگاه) ⭐
**هدف**: مدیریت جزئیات اتاق‌ها - مهم‌ترین بخش سیستم

**فیلدهای کلیدی**:
```python
- id (UUID, PK)
- floor (FK to DormitoryFloor)
- room_number (varchar) - شماره اتاق
- room_code (varchar, unique) - کد منحصر به فرد اتاق
- room_type (choice) - SINGLE/DOUBLE/TRIPLE/QUAD/SUITE
- capacity (int) - ظرفیت اتاق (1-6 نفر)
- status (choice) - AVAILABLE/OCCUPIED/MAINTENANCE/RESERVED/OUT_OF_ORDER
- area (int) - مساحت به متر مربع
```

**امکانات اتاق**:
```python
- has_private_bathroom (boolean)
- has_balcony (boolean)
- has_air_conditioning (boolean)
- has_heating (boolean)
- has_internet (boolean)
```

**محدودیت‌ها و شرایط**:
```python
- academic_level_restriction (JSON) - محدودیت مقطع تحصیلی
- min_gpa (decimal) - حداقل معدل مورد نیاز
- special_conditions (JSON) - شرایط خاص
```

**قیمت‌گذاری**:
```python
- monthly_rent (decimal) - اجاره ماهانه
- deposit (decimal) - ودیعه
```

**ویژگی‌های پیشرفته**:
- 🏷️ تولید خودکار کد اتاق: `{complex_code}-{building_code}-{floor}-{room}`
- 📊 محاسبه خودکار اشغال فعلی و تخت‌های خالی
- ⚡ بررسی خودکار ظرفیت بر اساس نوع اتاق

### 5️⃣ **DormitoryAccommodation** (اسکان دانشجو)
**هدف**: مدیریت اسکان دانشجویان در اتاق‌ها

**فیلدهای کلیدی**:
```python
- id (UUID, PK)
- student (FK to User) - دانشجو
- room (FK to DormitoryRoom) - اتاق
- start_date, end_date (date) - بازه زمانی اسکان
- actual_end_date (date) - تاریخ واقعی خروج
- status (choice) - PENDING/APPROVED/ACTIVE/SUSPENDED/TERMINATED/CANCELLED
- monthly_payment (decimal) - پرداخت ماهانه
- deposit_paid (decimal) - ودیعه پرداخت شده
- approved_by (FK to User) - تأیید کننده
- approved_at (datetime) - زمان تأیید
```

**ویژگی‌های امنیتی**:
- 🔐 بررسی جنسیت دانشجو با خوابگاه
- 📅 بررسی تداخل زمانی با سایر اسکان‌ها
- 🏠 بررسی ظرفیت اتاق قبل از تأیید

### 6️⃣ **DormitoryStaff** (کارکنان خوابگاه)
**هدف**: مدیریت کارکنان و سرپرستان خوابگاه

**نقش‌های مختلف**:
```python
ROLE_CHOICES = [
    ('MANAGER', 'مدیر خوابگاه'),           # مدیر کل مجموعه
    ('SUPERVISOR', 'سرپرست'),            # سرپرست ساختمان/طبقه
    ('GUARD', 'نگهبان'),
    ('CLEANER', 'نظافتچی'),
    ('MAINTENANCE', 'تعمیرکار'),
    ('KITCHEN_STAFF', 'کارمند آشپزخانه'),
    ('ADMIN', 'اداری'),
]
```

**شیفت‌ها**:
```python
SHIFT_CHOICES = [
    ('MORNING', 'صبح'),
    ('EVENING', 'عصر'),
    ('NIGHT', 'شب'),
    ('FULL_TIME', 'تمام وقت'),
]
```

### 7️⃣ **DormitoryMaintenance** (تعمیرات و نگهداری)
**هدف**: مدیریت درخواست‌های تعمیرات

**فیلدهای کلیدی**:
```python
- room (FK to DormitoryRoom) - اتاق مربوطه
- reported_by (FK to User) - گزارش‌دهنده
- assigned_to (FK to User) - محول شده به
- title (varchar) - عنوان مشکل
- category (choice) - ELECTRICAL/PLUMBING/HEATING/COOLING/etc.
- priority (choice) - LOW/MEDIUM/HIGH/URGENT
- status (choice) - REPORTED/ASSIGNED/IN_PROGRESS/COMPLETED/CANCELLED
- estimated_cost, actual_cost (decimal) - هزینه‌ها
```

**ردیابی زمان**:
```python
- reported_at (datetime) - زمان گزارش
- assigned_at (datetime) - زمان محولی  
- started_at (datetime) - زمان شروع کار
- completed_at (datetime) - زمان تکمیل
```

---

## 🔗 روابط بین جداول

### **روابط سلسله‌مراتبی**:
```
DormitoryComplex (1) ──→ (Many) DormitoryBuilding
DormitoryBuilding (1) ──→ (Many) DormitoryFloor  
DormitoryFloor (1) ──→ (Many) DormitoryRoom
DormitoryRoom (1) ──→ (Many) DormitoryAccommodation
```

### **روابط مدیریتی**:
```
User ──→ DormitoryComplex.manager (مدیر مجموعه)
User ──→ DormitoryBuilding.supervisor (سرپرست ساختمان)
User ──→ DormitoryFloor.supervisor (سرپرست طبقه)
User ──→ DormitoryStaff.user (کارکنان)
```

### **روابط عملیاتی**:
```
User (Student) ──→ DormitoryAccommodation (اسکان)
User ──→ DormitoryMaintenance.reported_by (گزارش‌دهنده)
User ──→ DormitoryMaintenance.assigned_to (تعمیرکار)
```

---

## 🎯 ویژگی‌های کلیدی سیستم

### 🔒 **امنیت و کنترل دسترسی**:
- ✅ جداسازی کامل برادران و خواهران
- ✅ بررسی جنسیت در تمام سطوح
- ✅ کنترل دسترسی بر اساس نقش کاربر
- ✅ لاگ کامل تمام تغییرات

### 📊 **مدیریت ظرفیت**:
- ✅ محاسبه خودکار ظرفیت در تمام سطوح
- ✅ ردیابی لحظه‌ای اشغال اتاق‌ها
- ✅ هشدار هنگام تکمیل ظرفیت
- ✅ پیش‌بینی ظرفیت آینده

### 🔧 **سیستم نگهداری**:
- ✅ ثبت و پیگیری درخواست‌های تعمیرات
- ✅ اولویت‌بندی بر اساس اهمیت
- ✅ تخصیص خودکار به تعمیرکاران
- ✅ ردیابی هزینه‌ها

### 📱 **API و Integration**:
- ✅ REST API کامل برای تمام عملیات
- ✅ فیلترهای پیشرفته
- ✅ پاگینیشن و جستجو
- ✅ آماده برای اپلیکیشن موبایل

### 📈 **گزارش‌گیری**:
- ✅ آمار لحظه‌ای اشغال
- ✅ گزارش‌های مالی
- ✅ تحلیل روند اسکان
- ✅ آمار تعمیرات

---

## 🚀 مثال‌های کاربردی

### **ساختار نمونه**:
```
دانشگاه ABC
├── خوابگاه برادران شهید بهشتی (کد: BR-BEH)
│   ├── ساختمان الف (کد: A) - 4 طبقه
│   │   ├── طبقه 1 - 20 اتاق دو نفره
│   │   ├── طبقه 2 - 20 اتاق دو نفره  
│   │   ├── طبقه 3 - 15 اتاق دو نفره + 5 اتاق تک
│   │   └── طبقه 4 - 10 اتاق سوئیت چهار نفره
│   └── ساختمان ب (کد: B) - 3 طبقه
└── خوابگاه خواهران فاطمه زهرا (کد: SI-FAT)
    ├── ساختمان الف (کد: A) - 5 طبقه
    └── ساختمان ب (کد: B) - 5 طبقه
```

### **کد اتاق نمونه**:
```
BR-BEH-A-3-15  = برادران بهشتی، ساختمان الف، طبقه 3، اتاق 15
SI-FAT-B-2-08  = خواهران فاطمه، ساختمان ب، طبقه 2، اتاق 8
```

### **سناریو اسکان**:
1. دانشجو درخواست اسکان می‌دهد
2. سیستم اتاق‌های مناسب را پیشنهاد می‌دهد
3. مدیر درخواست را بررسی و تأیید می‌کند
4. دانشجو به اتاق اختصاص می‌یابد
5. ظرفیت اتاق به‌روزرسانی می‌شود

این ساختار قابلیت پشتیبانی از دانشگاه‌های بزرگ با هزاران دانشجو را دارد و به راحتی قابل توسعه است.
