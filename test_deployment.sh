#!/bin/bash
# Test script for PythonAnywhere deployment

echo "=== Testing Django Configuration ==="

# Test if we can import Django settings
echo "Testing Django settings import..."
python3 -c "
import sys
import os

# Simulate PythonAnywhere environment
sys.path.insert(0, '/home/sinanej2/backend-uni')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production_simple'

try:
    import django
    from django.conf import settings
    django.setup()
    print('✅ Django settings loaded successfully')
    print(f'Debug mode: {settings.DEBUG}')
    print(f'Allowed hosts: {settings.ALLOWED_HOSTS}')
except Exception as e:
    print(f'❌ Error loading Django settings: {e}')
"

echo -e "\n=== Testing WSGI Configuration ==="
# Test WSGI file
echo "Testing WSGI file..."
python3 -c "
import sys
import os

# Simulate the WSGI environment
project_home = '/home/sinanej2/backend-uni'
sys.path.insert(0, project_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production_simple'

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print('✅ WSGI application created successfully')
except Exception as e:
    print(f'❌ Error creating WSGI application: {e}')
"

echo -e "\n=== Testing Apps Import ==="
# Test individual app imports
echo "Testing app imports..."
python3 -c "
import sys
import os

sys.path.insert(0, '/home/sinanej2/backend-uni')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production_simple'

try:
    import django
    django.setup()
    
    # Test importing each app
    apps_to_test = [
        'apps.users.apps.UsersConfig',
        'apps.courses.apps.CoursesConfig',
        'apps.authentication.apps.AuthenticationConfig'
    ]
    
    for app in apps_to_test:
        try:
            module_path, class_name = app.rsplit('.', 1)
            module = __import__(module_path, fromlist=[class_name])
            app_config = getattr(module, class_name)
            print(f'✅ {app} imported successfully')
        except Exception as e:
            print(f'❌ Error importing {app}: {e}')
            
except Exception as e:
    print(f'❌ Error setting up Django: {e}')
"

echo -e "\n=== Test Complete ==="
