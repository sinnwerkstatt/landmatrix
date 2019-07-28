from django.db import models
from django.utils.translation import ugettext_lazy as _


class Status(models.Model):
    name = models.CharField(_("Name"), max_length=255, db_index=True)
    description = models.TextField(_("Description"), blank=True, null=True)
