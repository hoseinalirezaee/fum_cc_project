from os import environ
from pathlib import Path

from dj_database_url import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get('SECRET_KEY', 'DummySecretKey')
JWT_ALGORITHM = environ.get('JWT_ALGORITHM', 'HS256')
JWT_SECRET = environ.get('JWT_SECRET', SECRET_KEY)

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

DATABASE_CONFIG = config('DATABASE_URL', engine=False, default='postgres://postgres:1@127.0.0.1:5432/doctors')

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
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser'
    ],
    'EXCEPTION_HANDLER': 'main.error_handlers.api_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'common.authentication.CustomTokenAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'UNAUTHENTICATED_USER': 'common.authentication.UnAuthenticatedUser'
}


AUTH_SERVICE_BASE_API_URL = environ.get('AUTH_SERVICE_BASE_API_URL', 'http://example.com')
AUTH_SERVICE_ACCESS_USERNAME = environ.get('AUTH_SERVICE_ACCESS_USERNAME', 'username')
AUTH_SERVICE_ACCESS_PASSWORD = environ.get('AUTH_SERVICE_ACCESS_PASSWORD', 'password')
