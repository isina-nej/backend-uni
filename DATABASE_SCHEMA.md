# 🗄️ نمودار روابط پایگاه داده - سیستم مدیریت دانشگاهی

## 📊 نمودار ER (Entity Relationship)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                             UNIVERSITY MANAGEMENT SYSTEM                            │
│                                  DATABASE SCHEMA                                   │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┐       ┌─────────────────────────┐       ┌─────────────────────────┐
│    OrganizationalUnit   │       │         Position        │       │         Permission      │
├─────────────────────────┤       ├─────────────────────────┤       ├─────────────────────────┤
│ 🔑 id (PK)              │       │ 🔑 id (PK)              │       │ 🔑 id (PK)              │
│ 📝 name                 │       │ 📝 title                │       │ 📝 name                 │
│ 📝 name_fa              │       │ 📝 title_fa             │       │ 📝 name_fa              │
│ 📝 type                 │       │ 📝 description          │       │ 📝 description          │
│ 📝 code                 │       │ 📝 level                │       │ 📝 category             │
│ 📝 description          │       │ 🔢 authority_level       │       │ ☑️ is_active             │
│ 🔗 parent_id (FK)       │       │ 🔗 organizational_unit  │       │ 📅 created_at           │
│ ☑️ is_active             │       │     _id (FK)            │       │                         │
│ 📅 created_at           │       │ ☑️ is_active             │       │                         │
│ 🌐 website              │       │ 📅 created_at           │       │                         │
│ 📞 phone                │       │                         │       │                         │
│ 📧 email                │       │                         │       │                         │
│ 📍 address              │       │                         │       │                         │
└─────────────────────────┘       └─────────────────────────┘       └─────────────────────────┘
           │                                     │                                     │
           │                                     │                                     │
           │ 1:Many                              │                                     │
           │                                     │ Many:Many                          │
           ▼                                     │ (through UserPosition)              │
┌─────────────────────────┐                     │                                     │
│         User            │                     │                                     │
├─────────────────────────┤◄────────────────────┘                                     │
│ 🔑 id (PK)              │                                                           │
│ 👤 username             │                                                           │
│ 📧 email                │                                                           │
│ 🔐 password             │                                                           │
│ 📝 first_name           │                                                           │
│ 📝 last_name            │                                                           │
│ 📝 first_name_fa        │                                                           │
│ 📝 last_name_fa         │                                                           │
│ 📝 role                 │                                                           │
│ 🆔 national_id          │                                                           │
│ 🎂 birth_date           │                                                           │
│ 👨‍👩‍👧‍👦 gender                │                                                           │
│ 📞 phone                │                                                           │
│ 📍 address              │                                                           │
│ 🖼️ avatar               │                                                           │
│ 📊 academic_rank        │                                                           │
│ 🎓 education_level      │                                                           │
│ 🏫 field_of_study       │                                                           │
│ 🆔 student_id           │                                                           │
│ 🆔 employee_id          │                                                           │
│ 💼 employment_type      │                                                           │
│ 📅 hire_date            │                                                           │
│ 🔗 organizational_unit  │                                                           │
│     _id (FK)            │                                                           │
│ ☑️ is_active             │                                                           │
│ ☑️ is_staff              │                                                           │
│ ☑️ is_superuser          │                                                           │
│ 📅 date_joined          │                                                           │
│ 📅 last_login           │                                                           │
│ 🔒 last_login_ip        │                                                           │
│ 📋 bio                  │                                                           │
│ 🌐 social_links         │                                                           │
│ 🏆 achievements         │                                                           │
│ 📜 certifications       │                                                           │
│ 💼 work_experience      │                                                           │
│ 🎯 skills               │                                                           │
│ 🗣️ languages            │                                                           │
│ 📞 emergency_contact    │                                                           │
│ 💾 preferences          │                                                           │
│ 📄 notes                │                                                           │
└─────────────────────────┘                                                           │
           │                                                                           │
           │ 1:Many                                                                    │
           │                                                                           │
           ▼                                                                           │
┌─────────────────────────┐       ┌─────────────────────────┐                       │
│      UserPosition       │       │      UserPermission     │◄──────────────────────┘
├─────────────────────────┤       ├─────────────────────────┤      Many:Many
│ 🔑 id (PK)              │       │ 🔑 id (PK)              │
│ 🔗 user_id (FK)         │       │ 🔗 user_id (FK)         │
│ 🔗 position_id (FK)     │       │ 🔗 permission_id (FK)   │
│ ☑️ is_primary            │       │ 🔗 organizational_unit  │
│ 📅 start_date           │       │     _id (FK)            │
│ 📅 end_date             │       │ 📅 granted_at           │
│ 📝 description          │       │ 📅 expires_at           │
│ ☑️ is_active             │       │ 🔗 granted_by_id (FK)   │
│ 📅 created_at           │       │ ☑️ is_active             │
└─────────────────────────┘       │ 📝 reason               │
                                  │ 📝 restrictions          │
                                  └─────────────────────────┘
                                             │
                                             │ 1:Many
                                             ▼
                                  ┌─────────────────────────┐
                                  │       AccessLog         │
                                  ├─────────────────────────┤
                                  │ 🔑 id (PK)              │
                                  │ 🔗 user_id (FK)         │
                                  │ 📝 action               │
                                  │ 📝 resource             │
                                  │ 📅 timestamp            │
                                  │ 🌐 ip_address           │
                                  │ 🖥️ user_agent           │
                                  │ ✅ success               │
                                  │ 📝 details              │
                                  │ 📝 session_id           │
                                  └─────────────────────────┘
```

## 🔗 روابط بین جداول

### 1️⃣ **OrganizationalUnit (واحد سازمانی)**
```sql
-- ساختار درختی (Tree Structure)
parent_id → OrganizationalUnit.id (Self-referencing)
```

### 2️⃣ **User (کاربر)**
```sql
-- ارتباط با واحد سازمانی
organizational_unit_id → OrganizationalUnit.id (Many-to-One)
```

### 3️⃣ **Position (سمت)**
```sql
-- ارتباط با واحد سازمانی
organizational_unit_id → OrganizationalUnit.id (Many-to-One)
```

### 4️⃣ **UserPosition (سمت کاربر)**
```sql
-- رابطه Many-to-Many بین User و Position
user_id → User.id
position_id → Position.id
```

### 5️⃣ **UserPermission (مجوز کاربر)**
```sql
-- رابطه Many-to-Many بین User و Permission
user_id → User.id
permission_id → Permission.id
organizational_unit_id → OrganizationalUnit.id (محدودیت دسترسی)
granted_by_id → User.id (چه کسی مجوز داده)
```

### 6️⃣ **AccessLog (لاگ دسترسی)**
```sql
-- ثبت فعالیت‌های کاربران
user_id → User.id (Many-to-One)
```

## 📋 انواع داده‌ها و فیلدها

### 🗂️ **انواع JSON Fields**
```python
# User Model
social_links = JSONField()          # لینک‌های شبکه‌های اجتماعی
achievements = JSONField()          # دستاورها
certifications = JSONField()        # گواهینامه‌ها  
work_experience = JSONField()       # سوابق کاری
skills = JSONField()                # مهارت‌ها
languages = JSONField()             # زبان‌ها
emergency_contact = JSONField()     # تماس اضطراری
preferences = JSONField()           # تنظیمات شخصی

# UserPermission Model
restrictions = JSONField()          # محدودیت‌های دسترسی

# AccessLog Model
details = JSONField()               # جزئیات فعالیت
```

### 📊 **Choices و Enums**
```python
# User Roles
ROLE_CHOICES = [
    ('STUDENT', 'دانشجو'),
    ('FACULTY', 'هیأت علمی'),
    ('STAFF', 'کارمند'),
    ('ADMIN', 'مدیر'),
    # ... and more
]

# Employment Types
EMPLOYMENT_CHOICES = [
    ('PERMANENT', 'رسمی'),
    ('CONTRACT', 'قراردادی'),
    ('PROJECT', 'پروژه‌ای'),
    # ... and more
]

# Academic Ranks
ACADEMIC_RANK_CHOICES = [
    ('INSTRUCTOR', 'مربی'),
    ('ASSISTANT_PROFESSOR', 'استادیار'),
    ('ASSOCIATE_PROFESSOR', 'دانشیار'),
    ('PROFESSOR', 'استاد'),
    # ... and more
]
```

## 🔍 ایندکس‌ها و بهینه‌سازی

### 📈 **Database Indexes**
```sql
-- کاربر
CREATE INDEX idx_user_role ON users_user(role);
CREATE INDEX idx_user_org_unit ON users_user(organizational_unit_id);
CREATE INDEX idx_user_active ON users_user(is_active);
CREATE INDEX idx_user_national_id ON users_user(national_id);

-- واحد سازمانی
CREATE INDEX idx_org_unit_parent ON users_organizationalunit(parent_id);
CREATE INDEX idx_org_unit_type ON users_organizationalunit(type);

-- سمت‌ها
CREATE INDEX idx_position_org_unit ON users_position(organizational_unit_id);
CREATE INDEX idx_user_position_user ON users_userposition(user_id);
CREATE INDEX idx_user_position_active ON users_userposition(is_active);

-- مجوزها
CREATE INDEX idx_user_permission_user ON users_userpermission(user_id);
CREATE INDEX idx_user_permission_org ON users_userpermission(organizational_unit_id);
CREATE INDEX idx_user_permission_active ON users_userpermission(is_active);

-- لاگ‌ها
CREATE INDEX idx_access_log_user ON users_accesslog(user_id);
CREATE INDEX idx_access_log_timestamp ON users_accesslog(timestamp);
CREATE INDEX idx_access_log_action ON users_accesslog(action);
```

## 🚀 Query Examples (نمونه کوئری‌ها)

### 1️⃣ **یافتن تمام اعضای یک واحد سازمانی**
```python
# تمام کاربران مستقیم واحد
unit = OrganizationalUnit.objects.get(name='Computer Science')
direct_members = User.objects.filter(organizational_unit=unit)

# تمام کاربران شامل زیرمجموعه‌ها
def get_all_unit_members(unit):
    """تمام اعضای یک واحد و زیرواحدهایش"""
    all_units = unit.get_descendants(include_self=True)
    return User.objects.filter(organizational_unit__in=all_units)
```

### 2️⃣ **یافتن تمام مجوزهای کاربر در واحد خاص**
```python
def get_user_permissions_in_unit(user, unit):
    """مجوزهای کاربر در واحد سازمانی خاص"""
    return UserPermission.objects.filter(
        user=user,
        organizational_unit=unit,
        is_active=True,
        expires_at__gt=timezone.now()
    ).select_related('permission')
```

### 3️⃣ **ساختار درختی واحدهای سازمانی**
```python
def get_organizational_tree():
    """دریافت ساختار درختی کامل"""
    root_units = OrganizationalUnit.objects.filter(
        parent=None, 
        is_active=True
    ).prefetch_related('children')
    
    return root_units
```

### 4️⃣ **آمار کاربران بر اساس نقش**
```python
def get_user_statistics():
    """آمار کاربران"""
    stats = User.objects.values('role').annotate(
        count=Count('id'),
        active_count=Count('id', filter=Q(is_active=True))
    )
    return stats
```

## 💾 حجم داده و عملکرد

### 📊 **تخمین حجم جداول**
- **User**: ~10,000 رکورد (دانشگاه متوسط)
- **OrganizationalUnit**: ~500 رکورد  
- **Position**: ~200 رکورد
- **UserPosition**: ~15,000 رکورد (چندسمتی)
- **Permission**: ~100 رکورد
- **UserPermission**: ~50,000 رکورد
- **AccessLog**: ~1,000,000 رکورد (سالانه)

### ⚡ **بهینه‌سازی عملکرد**
- استفاده از `select_related()` و `prefetch_related()`
- Cache کردن ساختار سازمانی
- Pagination برای لیست‌های بزرگ
- Archive کردن لاگ‌های قدیمی

## 🔒 امنیت پایگاه داده

### 🛡️ **محافظت از داده‌ها**
- Hash شدن رمزهای عبور (Django default)
- رمزگذاری اطلاعات حساس
- دسترسی محدود به فیلدهای شخصی
- Audit Trail کامل

### 🚨 **نظارت و گزارش‌گیری**
- ثبت تمام تغییرات در AccessLog
- نظارت بر دسترسی‌های مشکوک
- گزارش‌های امنیتی دوره‌ای

این ساختار پایگاه داده قابلیت پشتیبانی از دانشگاه‌های بزرگ با هزاران کاربر را دارد و امکان توسعه آینده را فراهم می‌کند.
