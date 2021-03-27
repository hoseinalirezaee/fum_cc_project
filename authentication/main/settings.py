from datetime import timedelta
from os import environ
from pathlib import Path

from dj_database_url import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get('SECRET_KEY', 'DummySecretKey')
JWT_ALGORITHM = environ.get('JWT_ALGORITHM', 'HS256')
JWT_SECRET = environ.get('JWT_SECRET', SECRET_KEY)
JWT_LIFETIME = timedelta(days=1)

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'main.wsgi.application'

DATABASE_CONFIG = config('DATABASE_URL', engine=False, default='postgres://postgres:1@127.0.0.1:5432/authentication')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_CONFIG['NAME'],
        'USER': DATABASE_CONFIG['USER'],
        'PASSWORD': DATABASE_CONFIG['PASSWORD'],
        'PORT': DATABASE_CONFIG['PORT'],
        'HOST': DATABASE_CONFIG['HOST']
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_TZ = True

USE_I18N = True

USE_L10N = True

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'EXCEPTION_HANDLER': 'main.error_handlers.api_exception_handler',
    'UNAUTHENTICATED_USER': 'common.authentication.UnAuthenticatedUser'
}

BASIC_AUTH_USERNAME = environ.get('BASIC_AUTH_USERNAME', 'username')
BASIC_AUTH_PASSWORD = environ.get('BASIC_AUTH_PASSWORD', 'passwrod')
