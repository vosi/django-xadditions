from collections import OrderedDict
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django import template
from django.conf import settings
from django.template.base import TemplateSyntaxError, \
    VARIABLE_ATTRIBUTE_SEPARATOR, Node


register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)

@register.filter()
def call_method(obj, methodName):
    if obj is list:
        #TODO: todo
        pass
    else:
        method = getattr(obj, methodName)

        if obj.__dict__.has_key("__callArg"):
            ret = method(*obj.__callArg)
            del obj.__callArg
            return ret
        return method()

@register.filter()
def args(obj, arg):
    if not obj.__dict__.has_key("__callArg"):
        obj.__callArg = []
    obj.__callArg += [arg]
    return obj

@register.simple_tag
def get_settings(name):
    try:
        return settings.__getattr__(str(name))
    except AttributeError:
        return ""


@register.filter
def tabindex(value, index):
    """
    Add a tabindex attribute to a field.
    """
    value.field.widget.attrs['tabindex'] = index
    return value


@register.filter()
def total(list, field):
    return sum(getattr(d, field) for d in list)


@register.filter()
def joinby(value, key):
    return ", ".join([getattr(c, key, 'empty') for c in value])


@register.filter()
def pk_in(pk, obj):
    return pk in [o.pk for o in obj]


@register.filter()
def get_min(list, field):
    return min(getattr(d, field) for d in list)


@register.filter()
def get_max(list, field):
    return max(getattr(d, field) for d in list)


@register.filter()
def date_past(date, delta=0):
    """
    :type date: datetime.date
    """
    if date - relativedelta(days=+delta) < timezone.now():
        return True
    return False

@register.filter()
def multiple_of(check, div):
    t = divmod(check, div)
    return t[1] == 0 and check != 0



class RegroupNode(Node):
    def __init__(self, target, expression, var_name):
        self.target, self.expression = target, expression
        self.var_name = var_name

    def resolve_expression(self, obj, context):
        # This method is called for each object in self.target. See regroup()
        # for the reason why we temporarily put the object in the context.
        context[self.var_name] = obj
        return self.expression.resolve(context, True)

    def render(self, context):
        obj_list = self.target.resolve(context, True)
        if obj_list is None:
            # target variable wasn't found in context; fail silently.
            context[self.var_name] = []
            return ''
        # List of dictionaries in the format:
        # {'grouper': 'key', 'list': [list of contents]}.
        res = OrderedDict()
        for obj in obj_list:
            if self.resolve_expression(obj, context) in res:
                res[self.resolve_expression(obj, context)].append(obj)
            else:
                res[self.resolve_expression(obj, context)] = [obj]

        context[self.var_name] = [
            {'grouper': key, 'list': list(val)}
            for key, val in res.items()
        ]
        return ''


@register.tag
def regroup2(parser, token):
    """
    Regroups a list of alike objects by a common attribute.
    ! A list may be unsorted or randomly sorted !

    This complex tag is best illustrated by use of an example:  say that
    ``people`` is a list of ``Person`` objects that have ``first_name``,
    ``last_name``, and ``gender`` attributes, and you'd like to display a list
    that looks like:

        * Male:
            * George Bush
            * Bill Clinton
        * Female:
            * Margaret Thatcher
            * Colendeeza Rice
        * Unknown:
            * Pat Smith

    The following snippet of template code would accomplish this dubious task::

        {% regroup people by gender as grouped %}
        <ul>
        {% for group in grouped %}
            <li>{{ group.grouper }}
            <ul>
                {% for item in group.list %}
                <li>{{ item }}</li>
                {% endfor %}
            </ul>
        {% endfor %}
        </ul>

    As you can see, ``{% regroup %}`` populates a variable with a list of
    objects with ``grouper`` and ``list`` attributes.  ``grouper`` contains the
    item that was grouped by; ``list`` contains the list of objects that share
    that ``grouper``.  In this case, ``grouper`` would be ``Male``, ``Female``
    and ``Unknown``, and ``list`` is the list of people with those genders.
    """
    firstbits = token.contents.split(None, 3)
    if len(firstbits) != 4:
        raise TemplateSyntaxError("'regroup' tag takes five arguments")
    target = parser.compile_filter(firstbits[1])
    if firstbits[2] != 'by':
        raise TemplateSyntaxError("second argument to 'regroup' tag "
                                  "must be 'by'")
    lastbits_reversed = firstbits[3][::-1].split(None, 2)
    if lastbits_reversed[1][::-1] != 'as':
        raise TemplateSyntaxError("next-to-last argument to 'regroup' tag must"
                                  " be 'as'")
    var_name = lastbits_reversed[0][::-1]
    # RegroupNode will take each item in 'target', put it in the context under
    # 'var_name', evaluate 'var_name'.'expression' in the current context, and
    # group by the resulting value. After all items are processed, it will
    # save the final result in the context under 'var_name', thus clearing the
    # temporary values. This hack is necessary because the template engine
    # doesn't provide a context-aware equivalent of Python's getattr.
    expression = parser.compile_filter(var_name +
                                       VARIABLE_ATTRIBUTE_SEPARATOR +
                                       lastbits_reversed[2][::-1])
    return RegroupNode(target, expression, var_name)
