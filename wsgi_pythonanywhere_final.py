# Content for WSGI file on PythonAnywhere
# Path: /var/www/sinanej2_pythonanywhere_com_wsgi.py

import os
import sys

# Add your project directory to sys.path
project_home = '/home/sinanej2/backend-uni'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = '/home/sinanej2/venv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
