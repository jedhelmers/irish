from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# app = Celery('my_app')
# app = Celery('tasks', broker='pyamqp://myuser:mypassword@rabbitmq:5672//')
app = Celery('my_app', broker='pyamqp://myuser:mypassword@rabbitmq:5672//')

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# app = Celery('your_project')

# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

# print(settings.INSTALLED_APPS)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# if 'CELERY_RESULT_BACKEND' in settings:
app.conf.update(result_backend=settings.CELERY_RESULT_BACKEND)