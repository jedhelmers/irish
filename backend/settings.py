"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# settings.py
from .celery import app as celery_app
from pathlib import Path
import os
from decouple import config


# Make sure it gets loaded when Django starts
__all__ = ('celery_app',)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DISABLE_COLLECTSTATIC = 1
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1tr_r#8q+9!te@7m*b3&8h0#yca6aa!1h*u83lp9soee5iha*_'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# DEBUG = False
DEBUG = config('DEBUG', default=False, cast=bool)
print('DEBUG', DEBUG)

# ALLOWED_HOSTS = ['backend', 'my_app', 'my_app_1', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = ['*']


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # If your frontend is served on localhost:3000
    # "http://127.0.0.1:9000",   # Or any other domain
    # "https://yourfrontend.com",
]

# CORS_ALLOWED_ORIGINS=['*']

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'my_app',
    'revproxy',
    'backend',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend',
    'django_prometheus',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'backend.user_creation.UserCreationMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'backend.urls'


BASE_DIR = Path(__file__).resolve().parent.parent
# print('BASE_DIR', BASE_DIR)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / "frontend/build"]
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'frontend', 'build', 'static')]
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/build/static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend/build')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# CELERY_BROKER_URL = 'amqp://myuser:mypassword@rabbitmq:5672/myvhost'
CELERY_BROKER_URL = 'amqp://myuser:mypassword@rabbitmq:5672/myvhost'
# CELERY_BROKER_URL = 'pyamqp://myuser:mypassword@rabbitmq:5672/'
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_BROKER_URL = 'redis://redis:6379/0'

# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'cache+memory://'
# CELERY_RESULT_BACKEND = None

CELERY_IGNORE_RESULT = True
# CELERY_ALWAYS_EAGER = True
CELERY_TRACK_STARTED = True
# CELERY_STORE_EAGER_RESULT = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


# PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'backend', 'mydatabase.sqlite3'),
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
    }
}

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': 'debug.log',
        # },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['file'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
    },
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# PROMETHEUS_METRICS_EXPORT_PORT = 8001
# PROMETHEUS_METRICS_EXPORT_ADDRESS = ''  # all addresses
