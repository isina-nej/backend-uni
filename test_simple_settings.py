#!/usr/bin/env python3
"""
تست تنظیمات simple production به صورت محلی
"""

import os
import sys

def test_simple_settings():
    print("🧪 Testing simple production settings locally...")
    
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')
        
        # Import Django
        import django
        django.setup()
        
        print("✅ Django setup successful")
        
        # Test basic imports
        from django.conf import settings
        print(f"✅ DEBUG mode: {settings.DEBUG}")
        print(f"✅ Allowed hosts: {settings.ALLOWED_HOSTS}")
        print(f"✅ Installed apps count: {len(settings.INSTALLED_APPS)}")
        
        # Test database config
        print(f"✅ Database engine: {settings.DATABASES['default']['ENGINE']}")
        
        # Test REST framework
        print(f"✅ REST Framework configured: {'rest_framework' in settings.INSTALLED_APPS}")
        
        # Test URL configuration
        from django.urls import get_resolver
        resolver = get_resolver()
        print("✅ URL configuration loaded successfully")
        
        # Test models
        from apps.users.models import User
        from apps.dormitory.models import DormitoryComplex
        print("✅ Models imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_simple_settings()
    exit(0 if success else 1)
