from django.contrib.gis.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class CountryManager(models.Manager):
    def get_queryset(self):
        # Defer geom field since it slows down queries, especially within the django admin
        return super().get_queryset().defer("geom")


class Country(models.Model):
    name = models.CharField(_("Name"))
    slug = models.SlugField(
        _("Slug"),
        max_length=100,  # not changing max_length to None, because it yields database problems for some reason
    )

    region = models.ForeignKey(
        "Region",
        verbose_name=_("Region"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    code_alpha2 = models.CharField(_("Code ISO 3166-1 alpha2"), max_length=2)
    code_alpha3 = models.CharField(_("Code ISO 3166-1 alpha3"), max_length=3)

    point_lat = models.DecimalField(
        _("Latitude of central point"),
        max_digits=18,
        decimal_places=12,
    )
    point_lon = models.DecimalField(
        _("Longitude of central point"),
        max_digits=18,
        decimal_places=12,
    )
    point_lat_min = models.DecimalField(
        _("Latitude of southernmost point"),
        max_digits=18,
        decimal_places=12,
    )
    point_lon_min = models.DecimalField(
        _("Longitude of westernmost point"),
        max_digits=18,
        decimal_places=12,
    )
    point_lat_max = models.DecimalField(
        _("Latitude of northernmost point"),
        max_digits=18,
        decimal_places=12,
    )
    point_lon_max = models.DecimalField(
        _("Longitude of easternmost point"),
        max_digits=18,
        decimal_places=12,
    )
    democracy_index = models.DecimalField(
        _("Democracy index"),
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
    )
    corruption_perception_index = models.DecimalField(
        _("Corruption perception index"),
        max_digits=2,
        decimal_places=1,
        blank=True,
        null=True,
    )
    high_income = models.BooleanField(
        _("High income"),
        help_text="Target countries are countries that are NOT high income",
        default=False,
    )
    geom = models.MultiPolygonField(null=True)

    objects = CountryManager()

    class Meta:
        ordering = ("name",)
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name

    @property
    def short_description(self):
        return (
            self.observatorypage.short_description
            if hasattr(self, "observatorypage")
            else None
        )

    def get_absolute_url(self):
        return reverse_lazy("country", kwargs={"country_slug": self.slug})


class Region(models.Model):
    name = models.CharField(_("Name"))
    slug = models.SlugField(_("Slug"))

    point_lat_min = models.DecimalField(
        _("Latitude of southernmost point"),
        max_digits=18,
        decimal_places=12,
    )
    point_lon_min = models.DecimalField(
        _("Longitude of westernmost point"),
        max_digits=18,
        decimal_places=12,
    )
    point_lat_max = models.DecimalField(
        _("Latitude of northernmost point"),
        max_digits=18,
        decimal_places=12,
    )
    point_lon_max = models.DecimalField(
        _("Longitude of easternmost point"),
        max_digits=18,
        decimal_places=12,
    )

    class Meta:
        ordering = ("name",)
        verbose_name_plural = _("Regions")

    def __str__(self):
        return self.name

    @property
    def point_lon(self):
        return (self.point_lon_min + self.point_lon_max) / 2

    @property
    def point_lat(self):
        return (self.point_lat_min + self.point_lat_max) / 2

    @property
    def short_description(self):
        return (
            self.observatorypage.short_description
            if hasattr(self, "observatorypage")
            else None
        )
