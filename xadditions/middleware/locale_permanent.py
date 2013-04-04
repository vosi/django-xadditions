from django.http import HttpResponseRedirect
from django.middleware.locale import LocaleMiddleware

class LocalePermanentMiddleware(LocaleMiddleware):
    def process_response(self, request, response):
        response = super(LocalePermanentMiddleware, self)\
            .process_response(request, response)
        if isinstance(response,HttpResponseRedirect):
            response.status_code = 301
        return response
