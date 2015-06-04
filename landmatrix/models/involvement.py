__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from landmatrix.models.default_string_representation import DefaultStringRepresentation

class Involvement(DefaultStringRepresentation, models.Model):
    fk_activity = models.ForeignKey(
        "Activity", verbose_name=_("Activity"), blank=True, null=True
    )
    fk_stakeholder = models.ForeignKey(
        "Stakeholder", verbose_name=_("Stakeholder"), blank=True, null=True
    )
    fk_primary_investor = models.ForeignKey(
        "PrimaryInvestor", verbose_name=_("Is primary"), blank=True, null=True
    )
    investment_ratio = models.DecimalField(
        _("Investment ratio"), blank=True, null=True, max_digits=19, decimal_places=2
    )