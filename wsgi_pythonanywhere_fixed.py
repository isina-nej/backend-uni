"""
WSGI config for PythonAnywhere deployment - FIXED VERSION
This fixes the path conflicts and properly configures the environment.
"""

import os
import sys

# Set the Django settings module FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')

# Add your project directory to Python path
project_home = '/home/sinanej2/backend-uni'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Remove any duplicate or problematic paths
# This helps prevent the "multiple filesystem locations" error
paths_to_remove = []
for path in sys.path:
    if path.endswith('/./apps/users') or path.endswith('/.'):
        paths_to_remove.append(path)

for path in paths_to_remove:
    sys.path.remove(path)

# Ensure we're using the correct working directory
os.chdir(project_home)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
