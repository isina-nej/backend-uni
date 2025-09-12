#!/usr/bin/env python
"""
Script برای اصلاح موقت viewset های مشکل‌ساز برای schema generation
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# بیا schema رو ایجاد کنیم با filterset fields ساده‌تر
from apps.mobile_api.views import PushNotificationViewSet

# Remove problematic fields temporarily
def temp_fix_viewsets():
    """موقتاً فیلدهای مشکل‌ساز را حذف می‌کند"""
    print("🔧 در حال اصلاح موقت ViewSet ها...")
    
    # Check PushNotification model directly
    from apps.mobile_api.models import PushNotification
    model_fields = [f.name for f in PushNotification._meta.fields]
    print(f"PushNotification fields: {model_fields}")
    
    if 'notification_type' in model_fields:
        print("✅ notification_type در مدل PushNotification موجود است")
    else:
        print("❌ notification_type در مدل PushNotification موجود نیست")

if __name__ == "__main__":
    temp_fix_viewsets()
