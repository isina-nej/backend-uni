#!/usr/bin/env python
"""
بررسی تمام ViewSet هایی که از filterset_fields استفاده می کنند و 'status' دارند
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

def check_viewset_status_fields():
    """بررسی ViewSet ها برای مشکلات status field"""
    
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
    all_status_viewsets = []
    
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
                
                # Check if it has 'status' in filterset_fields
                if 'status' in attr.filterset_fields:
                    all_status_viewsets.append(attr_name)
                    
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
                        
                        if 'status' not in model_fields:
                            print(f'   ❌ {attr_name}: مدل {model.__name__} فیلد status ندارد')
                            print(f'      فیلدهای مدل: {sorted(model_fields)}')
                            problematic_viewsets.append((attr_name, model.__name__))
                        else:
                            print(f'   ✅ {attr_name}: فیلد status در مدل {model.__name__} موجود است')
                    except Exception as e:
                        print(f'   ⚠️ {attr_name}: خطا در بررسی - {e}')
    
    print(f"\n📊 خلاصه:")
    print(f"🔍 ViewSet های با status در filterset_fields: {len(all_status_viewsets)}")
    for vs in all_status_viewsets:
        print(f"   - {vs}")
        
    if problematic_viewsets:
        print(f"\n❌ ViewSet های مشکل‌دار: {len(problematic_viewsets)}")
        for viewset, model in problematic_viewsets:
            print(f"   - {viewset} (مدل: {model})")
    else:
        print("\n✅ همه ViewSet ها درست هستند")
    
    return problematic_viewsets

if __name__ == "__main__":
    check_viewset_status_fields()
