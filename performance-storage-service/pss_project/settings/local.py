from .base import *

DEBUG = True
ALLOWED_HOSTS = ['0.0.0.0', 'kubernetes.docker.internal', 'localhost', '127.0.0.1', 'host.docker.internal','smee.io']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

MIDDLEWARE.insert(0, 'django_prometheus.middleware.PrometheusBeforeMiddleware')
MIDDLEWARE.insert(len(MIDDLEWARE), 'django_prometheus.middleware.PrometheusAfterMiddleware')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',  # 'timescaledb-service-local.performance',
        'PORT': '5432',
    }
}
