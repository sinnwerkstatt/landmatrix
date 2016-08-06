from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from landmatrix.models.default_string_representation import \
    DefaultStringRepresentation


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class InvestorQuerySet(models.QuerySet):

    def public(self):
        return self.filter(fk_status_id__in=(InvestorBase.STATUS_ACTIVE, InvestorBase.STATUS_OVERWRITTEN))

    def public_or_deleted(self):
        return self.filter(fk_status_id__in=(InvestorBase.STATUS_ACTIVE, InvestorBase.STATUS_OVERWRITTEN, InvestorBase.STATUS_DELETED))

    def pending(self):
        return self.filter(fk_status_id__in=(InvestorBase.STATUS_PENDING, InvestorBase.STATUS_TO_DELETE))

    def existing_operational_stakeholders(self):
        # TODO: not sure we should be filtering on this instead of
        # something else
        stakeholder_ids = InvestorActivityInvolvement.objects.values(
            'fk_investor_id').distinct()
        return self.filter(pk__in=stakeholder_ids)


class InvestorBase(DefaultStringRepresentation, models.Model):
    # FIXME: Replace fk_status with Choice Field
    STATUS_PENDING = 1
    STATUS_ACTIVE = 2
    STATUS_OVERWRITTEN = 3
    STATUS_DELETED = 4
    STATUS_REJECTED = 5
    STATUS_TO_DELETE = 6
    STATUS_CHOICES = (
        STATUS_PENDING, _('Pending'),
        STATUS_ACTIVE, _('Active'),
        STATUS_OVERWRITTEN, _('Overwritten'),
        STATUS_DELETED, _('Deleted'),
        STATUS_REJECTED, _('Rejected'),
        STATUS_TO_DELETE, _('To delete'),
    )
    INVESTOR_IDENTIFIER_DEFAULT = 2147483647  # max safe int
    OPERATIONAL_COMPANY_CLASSIFICATIONS = (
        ('10', _("Private company")),
        ('20', _("Stock-exchange listed company")),
        ('30', _("Individual entrepreneur")),
        ('40', _("Investment fund")),
        ('50', _("Semi state-owned company")),
        ('60', _("State-/government (owned) company")),
        ('70', _("Other (please specify in comment field)")),
    )
    INVESTOR_CLASSIFICATIONS = (
        ('110', _("Government")),
        ('120', _("Government institution")),
        ('130', _("Multilateral Development Bank (MDB)")),
        ('140', _("Bilateral Development Bank / Development Finance Institution")),
        ('150', _("Commercial Bank")),
        ('160', _("Investment Bank")),
        ('170', _("Investment Fund (all types incl. pension, hedge, mutual, private equity funds etc.)")),
        ('180', _("Insurance firm")),
        ('190', _("Private equity firm")),
        ('200', _("Asset management firm")),
        ('210', _("Non - Profit organization (e.g. Church, University etc.)")),
    )
    CLASSIFICATION_CHOICES = (
        OPERATIONAL_COMPANY_CLASSIFICATIONS + INVESTOR_CLASSIFICATIONS
    )
    PARENT_RELATION_CHOICES = (
        ('Subsidiary', _("Subsidiary of parent company")),
        ('Local branch', _("Local branch of parent company")),
        ('Joint venture', _("Joint venture of parent companies")),
    )

    investor_identifier = models.IntegerField(
        _("Investor id"), db_index=True, default=INVESTOR_IDENTIFIER_DEFAULT)
    name = models.CharField(_("Name"), max_length=1024)
    fk_country = models.ForeignKey(
        "Country", verbose_name=_("Country of registration/origin"),
        blank=True, null=True)
    classification = models.CharField(
        max_length=3, choices=CLASSIFICATION_CHOICES, blank=True, null=True)
    parent_relation = models.CharField(
        max_length=255, choices=PARENT_RELATION_CHOICES, blank=True, null=True)
    homepage = models.URLField(_("Investor homepage"), blank=True, null=True)
    opencorporates_link = models.URLField(
        _("Opencorporates link"), blank=True, null=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    comment = models.TextField(_("Comment"), blank=True, null=True)

    objects = InvestorQuerySet.as_manager()

    class Meta:
        ordering = ('-name',)
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''
        investor_identifier needs to be set to the PK, which we don't yet have
        for new records. So, set it to a default and then update.

        This is not super efficient (updating an index column twice)
        and may result in duplicate investor_identifiers due to crash or
        query timing, but it should be good enough for our purposes.

        Same thing goes for the name.
        '''
        update_fields = []
        super().save(*args, **kwargs)

        if self.investor_identifier == self.INVESTOR_IDENTIFIER_DEFAULT:
            self.investor_identifier = self.pk
            update_fields.append('investor_identifier')

        if not self.name:
            self.name = _("Unknown (#%s)") % (self.pk,)
            update_fields.append('name')

        if update_fields:
            super().save(update_fields=update_fields)

    @property
    def history(self):
        return HistoricalInvestor.objects.filter(
            investor_identifier=self.investor_identifier)

    @property
    def is_deleted(self):
        return self.fk_status_id == self.STATUS_DELETED

    @property
    def is_operational_company(self):
        '''
        Moved this logic from the view. Not sure though if we should
        determine this using classification in future.
        '''
        return (
            hasattr(self, 'investoractivityinvolvement_set') and
            self.investoractivityinvolvement_set.exists())

    @classmethod
    def get_latest_investor(cls, investor_identifier):
        return cls.objects.filter(investor_identifier=investor_identifier).order_by('-id').first()

    @classmethod
    def get_latest_active_investor(cls, investor_identifier):
        return cls.objects.filter(investor_identifier=investor_identifier).\
            filter(fk_status__name__in=("active", "overwritten", "deleted")).order_by('-id').first()


class Investor(InvestorBase):
    subinvestors = models.ManyToManyField(
        "self", through='InvestorVentureInvolvement', symmetrical=False,
        through_fields=('fk_venture', 'fk_investor'))

    class Meta:
        verbose_name = _("Investor")
        verbose_name_plural = _("Investors")


class HistoricalInvestor(InvestorBase):
    history_date = models.DateTimeField(auto_now_add=True)
    history_user = models.ForeignKey('auth.User', blank=True, null=True)

    class Meta:
        verbose_name = _("Historical investor")
        verbose_name_plural = _("Historical investors")
        get_latest_by = 'history_date'
        ordering = ['-history_date']


class InvestorVentureQuerySet(models.QuerySet):
    ACTIVE_STATUS_NAMES = ('pending', 'active', 'overwritten')

    def active(self):
        return self.filter(fk_status__name__in=self.ACTIVE_STATUS_NAMES)

    def stakeholders(self):
        return self.filter(role=InvestorVentureInvolvement.STAKEHOLDER_ROLE)

    def investors(self):
        return self.filter(role=InvestorVentureInvolvement.INVESTOR_ROLE)


class InvestorVentureInvolvement(models.Model):
    '''
    InvestorVentureInvolvement links investors to each other.
    Generally fk_venture links to the Operational Company, and fk_investor
    links to investors or parent stakeholders in that company (depending
    on the role).
    '''
    STAKEHOLDER_ROLE = 'ST'
    INVESTOR_ROLE = 'IN'
    ROLE_CHOICES = (
        (STAKEHOLDER_ROLE, _('Stakeholder')),
        (INVESTOR_ROLE, _('Investor')),
    )
    EQUITY_INVESTMENT_TYPE = '10'
    DEBT_FINANCING_INVESTMENT_TYPE = '20'
    INVESTMENT_TYPE_CHOICES = (
        (EQUITY_INVESTMENT_TYPE, _('Shares/Equity')),
        (DEBT_FINANCING_INVESTMENT_TYPE, _('Debt financing')),
    )

    fk_venture = models.ForeignKey(Investor, db_index=True,
                                   related_name='venture_involvements')
    fk_investor = models.ForeignKey(Investor, db_index=True, related_name='+')
    percentage = models.FloatField(
        _('Ownership share'), blank=True, null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    investment_type = models.CharField(
        max_length=2, choices=INVESTMENT_TYPE_CHOICES, blank=True, null=True)
    loans_amount = models.FloatField(_("Loan amount"), blank=True, null=True)
    loans_currency = models.ForeignKey(
        "Currency", verbose_name=_("Loan currency"), blank=True, null=True)
    loans_date = models.DateField("Loan date", blank=True, null=True)
    comment = models.TextField(_("Comment"), blank=True, null=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    objects = InvestorVentureQuerySet.as_manager()

    class Meta:
        ordering = ('-timestamp',)
        get_latest_by = 'timestamp'
        verbose_name = _('Investor Venture Involvement')
        verbose_name_plural = _('Investor Venture Involvements')


class InvestorActivityInvolvementManager(models.Manager):
    def get_involvements_for_activity(self, activity_identifier):
        return InvestorActivityInvolvement.objects.filter(fk_activity__activity_identifier=activity_identifier).\
            filter(fk_investor__fk_status_id__in=(Investor.STATUS_ACTIVE, Investor.STATUS_OVERWRITTEN))


class InvestorActivityInvolvement(models.Model):
    '''
    InvestorActivityInvolvments link Operational Companies (Investor model)
    to activities.

    There should only be one Operational Company per activity,
    although this is not enforced by the model currently. Other investors
    are then linked to the Operational Company through
    InvestorVentureInvolvement.
    '''
    # FIXME: Replace fk_status with Choice Field
    STATUS_PENDING = 1
    STATUS_ACTIVE = 2
    STATUS_OVERWRITTEN = 3
    STATUS_DELETED = 4
    STATUS_REJECTED = 5
    STATUS_TO_DELETE = 6
    STATUS_CHOICES = (
        STATUS_PENDING, _('Pending'),
        STATUS_ACTIVE, _('Active'),
        STATUS_OVERWRITTEN, _('Overwritten'),
        STATUS_DELETED, _('Deleted'),
        STATUS_REJECTED, _('Rejected'),
        STATUS_TO_DELETE, _('To delete'),
    )

    fk_activity = models.ForeignKey(
        "Activity", verbose_name=_("Activity"), db_index=True)
    fk_investor = models.ForeignKey(
        "Investor", verbose_name=_("Investor"), db_index=True)
    #percentage = models.FloatField(
    #    _('Percentage'), blank=True, null=True,
    #    validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    # investor can only be an Operational Stakeholder in an activity
    #comment = models.TextField(_("Comment"), blank=True, null=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    objects = InvestorActivityInvolvementManager()

    def __str__(self):
        return "Activity: %i Investor: %i" % (
            self.fk_activity_id,
            self.fk_investor_id,
        )

    class Meta:
        ordering = ('-timestamp',)
        get_latest_by = 'timestamp'
        verbose_name = _('Investor Activity Involvement')
        verbose_name_plural = _('Investor Activity Involvements')


def update_public_investor():
    # Newer public version of investor available?
    hinvestor = HistoricalInvestor.objects.public_or_deleted().latest()
    investor = Investor.objects.get(investor_identifier=hinvestor.investor_identifier)
    if hinvestor.id != investor.id:
        # Update investor (maintaining subinvestors)
        investor.id = hinvestor.id
        investor.investor_identifier = hinvestor.investor_identifier
        investor.name = hinvestor.name
        investor.fk_country_id = hinvestor.fk_country_id
        investor.classification = hinvestor.classification
        investor.parent_relation = hinvestor.parent_relation
        investor.homepage = hinvestor.homepage
        investor.opencorporates_link = hinvestor.opencorporates_link
        investor.fk_status_id = hinvestor.fk_status_id
        investor.timestamp = hinvestor.timestamp
        investor.comment = hinvestor.comment
        investor.save()

