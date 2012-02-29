from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^i18n/setlang/', 'xadditions.views.i18n.set_language'),
)
