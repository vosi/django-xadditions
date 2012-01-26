from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def get_settings(name):
    try:
        return settings.__getattr__(str(name))
    except AttributeError:
        return ""

@register.simple_tag(takes_context=True)
def absurl(context, path):
    if 'request' in context:
        return context['request'].build_absolute_uri(path)
    else:
        return ''

@register.assignment_tag(takes_context=True)
def absurlas(context, path):
    if 'request' in context:
        return context['request'].build_absolute_uri(path)
    else:
        return ''
