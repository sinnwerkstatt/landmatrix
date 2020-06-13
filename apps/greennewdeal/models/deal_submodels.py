import reversion
from django.contrib.gis.db import models as gismodels
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from apps.greennewdeal.models import Deal
from apps.greennewdeal.models.mixins import (
    OldContractMixin,
    OldDataSourceMixin,
    OldLocationMixin,
    UnderscoreDisplayParseMixin,
)


class DealSubmodelManager(models.Manager):
    def visible(self, user=None):
        qs = self.get_queryset()
        if user and (user.is_staff or user.is_superuser):
            return qs.all()
        return qs.filter(deal__status__in=(2, 3), deal__confidential=False)


@reversion.register(ignore_duplicates=True)
class Location(models.Model, UnderscoreDisplayParseMixin, OldLocationMixin):
    name = models.CharField(max_length=2000, blank=True)
    description = models.CharField(max_length=2000, blank=True)
    point = gismodels.PointField(blank=True, null=True)
    facility_name = models.CharField(max_length=2000, blank=True)
    ACCURACY_CHOICES = (
        ("COUNTRY", _("Country")),
        ("ADMINISTRATIVE_REGION", _("Administrative region")),
        ("APPROXIMATE_LOCATION", _("Approximate location")),
        ("EXACT_LOCATION", _("Exact location")),
        ("COORDINATES", _("Coordinates")),
    )
    level_of_accuracy = models.CharField(
        choices=ACCURACY_CHOICES, max_length=100, blank=True, null=True
    )
    comment = models.TextField(blank=True)

    # contract_area = gismodels.MultiPolygonField(blank=True, null=True)
    # intended_area = gismodels.MultiPolygonField(blank=True, null=True)
    # production_area = gismodels.MultiPolygonField(blank=True, null=True)
    areas = JSONField(blank=True, null=True)

    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="locations")
    old_group_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, null=False)

    objects = DealSubmodelManager()

    def __str__(self):
        return f"(#{self.deal_id}) {self.name}"


@reversion.register(ignore_duplicates=True)
class Contract(models.Model, UnderscoreDisplayParseMixin, OldContractMixin):
    number = models.CharField(_("Contract number"), max_length=255, blank=True)
    date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    agreement_duration = models.IntegerField(
        _("Duration of the agreement (in years)"), blank=True, null=True
    )
    comment = models.TextField(blank=True)

    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="contracts")
    old_group_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, null=False)

    objects = DealSubmodelManager()

    def __str__(self):
        return f"(#{self.deal_id}) {self.number}"


@reversion.register(ignore_duplicates=True)
class DataSource(models.Model, UnderscoreDisplayParseMixin, OldDataSourceMixin):
    TYPE_CHOICES = (
        ("MEDIA_REPORT", _("Media report")),
        ("RESEARCH_PAPER_OR_POLICY_REPORT", _("Research Paper / Policy Report")),
        ("GOVERNMENT_SOURCES", _("Government sources")),
        ("COMPANY_SOURCES", _("Company sources")),
        ("CONTRACT", _("Contract")),
        ("CONTRACT_FARMING_AGREEMENT", _("Contract (contract farming agreement)")),
        ("PERSONAL_INFORMATION", _("Personal information")),
        ("CROWDSOURCING", _("Crowdsourcing")),
        ("OTHER", _("Other (Please specify in comment field)")),
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=100, blank=True, null=True)
    url = models.URLField(max_length=5000, blank=True, null=True)
    file = models.FileField(
        _("File"),
        upload_to="uploads",
        max_length=5000,
        help_text=_("Maximum file size: 10MB"),
        blank=True,
        null=True,
    )
    file_not_public = models.BooleanField(_("Keep PDF not public"), default=False)
    publication_title = models.CharField(max_length=5000, blank=True)
    date = models.DateField(blank=True, null=True)
    name = models.CharField(_("Name"), max_length=500, blank=True)
    company = models.CharField(_("Company"), max_length=500, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    phone = models.CharField(_("Phone"), max_length=500, blank=True)

    includes_in_country_verified_information = models.BooleanField(
        _("Includes in-country-verified information"), default=False
    )
    open_land_contracts_id = models.CharField(max_length=500, blank=True)
    comment = models.TextField(_("Comment on data source"), blank=True)

    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="datasources")
    old_group_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, null=False)

    objects = DealSubmodelManager()

    def __str__(self):
        return f"(#{self.deal_id}) {self.get_type_display()}"
