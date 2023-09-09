import os
import django
from django.conf import settings

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # Replace 'my_project.settings' with the path to your settings

# Setup Django
django.setup()


print('\nBUTTS')
print(settings)
print(','.join(settings.INSTALLED_APPS))
print('BUTTS END\n')
