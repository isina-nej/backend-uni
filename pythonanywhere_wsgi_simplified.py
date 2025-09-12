#!/var/www/sinanej2_pythonanywhere_com_wsgi.py
# WSGI configuration for PythonAnywhere (Simplified)

import os
import sys

# Add your project directory to Python path
path = '/home/sinanej2/backend-uni'
if path not in sys.path:
    sys.path.insert(0, path)

# Set Django settings module to simplified version
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simplified_pythonanywhere')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
