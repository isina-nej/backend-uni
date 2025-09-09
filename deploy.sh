#!/bin/bash
# Complete deployment script for PythonAnywhere
# Run this step by step in PythonAnywhere Bash console

echo "=== Starting Django Deployment on PythonAnywhere ==="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Error: Not in Django project directory!"
    echo "Please run: cd ~/backend-uni"
    exit 1
fi

# Step 1: Pull latest changes
echo "Step 1: Pulling latest changes from git..."
git pull origin main

# Step 2: Activate virtual environment
echo "Step 2: Activating virtual environment..."
source ~/venv/bin/activate

# Step 3: Install/update requirements
echo "Step 3: Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Check environment file
if [ ! -f ".env" ]; then
    echo "Step 4: Creating .env file..."
    SECRET_KEY=$(python generate_secret_key.py)
    cat > .env << EOF
SECRET_KEY=$SECRET_KEY
DEBUG=False
DB_NAME=isinanej2\$default
DB_USER=isinanej2
DB_PASSWORD=YOUR_MYSQL_PASSWORD_HERE
DB_HOST=isinanej2.mysql.pythonanywhere-services.com
DB_PORT=3306
EOF
    echo "⚠️  IMPORTANT: Edit the .env file and replace YOUR_MYSQL_PASSWORD_HERE with your actual MySQL password!"
    echo "Run: nano .env"
    exit 1
fi

# Step 5: Test Django settings
echo "Step 5: Testing Django settings..."
python manage.py check --settings=config.settings_production

# Step 6: Run migrations
echo "Step 6: Running database migrations..."
python manage.py migrate --settings=config.settings_production

# Step 7: Collect static files
echo "Step 7: Collecting static files..."
python manage.py collectstatic --noinput --settings=config.settings_production

# Step 8: Create logs directory
echo "Step 8: Setting up logs directory..."
mkdir -p logs
touch logs/app.log
touch logs/django.log

echo "=== Deployment Complete! ==="
echo ""
echo "Next steps:"
echo "1. Go to PythonAnywhere Web tab and reload your web app"
echo "2. Your Django app should be available at: https://isinanej2.pythonanywhere.com"
echo "3. Test API endpoints: https://isinanej2.pythonanywhere.com/api/health/"
echo "4. Access admin: https://isinanej2.pythonanywhere.com/admin/"
echo ""
echo "Remember to replace 'isinanej2' with your actual PythonAnywhere username!"
