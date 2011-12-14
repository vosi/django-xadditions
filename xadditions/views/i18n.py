import re
from django import http
from django.conf import settings
from django.utils.translation import check_for_language


def set_language(request):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = http.HttpResponseRedirect(next)
    if request.method == 'GET':
        lang_code = request.GET.get('language', None)
        reg = re.compile(r'/\w{2}/')
        next = reg.sub('/'+lang_code+'/', next)
        response = http.HttpResponseRedirect(next)
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response
