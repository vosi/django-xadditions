from django.core.exceptions import ViewDoesNotExist
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.utils.translation import ugettext as _


def extract_patterns(urlpatterns, base='', namespace=None):
    views = []
    for p in urlpatterns:
        if isinstance(p, RegexURLPattern):
            try:
                views.append(
                    (p.callback, base + p.regex.pattern, p.name, namespace))
            except ViewDoesNotExist:
                continue
        elif isinstance(p, RegexURLResolver):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(
                extract_patterns(patterns,
                                               base + p.regex.pattern,
                                               namespace=p.namespace or namespace))
        elif hasattr(p, '_get_callback'):
            try:
                views.append((
                    p._get_callback(), base + p.regex.pattern, p.name,
                    namespace))
            except ViewDoesNotExist:
                continue
        elif hasattr(p, 'url_patterns') or hasattr(p, '_get_url_patterns'):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(extract_patterns(patterns,
                                                        base + p.regex.pattern,
                                                        namespace=namespace))
        else:
            raise TypeError, _(
                "%s does not appear to be a urlpattern object") % p
    return views
