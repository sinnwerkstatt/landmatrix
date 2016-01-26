from landmatrix.models.default_string_representation import DefaultStringRepresentation
from landmatrix.models.activity import Activity
from landmatrix.models.country import Country
from landmatrix.models.status import Status

from simple_history.models import HistoricalRecords

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class Investor(DefaultStringRepresentation, models.Model):

    classification_choices = (
        ('10', _("Private company")),
        ('20', _("Stock-exchange listed company")),
        ('30', _("Individual entrepreneur")),
        ('40', _("Investment fund")),
        ('50', _("Semi state-owned company")),
        ('60', _("State-/government(owned)")),
        ('70', _("Other (please specify in comment field)"))
    )
    investor_identifier = models.IntegerField(_("Investor id"), db_index=True)
    name = models.CharField(_("Name"), max_length=1024)
    fk_country = models.ForeignKey("Country", verbose_name=_("Country"), blank=True, null=True)
    classification = models.CharField(max_length=2, choices=classification_choices, blank=True, null=True)
    comment = models.TextField(_("Comment"), blank=True, null=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

#    version = models.IntegerField(_("Version"), db_index=True)
    history = HistoricalRecords()


class InvestorVentureInvolvement(models.Model):
    fk_venture = models.ForeignKey("Investor", db_index=True, related_name='+')
    fk_investor = models.ForeignKey("Investor", db_index=True, related_name='+')
    percentage = models.FloatField(
        _('Percentage'), blank=True, null=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    role = models.CharField(max_length=2, choices=(('ST', _('Stakeholder')), ('IN', _('Investor'))))
    comment = models.TextField(_("Comment"), blank=True, null=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    def __str__(self):
        return 'venture: %i stakeholder: %i percentage: %5.2f role: %s timestamp: %s' % \
               (self.fk_venture_id, self.fk_investor_id, self.percentage, self.role, self.timestamp)


class InvestorActivityInvolvement(models.Model):
    fk_activity = models.ForeignKey("Activity", verbose_name=_("Activity"), db_index=True)
    fk_investor = models.ForeignKey("Investor", verbose_name=_("Investor"), db_index=True)
    percentage = models.FloatField(
        _('Percentage'), blank=True, null=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    # investor can only be an Operational Stakeholder in an activity
    comment = models.TextField(_("Comment"), blank=True, null=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
