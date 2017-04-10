# -*- coding: utf-8 -*-
"""
Django staging settings for knowledge_base project.
"""
import os
import urlparse

from . import *  # noqa


DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'kb.pythonballz.com'
]

# Application definition
INSTALLED_APPS += (
    'opbeat.contrib.django',
)

MIDDLEWARE_CLASSES += (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
)


# Database settings
urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])

DATABASES = {
    'default': {
        'ENGINE': {
            'postgres': 'django.db.backends.postgresql_psycopg2'
        }[url.scheme],
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port
    }
}

# Static files and uploads
MEDIA_ROOT = os.path.realpath(os.path.join(
    os.environ['DATA_DIR'], 'uploads'))

STATIC_ROOT = os.path.realpath(os.path.join(
    os.environ['DATA_DIR'], 'assets'))

MEDIA_URL = '/uploads/'

STATIC_URL = '/static/'

# Opbeat
OPBEAT = {
    'ORGANIZATION_ID': os.environ['OPBEAT_ORGANIZATION_ID'],
    'APP_ID': os.environ['OPBEAT_APP_ID'],
    'SECRET_TOKEN': os.environ['OPBEAT_SECRET_TOKEN'],
    'INSTRUMENT_DJANGO_MIDDLEWARE': True,
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = int(os.environ['EMAIL_HOST_PORT'])
EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS'] == 'True'
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']

# Haystack Connections
if 'HAYSTACK_CONNECTION_URL' in os.environ:

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': os.environ['HAYSTACK_CONNECTION_URL']
        },
    }

# Cache
if 'MEMCACHED_URL' in os.environ:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': os.environ['MEMCACHED_URL'],
            'KEY_PREFIX': 'kb::'
        }
    }
