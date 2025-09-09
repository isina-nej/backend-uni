#!/bin/bash
# Script to update PythonAnywhere deployment with latest fixes
# Run this in PythonAnywhere bash console

echo "🔄 Updating PythonAnywhere deployment with API fixes..."

# Navigate to project directory
cd ~/backend-uni

# Pull latest changes
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ~/.virtualenvs/backend-uni-env/bin/activate

# Install any new requirements
echo "📦 Updating requirements..."
pip install -r requirements.txt

# Run migrations if any
echo "🗄️ Running migrations..."
python manage.py migrate --settings=config.settings_production

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=config.settings_production

# Test the application
echo "🧪 Testing Django configuration..."
python manage.py check --settings=config.settings_production

echo "✅ Update completed!"
echo ""
echo "📝 Next steps:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Click 'Reload' button"
echo "3. Test your API endpoints"
echo ""
echo "🔗 Test URLs:"
echo "- Health: https://sinanej2.pythonanywhere.com/api/health/"
echo "- Info: https://sinanej2.pythonanywhere.com/api/info/"
echo "- Admin: https://sinanej2.pythonanywhere.com/admin/"
