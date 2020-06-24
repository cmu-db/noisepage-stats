from .base import *

DEBUG = True
ALLOWED_HOSTS = ['incrudibles-testing.db.pdl.cmu.edu']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_environ_value('PSS_DATABASE_NAME'),
        'USER': get_environ_value('PSS_DATABASE_USER'),
        'PASSWORD': get_environ_value('PSS_DATABASE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': int(get_environ_value('PSS_DATABASE_PORT', 5432)),
    }
}