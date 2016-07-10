from django.db import models
from django.utils.translation import ugettext_lazy as _

from grid.forms.choices import int_choice_to_string, negotiation_status_choices, implementation_status_choices
from landmatrix.models.default_string_representation import DefaultStringRepresentation
from landmatrix.models.activity import Activity

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


#class PublicInterfaceCache(DefaultStringRepresentation, models.Model):
#    fk_activity = models.ForeignKey("Activity", verbose_name=_("Activity"), db_index=True)
#    is_public = models.BooleanField(verbose_name=_('Is this a public deal?'), default=False, db_index=True)
#    deal_scope = models.CharField(
#        verbose_name=_('Deal scope'), max_length=16,
#        choices=(('domestic', 'domestic'), ('transnational', 'transnational')),
#        blank=True, null=True,
#        db_index=True
#    )
#    negotiation_status = models.CharField(
#        verbose_name=_('Negotiation status'), max_length=64, choices=int_choice_to_string(negotiation_status_choices),
#        blank=True, null=True, db_index=True
#    )
#    implementation_status = models.CharField(
#        verbose_name=_('Implementation status'), max_length=64,
#        choices=int_choice_to_string(implementation_status_choices), blank=True, null=True, db_index=True
#    )
#    deal_size = models.IntegerField(verbose_name=_('Deal size'), blank=True, null=True, db_index=True)
#
#    class Meta:
#        index_together = [
#            ['is_public', 'deal_scope'],
#            ['is_public', 'deal_scope', 'negotiation_status'],
#            ['is_public', 'deal_scope', 'implementation_status'],
#            ['is_public', 'deal_scope', 'negotiation_status', 'implementation_status'],
#        ]#