from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from landmatrix.models.default_string_representation import \
    DefaultStringRepresentation
from simple_history.models import HistoricalRecords


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class Investor(DefaultStringRepresentation, models.Model):

    investor_identifier_default = 2147483647  # max safe int
    classification_choices = (
        # for operating company
        ('10', _("Private company")),
        ('20', _("Stock-exchange listed company")),
        ('30', _("Individual entrepreneur")),
        ('40', _("Investment fund")),
        ('50', _("Semi state-owned company")),
        ('60', _("State-/government(owned) company")),
        ('70', _("Other (please specify in comment field)")),
        # for parent companies
        ('110', _("Government")),
        ('120', _("Government institution")),
        ('130', _("Multilateral Development Bank(MDB)")),
        ('140', _("Bilateral Development Bank / Development Finance Institution")),
        ('150', _("Commercial Bank")),
        ('160', _("Investment Bank")),
        ('170', _(
            "Investment Fund(all types incl.pension, hedge, mutual, private equity funds etc.)"
        )),
        ('180', _("Insurance firm")),
        ('190', _("Private equity firm")),
        ('200', _("Asset management firm")),
        ('210', _("Non - Profit organization(e.g.Church, University etc.)")),
    )

    investor_identifier = models.IntegerField(
        _("Investor id"), db_index=True, default=investor_identifier_default,
    )
    name = models.CharField(
        _("Name"), max_length=1024
    )
    fk_country = models.ForeignKey(
        "Country", verbose_name=_("Country of registration/origin"), blank=True, null=True
    )
    classification = models.CharField(
        max_length=3, choices=classification_choices, blank=True, null=True
    )
    homepage = models.URLField(
        _("Investor homepage"), blank=True, null=True
    )
    opencorporates_link = models.URLField(
        _("Opencorporates link"), blank=True, null=True
    )

    comment = models.TextField(_("Comment"), blank=True, null=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name

    def get_subinvestors(self):
        investor_ids = InvestorVentureInvolvement.objects.filter(fk_venture=self.id).\
            values_list('fk_investor_id', flat=True).distinct()
        return Investor.objects.filter(pk__in=investor_ids)

    def save(self, *args, **kwargs):
        '''
        investor_identifier needs to be set to the PK, which we don't yet have
        for new records. So, set it to a default and then update.

        This is not super efficient (updateing an index column twice)
        and may result in duplicate investor_identifiers due to crash or
        query timing, but it should be good enough for our purposes.

        Same thing goes for the name.
        '''
        update_fields = []
        super().save(*args, **kwargs)

        if self.investor_identifier == self.investor_identifier_default:
            self.investor_identifier = self.pk
            update_fields.append('investor_identifier')

        if not self.name:
            self.name = _("Unknown (#%s)") % (self.pk,)
            update_fields.append('name')

        if update_fields:
            super().save(update_fields=update_fields)


    @property
    def venture_involvements(self):
        # TODO: not sure why this isn't a related name?
        return InvestorVentureInvolvement.objects.filter(fk_venture=self)


class InvestorVentureQuerySet(models.QuerySet):
    ACTIVE_STATUS_NAMES = ('pending', 'active', 'overwritten')

    def active(self):
        return self.filter(fk_status__name__in=self.ACTIVE_STATUS_NAMES)

    def stakeholders(self):
        return self.filter(role=InvestorVentureInvolvement.STAKEHOLDER_ROLE)

    def investors(self):
        return self.filter(role=InvestorVentureInvolvement.INVESTOR_ROLE)


class InvestorVentureInvolvement(models.Model):
    STAKEHOLDER_ROLE = 'ST'
    INVESTOR_ROLE = 'IN'
    ROLE_CHOICES = (
        (STAKEHOLDER_ROLE, _('Stakeholder')),
        (INVESTOR_ROLE, _('Investor')),
    )

    fk_venture = models.ForeignKey("Investor", db_index=True, related_name='+')
    fk_investor = models.ForeignKey("Investor", db_index=True, related_name='+',
                                    limit_choices_to={'fk_status_id__in': (2, 3)})
    percentage = models.FloatField(
        _('Ownership share'), blank=True, null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    investment_type = models.CharField(
        max_length=2, choices=(('10', 'Shares/Equity'), ('20', 'Debt financing')),
        blank=True, null=True
    )
    loans_amount = models.FloatField(
        _("Loan amount"), blank=True, null=True
    )
    loans_currency = models.ForeignKey(
        "Currency", verbose_name=_("Loan curency"), blank=True, null=True
    )
    lonas_date = models.DateField(
        "Loan date", blank=True, null=True
    )
    comment = models.TextField(_("Comment"), blank=True, null=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    objects = InvestorVentureQuerySet.as_manager()

    def __str__(self):
        return 'venture: %i stakeholder: %i percentage: %s role: %s timestamp: %s' % \
               (self.fk_venture_id, self.fk_investor_id, self.percentage, self.role, self.timestamp)


class InvestorActivityInvolvement(models.Model):

    class IAIManager(models.Manager):

        def get_involvements_for_activity(self, activity):
            def original_sql():
                return """
SELECT i.*
FROM primary_investors pi
JOIN status pi_st ON pi.fk_status = pi_st.id
JOIN involvements i ON i.fk_primary_investor = pi.id
LEFT OUTER JOIN stakeholders s ON i.fk_stakeholder = s.id
WHERE
  i.fk_activity = %i
  AND (
    s.version IS NULL
    OR s.version = (
      SELECT MAX(version)
      FROM stakeholders smax
      JOIN status st ON smax.fk_status = st.id
      WHERE smax.stakeholder_identifier = s.stakeholder_identifier AND st.name IN ("active", "overwritten")
      GROUP BY smax.stakeholder_identifier
    )
  )
  AND pi.version = (
    SELECT max(version)
    FROM primary_investors pimax
    JOIN status st ON pimax.fk_status = st.id
    WHERE pimax.primary_investor_identifier = pi.primary_investor_identifier AND st.name IN ("active", "overwritten", "deleted")
  )
  AND pi_st.name IN ("active", "overwritten")
""" % activity.id

            print('InvestorActivityInvolvement.Manager.get_involvements_for_activity() TODO: fix (learn from history)!')
            return InvestorActivityInvolvement.objects.filter(fk_activity=activity).\
                filter(fk_investor__fk_status__name__in=("active", "overwritten"))

    fk_activity = models.ForeignKey("Activity", verbose_name=_("Activity"), db_index=True)
    fk_investor = models.ForeignKey("Investor", verbose_name=_("Investor"), db_index=True)
    percentage = models.FloatField(
        _('Percentage'), blank=True, null=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    # investor can only be an Operational Stakeholder in an activity
    comment = models.TextField(_("Comment"), blank=True, null=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    objects = IAIManager()

    def __str__(self):
        return "Activity: %i Investor: %i Percentage: %s comment: '%s'" % (
            self.fk_activity_id, self.fk_investor_id, str(self.percentage), str(self.comment)[:40]
        )
