from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^i18n/setlang/$', 'xadditions.views.i18n.set_language', name='i18n_setlang'),
    url(r'^js/urls\.js$', 'xadditions.views.common.get_urls', name='js_urls'),
)
