"""
WSGI config for PythonAnywhere deployment.
This file will be used as a template for the actual WSGI file on PythonAnywhere.
"""

import os
import sys

# Add your project directory to the sys.path
path = '/home/sinanej2/backend-uni'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
