#!/bin/bash
# PythonAnywhere Deployment Script
# اسکریپت استقرار در PythonAnywhere

echo "🚀 Starting PythonAnywhere deployment..."

# Step 1: Install requirements
echo "📦 Installing Python packages..."
pip3.10 install --user -r requirements_pythonanywhere.txt

# Step 2: Collect static files
echo "📁 Collecting static files..."
python3.10 manage.py collectstatic --noinput --settings=config.settings_pythonanywhere

# Step 3: Run migrations
echo "🗄️ Running database migrations..."
python3.10 manage.py migrate --settings=config.settings_pythonanywhere

# Step 4: Create superuser (optional)
echo "👤 Creating superuser (you'll be prompted)..."
python3.10 manage.py createsuperuser --settings=config.settings_pythonanywhere

echo "✅ Deployment completed successfully!"
echo "📝 Don't forget to:"
echo "   1. Update your .env.pythonanywhere file with correct values"
echo "   2. Configure your web app in PythonAnywhere dashboard"
echo "   3. Set the WSGI file path to: /home/yourusername/backend-uni/pythonanywhere_wsgi.py"
echo "   4. Set static files URL to /static/ and directory to /home/yourusername/yourusername.pythonanywhere.com/static"
