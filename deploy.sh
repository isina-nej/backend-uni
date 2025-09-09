#!/bin/bash
# PythonAnywhere Deployment Script

echo "🚀 Starting deployment to PythonAnywhere..."

# Install/Update dependencies
echo "📦 Installing dependencies..."
pip3.10 install --user -r requirements_production.txt

# Collect static files
echo "📁 Collecting static files..."
python3.10 manage.py collectstatic --noinput --settings=config.settings_production

# Run migrations
echo "🗃️ Running database migrations..."
python3.10 manage.py migrate --settings=config.settings_production

# Create superuser (optional - uncomment if needed)
# echo "👤 Creating superuser..."
# python3.10 manage.py createsuperuser --settings=config.settings_production

echo "✅ Deployment completed!"
echo "Don't forget to:"
echo "1. Update your WSGI file in PythonAnywhere dashboard"
echo "2. Set environment variables"
echo "3. Reload your web app"
