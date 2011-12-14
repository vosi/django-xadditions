from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def get_settings(name):
    try:
        return settings.__getattr__(str(name))
    except AttributeError:
        return ""
