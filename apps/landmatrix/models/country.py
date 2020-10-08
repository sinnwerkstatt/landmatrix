from django.contrib.gis.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class CountryManager(models.Manager):
    def get_queryset(self):
        # Defer geom field since it slows down queries, especially within the django admin
        return super(CountryManager, self).get_queryset().defer("geom")


class Country(models.Model):
    fk_region = models.ForeignKey(
        "Region", verbose_name=_("Region"), on_delete=models.PROTECT
    )
    code_alpha2 = models.CharField(_("Code ISO 3166-1 alpha2"), max_length=2)
    code_alpha3 = models.CharField(_("Code ISO 3166-1 alpha3"), max_length=3)
    name = models.CharField("Name", max_length=255)
    slug = models.SlugField("Slug", max_length=100)
    point_lat = models.DecimalField(
        _("Latitude of central point"),
        max_digits=18,
        decimal_places=12,
        blank=True,
        null=True,
    )
    point_lon = models.DecimalField(
        _("Longitude of central point"),
        max_digits=18,
        decimal_places=12,
        blank=True,
        null=True,
    )
    point_lat_min = models.DecimalField(
        _("Latitude of southernmost point"),
        max_digits=18,
        decimal_places=12,
        blank=True,
        null=True,
    )
    point_lon_min = models.DecimalField(
        _("Longitude of westernmost point"),
        max_digits=18,
        decimal_places=12,
        blank=True,
        null=True,
    )
    point_lat_max = models.DecimalField(
        _("Latitude of northernmost point"),
        max_digits=18,
        decimal_places=12,
        blank=True,
        null=True,
    )
    point_lon_max = models.DecimalField(
        _("Longitude of easternmost point"),
        max_digits=18,
        decimal_places=12,
        blank=True,
        null=True,
    )
    democracy_index = models.DecimalField(
        _("Democracy index"), max_digits=3, decimal_places=2, blank=True, null=True
    )
    corruption_perception_index = models.DecimalField(
        _("Corruption perception index"),
        max_digits=2,
        decimal_places=1,
        blank=True,
        null=True,
    )
    high_income = models.BooleanField(_("High income"), default=False)
    is_target_country = models.BooleanField(_("Is target country"), default=False)
    geom = models.MultiPolygonField(null=True)

    objects = CountryManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)

    @property
    def country_page_id(self):
        return self.countrypage.id if hasattr(self, "countrypage") else None

    @property
    def short_description(self):
        return self.countrypage.short_description if hasattr(self, "countrypage") else None

    def get_absolute_url(self):
        return reverse_lazy("country", kwargs={"country_slug": self.slug})

    def to_dict(self, deep=False):
        dict = {"id": self.id, "name": self.name, "code_alpha2": self.code_alpha2}
        if deep:
            dict["high_income"] = self.high_income
            dict["region"] = self.fk_region.to_dict()
        return dict


class Region(models.Model):
    name = models.CharField("Name", max_length=255)
    slug = models.SlugField("Slug")
    point_lat_min = models.DecimalField(
        _("Latitude of northernmost point"),
        max_digits=18,
        decimal_places=12,
        blank=True,
        null=True,
    )
    point_lon_min = models.DecimalField(
        _("Longitude of westernmost point"),
        max_digits=18,
        decimal_places=12,
        blank=True,
        null=True,
    )
    point_lat_max = models.DecimalField(
        _("Latitude of southernmost point"),
        max_digits=18,
        decimal_places=12,
        blank=True,
        null=True,
    )
    point_lon_max = models.DecimalField(
        _("Longitude of easternmost point"),
        max_digits=18,
        decimal_places=12,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    @property
    def point_lon(self):
        return (self.point_lon_min + self.point_lon_max) / 2

    @property
    def point_lat(self):
        return (self.point_lat_min + self.point_lat_max) / 2

    @property
    def region_page_id(self):
        return self.regionpage.id if hasattr(self, "regionpage") else None

    @property
    def short_description(self):
        return self.regionpage.short_description if hasattr(self, "regionpage") else None

    def to_dict(self):
        return {"id": self.id, "name": self.name}
