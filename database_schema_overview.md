# 🗄️ ساختار دیتابیس سیستم مدیریت دانشگاهی

## 📊 نمای کلی ساختار دیتابیس

### 🔥 تیبل‌های اصلی (Core Tables)

#### 1️⃣ **Users** (کاربران) - `apps_users_user`
```sql
- id (Primary Key)
- username (unique, VARCHAR(150))
- email (VARCHAR(254))
- first_name (VARCHAR(150))
- last_name (VARCHAR(150))
- password (hashed)
- role (CHOICES: student, professor, admin, staff)
- student_id (VARCHAR(20), optional)
- department (VARCHAR(100), optional)
- is_active (Boolean)
- is_staff (Boolean)
- is_superuser (Boolean)
- date_joined (DateTime)
- last_login (DateTime)
```

**ویژگی‌ها:**
- ✅ نقش‌بندی کاربران (4 نوع: دانشجو، استاد، ادمین، کارمند)
- ✅ شماره دانشجویی برای دانشجویان
- ✅ دپارتمان برای هر کاربر
- ✅ سیستم احراز هویت Django built-in

---

### 📚 بخش آکادمیک (Academic Section)

#### 2️⃣ **Courses** (دروس) - `apps_courses_course`
```sql
- id (Primary Key)
- title (VARCHAR(200))
- code (VARCHAR(20), unique)
- description (Text)
- professor_id (Foreign Key -> User)
- created_at (DateTime)
```

**رابطه Many-to-Many:**
- `students` -> User (دانشجویان ثبت‌نام شده)

#### 3️⃣ **Grades** (نمرات) - `apps_grades_grade`
```sql
- id (Primary Key)
- student_id (Foreign Key -> User)
- course_id (Foreign Key -> Course)
- professor_id (Foreign Key -> User, nullable)
- score (Decimal(5,2))
- grade_letter (VARCHAR(2))
- date_assigned (Date)
```

#### 4️⃣ **Assignments** (تکالیف) - `apps_assignments_assignment`
```sql
- id (Primary Key)
- title (VARCHAR(200))
- description (Text)
- course_id (Foreign Key -> Course)
- professor_id (Foreign Key -> User)
- due_date (DateTime)
- max_score (Decimal(5,2), default=100.00)
- created_at (DateTime)
```

#### 5️⃣ **Submissions** (پاسخ تکالیف) - `apps_assignments_submission`
```sql
- id (Primary Key)
- assignment_id (Foreign Key -> Assignment)
- student_id (Foreign Key -> User)
- submitted_at (DateTime)
- content (Text)
- file_url (URL, optional)
- score (Decimal(5,2), nullable)
- feedback (Text)
- graded_at (DateTime, nullable)

UNIQUE CONSTRAINT: (assignment_id, student_id)
```

#### 6️⃣ **Schedules** (برنامه کلاس‌ها) - `apps_schedules_schedule`
```sql
- id (Primary Key)
- course_id (Foreign Key -> Course)
- professor_id (Foreign Key -> User)
- day_of_week (CHOICES: monday-sunday)
- start_time (Time)
- end_time (Time)
- location (VARCHAR(100))
```

#### 7️⃣ **Exams** (امتحانات) - `apps_exams_exam`
```sql
- id (Primary Key)
- course_id (Foreign Key -> Course)
- professor_id (Foreign Key -> User)
- title (VARCHAR(200))
- date (Date)
- start_time (Time)
- end_time (Time)
- location (VARCHAR(100))
```

#### 8️⃣ **Attendance** (حضور و غیاب) - `apps_attendance_attendance`
```sql
- id (Primary Key)
- student_id (Foreign Key -> User)
- schedule_id (Foreign Key -> Schedule)
- date (Date)
- is_present (Boolean, default=False)
```

---

### 🏛️ بخش خدمات دانشگاهی (University Services)

#### 9️⃣ **Library Books** (کتاب‌های کتابخانه) - `apps_library_book`
```sql
- id (Primary Key)
- title (VARCHAR(200))
- author (VARCHAR(100))
- isbn (VARCHAR(13), unique)
- available_copies (PositiveInteger)
- total_copies (PositiveInteger)
```

#### 🔟 **Library Loans** (امانت کتاب‌ها) - `apps_library_loan`
```sql
- id (Primary Key)
- user_id (Foreign Key -> User)
- book_id (Foreign Key -> Book)
- loan_date (Date)
- return_date (Date, nullable)
- is_returned (Boolean, default=False)
```

#### 1️⃣1️⃣ **Financial Payments** (پرداخت‌ها) - `apps_financial_payment`
```sql
- id (Primary Key)
- user_id (Foreign Key -> User)
- amount (Decimal(10,2))
- description (VARCHAR(200))
- payment_date (Date)
- is_paid (Boolean, default=False)
```

#### 1️⃣2️⃣ **Research Projects** (پروژه‌های تحقیقاتی) - `apps_research_researchproject`
```sql
- id (Primary Key)
- title (VARCHAR(200))
- description (Text)
- lead_researcher_id (Foreign Key -> User)
- start_date (Date)
- end_date (Date, nullable)
- status (CHOICES: ongoing, completed, paused)
```

**رابطه Many-to-Many:**
- `team_members` -> User (اعضای تیم)

---

### 📢 بخش ارتباطات (Communication Section)

#### 1️⃣3️⃣ **Announcements** (اعلان‌ها) - `apps_announcements_announcement`
```sql
- id (Primary Key)
- title (VARCHAR(200))
- content (Text)
- author_id (Foreign Key -> User)
- target_audience (CHOICES: all, students, professors, staff, admins)
- priority (CHOICES: low, medium, high, urgent)
- is_published (Boolean, default=True)
- created_at (DateTime)
- updated_at (DateTime)
- expires_at (DateTime, nullable)
```

#### 1️⃣4️⃣ **Notifications** (اطلاعیه‌ها) - `apps_notifications_notification`
```sql
- id (Primary Key)
- user_id (Foreign Key -> User)
- platform (CHOICES: web, flutter, telegram, discord, slack)
- title (VARCHAR(200))
- message (Text)
- is_read (Boolean, default=False)
- created_at (DateTime)
```

---

## 🔗 روابط بین تیبل‌ها (Relationships)

### 🎯 **One-to-Many Relationships:**
1. **User** → **Courses** (یک استاد چندین درس)
2. **User** → **Grades** (یک دانشجو چندین نمره)
3. **User** → **Assignments** (یک استاد چندین تکلیف)
4. **User** → **Submissions** (یک دانشجو چندین پاسخ)
5. **Course** → **Grades** (یک درس چندین نمره)
6. **Course** → **Assignments** (یک درس چندین تکلیف)
7. **Assignment** → **Submissions** (یک تکلیف چندین پاسخ)

### 🔗 **Many-to-Many Relationships:**
1. **Course** ↔ **User** (students) - دانشجویان ثبت‌نام شده
2. **ResearchProject** ↔ **User** (team_members) - اعضای تیم تحقیق

### 🎪 **Unique Constraints:**
- `User.username` - نام کاربری یکتا
- `Course.code` - کد درس یکتا
- `Book.isbn` - شابک کتاب یکتا
- `(Assignment, Student)` - هر دانشجو یک پاسخ به هر تکلیف

---

## 📈 آمار و اندازه‌گیری

### 👥 **انواع کاربران و دسترسی‌ها:**

#### 🎓 **Student (دانشجو):**
- ✅ مشاهده نمرات خود
- ✅ ثبت‌نام در دروس
- ✅ ارسال تکالیف
- ✅ مشاهده برنامه کلاس‌ها
- ✅ امانت کتاب از کتابخانه
- ✅ مشاهده اعلان‌ها
- ✅ دریافت اطلاعیه‌ها

#### 👨‍🏫 **Professor (استاد):**
- ✅ مدیریت دروس خود
- ✅ ثبت نمرات دانشجویان
- ✅ ایجاد و مدیریت تکالیف
- ✅ تنظیم برنامه کلاس‌ها
- ✅ ثبت حضور و غیاب
- ✅ مدیریت پروژه‌های تحقیقاتی

#### 👔 **Staff (کارمند):**
- ✅ مدیریت کتابخانه
- ✅ انتشار اعلان‌ها
- ✅ مدیریت امور مالی
- ✅ مشاهده گزارش‌ها

#### 🔑 **Admin (مدیر):**
- ✅ دسترسی کامل به تمام بخش‌ها
- ✅ مدیریت کاربران
- ✅ مشاهده آمار کلی سیستم
- ✅ مدیریت تمام داده‌ها

---

## 🛠️ بهینه‌سازی‌های اعمال شده

### 🚀 **Database Optimization:**
1. **Indexing** - روی فیلدهای پرکاربرد مثل username, email, course_code
2. **Foreign Key Constraints** - حفظ یکپارچگی داده‌ها
3. **Unique Constraints** - جلوگیری از تکرار داده‌ها
4. **Cascade Deletions** - حذف خودکار داده‌های وابسته
5. **Default Values** - مقادیر پیش‌فرض برای فیلدهای اختیاری

### 📊 **Query Optimization:**
1. **Related Name** - دسترسی آسان به روابط معکوس
2. **Select Related** - کاهش تعداد query ها
3. **Prefetch Related** - بهینه‌سازی Many-to-Many
4. **Database Functions** - استفاده از توابع MySQL

### 🔒 **Security Features:**
1. **Password Hashing** - رمزگذاری پسوردها
2. **Token Authentication** - احراز هویت امن
3. **Permission System** - کنترل دسترسی بر اساس نقش
4. **Data Validation** - اعتبارسنجی ورودی‌ها

---

## 🎯 نکات مهم طراحی

### ✅ **مزایا:**
- 🔥 طراحی مدولار و قابل توسعه
- 🛡️ امنیت بالا با نقش‌بندی کاربران  
- 📊 گزارش‌گیری جامع و دقیق
- 🔗 روابط منطقی بین تیبل‌ها
- 🚀 بهینه‌سازی برای عملکرد بالا

### 🎪 **ویژگی‌های خاص:**
- 🌐 پشتیبانی از چندین platform برای notifications
- 📱 طراحی آماده برای موبایل اپ
- 🤖 آماده برای bot integration
- 📈 سیستم گزارش‌گیری پیشرفته
- 🔄 قابلیت backup و restore

این ساختار برای دانشگاه متوسط با حدود 1000-5000 کاربر بهینه شده و قابلیت مقیاس‌پذیری بالایی دارد.
