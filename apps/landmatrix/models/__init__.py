from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.landmatrix.models.country import Country, Region
from .currency import Currency
from .investor import Investor, InvestorVersion, InvestorVentureInvolvement
from .deal import Deal, DealVersion


class Language(models.Model):
    english_name = models.CharField(_("English name"), max_length=255)
    local_name = models.CharField(_("Local name"), max_length=255)
    locale = models.CharField(_("Locale"), max_length=31)


class Status(models.Model):
    name = models.CharField(_("Name"), max_length=255, db_index=True)
    description = models.TextField(_("Description"), blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.name}"
