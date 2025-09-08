# API Documentation
# This file provides examples and documentation for using the University Management System APIs

## Authentication APIs
POST /api/auth/login/
{
    "username": "admin",
    "password": "your_password"
}

GET /api/auth/profile/
Headers: Authorization: Token your_token_here

## User Management
GET /api/users/users/
POST /api/users/users/
{
    "username": "john_doe",
    "email": "john@university.com",
    "role": "student",
    "student_id": "20250001",
    "department": "Computer Science"
}

## Course Management
GET /api/courses/courses/
POST /api/courses/courses/
{
    "title": "Introduction to Programming",
    "code": "CS101",
    "description": "Basic programming concepts",
    "professor": 1
}

## Grades
GET /api/grades/grades/
POST /api/grades/grades/
{
    "student": 1,
    "course": 1,
    "score": 85.50,
    "grade_letter": "B"
}

## Announcements
GET /api/announcements/announcements/
POST /api/announcements/announcements/
{
    "title": "Important Notice",
    "content": "This is an important announcement",
    "target_audience": "students",
    "priority": "high"
}

## Assignments
GET /api/assignments/assignments/
POST /api/assignments/assignments/
{
    "title": "Homework 1",
    "description": "Complete exercises 1-10",
    "course": 1,
    "due_date": "2025-09-15T23:59:59Z",
    "max_score": 100.00
}

## Reports
GET /api/reports/dashboard/  # Admin dashboard stats
GET /api/reports/student/    # Individual student report
GET /api/reports/course/1/   # Course performance report

## Filtering and Search Examples
GET /api/announcements/announcements/?target_audience=students&priority=high
GET /api/grades/grades/?course=1&score__gte=80
GET /api/assignments/assignments/?search=homework
