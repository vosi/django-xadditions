from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


class ModelWithDateTrace(models.Model):
    created_at = models.DateTimeField(
        _('Date created'), auto_now_add=True, db_index=True, editable=False,
        default=timezone.now())
    modified_at = models.DateTimeField(
        _('Date modified'), auto_now_add=True, auto_now=True, db_index=True,
        editable=False, default=timezone.now())

    class Meta:
        abstract = True


class ModelWithUserTrace(models.Model):
    #created_by = models.ForeignKey(User, related_name='+',
    #                               editable=False, blank=True,
    #                               null=True, default=None)
    #modified_by = models.ForeignKey(User, related_name='+',
    #                                editable=False, blank=True,
    #                                null=True, default=None)

    class Meta:
        abstract = True
