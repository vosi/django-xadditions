from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def get_settings(name):
    try:
        return settings.__getattr__(str(name))
    except AttributeError:
        return ""


@register.filter()
def total(list, field):
    return sum(getattr(d, field) for d in list)


@register.filter()
def joinby(value, key):
    return ", ".join([getattr(c, key, 'empty') for c in value])


@register.filter()
def pk_in(pk, obj):
    return pk in [o.pk for o in obj]
