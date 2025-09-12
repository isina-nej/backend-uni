#!/bin/bash
# Script to test production requirements installation
echo "🧪 Testing production requirements installation..."

# Activate virtual environment
source ~/.virtualenvs/backend-uni-env/bin/activate

# Install production requirements only
echo "📦 Installing production requirements..."
pip install -r requirements_production.txt

# Test Django setup
echo "🔧 Testing Django setup..."
python manage.py check --settings=config.settings_simple

# Test imports
echo "🐍 Testing Python imports..."
python -c "
import django
django.setup()
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.users.models import User
print('✅ All imports successful')
"

echo "✅ Production test completed!"
