from .base import *

ALLOWED_HOSTS = '*'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']

MIDDLEWARE += [
    'corsheaders.middleware.CorsMiddleware',
]
