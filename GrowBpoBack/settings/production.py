from .base import *

DEBUG = False

ALLOWED_HOSTS = ['growbpo.com', '13.59.176.156']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('PRODUCTION_DB_NAME'),
        'USER': os.getenv('PRODUCTION_DB_USER'),
        'PASSWORD': os.getenv('PRODUCTION_DB_PASSWORD'),
        'HOST': os.getenv('PRODUCTION_DB_HOST'),
        'PORT': os.getenv('PRODUCTION_DB_PORT'),
    }
}

# Configurações adicionais de segurança para produção
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
