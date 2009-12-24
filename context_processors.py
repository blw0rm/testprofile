# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def context_settings(request):
    return {'ADMIN_MEDIA_PREFIX':settings.ADMIN_MEDIA_PREFIX,
            'settings': settings}