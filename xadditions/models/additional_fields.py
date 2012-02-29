from django.db import models
from autoslug.fields import AutoSlugField


class ModelWithSlug(models.Model):
    slug = AutoSlugField(populate_from='get_slug_source', always_update=True, db_index=True, max_length=255, null=True)

    def get_slug_source(obj):
        return getattr(obj, 'title', 'no slug')


    class Meta:
        abstract = True
