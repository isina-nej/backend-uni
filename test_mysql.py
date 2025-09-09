#!/usr/bin/env python3
"""
MySQL Connection Test Script
Run this to verify MySQL connection is working properly
"""

import os
import sys
import django
import platform

# Add project path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
try:
    django.setup()
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    print("🔧 Make sure you're in the correct directory and virtual environment is activated")
    sys.exit(1)

from django.db import connection

def check_mysql_service():
    """Check if MySQL service is running"""
    print("🔍 Checking MySQL service status...")

    system = platform.system().lower()

    if system == "windows":
        try:
            import subprocess
            result = subprocess.run(['net', 'start'], capture_output=True, text=True)
            if 'mysql' in result.stdout.lower():
                print("✅ MySQL service is running")
                return True
            else:
                print("⚠️  MySQL service might not be running")
                print("🔧 Try: net start mysql80")
                return False
        except:
            print("⚠️  Could not check MySQL service status")
            return None

    elif system == "linux":
        try:
            import subprocess
            result = subprocess.run(['systemctl', 'is-active', 'mysql'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MySQL service is running")
                return True
            else:
                print("⚠️  MySQL service is not running")
                print("🔧 Try: sudo systemctl start mysql")
                return False
        except:
            print("⚠️  Could not check MySQL service status")
            return None

    else:
        print(f"⚠️  Unsupported OS: {system}")
        return None

def test_mysql_connection():
    """Test MySQL database connection"""
    print("🔍 Testing MySQL connection...")

    try:
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL connection successful! Version: {version[0]}")

        # Test database selection
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"✅ Connected to database: {db_name[0]}")

        print("✅ MySQL connection and Django setup successful!")

    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")

        if "2002" in str(e) or "10061" in str(e):
            print("1. ❌ MySQL Server is not running")
            print("   🔧 Windows: net start mysql80")
            print("   🔧 Linux: sudo systemctl start mysql")
            print("   🔧 Check: https://localhost:3306 in browser")

        elif "2003" in str(e):
            print("1. ❌ Cannot connect to MySQL server")
            print("   🔧 Check if MySQL is installed and running")
            print("   🔧 Verify port 3306 is not blocked by firewall")

        elif "1045" in str(e):
            print("1. ❌ Access denied for user")
            print("   🔧 Check username and password in settings.py")
            print("   🔧 Try resetting MySQL root password")

        elif "1049" in str(e):
            print("1. ❌ Database does not exist")
            print("   🔧 Create database: CREATE DATABASE backend_uni_db;")
            print("   🔧 Or check database name in settings.py")

        else:
            print("1. ❌ Unknown MySQL error")
            print("   🔧 Check MySQL error logs")
            print("   🔧 Verify MySQL installation")

        print("\n📖 For detailed setup guide:")
        print("   - Windows: See MYSQL_WINDOWS_SETUP.md")
        print("   - General: See MYSQL_SETUP.md")

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

    # Mask password for security
    password = db_settings.get('PASSWORD', '')
    if password:
        print(f"Password: {'*' * len(password)}")
    else:
        print("Password: (empty)")

def show_system_info():
    """Show system information"""
    print("\n🖥️  System Information:")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Django: {django.get_version()}")

def main():
    print("🚀 MySQL Connection Test")
    print("=" * 50)

    show_system_info()
    show_database_info()

    # Check MySQL service
    service_status = check_mysql_service()
    if service_status is False:
        print("\n⚠️  MySQL service check failed. Continuing with connection test...")

    print()

    if test_mysql_connection():
        print("\n🎉 All tests passed! Your MySQL setup is working correctly.")
        print("🚀 You can now run: python manage.py migrate")
        return True
    else:
        print("\n⚠️  Please check your MySQL configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
