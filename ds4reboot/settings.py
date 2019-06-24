"""
Django settings for ds4reboot project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import datetime
import os
from ds4reboot.secret_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'base.apps.BaseConfig',
    'user.apps.UserConfig',
    'bierlijst.apps.BierlijstConfig',
    'eetlijst.apps.EetlijstConfig',
    'thesau.apps.ThesauConfig',
    'ds4admin.apps.Ds4AdminConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Angular
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # Wiki
    'django.contrib.sites.apps.SitesConfig',
    'django.contrib.humanize.apps.HumanizeConfig',
    'django_nyt.apps.DjangoNytConfig',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki.apps.WikiConfig',
    'wiki.plugins.attachments.apps.AttachmentsConfig',
    'wiki.plugins.notifications.apps.NotificationsConfig',
    'wiki.plugins.images.apps.ImagesConfig',
    'wiki.plugins.macros.apps.MacrosConfig',
    # 'debug_toolbar'
]

INSTALLED_APPS += SECRET_APPS

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ds4reboot.urls'

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
                "sekizai.context_processors.sekizai",
            ],
        },
    },
]

# Production
WSGI_APPLICATION = 'ds4reboot.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
]
APPEND_SLASH = True
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'BEARER',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_ALLOW_REFRESH': False
}

# Frontend CORS
# https://github.com/ottoyiu/django-cors-headers/#configuration
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    "https://app.ds4.nl",
    "http://localhost:4200",
]

CSRF_TRUSTED_ORIGINS = [
    'ds4.nl',
]

# Debug toolbar
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

# Timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True  # Use local time

# Generated uploads
HR_REPORTS_FOLDER = 'hr_reports/'
TEMP_FOLDER = 'temp/'

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'
MEDIA_URL = '/media/'
if DEBUG:
    MEDIA_ROOT = './media/'
else:
    MEDIA_ROOT = '/var/www/media/'

if not os.path.exists(MEDIA_ROOT + TEMP_FOLDER):
    os.mkdir(MEDIA_ROOT + TEMP_FOLDER)
if not os.path.exists(MEDIA_ROOT + HR_REPORTS_FOLDER):
    os.mkdir(MEDIA_ROOT + HR_REPORTS_FOLDER)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# Wiki part
WIKI_ACCOUNT_HANDLING = True
WIKI_ACCOUNT_SIGNUP_ALLOWED = True
SITE_ID = 1
