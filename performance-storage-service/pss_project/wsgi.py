"""
WSGI config for pss_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

env = os.environ.get("ENV", "local")
os.environ['DJANGO_SETTINGS_MODULE'] = 'pss_project.settings.{}'.format(env)

application = get_wsgi_application()