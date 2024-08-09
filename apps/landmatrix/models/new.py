from django.db import models
from django.utils.translation import gettext as _
from nanoid import generate

from apps.landmatrix.models import choices
from apps.landmatrix.models.deal import DealVersion
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
