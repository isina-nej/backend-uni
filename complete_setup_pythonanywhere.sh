#!/bin/bash
# Complete PythonAnywhere Setup Script (Simplified Version)
# اسکریپت کامل راه‌اندازی PythonAnywhere (نسخه ساده)

echo "🚀 PythonAnywhere Complete Setup (Simplified)..."

# Step 1: Clean up
echo "🧹 Cleaning up..."
rm -rf ~/.cache/pip/* 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# Step 2: Install minimal requirements
echo "📦 Installing minimal requirements..."
cat > requirements_simple.txt << EOF
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

pip3.10 install --user -r requirements_simple.txt --no-cache-dir

# Step 3: Create directories
echo "📁 Creating directories..."
mkdir -p /home/sinanej2/sinanej2.pythonanywhere.com/static
mkdir -p /home/sinanej2/sinanej2.pythonanywhere.com/media

# Step 4: Test simplified Django setup
echo "🧪 Testing simplified Django setup..."
python3.10 manage.py check --settings=config.settings_simplified_pythonanywhere

if [ $? -eq 0 ]; then
    echo "✅ Django check passed!"
    
    # Step 5: Collect static files
    echo "📁 Collecting static files..."
    python3.10 manage.py collectstatic --noinput --settings=config.settings_simplified_pythonanywhere
    
    # Step 6: Run migrations
    echo "🗄️ Running migrations..."
    python3.10 manage.py migrate --settings=config.settings_simplified_pythonanywhere
    
    echo "✅ Setup completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Update .env.pythonanywhere with your MySQL database info"
    echo "2. In PythonAnywhere Web App settings:"
    echo "   - WSGI file: Use pythonanywhere_wsgi_simplified.py content"
    echo "   - Static files: /static/ -> /home/sinanej2/sinanej2.pythonanywhere.com/static"
    echo "3. Reload your web app"
    echo "4. Test: https://sinanej2.pythonanywhere.com/admin/"
    
else
    echo "❌ Django check failed. Check the error messages above."
fi

# Cleanup
rm -f requirements_simple.txt

echo ""
echo "🔧 If issues persist, check:"
echo "   - Database credentials in .env.pythonanywhere"
echo "   - MySQL database is created in PythonAnywhere dashboard"
echo "   - All file paths are correct"
