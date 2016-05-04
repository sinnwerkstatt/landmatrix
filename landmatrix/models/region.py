from django.db import models
from django.utils.translation import ugettext_lazy as _

from landmatrix.models.default_string_representation import DefaultStringRepresentation

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class RegionManager(models.Manager):

    def get_target_regions_by_activity(self, activity):
        '''
        Seems like there should be a way to do this using PostgreSQL hvals
        but it doesn't seem like django-hstore has implemented it.

        TODO: check the attribute name. Currently, there are no regions
        assigned in the data set, but I assume if there were, the attribute
        would be called 'target_region'.
        '''
        attribute_groups = activity.activityattributegroup_set.filter(
            attributes__contains=['target_region'])
        region_ids = {
            int(attribute_group.attributes['target_region'])
            for attribute_group in attribute_groups
        }
        matching_regions = self.filter(pk__in=region_ids)

        return matching_regions


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

