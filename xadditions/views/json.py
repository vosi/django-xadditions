from django import http
from django.utils import simplejson as json

class JSONResponseMixin(object):
    def render_to_response(self, context, **response_kwargs):
        return self.get_json_response(self.convert_context_to_json(context), **response_kwargs)

    def get_json_response(self, content, **httpresponse_kwargs):
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)
