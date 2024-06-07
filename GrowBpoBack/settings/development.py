from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DEVELOPMENT_DB_NAME'),
        'USER': os.getenv('DEVELOPMENT_DB_USER'),
        'PASSWORD': os.getenv('DEVELOPMENT_DB_PASSWORD'),
        'HOST': os.getenv('DEVELOPMENT_DB_HOST'),
        'PORT': os.getenv('DEVELOPMENT_DB_PORT'),
    }
}

