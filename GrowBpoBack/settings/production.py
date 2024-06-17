from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'https://growbpo.com.br',
    'https://www.growbpo.com.br',
    'http://growbpo.com.br',
    'http://www.growbpo.com.br',
    'growbpo.com.br', 
    'www.growbpo.com.br',
    '127.0.0.1',
    'localhost',
    '3.19.140.120', 
]

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


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True