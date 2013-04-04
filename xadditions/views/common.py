import json
from django.conf import settings
from django import http
from django.template import loader, RequestContext
from django.views.decorators.cache import cache_page
from xadditions.tools.show_urls import extract_patterns

from django.utils.functional import Promise
from django.utils.translation import force_text

try:
    from django.contrib.admindocs.views import simplify_regex
except ImportError:
    from django.contrib.admin.views.doc import simplify_regex


class LazyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


class JSONResponseCommon(object):
    def get_json_response(self, content, **httpresponse_kwargs):
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context, cls=LazyEncoder)


class JSONResponseMixin(JSONResponseCommon):
    def render_to_response(self, context, **response_kwargs):
        return self.get_json_response(self.convert_context_to_json(context),
                                      **response_kwargs)


class JSONResponseSynMixin(JSONResponseCommon):
    def render_to_response_json(self, context, **response_kwargs):
        return self.get_json_response(self.convert_context_to_json(context),
                                      **response_kwargs)


GET_URLS_TPL = "var X_ALL_URLS = {{ urls|safe }};"


@cache_page(60 * 60 * 24 * 10)
def get_urls(request):
    def _get_urls():
        urls = {}
        if settings.ADMIN_FOR:
            settings_modules = [__import__(m, {}, {}, ['']) for m in
                                settings.ADMIN_FOR]
        else:
            settings_modules = [settings]

        for settings_mod in settings_modules:
            urlconf = __import__(settings_mod.ROOT_URLCONF, {}, {}, [''])
            view_functions = \
                extract_patterns(urlconf.urlpatterns)

            for (func, regex, url_name, namespace) in view_functions:
                if namespace is not None and url_name is not None:
                    url_name = namespace + '_' + url_name
                urls.update({url_name: simplify_regex(regex)})
        return urls

    t = loader.get_template_from_string(GET_URLS_TPL)
    c = RequestContext(request, {'urls': json.dumps(_get_urls(), indent=0,
                                                    cls=LazyEncoder)})
    return http.HttpResponse(t.render(c),
                             content_type='application/javascript')
