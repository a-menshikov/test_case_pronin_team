import os
from pathlib import Path

from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError

from api.v1.exceptions import FileFormatError

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('ENVIRONMENT') == 'dev'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'deals',
    'api',
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

ROOT_URLCONF = 'core.urls'

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
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT')
    }
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/web-static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'web-static')

MEDIA_URL = '/web-media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'web-media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PARSE_ERROR_MESSAGES = {
    KeyError: 'В запросе не передан ключ deals',
    AttributeError: 'В запросе не передан файл',
    UnicodeDecodeError: 'Кодировка файла не UTF-8',
    MultiValueDictKeyError: 'В запросе не передан ключ deals',
    ValueError: (
        'Некорректные данные в файле. Проверьте, что содержание '
        'столбцов соответствует заявленному формату данных.'
    ),
    IntegrityError: (
        'Некорректные данные в файле. Проверьте, что содержание '
        'столбцов соответствует заявленному формату данных.'
    ),
    FileFormatError: (
        'Формат загруженного файла не соответствует требованиям. '
        'Проверьте названия столбцов.'
    ),
}

HEADERS_LIST = ["customer", "item", "total", "quantity", "date"]

TOP_CUSTOMER_LIMIT = 5
COMMON_GEMS = 2

CACHE_TIME = 60 * 60

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
