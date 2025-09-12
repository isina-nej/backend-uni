"""
WSGI config for PythonAnywhere deployment.
This file should be used as the content for the WSGI file on PythonAnywhere.
"""
import os
import sys

# Add project directory to Python path
project_home = '/home/sinanej2/backend-uni'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set Django settings module to the simplified version
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
