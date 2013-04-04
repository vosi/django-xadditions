from django import template

register = template.Library()


@register.filter
def permissions(obj, user):
    return user.get_all_permissions(obj=obj)


class RulezPermsNode(template.Node):
    def __init__(self, codename, objname, varname):
        self.codename = codename
        self.objname = objname
        self.varname = varname

    def render(self, context):
        user_obj = template.resolve_variable('user', context)
        obj = template.resolve_variable(self.objname, context)
        context[self.varname] = user_obj.has_perm(self.codename, obj)
        return ''

def has_xperms(parser, token):
    '''
    Template tag to check for permission against an object.
    Built out of a need to use permissions with anonymous users at an
    object level.

    Usage:
        {% load xperms %}

        {% for VARNAME in QUERYRESULT %}
            {% has_xperms CODENAME VARNAME as BOOLEANVARNAME %}
            {% if BOOLEANVARNAME %}
                I DO
            {% else %}
                I DON'T
            {% endif %}
            have permission for {{ VARNAME }}.{{ CODENAME }}!!
        {% endfor %}
    '''
    try:
        bits = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'tag requires exactly three arguments')
    if len(bits) != 5:
        raise template.TemplateSyntaxError(
            'tag requires exactly three arguments')
    if bits[3] != 'as':
        raise template.TemplateSyntaxError(
            "third argument to tag must be 'as'")
    return RulezPermsNode(bits[1], bits[2], bits[4])

has_xperms = register.tag(has_xperms)
