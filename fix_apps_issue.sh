#!/bin/bash
# Fix script for PythonAnywhere Django apps multiple locations issue

echo "🔧 Fixing Django apps configuration issue..."

# Navigate to project directory
cd /home/sinanej2/backend-uni

# Remove any duplicate or problematic directory references
echo "📁 Cleaning up directory structure..."

# Ensure we have clean Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Check if manage.py works with production settings
echo "🧪 Testing Django configuration..."
python manage.py check --settings=config.settings_production

echo "✅ Fix completed!"
