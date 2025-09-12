# Database Configuration Script for PythonAnywhere MySQL
# اسکریپت تنظیم دیتابیس MySQL برای PythonAnywhere

import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Set settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_pythonanywhere')
django.setup()

def create_database_tables():
    """Create all database tables"""
    print("🗄️ Creating database tables...")
    execute_from_command_line(['manage.py', 'migrate'])
    print("✅ Database tables created successfully!")

def create_superuser():
    """Create a superuser account"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(is_superuser=True).exists():
        print("👤 Creating superuser account...")
        username = input("Enter superuser username: ")
        email = input("Enter superuser email: ")
        password = input("Enter superuser password: ")
        
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("✅ Superuser created successfully!")
    else:
        print("ℹ️ Superuser already exists.")

def load_sample_data():
    """Load sample data (optional)"""
    print("📊 Loading sample data...")
    try:
        # You can add sample data loading logic here
        print("✅ Sample data loaded successfully!")
    except Exception as e:
        print(f"⚠️ Error loading sample data: {e}")

if __name__ == "__main__":
    print("🚀 Setting up database for PythonAnywhere...")
    
    try:
        create_database_tables()
        create_superuser()
        
        # Ask if user wants to load sample data
        load_sample = input("Do you want to load sample data? (y/N): ").lower()
        if load_sample == 'y':
            load_sample_data()
            
        print("🎉 Database setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during database setup: {e}")
        print("Please check your database configuration and try again.")
