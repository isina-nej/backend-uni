#!/bin/bash
# اسکریپت حل مشکل Disk Quota و تنظیم مجدد
# PythonAnywhere Recovery Script

echo "🔧 PythonAnywhere Recovery Script - Fixing Issues..."

# Step 1: Clean up unnecessary files to free space
echo "🧹 Cleaning up to free disk space..."

# Remove old Django installation if possible
pip uninstall Django -y 2>/dev/null || echo "Django not found in pip list"

# Remove cache files
rm -rf ~/.cache/pip/* 2>/dev/null || echo "Pip cache already clean"
rm -rf __pycache__ 2>/dev/null || echo "No __pycache__ found"
find . -name "*.pyc" -delete 2>/dev/null || echo "No .pyc files found"

# Step 2: Install only essential packages
echo "📦 Installing minimal required packages..."

# Create a minimal requirements file
cat > requirements_minimal.txt << EOF
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
mysqlclient==2.2.0
python-decouple==3.8
drf-spectacular==0.26.5
djangorestframework-simplejwt==5.3.0
gunicorn==21.2.0
Pillow==10.1.0
pytz==2023.3
EOF

# Install minimal packages
pip3.10 install --user -r requirements_minimal.txt --no-cache-dir

# Step 3: Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p /home/sinanej2/sinanej2.pythonanywhere.com/static
mkdir -p /home/sinanej2/sinanej2.pythonanywhere.com/media

# Step 4: Test Django setup with simplified settings
echo "🧪 Testing Django configuration..."
python3.10 manage.py check --settings=config.settings_simplified_pythonanywhere

# Step 5: Try collectstatic with simplified settings
echo "📁 Collecting static files..."
python3.10 manage.py collectstatic --noinput --settings=config.settings_simplified_pythonanywhere

# Step 6: Try migrations with simplified settings
echo "🗄️ Running database migrations..."
python3.10 manage.py migrate --settings=config.settings_simplified_pythonanywhere

echo "✅ Recovery script completed!"
echo ""
echo "📋 Next steps:"
echo "1. Check if MySQL database is created in PythonAnywhere dashboard"
echo "2. Update .env.pythonanywhere with correct database credentials"
echo "3. Configure Web App with correct WSGI file path"
echo "4. Test the application"

# Clean up temporary file
rm -f requirements_minimal.txt
