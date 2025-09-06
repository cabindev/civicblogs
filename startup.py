#!/usr/bin/env python3
import os
import subprocess
import sys
import django
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civicblogs.settings')

def main():
    print("🚀 Starting CivicBlogs deployment setup...")
    
    try:
        # Install dependencies if needed
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        # Setup Django
        django.setup()
        
        # Collect static files
        print("🎨 Collecting static files...")
        result = subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                               capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  Static files collection warning: {result.stderr}")
        
        # Run migrations
        print("🗄️  Running database migrations...")
        result = subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], 
                               capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  Migration warning: {result.stderr}")
            
        # Create superuser if environment variables are set
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@civicblogs.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123456')
        
        if admin_username and admin_email and admin_password:
            print("👤 Creating superuser...")
            try:
                from django.contrib.auth.models import User
                if not User.objects.filter(username=admin_username).exists():
                    User.objects.create_superuser(admin_username, admin_email, admin_password)
                    print(f"✅ Superuser '{admin_username}' created successfully!")
                else:
                    print(f"✅ Superuser '{admin_username}' already exists.")
            except Exception as e:
                print(f"⚠️  Superuser creation skipped: {e}")
        
        print("🎉 CivicBlogs deployment setup completed!")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()