# coding=utf-8
from django.db import models
from autoslug.fields import AutoSlugField


class ModelWithSlug(models.Model):
    slug = AutoSlugField(populate_from='get_slug_source', always_update=True,
                         unique=True, max_length=255, null=True)

    SLUG_FIELD = 'title'

    def get_slug_source(instance):
        return getattr(instance, instance.SLUG_FIELD)


    class Meta:
        abstract = True
