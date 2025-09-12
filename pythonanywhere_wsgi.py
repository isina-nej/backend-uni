#!/var/www/sinanej2_pythonanywhere_com_wsgi.py
# WSGI configuration for PythonAnywhere
# Replace 'sinanej2' with your actual PythonAnywhere username

import os
import sys

# Add your project directory to Python path
path = '/home/sinanej2/backend-uni/backend-uni'  # Your actual path
if path not in sys.path:
    sys.path.insert(0, path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_pythonanywhere')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
