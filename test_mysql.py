#!/usr/bin/env python3
"""
MySQL Connection Test Script
Run this to verify MySQL connection is working properly
"""

import os
import sys
import django

# Add project path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def test_mysql_connection():
    """Test MySQL database connection"""
    print("🔍 Testing MySQL connection...")

    try:
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Basic connection test passed: {result}")

        # Test Django tables
        from django.core.management import call_command
        print("📊 Checking Django tables...")
        call_command('check')

        print("✅ MySQL connection and Django setup successful!")

    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure MySQL server is running")
        print("2. Check database credentials in settings.py")
        print("3. Verify MySQL user has proper permissions")
        print("4. Try: pip install mysqlclient")
        return False

    return True

def show_database_info():
    """Show current database configuration"""
    print("\n📋 Current Database Configuration:")
    db_settings = connection.settings_dict
    print(f"Engine: {db_settings.get('ENGINE')}")
    print(f"Name: {db_settings.get('NAME')}")
    print(f"User: {db_settings.get('USER')}")
    print(f"Host: {db_settings.get('HOST')}")
    print(f"Port: {db_settings.get('PORT')}")

if __name__ == "__main__":
    print("🚀 MySQL Connection Test")
    print("=" * 50)

    show_database_info()

    if test_mysql_connection():
        print("\n🎉 All tests passed! Your MySQL setup is working correctly.")
    else:
        print("\n⚠️  Please check your MySQL configuration.")
        sys.exit(1)
