#!/usr/bin/env python3
"""
Test Python packages in PythonAnywhere environment
"""
import os
import sys

print("🔧 Testing Python packages in production environment...")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.executable}")

# Core packages to test
packages_to_test = [
    'django',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_environ',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'jwt',
    'decouple',
    'PIL',
]

print("\n📦 Testing package imports...")
failed_imports = []

for package in packages_to_test:
    try:
        __import__(package)
        print(f"✅ {package} - OK")
    except ImportError as e:
        print(f"❌ {package} - FAILED: {e}")
        failed_imports.append(package)

if failed_imports:
    print(f"\n❌ Failed imports: {failed_imports}")
    print("Please install missing packages with: pip install <package_name>")
    
    # Specific installation commands
    print("\n💡 Installation commands:")
    if 'rest_framework_simplejwt' in failed_imports:
        print("pip install djangorestframework-simplejwt==5.3.0")
    if 'django_environ' in failed_imports:
        print("pip install django-environ==0.11.2")
    if 'corsheaders' in failed_imports:
        print("pip install django-cors-headers==4.3.1")
    if 'django_filters' in failed_imports:
        print("pip install django-filter==23.4")
    if 'drf_spectacular' in failed_imports:
        print("pip install drf-spectacular==0.26.5")
else:
    print("\n✅ All packages imported successfully!")
    
    # Test Django setup
    print("\n🧪 Testing Django setup...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_simple')
        import django
        django.setup()
        print("✅ Django setup successful!")
        
        # Test database connection
        from django.db import connection
        cursor = connection.cursor()
        print("✅ Database connection successful!")
        
    except Exception as e:
        print(f"❌ Django setup failed: {e}")

print("\n🎉 Test completed!")
