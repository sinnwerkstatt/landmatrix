from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from nanoid import generate
from wagtail.models import Site

from apps.landmatrix.models import choices
from apps.landmatrix.models.deal import DealVersion, DealHull
from apps.landmatrix.models.fields import (
    LooseDateField,
    NanoIDField,
)
from apps.landmatrix.models.investor import InvestorVersion, InvestorHull

VERSION_STATUS_CHOICES = (
    ("DRAFT", _("Draft")),
    ("REVIEW", _("Review")),
    ("ACTIVATION", _("Activation")),
    ("ACTIVATED", _("Activated")),
)


class BaseDataSource(models.Model):
    nid = NanoIDField("ID", max_length=15, db_index=True)
    type = models.CharField(_("Type"), choices=choices.DATASOURCE_TYPE_CHOICES)
    # NOTE hit a URL > 1000 chars... so going with 5000 for now.
    url = models.URLField(_("Url"), blank=True, max_length=5000)
    file = models.FileField(_("File"), blank=True, null=True, max_length=3000)
    file_not_public = models.BooleanField(_("Keep PDF not public"), default=False)
    publication_title = models.CharField(_("Publication title"), blank=True)
    date = LooseDateField(_("Date"), blank=True, null=True)
    name = models.CharField(_("Name"), blank=True)
    company = models.CharField(_("Organisation"), blank=True)
    email = models.EmailField(_("Email"), blank=True)
    phone = models.CharField(_("Phone"), blank=True)
    includes_in_country_verified_information = models.BooleanField(
        _("Includes in-country-verified information"), blank=True, null=True
    )
    open_land_contracts_id = models.CharField(_("Open Contracting ID"), blank=True)
    comment = models.TextField(_("Comment"), blank=True)

    def to_dict(self):
        return {
            "nid": self.nid,
            "type": self.type,
            "url": self.url,
            "file": str(self.file),
            "file_not_public": self.file_not_public,
            "publication_title": self.publication_title,
            "date": self.date,
            "name": self.name,
            "company": self.company,
            "email": self.email,
            "phone": self.phone,
            "includes_in_country_verified_information": self.includes_in_country_verified_information,
            "open_land_contracts_id": self.open_land_contracts_id,
            "comment": self.comment,
        }

    def save(self, *args, **kwargs):
        if self._state.adding and not self.nid:
            self.nid = generate(size=8)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]


class DealDataSource(BaseDataSource):
    dealversion = models.ForeignKey(
        DealVersion, on_delete=models.CASCADE, related_name="datasources"
    )

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]


class InvestorDataSource(BaseDataSource):
    investorversion = models.ForeignKey(
        InvestorVersion, on_delete=models.CASCADE, related_name="datasources"
    )

    class Meta:
        unique_together = ["investorversion", "nid"]
        indexes = [models.Index(fields=["investorversion", "nid"])]
        ordering = ["id"]


class _WorkflowInfo(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
    )
    status_before = models.CharField(
        choices=VERSION_STATUS_CHOICES, null=True, blank=True
    )
    status_after = models.CharField(
        choices=VERSION_STATUS_CHOICES, null=True, blank=True
    )
    timestamp = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True)
    replies = models.JSONField(null=True, default=list)
    resolved = models.BooleanField(default=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
            "status_before": self.status_before,
            "status_after": self.status_after,
            "timestamp": self.timestamp,
            "comment": self.comment,
            "resolved": self.resolved,
            "replies": self.replies,
        }

    def get_object_url(self):
        _site = Site.objects.get(is_default_site=True)
        _port = f":{_site.port}" if _site.port not in [80, 443] else ""
        base_url = f"http{'s' if _site.port == 443 else ''}://{_site.hostname}{_port}"
        return base_url

    class Meta:
        abstract = True


class DealWorkflowInfo(_WorkflowInfo):
    deal = models.ForeignKey(
        DealHull, on_delete=models.CASCADE, related_name="workflowinfos"
    )
    deal_version = models.ForeignKey(
        DealVersion,
        on_delete=models.SET_NULL,
        related_name="workflowinfos",
        null=True,
        blank=True,
    )

    # OLD Code
    # # WARNING
    # # Do not use to map large query sets!
    # # Takes tons of memory storing related deal and deal_version objects.
    # def to_dict(self) -> dict:
    #     d = super().to_dict()
    #     d.update({"deal": self.deal, "deal_version": self.deal_version})
    #     return d

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"deal_id": self.deal_id, "deal_version_id": self.deal_version_id})
        return d

    def get_object_url(self):
        base_url = super().get_object_url()
        return base_url + f"/deal/{self.deal_id}/"


class InvestorWorkflowInfo(_WorkflowInfo):
    investor = models.ForeignKey(
        InvestorHull, on_delete=models.CASCADE, related_name="workflowinfos"
    )
    investor_version = models.ForeignKey(
        InvestorVersion,
        on_delete=models.SET_NULL,
        related_name="workflowinfos",
        null=True,
        blank=True,
    )

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "investor_id": self.investor_id,
                "investor_version_id": self.investor_version_id,
            }
        )
        return d

    def get_object_url(self):
        base_url = super().get_object_url()
        return base_url + f"/investor/{self.investor_id}/"


class DealTopInvestors(models.Model):
    """A view on dealversion.top_investors M2M relation table."""

    dealversion = models.ForeignKey(
        DealVersion, on_delete=models.CASCADE, related_name="+"
    )
    investorhull = models.ForeignKey(
        InvestorHull, on_delete=models.CASCADE, related_name="+"
    )

    class Meta:
        managed = False
        db_table = "landmatrix_dealversion_top_investors"

    def __str__(self):
        return f"#{self.dealversion.deal_id} - {self.investorhull.active_version.name}"
