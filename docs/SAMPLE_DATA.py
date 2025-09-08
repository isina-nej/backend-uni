# Sample data for testing the University Management System

# Create some test data after setting up the system

# Test Users
from apps.users.models import User
from apps.courses.models import Course
from apps.announcements.models import Announcement

# Sample API calls you can test:

# 1. Authentication
# POST /api/auth/login/
# {
#     "username": "admin",
#     "password": "your_password"
# }

# 2. Get user profile
# GET /api/auth/profile/
# Headers: Authorization: Token your_token_here

# 3. Create announcement
# POST /api/announcements/announcements/
# Headers: Authorization: Token your_token_here
# {
#     "title": "Welcome to New Semester",
#     "content": "Welcome all students to the new academic semester!",
#     "target_audience": "students",
#     "priority": "high"
# }

# 4. List assignments  
# GET /api/assignments/assignments/
# Headers: Authorization: Token your_token_here

# 5. Student report
# GET /api/reports/student/
# Headers: Authorization: Token your_token_here

# 6. Dashboard stats (admin only)
# GET /api/reports/dashboard/
# Headers: Authorization: Token your_token_here
