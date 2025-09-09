"""
WSGI config for PythonAnywhere deployment - SIMPLE VERSION
This uses simple environment variables without django-environ
"""

import os
import sys

# Set the Django settings module to use simple production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production_simple')

# Clean sys.path to prevent conflicts
project_home = '/home/sinanej2/backend-uni'

# Remove all existing project-related paths to prevent conflicts
paths_to_remove = []
for path in list(sys.path):
    if 'backend-uni' in path:
        paths_to_remove.append(path)

for path in paths_to_remove:
    if path in sys.path:
        sys.path.remove(path)

# Add clean project path
sys.path.insert(0, project_home)

# Ensure we're using the correct working directory
os.chdir(project_home)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
