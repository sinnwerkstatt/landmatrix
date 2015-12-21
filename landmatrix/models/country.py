
__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):

    fk_region = models.ForeignKey("Region", verbose_name=_("Region"))
    code_alpha2 = models.CharField(_("Code ISO 3166-1 alpha2"), max_length=2)
    code_alpha3 = models.CharField(_("Code ISO 3166-1 alpha3"), max_length=3)
    name = models.CharField("Name", max_length=255)
    slug = models.SlugField("Slug", max_length=100)
    point_lat = models.DecimalField(
        _("Point lat"), max_digits=18, decimal_places=12, blank=True, null=True
    )
    point_lon = models.DecimalField(
        _("Point lon"), max_digits=18, decimal_places=12, blank=True, null=True
    )
    democracy_index = models.DecimalField(
        _("Democracy index"), max_digits=3, decimal_places=2, blank=True, null=True
    )
    corruption_perception_index = models.DecimalField(
        _("Corruption perception index"), max_digits=2, decimal_places=1, blank=True, null=True
    )
    high_income = models.BooleanField(_("High income"), default=False)

    def __str__(self):
        return self.name
