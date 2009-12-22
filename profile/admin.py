# -*- coding: utf-8 -*-

from django.contrib import admin
from models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birthday', 'contacts')
    list_filter = ('user',)
    
admin.site.register(UserProfile, UserProfileAdmin)