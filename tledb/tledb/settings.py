
import json
import os
import sys

"""
Django settings for the tledb project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
with open('../.secrets/django.json') as file:
    django_secrets = json.load(file)
SECRET_KEY = django_secrets['secret_key']

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', 'localhost']
DEBUG = True

""" TODO Find what is the problem with this code... static files not served
if sys.argv[1] == 'manage.py':
    print('DEBUG activated for testing')
    ALLOWED_HOSTS = []
    DEBUG = True
else:
    print('DEBUG deactivated for production')
    ALLOWED_HOSTS = ['0.0.0.0', 'localhost']
    DEBUG = False
"""

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ### additional apps
    'django_filters',
    'django_celery_beat',
    'django_celery_results',
    'rest_framework',
    # ### custom appls
    'fetcher',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tledb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'tledb', 'templates')
        ],
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

WSGI_APPLICATION = 'tledb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
with open('../.secrets/mysql.json') as file:
    db_secrets = json.load(file)

DATABASES = {
    'default': {
        'ENGINE': db_secrets['ngin'],
        'NAME': db_secrets['name'],
        'USER': db_secrets['user'],
        'PASSWORD': db_secrets['pass'],
        'HOST': db_secrets['host'],
        'PORT': db_secrets['port'],
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, '../static')
STATIC_URL = '/static/'


# ### CELERY configuration
with open('../.secrets/celery.json') as file:
    celery_secrets = json.load(file)

CELERY_BROKER_URL = celery_secrets['broker']
CELERY_RESULT_BACKEND =  celery_secrets['backend']


# ### REST Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
