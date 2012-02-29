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


class SetVarNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


def set_var(parser, token):
    """{% set <var_name>  = <var_value> %}"""
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: " +
                                           "{% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])
register.tag('set', set_var)
