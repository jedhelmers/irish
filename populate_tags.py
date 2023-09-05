# populate_tags.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from my_app.models import Tags  # Import the model

def populate():
    tags = ['travel', 'food', 'technology', 'health', 'finance']

    for tag in tags:
        Tags.objects.get_or_create(tag=tag)  # This will get the object if it already exists, otherwise it will create it.

if __name__ == '__main__':
    print('Populating tags...')
    populate()
    print('Population complete.')
