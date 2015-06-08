__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Region(models.Model):
    name = models.CharField("Name", max_length=255)
    slug = models.SlugField("Slug")
    point_lat = models.DecimalField(_("Point lat"), max_digits=18, decimal_places=12, blank=True, null=True)
    point_lon = models.DecimalField(_("Point lon"), max_digits=18, decimal_places=12, blank=True, null=True)

    def __unicode__(self):
        return self.name
