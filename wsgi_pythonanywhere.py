import os
import sys
from django.core.wsgi import get_wsgi_application

# Add your project directory to the sys.path
path = '/home/yourusername/backend'  # Change this to your actual path
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable for production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')

application = get_wsgi_application()
