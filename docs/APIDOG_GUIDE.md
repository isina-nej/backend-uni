# 🚀 راهنمای استفاده از APIdog برای University Management System

## 📁 import کردن Collection در APIdog

### مرحله 1: باز کردن APIdog
1. وارد [APIdog](https://apidog.com) شوید
2. یک workspace جدید بسازید یا از workspace موجود استفاده کنید

### مرحله 2: Import کردن فایل
1. روی **Import** کلیک کنید
2. فایل `apidog_collection.json` را انتخاب کنید
3. روی **Import** کلیک کنید

## 🏗️ ساختار فولدربندی Collection

### 🔐 Authentication
```
🔐 Authentication/
├── 🔑 Login (POST /api/auth/login/)
├── 🚪 Logout (POST /api/auth/logout/)
├── 👤 Get Profile (GET /api/auth/profile/)
└── ✏️ Update Profile (PUT /api/auth/profile/update/)
```

### 👥 User Management
```
👥 User Management/
├── 📋 List Users (GET /api/users/users/)
├── ➕ Create User (POST /api/users/users/)
└── 🔍 Search Users (GET /api/users/users/?search=...)
```

### 📚 Academic Modules
```
📚 Academic - Courses/
├── 📖 List Courses (GET /api/courses/courses/)
├── ➕ Create Course (POST /api/courses/courses/)
└── 🔍 Search Courses

📊 Academic - Grades/
├── 📊 List Grades (GET /api/grades/grades/)
├── ➕ Add Grade (POST /api/grades/grades/)
└── 📈 Filter by Course/Student

📅 Academic - Schedules/
├── 🗓️ View Schedule (GET /api/schedules/schedules/)
└── 📅 Filter by Day/Course

📝 Academic - Exams/
├── 📝 List Exams (GET /api/exams/exams/)
└── 🔍 Filter by Type/Date

📋 Academic - Assignments/
├── 📋 List Assignments (GET /api/assignments/assignments/)
├── ➕ Create Assignment (POST /api/assignments/assignments/)
├── 📝 List Submissions (GET /api/assignments/submissions/)
└── 📤 Submit Assignment (POST /api/assignments/submissions/)
```

### 🏛️ University Services
```
🏛️ Services - Library/
├── 📚 Browse Books (GET /api/library/books/)
├── 📖 Borrow Book (POST /api/library/borrowings/)
└── 📜 Borrowing History (GET /api/library/borrowings/)

💰 Services - Financial/
├── 💳 Payment History (GET /api/financial/payments/)
└── 🔍 Filter by Type/Status

✅ Services - Attendance/
├── ✅ Attendance Records (GET /api/attendance/records/)
└── 📊 Filter by Course/Date

🔬 Services - Research/
├── 🔬 Research Projects (GET /api/research/projects/)
└── 📈 Filter by Status
```

### 📢 Communication
```
📢 Communication - Announcements/
├── 📢 List Announcements (GET /api/announcements/announcements/)
├── ➕ Create Announcement (POST /api/announcements/announcements/)
└── 🔍 Filter by Priority/Audience

🔔 Communication - Notifications/
├── 🔔 Personal Notifications (GET /api/notifications/notifications/)
└── 📖 Mark as Read Filter
```

### 📈 Reports & Analytics
```
📈 Reports & Analytics/
├── 📊 Admin Dashboard (GET /api/reports/dashboard/)
├── 🎓 Student Report (GET /api/reports/student/)
└── 📚 Course Report (GET /api/reports/course/{id}/)
```

## 🛠️ تنظیمات Environment در APIdog

### Environment Variables
```json
{
  "base_url": "http://127.0.0.1:8000",
  "prod_url": "https://api.university.edu",
  "auth_token": "{{token}}",
  "student_id": "1",
  "course_id": "1",
  "admin_username": "admin",
  "admin_password": "admin123"
}
```

### Pre-request Script برای Authentication
```javascript
// Auto login and set token
const loginUrl = pm.environment.get("base_url") + "/api/auth/login/";
const username = pm.environment.get("admin_username");
const password = pm.environment.get("admin_password");

pm.sendRequest({
    url: loginUrl,
    method: 'POST',
    header: {
        'Content-Type': 'application/json',
    },
    body: {
        mode: 'raw',
        raw: JSON.stringify({
            username: username,
            password: password
        })
    }
}, function (err, response) {
    if (!err && response.code === 200) {
        const token = response.json().token;
        pm.environment.set("auth_token", token);
        console.log("Token set: " + token);
    }
});
```

## 🔧 استفاده از ویژگی‌های پیشرفته APIdog

### 1. 🧪 Test Scenarios
```javascript
// Test successful login
pm.test("Login successful", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json()).to.have.property('token');
    pm.expect(pm.response.json()).to.have.property('user');
});

// Test grade creation
pm.test("Grade created successfully", function () {
    pm.response.to.have.status(201);
    pm.expect(pm.response.json().score).to.be.a('number');
});
```

### 2. 📋 Mock Server
- در APIdog می‌توانید Mock Server فعال کنید
- برای تست Frontend بدون نیاز به Backend
- URL: `https://mock.apidog.com/your-project-id`

### 3. 🔄 API Documentation
- APIdog خودکار documentation تولید می‌کند
- قابلیت export به HTML/PDF
- اشتراک‌گذاری با تیم

### 4. 🧪 Automated Testing
```javascript
// Test Suite for Authentication
pm.test("Authentication Flow", function () {
    // Test login
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/auth/login/",
        method: 'POST',
        header: {'Content-Type': 'application/json'},
        body: {
            mode: 'raw',
            raw: JSON.stringify({
                username: "admin",
                password: "admin123"
            })
        }
    }, function(err, response) {
        pm.test("Login works", function() {
            pm.expect(response).to.have.property('code', 200);
        });
    });
});
```

## 📊 مثال‌های استفاده عملی

### 1. 🔐 ورود به سیستم
```http
POST {{base_url}}/api/auth/login/
Content-Type: application/json

{
    "username": "{{admin_username}}",
    "password": "{{admin_password}}"
}
```

### 2. 📚 ایجاد درس جدید
```http
POST {{base_url}}/api/courses/courses/
Authorization: Token {{auth_token}}
Content-Type: application/json

{
    "title": "ساختمان داده‌ها",
    "code": "CS201",
    "description": "مفاهیم پایه ساختمان داده‌ها",
    "professor": 1,
    "credits": 3
}
```

### 3. 📢 انتشار اعلان
```http
POST {{base_url}}/api/announcements/announcements/
Authorization: Token {{auth_token}}
Content-Type: application/json

{
    "title": "شروع ترم جدید",
    "content": "ترم جدید از تاریخ 1 مهر آغاز می‌شود",
    "target_audience": "students",
    "priority": "high"
}
```

### 4. 📊 مشاهده گزارش دانشجو
```http
GET {{base_url}}/api/reports/student/
Authorization: Token {{auth_token}}
```

## 🎯 بهترین روش‌های استفاده

### 1. 📁 سازماندهی Requests
- از فولدربندی منطقی استفاده کنید
- نام‌گذاری واضح برای requestها
- توضیحات کامل برای هر endpoint

### 2. 🔄 Environment Management
- Development, Staging, Production environments
- متغیرهای مشترک در environment
- Token management خودکار

### 3. 🧪 Testing Strategy
- تست‌های خودکار برای هر endpoint
- Validation of response structure
- Error handling tests

### 4. 📚 Documentation
- توضیحات کامل برای هر API
- مثال‌های واقعی
- راهنمای استفاده برای developers

## 🚀 نکات پیشرفته

### 1. 🔄 Batch Operations
```javascript
// ایجاد چندین دانشجو به صورت batch
const students = [
    {username: "student1", email: "s1@uni.edu", role: "student"},
    {username: "student2", email: "s2@uni.edu", role: "student"},
    {username: "student3", email: "s3@uni.edu", role: "student"}
];

students.forEach(student => {
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/users/users/",
        method: 'POST',
        header: {
            'Authorization': 'Token ' + pm.environment.get("auth_token"),
            'Content-Type': 'application/json'
        },
        body: {
            mode: 'raw',
            raw: JSON.stringify(student)
        }
    });
});
```

### 2. 📊 Performance Testing
```javascript
// تست سرعت response
pm.test("Response time is less than 200ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(200);
});
```

### 3. 🔍 Dynamic Testing
```javascript
// تست پویا بر اساس داده‌های دریافتی
pm.test("All users have required fields", function () {
    const users = pm.response.json().results;
    users.forEach(user => {
        pm.expect(user).to.have.property('username');
        pm.expect(user).to.have.property('email');
        pm.expect(user).to.have.property('role');
    });
});
```

---

## 🎉 نتیجه‌گیری

با این collection کامل در APIdog، شما می‌توانید:
- ✅ تمام API های سیستم را تست کنید
- ✅ Documentation کامل و حرفه‌ای داشته باشید
- ✅ تست‌های خودکار راه‌اندازی کنید
- ✅ با تیم توسعه به راحتی همکاری کنید
- ✅ Mock server برای Frontend استفاده کنید

**فایل `apidog_collection.json` آماده import در APIdog است!** 🚀
