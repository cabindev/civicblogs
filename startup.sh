#!/bin/bash

# CivicBlogs Azure App Service Startup Script
echo "🚀 Starting CivicBlogs on Azure App Service..."

# Install dependencies
echo "📦 Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Set environment variables for production
export DEBUG=False
export USE_POSTGRES=True
export USE_AZURE_STORAGE=True
export DJANGO_SETTINGS_MODULE=civicblogs.settings

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "🗄️ Running migrations..."
python manage.py migrate --noinput

# Start Gunicorn server
echo "🌟 Starting Gunicorn server..."
exec gunicorn civicblogs.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 60 \
    --keep-alive 2 \
    --max-requests 1000 \
    --preload \
    --log-level info \
    --access-logfile - \
    --error-logfile -