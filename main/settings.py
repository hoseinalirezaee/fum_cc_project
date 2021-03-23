from os import environ
from pathlib import Path

from dj_database_url import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get('SECRET_KEY', 'DummySecretKey')
JWT_ALGORITHM = 'HS256'
JWT_SECRET = SECRET_KEY

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'documents',
    'users'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'main.wsgi.application'

DATABASE_CONFIG = config('DATABASE_URL', engine=False)

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

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'static_files'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'EXCEPTION_HANDLER': 'main.error_handlers.api_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'common.authentication.CustomTokenAuthentication'
    ]
}


AUTH_SERVICE_BASE_API_URL = 'http://example.com'
AUTH_SERVICE_ACCESS_USERNAME = 'example'
AUTH_SERVICE_ACCESS_PASSWORD = 'password'
