# PythonAnywhere Deployment Guide

Complete guide for deploying Django application on PythonAnywhere.

## Prerequisites
- GitHub repository with your Django project
- PythonAnywhere account
- MySQL database (provided by PythonAnywhere)

## Step 1: Prepare Code
1. Commit and push all changes:
```bash
git add .
git commit -m "Prepare for PythonAnywhere deployment"
git push origin main
```

## Step 2: PythonAnywhere Setup

### 2.1 Create MySQL Database
1. Go to "Databases" tab
2. Create a new MySQL database
3. Note your database name: `username$default`
4. Set a strong password

### 2.2 Clone Project
1. Open "Consoles" tab
2. Start a new Bash console
3. Run these commands:
```bash
cd ~
git clone https://github.com/isina-nej/backend-uni.git
python3.10 -m venv venv
source venv/bin/activate
cd backend-uni
pip install -r requirements.txt
```

### 2.3 Environment Configuration
Create `.env` file:
```bash
# Generate secret key
python generate_secret_key.py

# Create .env file
cat > .env << EOF
SECRET_KEY=your-generated-secret-key
DEBUG=False
DB_NAME=username\$default
DB_USER=username
DB_PASSWORD=your-mysql-password
DB_HOST=username.mysql.pythonanywhere-services.com
DB_PORT=3306
EOF
```

### 2.4 Database Migration
```bash
python manage.py migrate --settings=config.settings_production
python manage.py createsuperuser --settings=config.settings_production
python manage.py collectstatic --noinput --settings=config.settings_production
```

## Step 3: Web App Configuration

### 3.1 Create Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose Django
4. Select Python 3.10
5. Set project path: `/home/username/backend-uni`

### 3.2 Configure WSGI
1. Click on WSGI file link in Web tab
2. Replace content with the code from `wsgi_pythonanywhere.py`
3. Update the paths with your username

### 3.3 Static Files
In Web tab, configure:
- **Static files URL**: `/static/`
- **Static files directory**: `/home/username/static/`

### 3.4 Reload Web App
Click "Reload" button in Web tab

## Step 4: Testing
- Visit your website: `https://username.pythonanywhere.com`
- Test API endpoints: `https://username.pythonanywhere.com/api/health/`
- Access admin: `https://username.pythonanywhere.com/admin/`

## Troubleshooting

### Common Issues
1. **Import Errors**: Check WSGI file paths
2. **Database Connection**: Verify .env file settings
3. **Static Files**: Run `collectstatic` command
4. **Permissions**: Check file permissions

### Logs
- Check error logs in Web tab
- Use `print()` statements in WSGI for debugging
- Monitor console output

## Updates
To update your deployment:
```bash
cd ~/backend-uni
git pull origin main
source ~/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=config.settings_production
python manage.py collectstatic --noinput --settings=config.settings_production
```
Then reload the web app.

---
**Note**: Replace `username` with your actual PythonAnywhere username throughout this guide.


cd ~/backend-uni && chmod +x update_deployment.sh && ./update_deployment.sh