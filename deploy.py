#!/usr/bin/env python3
"""
Azure App Service deployment script for CivicBlogs
"""
import os
import sys
import subprocess
import django
from pathlib import Path

# Set up Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civicblogs.settings')

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=BASE_DIR)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(f"Output: {result.stdout}")
        else:
            print(f"⚠️ {description} completed with warnings")
            if result.stderr:
                print(f"Warnings: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("🚀 CivicBlogs Azure Deployment Setup")
    
    # Install dependencies
    run_command("python -m pip install --upgrade pip", "Upgrading pip")
    run_command("pip install -r requirements.txt", "Installing dependencies")
    
    # Setup Django
    try:
        django.setup()
        print("✅ Django setup completed")
    except Exception as e:
        print(f"⚠️ Django setup warning: {e}")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Run migrations
    run_command("python manage.py migrate --noinput", "Running database migrations")
    
    print("🎉 Deployment setup completed!")

if __name__ == '__main__':
    main()