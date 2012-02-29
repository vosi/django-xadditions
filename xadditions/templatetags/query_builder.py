from django import template
from django.http import QueryDict


register = template.Library()


@register.tag()
def qstring(parser, token):
    """
    {% qstring as querystring %}
    """
    tokens = token.split_contents()
    if len(tokens) not in (1, 3):
        raise template.TemplateSyntaxError("'%s' takes zero or 2 arguments "
                                           "(as var_name)." % tokens[0])
    if len(tokens) == 1:
        asvar = None
    else:
        asvar = tokens[2]
    return GetRequestQueryStringNode(asvar)


class GetRequestQueryStringNode(template.Node):
    def __init__(self, asvar=None):
        self.asvar = asvar

    def __repr__(self):
        return '<GetRequestQueryStringNode>'

    def render(self, context):
        request = context.get('request', None)
        if request is None:
            return ''
        qstring = request.GET.urlencode()
        if self.asvar:
            context[self.asvar] = qstring
            return ''
        return qstring


def _qset(qdict, qset):
    qset_dict = QueryDict(qset)
    for key, val in qset_dict.items():
        qdict[key] = val
    return qdict

def _qadd(qdict, qadd):
    qadd_dict = QueryDict(qadd)
    for key, val in qadd_dict.items():
        qdict.appendlist(key, val)
    return qdict

def _qdel(qdict, qdel):
    for key in qdel.split(','):
        try:
            del qdict[key]
        except KeyError:
            pass
    return qdict

def _qrem(qdict, qrem):
    qrem_dict = QueryDict(qrem)
    for key, val in qrem_dict.items():
        oldlist = qdict.getlist(key)
        oldlist.remove(val)
        qdict.setlist(key, oldlist)
    return qdict


def _qremain(qdict, qremain):
    qremain_dict = QueryDict(qremain)
    for key in qdict.items():
        if key not in qremain_dict:
            try:
                del qdict[key]
            except KeyError:
                pass
    return qdict

@register.filter()
def qset(qstring, modifier):
    qdict = QueryDict(qstring, mutable=True)
    return _qset(qdict, modifier).urlencode()

@register.filter()
def qadd(qstring, modifier):
    qdict = QueryDict(qstring, mutable=True)
    return _qadd(qdict, modifier).urlencode()

@register.filter()
def qdel(qstring, modifier):
    qdict = QueryDict(qstring, mutable=True)
    return _qdel(qdict, modifier).urlencode()

@register.filter()
def qrem(qstring, modifier):
    qdict = QueryDict(qstring, mutable=True)
    return _qrem(qdict, modifier).urlencode()

@register.filter()
def qremain(qstring, modifier):
    qdict = QueryDict(qstring, mutable=True)
    return _qremain(qdict, modifier).urlencode()

@register.filter()
def qget(qstring, modifier):
    """ :type qstring: QueryDict"""
    if isinstance(qstring, QueryDict):
        return qstring.getlist(modifier)


class GetUriNode(template.Node):
    def __init__(self, url):
        self.url = url
    def render(self, context):
        try:
            url = template.Variable(self.url).resolve(context)
        except template.VariableDoesNotExist:
            url = ""
        return context['request'].build_absolute_uri(url)


@register.tag
def get_uri(parser, token):
    parts = token.split_contents()
    if not len(parts) == 2:
        raise template.TemplateSyntaxError("get_uri must be of the form: {% get_uri url %}")
    return GetUriNode(parts[1])
