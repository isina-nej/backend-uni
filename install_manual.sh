#!/bin/bash
# Manual installation script for PythonAnywhere
echo "🔧 Installing Django backend packages manually..."

# First, make sure we're in the right virtualenv
echo "Virtual environment status:"
echo "VIRTUAL_ENV: $VIRTUAL_ENV"
which python
which pip

echo "📦 Installing packages one by one..."

# Install Django first
echo "Installing Django..."
pip install Django==4.2.7

# Install DRF
echo "Installing Django REST Framework..."
pip install djangorestframework==3.14.0

# Install JWT - this is the problematic one
echo "Installing Django REST Framework Simple JWT..."
pip install djangorestframework-simplejwt==5.3.0

# Install other packages
echo "Installing django-environ..."
pip install django-environ==0.11.2

echo "Installing django-cors-headers..."
pip install django-cors-headers==4.3.1

echo "Installing django-filter..."
pip install django-filter==23.4

echo "Installing drf-spectacular..."
pip install drf-spectacular==0.26.5

echo "Installing PyJWT..."
pip install PyJWT==2.8.0

echo "Installing python-decouple..."
pip install python-decouple==3.8

echo "Installing Pillow..."
pip install Pillow==10.1.0

echo "Installing requests..."
pip install requests==2.31.0

echo "Installing sqlparse..."
pip install sqlparse==0.4.4

echo "✅ All packages installed!"

# Test imports
echo "🧪 Testing imports..."
python -c "
import django
print('✅ Django:', django.VERSION)

import rest_framework
print('✅ DRF version:', rest_framework.VERSION)

try:
    import rest_framework_simplejwt
    print('✅ JWT package imported successfully')
except ImportError as e:
    print('❌ JWT import failed:', e)

try:
    import environ
    print('✅ django-environ imported successfully')
except ImportError as e:
    print('❌ django-environ import failed:', e)

print('✅ Import test completed')
"

echo "🎉 Installation completed!"
