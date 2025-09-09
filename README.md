# University Management System - Backend

A comprehensive Django REST API backend for university management system with support for multiple platforms including web, Flutter app, and various bots.

## 🚀 Features

### Core Modules
- **User Management**: Students, professors, staff, and admin roles
- **Course Management**: Course creation, enrollment, and management
- **Academic Records**: Grades, assignments, and exams
- **Attendance Tracking**: Student attendance monitoring
- **Financial Management**: Fee payments and financial records
- **Library System**: Book management and lending
- **Research Projects**: Research project tracking and collaboration
- **Notifications**: Multi-platform notification system
- **Reports & Analytics**: Academic reports and dashboard

### Technical Features
- **REST API**: Comprehensive API endpoints for all operations
- **Multi-platform Support**: Web, Flutter app, Telegram bot, Discord bot
- **Role-based Access Control**: Secure access based on user roles
- **Real-time Notifications**: WebSocket support for real-time updates
- **Database**: MySQL for production, SQLite for development
- **Logging**: Comprehensive error tracking and monitoring
- **Fault Tolerance**: Isolated app architecture prevents cascading failures

## 📋 Prerequisites

- Python 3.10+
- MySQL 8.0+ (for production)
- Redis (for caching and real-time features)
- Git

## 🛠 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/isina-nej/backend-uni.git
cd backend-uni
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=backend_uni_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

### 5. Database Setup
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE backend_uni_db;

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

## 🏗 Project Structure

```
backend/
├── apps/                           # Django applications
│   ├── announcements/             # University announcements
│   ├── assignments/               # Course assignments
│   ├── attendance/                # Attendance tracking
│   ├── authentication/            # User authentication
│   ├── common/                    # Common utilities
│   ├── courses/                   # Course management
│   ├── exams/                     # Exam management
│   ├── financial/                 # Financial records
│   ├── grades/                    # Grade management
│   ├── library/                   # Library system
│   ├── notifications/             # Notification system
│   ├── reports/                   # Reports and analytics
│   ├── research/                  # Research projects
│   ├── schedules/                 # Class schedules
│   └── users/                     # User management
├── config/                        # Django configuration
│   ├── settings.py               # Main settings
│   ├── settings_local.py         # Development settings
│   ├── settings_production.py    # Production settings
│   ├── urls.py                   # Main URL configuration
│   └── api_urls.py               # API URL configuration
├── docs/                          # Documentation
├── logs/                          # Log files
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
└── wsgi_pythonanywhere.py        # WSGI configuration for deployment
```

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update user profile

### Core Resources
- `/api/users/` - User management
- `/api/courses/` - Course operations
- `/api/assignments/` - Assignment management
- `/api/grades/` - Grade management
- `/api/attendance/` - Attendance tracking
- `/api/exams/` - Exam management
- `/api/library/` - Library operations
- `/api/financial/` - Financial records
- `/api/research/` - Research projects
- `/api/notifications/` - Notifications
- `/api/reports/` - Reports and analytics

### Utility Endpoints
- `GET /api/health/` - Health check
- `GET /api/info/` - API information

## 🚀 Deployment

### PythonAnywhere Deployment

1. **Upload Code**:
   ```bash
   git push origin main
   ```

2. **On PythonAnywhere**:
   ```bash
   cd ~
   git clone https://github.com/isina-nej/backend-uni.git
   python3.10 -m venv venv
   source venv/bin/activate
   cd backend-uni
   pip install -r requirements.txt
   ```

3. **Configure Database**: Create MySQL database and update `.env` file

4. **Run Migrations**:
   ```bash
   python manage.py migrate --settings=config.settings_production
   python manage.py collectstatic --noinput --settings=config.settings_production
   ```

5. **Configure WSGI**: Use content from `wsgi_pythonanywhere.py`

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📚 Documentation

- API documentation is available at `/api/` when running in development mode
- Each app contains its own models, views, and serializers documentation
- Database schema documentation in `docs/` directory

## 🔧 Development

### Adding New Apps
```bash
python manage.py startapp new_app_name apps/new_app_name
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic
```

## 🛡 Security Features

- JWT token authentication
- Role-based permissions
- CORS configuration for web clients
- SQL injection protection
- XSS protection
- CSRF protection

## 📊 Monitoring & Logging

- Comprehensive logging with different levels
- Error tracking and monitoring
- Performance monitoring capabilities
- Health check endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

---

**Built with ❤️ for the academic community**
