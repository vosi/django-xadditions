from django.contrib import admin


class AdminTrace(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.pk:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
        super(AdminTrace, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if hasattr(instance, 'modified_by') and instance.pk:
                instance.modified_by = request.user
            if hasattr(instance, 'created_by') and not instance.pk:
                instance.created_by = request.user
            instance.save()

