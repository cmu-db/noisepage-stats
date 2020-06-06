from .base import *

DEBUG = True
ALLOWED_HOSTS = ['0.0.0.0', 'kubernetes.docker.internal', 'localhost']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
