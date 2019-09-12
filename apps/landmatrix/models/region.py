from django.db import models
from django.utils.translation import ugettext_lazy as _


class Region(models.Model):
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

    def __str__(self):
        return self.name

    @property
    def point_lon(self):
        return (self.point_lon_min + self.point_lon_max) / 2

    @property
    def point_lat(self):
        return (self.point_lat_min + self.point_lat_max) / 2
