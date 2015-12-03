from django.db import models
from django.utils.translation import ugettext_lazy as _
from landmatrix.models.default_string_representation import DefaultStringRepresentation
from landmatrix.models.activity import Activity

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class PublicInterfaceCache(DefaultStringRepresentation, models.Model):
    fk_activity = models.ForeignKey("Activity", verbose_name=_("Activity"), db_index=True)
    is_deal = models.BooleanField(verbose_name=_('Is this a deal?'), default=False, db_index=True)
    deal_scope = models.CharField(
        verbose_name=_('Deal scope'), max_length=16,
        choices=(('domestic', 'domestic'), ('transnational', 'transnational')),
        blank=True, null=True,
        db_index=True
    )
    negotiation_status = models.CharField(
        verbose_name=_('Negotiation status'), max_length=64,
        choices=(
            ("Intended (Expression of interest)", "Intended (Expression of interest)"),
            ("Intended (Under negotiation)", "Intended (Under negotiation)"),
            ("Concluded (Oral Agreement)", "Concluded (Oral Agreement)"),
            ("Concluded (Contract signed)", "Concluded (Contract signed)"),
            ("Failed (Negotiations failed)", "Failed (Negotiations failed)"),
            ("Failed (Contract canceled)", "Failed (Contract canceled)"),
        ), blank=True, null=True,
        db_index=True)
    implementation_status = models.CharField(
        verbose_name=_('Implementation status'), max_length=64,
        choices=(
            ("Project not started", "Project not started"),
            ("Startup phase (no production)", "Startup phase (no production)"),
            ("In operation (production)", "In operation (production)"),
            ("Project abandoned", "Project abandoned"),
        ), blank=True, null=True,
        db_index=True)
    deal_size = models.IntegerField(verbose_name=_('Deal size'), blank=True, null=True, db_index=True)

    class Meta:
        index_together = [
            ['is_deal', 'deal_scope'],
            ['is_deal', 'deal_scope', 'negotiation_status'],
            ['is_deal', 'deal_scope', 'implementation_status'],
            ['is_deal', 'deal_scope', 'negotiation_status', 'implementation_status'],
        ]