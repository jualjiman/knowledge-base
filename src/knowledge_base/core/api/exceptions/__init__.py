# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _


class BaseAPIException(Exception):
    def __init__(self, custom_param):
        self.custom_param = custom_param

    def __str__(self):
        return unicode(self).encode('utf-8')


class MissingConfiguration(BaseAPIException):
    def __unicode__(self):
        if self.custom_param:
            return _(
                '"{}" configuration is missing.'.format(self.custom_param)
            )
        else:
            _('Needed configuration is missing.')


class ImproperlyConfigured(BaseAPIException):
    def __unicode__(self):
        if self.custom_param:
            return _(
                '"{}" variable was improperly configured.'.format(
                    self.custom_param
                )
            )
        else:
            _('A needed configuration was improperly configurated.')
