#!/usr/bin/env python3
"""
Safe deployment script for Azure with minimal dependencies
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {str(e)}")
        return False

def main():
    print("🚀 Starting Safe Azure Deployment...")
    
    # Set Django settings to production
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civicblogs.settings')
    
    # Use minimal requirements if available
    requirements_file = 'requirements.txt'
    if os.path.exists('requirements_minimal.txt'):
        requirements_file = 'requirements_minimal.txt'
        print(f"📦 Using {requirements_file}")
    
    # Install dependencies
    if not run_command(f'pip install -r {requirements_file}', 'Installing dependencies'):
        print("⚠️ Dependency installation failed, continuing...")
    
    # Collect static files
    if not run_command('python manage.py collectstatic --noinput', 'Collecting static files'):
        print("⚠️ Static collection failed, continuing...")
    
    # Check if we can connect to database
    print("🔍 Testing database connection...")
    try:
        import django
        django.setup()
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        
        # Run migrations if database is available
        run_command('python manage.py migrate --noinput', 'Running database migrations')
        
    except Exception as e:
        print(f"⚠️ Database connection failed: {str(e)}")
        print("   Continuing without database operations...")
    
    print("🎉 Safe deployment preparation complete!")

if __name__ == '__main__':
    main()