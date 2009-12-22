# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    birthday = models.DateTimeField(u'Дата рождения')
    biography = models.TextField(u'Биография')
    contacts = models.EmailField(u'Адресс электронной почты', help_text='email')
    
    def __unicode__(self):
        return self.biography