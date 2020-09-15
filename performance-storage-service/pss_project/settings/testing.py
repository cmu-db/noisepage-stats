from .base import *

DEBUG = True
ALLOWED_HOSTS = [
    'incrudibles-testing.db.pdl.cmu.edu',
    'performance-service-testing.performance'
]

MIDDLEWARE.insert(0, 'django_prometheus.middleware.PrometheusBeforeMiddleware')
MIDDLEWARE.insert(len(MIDDLEWARE),
                  'django_prometheus.middleware.PrometheusAfterMiddleware')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_environ_value('PSS_DATABASE_NAME'),
        'USER': get_environ_value('PSS_DATABASE_USER'),
        'PASSWORD': get_environ_value('PSS_DATABASE_PASSWORD'),
        'HOST': 'timescaledb-service-testing.performance',
        'PORT': int(get_environ_value('PSS_DATABASE_PORT', 5432)),
    }
}