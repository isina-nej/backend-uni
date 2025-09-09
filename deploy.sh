#!/bin/bash

# Deployment script for PythonAnywhere
echo "🚀 Starting deployment to PythonAnywhere..."

# Step 1: Pull latest changes from git
echo "📥 Pulling latest changes from git..."
git pull origin main

# Step 2: Activate virtual environment
echo "🔄 Activating virtual environment..."
source ~/.virtualenvs/backend-uni-env/bin/activate

# Step 3: Install/update requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Step 4: Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p /home/sinanej2/backend-uni/logs
mkdir -p /home/sinanej2/backend-uni/static
mkdir -p /home/sinanej2/backend-uni/media

# Step 5: Test database connection
echo "🔍 Testing database connection..."
chmod +x test_neon_connection.sh
./test_neon_connection.sh

# Step 6: Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=config.settings_production

# Step 7: Run migrations (only if database connection works)
echo "🗄️ Running database migrations..."
echo "⚠️  Attempting migrations (may fail if database is sleeping)..."
python manage.py migrate --settings=config.settings_production || echo "❌ Migration failed - check database connection"

echo "✅ Deployment completed!"
echo "🔄 Don't forget to reload your web app in PythonAnywhere!"
echo "💡 If migrations failed, wake up your Neon database and run:"
echo "   python manage.py migrate --settings=config.settings_production"
