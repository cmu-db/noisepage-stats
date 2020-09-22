import os
from django.core.exceptions import ImproperlyConfigured


def get_environ_value(env_variable, default_value=None):
    value = os.environ.get(env_variable, default_value)
    if (value):
        return value
    else:
        error_msg = 'Set the {} environment variable'.format(env_variable)
        if (os.environ.get("ENV", "local") != 'local'):
            raise ImproperlyConfigured(error_msg)
