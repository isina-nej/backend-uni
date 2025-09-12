#!/bin/bash
# Force install production requirements on PythonAnywhere
echo "🔧 Force installing production requirements..."

# Activate virtual environment
source ~/.virtualenvs/backend-uni-env/bin/activate

# Force reinstall key packages
echo "📦 Force installing key packages..."
pip install --force-reinstall Django==4.2.7
pip install --force-reinstall djangorestframework==3.14.0
pip install --force-reinstall djangorestframework-simplejwt==5.3.0
pip install --force-reinstall django-environ==0.11.2
pip install --force-reinstall django-cors-headers==4.3.1
pip install --force-reinstall django-filter==23.4
pip install --force-reinstall drf-spectacular==0.26.5
pip install --force-reinstall PyJWT==2.8.0
pip install --force-reinstall python-decouple==3.8
pip install --force-reinstall Pillow==10.1.0

echo "✅ Key packages installed!"

# Test Django
echo "🧪 Testing Django..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')
import django
django.setup()
print('✅ Django setup successful')
"

echo "🎉 Production setup completed!"
