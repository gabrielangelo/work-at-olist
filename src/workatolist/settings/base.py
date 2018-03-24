"""
Django settings for {{ project_name }} project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template
For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os.path import join, dirname, exists
import environ

# from django.conf import settings
# settings.configure()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = dirname(dirname(dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

env = environ.Env()
env_file = join(dirname(dirname(dirname(__file__))), '.env')
if exists(env_file):
    environ.Env.read_env(str(env_file))

# SECURITY WARNING: don't run with d ebug turned on in production!
DEBUG = True#env('DEBUG')
SECRET_KEY = "LRYw5C8{8?{pHvk9g_;|/!uhpSeMdW3QBlQAt!$CXu&IwcgC4~*!/S:f*5`=dq=8A<PiR*Ao6g@>T3f<<j}q'(74I=4iv~KNTZo5"
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters'
]

THIRD_APPS = [
    'rest_framework',
    'rest_framework_swagger',
]

INTERNAL_APPS = [
    'channels',
    'categories',
    'core'
]

INSTALLED_APPS += INTERNAL_APPS + THIRD_APPS
# INSTALLED_APPS += THIRD_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'workatolist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'workatolist.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Allow all host headers
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = "/media/"