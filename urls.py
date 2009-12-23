# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.list_detail import object_detail
from profile.views import profile_view, edit_profile
import registration

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', profile_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
    url(r'^edit/', edit_profile, name='profile_edit'),
)
