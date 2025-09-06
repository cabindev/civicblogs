import os
import subprocess
import sys


def main():
    # Install dependencies if needed
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    # Collect static files
    os.system('python manage.py collectstatic --noinput')
    
    # Run migrations
    os.system('python manage.py migrate --noinput')
    
    # Create superuser if it doesn't exist
    os.system('python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username=\'admin\').exists() or User.objects.create_superuser(\'admin\', \'admin@civicblogs.com\', \'admin123456\')"')


if __name__ == '__main__':
    main()