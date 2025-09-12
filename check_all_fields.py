#!/usr/bin/env python
"""
بررسی تمام ViewSet هایی که از filterset_fields استفاده می کنند و فیلدهای غیرموجود در مدل دارند
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

def check_all_viewset_fields():
    """بررسی ViewSet ها برای مشکلات فیلدها"""
    
    # Import all views modules
    try:
        from apps.users import views as users_views
        from apps.dormitory import views as dormitory_views
        from apps.mobile_api import views as mobile_views
        from apps.data_management import views as data_views
        from apps.analytics import views as analytics_views
        from apps.ai_ml import views as ai_views
    except ImportError as e:
        print(f"❌ خطا در import: {e}")
        return
    
    modules = [users_views, dormitory_views, mobile_views, data_views, analytics_views, ai_views]
    
    problematic_viewsets = []
    
    for module in modules:
        module_name = module.__name__
        print(f"\n🔍 بررسی {module_name}:")
        
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            
            # Check if it's a ViewSet class
            if (isinstance(attr, type) and 
                (issubclass(attr, viewsets.ModelViewSet) or issubclass(attr, viewsets.ReadOnlyModelViewSet)) and 
                attr not in [viewsets.ModelViewSet, viewsets.ReadOnlyModelViewSet] and
                hasattr(attr, 'filterset_fields') and 
                attr.filterset_fields):
                
                print(f"   📋 {attr_name}: filterset_fields = {attr.filterset_fields}")
                
                try:
                    if hasattr(attr, 'queryset') and attr.queryset is not None:
                        model = attr.queryset.model
                    elif hasattr(attr, 'get_queryset'):
                        # Try to get model from get_queryset method
                        continue  # Skip dynamic querysets for now
                    else:
                        print(f"   ⚠️ {attr_name}: هیچ queryset تعریف نشده")
                        continue
                        
                    model_fields = [f.name for f in model._meta.fields]
                    
                    # Check each field in filterset_fields
                    missing_fields = []
                    for field in attr.filterset_fields:
                        # Handle related fields like 'room__floor__building__complex'
                        base_field = field.split('__')[0]
                        if base_field not in model_fields:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        print(f'   ❌ {attr_name}: مدل {model.__name__} این فیلدها را ندارد: {missing_fields}')
                        print(f'      فیلدهای مدل: {sorted(model_fields)}')
                        problematic_viewsets.append((attr_name, model.__name__, missing_fields))
                    else:
                        print(f'   ✅ {attr_name}: همه فیلدها در مدل {model.__name__} موجود هستند')
                except Exception as e:
                    print(f'   ⚠️ {attr_name}: خطا در بررسی - {e}')
    
    print(f"\n📊 خلاصه:")
    if problematic_viewsets:
        print(f"❌ ViewSet های مشکل‌دار: {len(problematic_viewsets)}")
        for viewset, model, missing_fields in problematic_viewsets:
            print(f"   - {viewset} (مدل: {model}) - فیلدهای مفقود: {missing_fields}")
    else:
        print("✅ همه ViewSet ها درست هستند")
    
    return problematic_viewsets

if __name__ == "__main__":
    check_all_viewset_fields()
