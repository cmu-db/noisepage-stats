from .base import *

DEBUG = True
ALLOWED_HOSTS = ['incrudibles-staging.db.pdl.cmu.edu']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_environ_value('PSS_DATABASE_NAME'),
        'USER': get_environ_value('PSS_DATABASE_USER'),
        'PASSWORD': get_environ_value('PSS_DATABASE_PASSWORD'),
        'HOST': 'timescaledb-service-staging.performance',
        'PORT': int(get_environ_value('PSS_DATABASE_PORT', 5432)),
    }
}