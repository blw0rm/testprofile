# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.db.models.signals import post_delete, post_save
from django.contrib.contenttypes.models import ContentType

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    birthday = models.DateTimeField(u'Date of birth', null=True)
    biography = models.TextField(u'Biography', null=True)
    #contacts = models.EmailField(u'Адресс электронной почты', null=True)
    
    def __unicode__(self):
        return self.user.username+' profile'
    
ADDITION = 1
CHANGE = 2
DELETION = 3

def log_cr_upd(sender, **kwargs):
    if not isinstance(sender, LogEntry):
        instance = kwargs['instance']
        created = kwargs['created']
        usr = User.objects.all()[0]
        content_type = ContentType.objects.get(app_label=instance._meta.app_label, model=instance._meta.module_name)
        if created:
            action_flag = ADDITION
        else:
            action_flag = CHANGE
            log_entry = LogEntry(object_id=instance.id, object_repr=instance.__repr__(), action_flag=action_flag, content_type=content_type, user=usr)
            log_entry.save()
    
post_save.connect(log_cr_upd)

def log_deletion(sender, **kwargs):
    if not isinstance(sender, LogEntry):
        instance = kwargs['instance']
        usr = User.objects.all()[0]
        content_type = ContentType.objects.get(app_label=instance._meta.app_label, model=instance._meta.module_name)
        action_flag = DELETION
        log_entry = LogEntry(object_id=instance.id, object_repr=instance.__repr__(), action_flag=action_flag, content_type=content_type, user=usr)
        log_entry.save()
    
post_delete.connect(log_deletion)
    