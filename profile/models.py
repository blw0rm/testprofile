# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    birthday = models.DateTimeField(u'Дата рождения', null=True)
    biography = models.TextField(u'Биография', null=True)
    #contacts = models.EmailField(u'Адресс электронной почты', null=True)
    
    def __unicode__(self):
        return self.user.username+' profile'