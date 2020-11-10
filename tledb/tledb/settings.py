
import json
import os
import sys

"""
Django settings for the tledb project.
"""

if '__DJ_DEVPROD' in os.environ and os.environ['__DJ_DEVPROD'] == 'dev':
    print('DEBUG activated for testing')
    ALLOWED_HOSTS = []
    DBCONFIG = '../conf/dev/db-dev.json'
    DEBUG = True
    LOG_LEVEL = 'INFO'
else:
    print('DEBUG deactivated for production')
    ALLOWED_HOSTS = ['0.0.0.0', 'localhost']
    DBCONFIG = '../.secrets/mysql.json'
    DEBUG = False
    LOG_LEVEL = 'DEBUG'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ID = 1


# SECURITY WARNING: keep the secret key used in production secret!
with open('../.secrets/django.json') as file:
    django_secrets = json.load(file)
SECRET_KEY = django_secrets['secret_key']


INSTALLED_APPS = [
    # Pre-shipped apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    # ### additional apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrap3',
    'bootstrapform',
    'django_celery_beat',
    'django_celery_results',
    'django_filters',
    'django_tables2',
    'rest_framework',
    'widget_tweaks',
    # ### custom apps
    'fetcher',
    'users',
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


# ### Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django':{
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': True,
        },
       'gunicorn.errors': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': True,
        }
    },
}


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
with open(DBCONFIG) as file:
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


# Authenticaion backends, added because of django-allauth
# https://django-allauth.readthedocs.io/en/latest/installation.html
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


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


# ### django-allauth
LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
ACCOUNT_USERNAME_REQUIRED = False


# ### email backend
with open('../.secrets/mail.json') as file:
    email_secrets = json.load(file)

EMAIL_BACKEND = email_secrets['back']
EMAIL_HOST = email_secrets['host']
EMAIL_PORT = email_secrets['port']
EMAIL_HOST_USER = email_secrets['user']
EMAIL_HOST_PASSWORD = email_secrets['pass']
EMAIL_USE_TLS = True


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
