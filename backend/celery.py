from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# from decouple import config

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# x = config('RABBITMQ_DEFAULT_USER', default=False, cast=bool)
# y = config('RABBITMQ_DEFAULT_PASS', default=False, cast=bool)

RABBITMQ_DEFAULT_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS')

# print('RABBITMQ_DEFAULT_USER\n', RABBITMQ_DEFAULT_USER)
# print('RABBITMQ_DEFAULT_PASS\n', RABBITMQ_DEFAULT_PASS)
# app = Celery('my_app')
# app = Celery('tasks', broker='pyamqp://myuser:mypassword@rabbitmq:5672//')
app = Celery('backend', broker=f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@rabbitmq:5672//')
# app = Celery('your_project')

# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

# print(settings.INSTALLED_APPS)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# if 'CELERY_RESULT_BACKEND' in settings:
app.conf.update(result_backend=settings.CELERY_RESULT_BACKEND)
