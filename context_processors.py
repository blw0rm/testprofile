# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class SettingsProcessor(object):
    
    def __init__(self, *settings_list):
        self.settings_list = settings_list
        
    def __call__(self, request):
        cotext_extras = {}
        for sn in self.settings_list:
            try:
                cotext_extras[sn] = getattr(settings, sn)
            except AttributeError, e:
                raise ImproperlyConfigured("Missing required settings: %s" % sn)
        return cotext_extras

def admin_media(request):
    return {'ADMIN_MEDIA_PREFIX':settings.ADMIN_MEDIA_PREFIX,}