# -*- coding: utf-8 -*-
from django import template
from django.contrib import admin

register = template.Library()

@register.tag
def admin_url(parser, token):
    try:
        tag_name, args = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()
    if not (args[0] == args[-1] and args[0] in ("'",'"')):
        raise template.TemplateSyntaxError, "%r tag's argument should be in qoutes" % tag_name
    return AdminUrlNode(args[1:-1])

class AdminUrlNode(template.Node):
    def __init__(self, args):
        self.args = template.Variable(args)
        
    def render(self, context):
        instance = self.args.resolve(context)#getattr(context, self.args)
        # Checks if model is registered in admin application
        if instance:
            try:
                model = instance.__class__
                try:
                    admin.site.unregister(model)
                    admin.site.register(model)
                    return "/admin/%s/%s/%s" % (instance._meta.app_label,
                                        instance._meta.module_name,
                                        instance.id)
                except admin.sites.NotRegistered:
                    return ''
            except AttributeError:
                return ''
            