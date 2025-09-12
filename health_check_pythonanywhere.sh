#!/bin/bash
# Health check script for PythonAnywhere deployment
# اسکریپت بررسی سلامت استقرار

echo "🏥 PythonAnywhere Health Check..."

# Check Python version
echo "🐍 Python Version:"
python3.10 --version

# Check Django installation
echo "🔧 Django Installation:"
python3.10 -c "import django; print(f'Django {django.get_version()}')"

# Check database connection
echo "🗄️ Database Connection:"
python3.10 manage.py check --database default --settings=config.settings_pythonanywhere

# Check for missing migrations
echo "📋 Migration Status:"
python3.10 manage.py showmigrations --settings=config.settings_pythonanywhere

# Check static files
echo "📁 Static Files:"
if [ -d "/home/$(whoami)/$(whoami).pythonanywhere.com/static" ]; then
    echo "✅ Static files directory exists"
    ls -la /home/$(whoami)/$(whoami).pythonanywhere.com/static | wc -l
    echo "files found in static directory"
else
    echo "❌ Static files directory not found"
fi

# Check media files
echo "🖼️ Media Files:"
if [ -d "/home/$(whoami)/$(whoami).pythonanywhere.com/media" ]; then
    echo "✅ Media files directory exists"
else
    echo "❌ Media files directory not found"
fi

# Test basic Django functionality
echo "🧪 Django System Check:"
python3.10 manage.py check --settings=config.settings_pythonanywhere

# Check for common issues
echo "🔍 Common Issues Check:"

# Check SECRET_KEY
if python3.10 -c "from config.settings_pythonanywhere import SECRET_KEY; print('SECRET_KEY is set')" 2>/dev/null; then
    echo "✅ SECRET_KEY is configured"
else
    echo "❌ SECRET_KEY not properly configured"
fi

# Check DEBUG setting
if python3.10 -c "from config.settings_pythonanywhere import DEBUG; print(f'DEBUG = {DEBUG}')" 2>/dev/null; then
    echo "✅ DEBUG setting is accessible"
else
    echo "❌ DEBUG setting issue"
fi

echo "🏁 Health check completed!"
echo "📊 Check the results above for any issues."
