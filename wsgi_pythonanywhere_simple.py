"""
WSGI config for PythonAnywhere deployment - FINAL FIXED VERSION
Based on PythonAnywhere debugging guidelines
"""

import os
import sys

# Set the working directory to the project root
project_home = '/home/sinanej2/backend-uni'
os.chdir(project_home)

# Clean sys.path completely to avoid multiple filesystem locations error
# Remove all paths that might cause conflicts
new_sys_path = []
for path in sys.path:
    # Keep only essential Python paths, exclude project-related duplicates
    if not any(x in path for x in ['backend-uni', './apps', '/.']):
        new_sys_path.append(path)

# Set clean sys.path
sys.path = new_sys_path

# Add project directory as the FIRST path
sys.path.insert(0, project_home)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production_simple')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
