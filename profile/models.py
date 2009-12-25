# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Message
from django.contrib.admin.models import LogEntry
from django.db.models.signals import post_delete, post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session


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
    if not (issubclass(sender, LogEntry) or issubclass(sender, Session)):
        instance = kwargs['instance']
        if not isinstance(instance, Session):
            created = kwargs['created']
            try:
                usr = User.objects.all()[0]                
                try:
                    rpr = instance.__unicode__()
                except:
                    rpr = repr(instance)
                content_type = ContentType.objects.get(app_label=instance._meta.app_label, model=instance._meta.module_name)
                if created:
                    action_flag = ADDITION
                else:
                    action_flag = CHANGE
                    log_entry = LogEntry(object_id=instance.id, object_repr=rpr, action_flag=action_flag, content_type=content_type, user=usr)
                    log_entry.save()
            except:
                pass
    
post_save.connect(log_cr_upd)

def log_deletion(sender, **kwargs):
    if not (issubclass(sender, LogEntry) or issubclass(sender, Session)):
        instance = kwargs['instance']
        if not isinstance(instance, Session):
            try:
                usr = User.objects.all()[0]
                try:
                    rpr = instance.__unicode__()
                except:
                    rpr = repr(instance)
                content_type = ContentType.objects.get(app_label=instance._meta.app_label, model=instance._meta.module_name)
                action_flag = DELETION
                log_entry = LogEntry(object_id=instance.id, object_repr=rpr, action_flag=action_flag, content_type=content_type, user=usr)
                log_entry.save()
            except:
                pass

    
post_delete.connect(log_deletion)
    