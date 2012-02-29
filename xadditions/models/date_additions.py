from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class ModelWithTrace(models.Model):
    created_at = models.DateTimeField(_('Date created'),
                                      auto_now_add=True, db_index=True,
                                      editable=False,
                                      default=datetime.now())
    created_by = models.ForeignKey(User, related_name='+',
                                   editable=False, blank=True,
                                   null=True, default=None)
    modified_at = models.DateTimeField(_('Date modified'),
                                       auto_now_add=True, auto_now=True, db_index=True,
                                       editable=False, default=datetime.now())
    modified_by = models.ForeignKey(User, related_name='+',
                                    editable=False, blank=True,
                                    null=True, default=None)

    class Meta:
        abstract = True
