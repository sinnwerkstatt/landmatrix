from django.db import models
from django.utils.translation import ugettext_lazy as _

from landmatrix.models.default_string_representation import DefaultStringRepresentation



class RegionManager(models.Manager):
    pass


class Region(models.Model, DefaultStringRepresentation):
    name = models.CharField("Name", max_length=255)
    slug = models.SlugField("Slug")
    point_lat_min = models.DecimalField(
        _("Latitude of northernmost point"), max_digits=18, decimal_places=12, blank=True, null=True
    )
    point_lon_min = models.DecimalField(
        _("Longitude of westernmost point"), max_digits=18, decimal_places=12, blank=True, null=True
    )
    point_lat_max = models.DecimalField(
        _("Latitude of southernmost point"), max_digits=18, decimal_places=12, blank=True, null=True
    )
    point_lon_max = models.DecimalField(
        _("Longitude of easternmost point"), max_digits=18, decimal_places=12, blank=True, null=True
    )

    objects = RegionManager()

    def __str__(self):
        return self.name

