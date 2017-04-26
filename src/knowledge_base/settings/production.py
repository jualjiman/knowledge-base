# -*- coding: utf-8 -*-
"""
Django production settings for knowledge-base project.
"""
from .staging import *  # noqa


ALLOWED_HOSTS = [
    'pensadero.vincoorbis.com',
]

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PRODUCTION = True
