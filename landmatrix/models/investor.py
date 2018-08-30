from django.conf import settings
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from multiselectfield import MultiSelectField

from landmatrix.models.default_string_representation import \
    DefaultStringRepresentation


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
    PUBLIC_STATUSES = (STATUS_ACTIVE, STATUS_OVERWRITTEN)
    STATUS_CHOICES = (
        STATUS_PENDING, _('Pending'),
        STATUS_ACTIVE, _('Active'),
        STATUS_OVERWRITTEN, _('Overwritten'),
        STATUS_DELETED, _('Deleted'),
        STATUS_REJECTED, _('Rejected'),
        STATUS_TO_DELETE, _('To delete'),
    )
    INVESTOR_IDENTIFIER_DEFAULT = 2147483647  # max safe int
    STAKEHOLDER_CLASSIFICATIONS = (
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
        STAKEHOLDER_CLASSIFICATIONS + INVESTOR_CLASSIFICATIONS
    )
    PARENT_RELATION_CHOICES = (
        ('Subsidiary', _("Subsidiary of parent company")),
        ('Local branch', _("Local branch of parent company")),
        ('Joint venture', _("Joint venture of parent companies")),
    )

    investor_identifier = models.IntegerField(
        _("Investor ID"), db_index=True, default=INVESTOR_IDENTIFIER_DEFAULT)
    name = models.CharField(_("Name"), max_length=1024)
    fk_country = models.ForeignKey(
        "Country", verbose_name=_("Country of registration/origin"),
        blank=True, null=True)
    classification = models.CharField(verbose_name=_('Classification'),
        max_length=3, choices=CLASSIFICATION_CHOICES, blank=True, null=True)
    parent_relation = models.CharField(verbose_name=_('Parent relation'),
        max_length=255, choices=PARENT_RELATION_CHOICES, blank=True, null=True)
    homepage = models.URLField(_("Investor homepage"), blank=True, null=True)
    opencorporates_link = models.URLField(
        _("Opencorporates link"), blank=True, null=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))
    comment = models.TextField(_("Comment"), blank=True, null=True)

    objects = InvestorQuerySet.as_manager()

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self):
        return '%s (#%i)' % (self.name, self.investor_identifier)

    @classmethod
    def get_next_investor_identifier(cls):
        queryset = cls.objects#.using('v2')
        queryset = queryset.exclude(investor_identifier=cls.INVESTOR_IDENTIFIER_DEFAULT)
        queryset = queryset.aggregate(models.Max('investor_identifier'))
        return (queryset['investor_identifier__max'] or 0) + 1

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

        if self.investor_identifier is None:
            self.investor_identifier = self.INVESTOR_IDENTIFIER_DEFAULT

        super().save(*args, **kwargs)

        if self.investor_identifier == self.INVESTOR_IDENTIFIER_DEFAULT:
            self.investor_identifier = self.__class__.get_next_investor_identifier()
            update_fields.append('investor_identifier')

        if not self.name or self.name == 'Unknown (#{})'.format(self.pk):
            self.name = self._get_default_name()
            update_fields.append('name')

        if update_fields:
            super().save(update_fields=update_fields)

    def _get_default_name(self):
        '''
        If we have an unknown (blank) name, get the correct generic text.
        '''
        if self.is_operating_company:
            name = _("Unknown operating company (#%s)") % (self.pk,)
        elif self.is_parent_company:
            name = _("Unknown parent company (#%s)") % (self.pk,)
        elif self.is_parent_investor:
            name = _("Unknown tertiary investor/lender (#%s)") % (self.pk,)
        else:
            # Just stick with unknown if no relations
            name = _("Unknown (#%s)") % (self.pk,)

        return name

    def get_history(self, user=None):
        """
        Returns all deal versions
        """
        queryset = HistoricalInvestor.objects.filter(investor_identifier=self.investor_identifier)
        if not (user and user.is_authenticated()):
            queryset = queryset.filter(fk_status__in=(HistoricalInvestor.STATUS_ACTIVE,
                                                      HistoricalInvestor.STATUS_OVERWRITTEN))
        return queryset.order_by('-history_date')

    @property
    def is_deleted(self):
        return self.fk_status_id == self.STATUS_DELETED

    @property
    def is_operating_company(self):
        '''
        Moved this logic from the view. Not sure though if we should
        determine this using classification in future.
        '''
        return (
            hasattr(self, 'involvements') and
            self.involvements.exists())

    @property
    def is_parent_company(self):
        '''
        Right now, this is determined based on if any relations exist.
        It probably makes more sense to have this as a flag on the model.
        '''
        if hasattr(self, 'venture_involvements'):
            queryset = self.venture_involvements.all()
            queryset = queryset.filter(
                role=InvestorVentureInvolvement.STAKEHOLDER_ROLE)
            return queryset.exists()
        else:
            return False

    @property
    def is_parent_investor(self):
        if hasattr(self, 'venture_involvements'):
            queryset = self.venture_involvements.all()
            queryset = queryset.filter(
                role=InvestorVentureInvolvement.INVESTOR_ROLE)
            return queryset.exists()
        else:
            return False

    @classmethod
    def get_latest_investor(cls, investor_identifier):
        return cls.objects.filter(investor_identifier=investor_identifier).order_by('-id').first()

    @classmethod
    def get_latest_active_investor(cls, investor_identifier):
        return cls.objects.filter(investor_identifier=investor_identifier).\
            filter(fk_status__name__in=("active", "overwritten", "deleted")).order_by('-id').first()

    def approve(self):
        if self.fk_status_id != HistoricalInvestor.STATUS_PENDING:
            return
        self.update_public_investor()

    def reject(self):
        if self.fk_status_id != HistoricalInvestor.STATUS_PENDING:
            return
        self.fk_status_id = HistoricalInvestor.STATUS_REJECTED
        self.save(update_fields=['fk_status'])

    def get_top_investors(self):
        """
        Get list of highest parent companies (all right-hand side parent companies of the network
        visualisation)
        """
        def get_parent_companies(investors):
            parents = []
            for investor in investors:
                # Check if there are parent companies for investor
                parent_companies = [ivi.fk_investor for ivi in InvestorVentureInvolvement.objects.filter(
                    fk_venture=investor,
                    fk_venture__fk_status__in=(InvestorBase.STATUS_ACTIVE, InvestorBase.STATUS_OVERWRITTEN),
                    fk_investor__fk_status__in=(InvestorBase.STATUS_ACTIVE, InvestorBase.STATUS_OVERWRITTEN),
                    role=InvestorVentureInvolvement.STAKEHOLDER_ROLE).exclude(fk_investor=investor)]
                if parent_companies:
                    parents.extend(get_parent_companies(parent_companies))
                elif investor.fk_status_id in (InvestorBase.STATUS_ACTIVE, InvestorBase.STATUS_OVERWRITTEN):
                    parents.append(investor)
            return parents
        top_investors = list(set(get_parent_companies([self,])))
        return top_investors

    def format_investors(self, investors):
        return '|'.join(['#'.join([str(i.investor_identifier), i.name.replace('#', '').replace("\n", '')])
                         for i in investors])


class Investor(InvestorBase):
    subinvestors = models.ManyToManyField(
        "self", through='InvestorVentureInvolvement', symmetrical=False,
        through_fields=('fk_venture', 'fk_investor'))

    class Meta:
        ordering = ('name',)
        verbose_name = _("Investor")
        verbose_name_plural = _("Investors")


class HistoricalActivityQuerySet(InvestorQuerySet):

    def latest_only(self):
        queryset = HistoricalInvestor.objects.values('investor_identifier').annotate(
            max_id=models.Max('id'),
        ).values_list('max_id', flat=True)
        return queryset


class HistoricalInvestor(InvestorBase):
    history_date = models.DateTimeField(default=timezone.now)
    history_user = models.ForeignKey('auth.User', blank=True, null=True)

    objects = HistoricalActivityQuerySet.as_manager()

    def get_top_investors(self):
        """
        Get list of highest parent companies (all right-hand side parent companies of the network
        visualisation)
        """
        def get_parent_companies(investors):
            parents = []
            for investor in investors:
                # Check if there are parent companies for investor
                parent_companies = [ivi.fk_investor for ivi in
                                    HistoricalInvestorVentureInvolvement.objects.filter(
                    fk_venture=investor,
                    fk_venture__fk_status__in=(InvestorBase.STATUS_ACTIVE, InvestorBase.STATUS_OVERWRITTEN),
                    fk_investor__fk_status__in=(InvestorBase.STATUS_ACTIVE, InvestorBase.STATUS_OVERWRITTEN),
                    role=HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE).exclude(fk_investor=investor)]
                if parent_companies:
                    parents.extend(get_parent_companies(parent_companies))
                elif investor.fk_status_id in (InvestorBase.STATUS_ACTIVE, InvestorBase.STATUS_OVERWRITTEN):
                    parents.append(investor)
            return parents
        top_investors = list(set(get_parent_companies([self,])))
        return top_investors

    def update_public_investor(self, approve=True):
        """Recursively update investor chain"""
        # Keep track of investor identifiers to prevent infinite loops
        investor_identifiers = []
        def update_investor(hinv, approve=True):
            if approve:
                # Update status of historical investor
                if hinv.fk_status_id == hinv.STATUS_PENDING:
                    hinv.fk_status_id = hinv.STATUS_OVERWRITTEN
                elif hinv.fk_status_id == hinv.STATUS_TO_DELETE:
                    hinv.fk_status_id = hinv.STATUS_DELETED
                hinv.save()

            # Update public investor (leaving involvements)
            investor = Investor.objects.filter(investor_identifier=hinv.investor_identifier)
            if investor.count() > 0:
                investor = investor[0]
            else:
                investor = Investor(investor_identifier=hinv.investor_identifier)
            if investor.investor_identifier in investor_identifiers:
                return investor
            else:
                investor_identifiers.append(investor.investor_identifier)
            #investor.id = hinv.id
            investor.investor_identifier = hinv.investor_identifier
            investor.name = hinv.name
            investor.fk_country_id = hinv.fk_country_id
            investor.classification = hinv.classification
            investor.parent_relation = hinv.parent_relation
            investor.homepage = hinv.homepage
            investor.opencorporates_link = hinv.opencorporates_link
            investor.fk_status_id = hinv.fk_status_id
            investor.comment = hinv.comment
            investor.save()

            # Recreate involvements
            investor.venture_involvements.all().delete()
            for hinvolvement in hinv.venture_involvements.all():
                # Update InvestorVentureInvolvement
                hinvolvement.fk_status_id = hinv.STATUS_OVERWRITTEN
                hinvolvement.save()
                subinvestor = Investor.objects.filter(
                    investor_identifier=hinvolvement.fk_investor.investor_identifier)[0]
                # Replace InvestorVentureInvolvement
                investor.venture_involvements.create(
                    fk_investor=subinvestor,
                    role=hinvolvement.role,
                    investment_type=hinvolvement.investment_type,
                    percentage=hinvolvement.percentage,
                    loans_amount=hinvolvement.loans_amount,
                    loans_currency=hinvolvement.loans_currency,
                    loans_date=hinvolvement.loans_date,
                    comment=hinvolvement.comment,
                    fk_status=hinvolvement.fk_status
                )
                # Update investor
                update_investor(hinvolvement.fk_investor, approve=approve)

            return investor

        investor = update_investor(self, approve=approve)
        self.update_current_involvements(investor)
        return investor

    def update_current_involvements(self, investor):
        # Update all current involvements (linking to the old investor version) to the new investor version
        queryset = HistoricalInvestorActivityInvolvement.objects.for_current_activities()
        queryset = queryset.filter(fk_investor__investor_identifier=self.investor_identifier)
        queryset = queryset.exclude(fk_investor_id=self.id)
        for involvement in queryset:
            involvement.fk_investor_id = self.id
            involvement.save()

        queryset = InvestorActivityInvolvement.objects.all()
        queryset = queryset.filter(fk_investor__investor_identifier=self.investor_identifier)
        queryset = queryset.exclude(fk_investor_id=investor.id)
        for involvement in queryset:
            involvement.fk_investor_id = investor.id
            involvement.save()

    def save(self, *args, **kwargs):
        update_elasticsearch = kwargs.pop('update_elasticsearch', True)
        super().save(*args, **kwargs)
        if update_elasticsearch and not settings.CONVERT_DB:
            from ..tasks import index_investor, delete_investor
            if self.fk_status_id == self.STATUS_DELETED:
                transaction.on_commit(lambda: delete_investor.delay(self.investor_identifier))
            else:
                transaction.on_commit(lambda: index_investor.delay(self.id))

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


class InvestorVentureInvolvementBase(models.Model):
    '''
    InvestorVentureInvolvement links investors to each other.
    Generally fk_venture links to the Operating company, and fk_investor
    links to investors or parent stakeholders in that company (depending
    on the role).
    '''
    # FIXME: Replace fk_status with Choice Field
    STATUS_PENDING = 1
    STATUS_ACTIVE = 2
    STATUS_OVERWRITTEN = 3
    STATUS_DELETED = 4
    STATUS_REJECTED = 5
    STATUS_TO_DELETE = 6
    PUBLIC_STATUSES = (STATUS_ACTIVE, STATUS_OVERWRITTEN)
    STATUS_CHOICES = (
        STATUS_PENDING, _('Pending'),
        STATUS_ACTIVE, _('Active'),
        STATUS_OVERWRITTEN, _('Overwritten'),
        STATUS_DELETED, _('Deleted'),
        STATUS_REJECTED, _('Rejected'),
        STATUS_TO_DELETE, _('To delete'),
    )
    STAKEHOLDER_ROLE = 'ST'
    INVESTOR_ROLE = 'IN'
    ROLE_CHOICES = (
        (STAKEHOLDER_ROLE, _('Parent company')),
        (INVESTOR_ROLE, _('Tertiary investor/lendor')),
    )
    EQUITY_INVESTMENT_TYPE = 10
    DEBT_FINANCING_INVESTMENT_TYPE = 20
    INVESTMENT_TYPE_CHOICES = (
        (EQUITY_INVESTMENT_TYPE, _('Shares/Equity')),
        (DEBT_FINANCING_INVESTMENT_TYPE, _('Debt financing')),
    )

    role = models.CharField(verbose_name=_("Relation type"), max_length=2, choices=ROLE_CHOICES)
    investment_type = MultiSelectField(
        max_length=255, choices=INVESTMENT_TYPE_CHOICES,
        default='', blank=True, null=True)
    percentage = models.FloatField(
        _('Ownership share'), blank=True, null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    loans_amount = models.FloatField(_("Loan amount"), blank=True, null=True)
    loans_currency = models.ForeignKey(
        "Currency", verbose_name=_("Loan currency"), blank=True, null=True)
    loans_date = models.CharField("Loan date", max_length=10, blank=True, null=True)
    comment = models.TextField(_("Comment"), blank=True, null=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"), default=1)

    objects = InvestorVentureQuerySet.as_manager()

    class Meta:
        abstract = True


class InvestorVentureInvolvement(InvestorVentureInvolvementBase):
    # FIXME: related names are named the wrong way here
    fk_venture = models.ForeignKey(Investor, verbose_name=_('Investor ID Downstream'), db_index=True,
                                   related_name='venture_involvements')
    fk_investor = models.ForeignKey(Investor, verbose_name=_('Investor ID Upstream'), db_index=True,
                                    related_name='investors')

    class Meta:
        verbose_name = _('Investor Venture Involvement')
        verbose_name_plural = _('Investor Venture Involvements')
        ordering = ('-id',)


class HistoricalInvestorVentureInvolvement(InvestorVentureInvolvementBase):
    # FIXME: related names are named the wrong way here
    fk_venture = models.ForeignKey(HistoricalInvestor, verbose_name=_('Investor ID Downstream'),
                                   db_index=True, related_name='venture_involvements')
    fk_investor = models.ForeignKey(HistoricalInvestor, verbose_name=_('Investor ID Upstream'),
                                    db_index=True, related_name='investors')

    class Meta:
        verbose_name = _('Historical Investor Venture Involvement')
        verbose_name_plural = _('Historical Investor Venture Involvements')
        get_latest_by = '-id'


class InvestorActivityInvolvementManager(models.Manager):
    def get_involvements_for_activity(self, activity_identifier):
        return InvestorActivityInvolvement.objects.filter(fk_activity__activity_identifier=activity_identifier).\
            filter(fk_investor__fk_status_id__in=(Investor.STATUS_ACTIVE, Investor.STATUS_OVERWRITTEN))

    def for_current_activities(self):
        """
        Get involvements for newest versions of activities
        :return:
        """
        activity_class = self.model._meta.get_field('fk_activity').rel.model
        current_activities = activity_class.objects.latest_only()
        return self.filter(fk_activity_id__in=current_activities)


class InvestorActivityInvolvementBase(models.Model):
    '''
    InvestorActivityInvolvments link Operational Companies (Investor model)
    to activities.

    There should only be one Operating company per activity,
    although this is not enforced by the model currently. Other investors
    are then linked to the Operating company through
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

    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))

    objects = InvestorActivityInvolvementManager()

    def __str__(self):
        return "Activity: %i Investor: %i" % (
            self.fk_activity_id,
            self.fk_investor_id,
        )

    class Meta:
        abstract = True


class InvestorActivityInvolvement(InvestorActivityInvolvementBase):
    fk_activity = models.ForeignKey("Activity", verbose_name=_("Activity"),
                                    related_name='involvements', db_index=True)
    fk_investor = models.ForeignKey("Investor", verbose_name=_("Investor"),
                                    related_name='involvements', db_index=True)

    class Meta:
        verbose_name = _('Investor Activity Involvement')
        verbose_name_plural = _('Investor Activity Involvements')
        ordering = ('-id',)


class HistoricalInvestorActivityInvolvement(InvestorActivityInvolvementBase):
    fk_activity = models.ForeignKey("HistoricalActivity", verbose_name=_("Activity"),
                                    related_name='involvements', db_index=True)
    fk_investor = models.ForeignKey("HistoricalInvestor", verbose_name=_("Investor"),
                                    related_name='involvements', db_index=True)

    class Meta:
        verbose_name = _('Historical Investor Activity Involvement')
        verbose_name_plural = _('Historical Investor Activity Involvements')
        ordering = ['-id']
