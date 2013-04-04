from django.contrib import admin
from django import http


class PersistentFilters(admin.ModelAdmin):
    def add_view(self, request, *args, **kwargs):
        result = super(PersistentFilters, self).add_view(request,
                                                         *args, **kwargs )
        request.session['filtered'] =  None

        return result

    def change_view(self, request, object_id, form_url='', extra_context=None):
        result = super(PersistentFilters, self).change_view(request,
                                                            object_id,
                                                            form_url,
                                                            extra_context)

        ref = request.META.get('HTTP_REFERER', '')
        if ref.find('?') != -1:
            request.session['filtered'] =  ref

        if request.POST.has_key('_save'):
            try:
                if request.session['filtered'] is not None:
                    result['Location'] = request.session['filtered']
                    request.session['filtered'] = None
            except:
                pass

        return result

    def changelist_view(self, request, extra_context=None):
        try:
            if request.session['filtered'] is not None:
                filtered = request.session['filtered']
                request.session['filtered'] = None
                return http.HttpResponseRedirect(filtered)
        except:
            pass
        return super(PersistentFilters, self).changelist_view(request,
                                                                extra_context)
