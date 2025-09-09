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

# Step 4: Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=config.settings_production

# Step 5: Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --settings=config.settings_production

# Step 6: Create logs directory if it doesn't exist
echo "📝 Setting up logs directory..."
mkdir -p /home/sinanej2/backend-uni/logs

echo "✅ Deployment completed successfully!"
echo "🔄 Don't forget to reload your web app in PythonAnywhere!"
