import re

from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.functions import Coalesce
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from landmatrix.models.default_string_representation import DefaultStringRepresentation
from landmatrix.models.status import Status
from landmatrix.models.activity_attribute_group import ActivityAttribute, HistoricalActivityAttribute
from landmatrix.models.investor import Investor, InvestorActivityInvolvement, InvestorVentureInvolvement
from landmatrix.models.country import Country

class ActivityQuerySet(models.QuerySet):
    def public(self):
        return self.filter(fk_status_id__in=(ActivityBase.STATUS_ACTIVE, ActivityBase.STATUS_OVERWRITTEN))

    def public_or_deleted(self):
        return self.filter(fk_status_id__in=(ActivityBase.STATUS_ACTIVE, ActivityBase.STATUS_OVERWRITTEN, ActivityBase.STATUS_DELETED))

    def public_or_pending(self):
        return self.filter(fk_status_id__in=(ActivityBase.STATUS_ACTIVE, ActivityBase.STATUS_OVERWRITTEN, ActivityBase.STATUS_PENDING, ActivityBase.STATUS_TO_DELETE))

    def pending(self):
        return self.filter(fk_status_id__in=(ActivityBase.STATUS_PENDING, ActivityBase.STATUS_TO_DELETE))


class NegotiationStatusManager(models.Manager):
    '''
    Manager for Negotiation status grouped query. (used by API call)
    '''

    def get_queryset(self):
        deals_count = Coalesce(
            models.Count('activity_identifier'), models.Value(0))
        hectares_sum = Coalesce(models.Sum('deal_size'), models.Value(0))

        queryset = ActivityQuerySet(self.model, using=self._db)
        queryset = queryset.exclude(negotiation_status__isnull=True)
        queryset = queryset.values('negotiation_status')
        queryset = queryset.annotate(
            deals_count=deals_count, hectares_sum=hectares_sum)
        queryset = queryset.distinct()

        return queryset


class ActivityBase(DefaultStringRepresentation, models.Model):
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

    activity_identifier = models.IntegerField(_("Activity identifier"), db_index=True)
    availability = models.FloatField(_("availability"), blank=True, null=True)
    fully_updated = models.BooleanField(_("Fully updated"), default=False)#, auto_now_add=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"), default=1)

    objects = ActivityQuerySet.as_manager()
    negotiation_status_objects = NegotiationStatusManager()

    class Meta:
        abstract = True

    @classmethod
    def get_latest_activity(cls, activity_identifier):
        return cls.objects.filter(activity_identifier=activity_identifier).order_by('-id').first()

    @classmethod
    def get_latest_active_activity(cls, activity_identifier):
        return cls.objects.filter(activity_identifier=activity_identifier).\
            filter(fk_status__in=(cls.STATUS_ACTIVE, cls.STATUS_OVERWRITTEN, cls.STATUS_DELETED)).order_by('-id').first()

    @property
    def operational_stakeholder(self):
        #involvements = InvestorActivityInvolvement.objects.filter(fk_activity_id=self.id)
        involvement = InvestorActivityInvolvement.objects.filter(
            fk_activity__activity_identifier=self.activity_identifier,
            #fk_status_id__in=(2,3,4), # FIXME: Based upon user permission also show pending
        )
        #if len(involvements) > 1:
        #    raise MultipleObjectsReturned('More than one OP for activity %s: %s' % (str(self), str(involvements)))
        if not involvement:
            return
            raise ObjectDoesNotExist('No OP for activity %s: %s' % (str(self), str(involvement)))
        else:
            involvement = involvement.latest()
        return Investor.objects.get(pk=involvement.fk_investor_id)

    @property
    def stakeholders(self):
        operational_stakeholder = self.operational_stakeholder
        if operational_stakeholder:
            stakeholder_involvements = InvestorVentureInvolvement.objects.filter(fk_venture=operational_stakeholder.pk)
            return [Investor.objects.get(pk=involvement.fk_investor_id) for involvement in stakeholder_involvements]
        else:
            return []

    @property
    def history(self):
        return HistoricalActivity.objects.filter(activity_identifier=self.activity_identifier)

    @property
    def target_country(self):
        country = self.attributes.filter(name='target_country')
        if country.count() > 0:
            country = country.first()
            try:
                return Country.objects.get(id=country.value)
            except:
                return None
        else:
            return None

class Activity(ActivityBase):
    """Just the most recent approved version of an activity (for simple queries in the public interface)"""
    DEAL_SCOPE_DOMESTIC = 'domestic'
    DEAL_SCOPE_TRANSNATIONAL = 'transnational'
    DEAL_SCOPE_CHOICES = (
        (DEAL_SCOPE_DOMESTIC, _('Domestic')),
        (DEAL_SCOPE_DOMESTIC, _('Transnational')),
    )

    NEGOTIATION_STATUS_EXPRESSION_OF_INTEREST = 'Expression of interest'
    NEGOTIATION_STATUS_UNDER_NEGOTIATION = 'Under negotiation'
    NEGOTIATION_STATUS_MEMO_OF_UNDERSTANDING = 'Memorandum of understanding'
    NEGOTIATION_STATUS_ORAL_AGREEMENT = 'Oral agreement'
    NEGOTIATION_STATUS_CONTRACT_SIGNED = 'Contract signed'
    NEGOTIATION_STATUS_NEGOTIATIONS_FAILED = 'Negotiations failed'
    NEGOTIATION_STATUS_CONTRACT_CANCELLED = 'Contract cancelled'
    NEGOTIATION_STATUS_CONTRACT_EXPIRED = 'Contract expired'
    NEGOTIATION_STATUS_CHANGE_OF_OWNERSHIP = 'Change of ownership'

    # These groupings are used for determining filter behaviour
    NEGOTIATION_STATUSES_INTENDED = (
        NEGOTIATION_STATUS_EXPRESSION_OF_INTEREST,
        NEGOTIATION_STATUS_UNDER_NEGOTIATION,
        NEGOTIATION_STATUS_MEMO_OF_UNDERSTANDING,
    )
    NEGOTIATION_STATUSES_CONCLUDED = (
        NEGOTIATION_STATUS_ORAL_AGREEMENT,
        NEGOTIATION_STATUS_CONTRACT_SIGNED,
    )
    NEGOTIATION_STATUSES_FAILED = (
        NEGOTIATION_STATUS_NEGOTIATIONS_FAILED,
        NEGOTIATION_STATUS_CONTRACT_CANCELLED,
        NEGOTIATION_STATUS_CONTRACT_EXPIRED,
    )
    NEGOTIATION_STATUS_CHOICES = (
        BLANK_CHOICE_DASH[0],
        (
            NEGOTIATION_STATUS_EXPRESSION_OF_INTEREST,
            _("Intended (Expression of interest)"),
        ),
        (
            NEGOTIATION_STATUS_UNDER_NEGOTIATION,
            _("Intended (Under negotiation)"),
        ),
        (
            NEGOTIATION_STATUS_MEMO_OF_UNDERSTANDING,
            _("Intended (Memorandum of understanding)"),
        ),
        (
            NEGOTIATION_STATUS_ORAL_AGREEMENT,
            _("Concluded (Oral Agreement)"),
        ),
        (
            NEGOTIATION_STATUS_CONTRACT_SIGNED,
            _("Concluded (Contract signed)"),
        ),
        (
            NEGOTIATION_STATUS_NEGOTIATIONS_FAILED,
            _("Failed (Negotiations failed)"),
        ),
        (
            NEGOTIATION_STATUS_CONTRACT_CANCELLED,
            _("Failed (Contract cancelled)"),
        ),
        (
            NEGOTIATION_STATUS_CONTRACT_EXPIRED, _("Contract expired"),
        ),
        (
            NEGOTIATION_STATUS_CHANGE_OF_OWNERSHIP, _("Change of ownership"),
        )
    )

    IMPLEMENTATION_STATUS_PROJECT_NOT_STARTED = 'Project not started'
    IMPLEMENTATION_STATUS_STARTUP_PHASE = 'Startup phase (no production)'
    IMPLEMENTATION_STATUS_IN_OPERATION = 'In operation (production)'
    IMPLEMENTATION_STATUS_PROJECT_ABANDONED = 'Project abandoned'
    IMPLEMENTATION_STATUS_CHOICES = (
        BLANK_CHOICE_DASH[0],
        (
            IMPLEMENTATION_STATUS_PROJECT_NOT_STARTED,
            _("Project not started"),
        ),
        (
            IMPLEMENTATION_STATUS_STARTUP_PHASE,
            _("Startup phase (no production)"),
        ),
        (
            IMPLEMENTATION_STATUS_IN_OPERATION,
            _("In operation (production)"),
        ),
        (
            IMPLEMENTATION_STATUS_PROJECT_ABANDONED,
            _("Project abandoned"),
        ),
    )

    is_public = models.BooleanField(_('Is this a public deal?'), default=False, db_index=True)
    deal_scope = models.CharField(_('Deal scope'), max_length=16, choices=DEAL_SCOPE_CHOICES,
        blank=True, null=True, db_index=True)
    negotiation_status = models.CharField(_('Negotiation status'), max_length=64,
        choices=NEGOTIATION_STATUS_CHOICES, blank=True, null=True, db_index=True)
    implementation_status = models.CharField(
        verbose_name=_('Implementation status'), max_length=64,
        choices=IMPLEMENTATION_STATUS_CHOICES, blank=True, null=True, db_index=True)
    deal_size = models.IntegerField(verbose_name=_('Deal size'), blank=True, null=True, db_index=True)


    def refresh_cached_attributes(self):
        # Implementation status (Latest date entered for the deal, then highest id)
        self.implementation_status = None
        # Null dates go last
        attributes = self.attributes.filter(name='implementation_status')
        attributes = attributes.extra(select={'date_is_null': 'date IS NULL'})
        attributes = attributes.extra(
            order_by=['date_is_null', '-date', '-id'])
        if attributes.count() > 0:
            self.implementation_status = attributes.first().value
            
        # Negotiation status (Latest date entered for the deal, then highest id)
        self.negotiation_status = None
        # Null dates go last
        attributes = self.attributes.filter(name='negotiation_status')
        attributes = attributes.extra(select={'date_is_null': 'date IS NULL'})
        attributes = attributes.extra(
            order_by=['date_is_null', '-date', '-id'])
        if attributes.count() > 0:
            self.negotiation_status = attributes.first().value

        # Deal size
        self.deal_size = None
        if self.negotiation_status:
            self.deal_size = self.get_deal_size()

        # Deal scope (domestic or transnational)
        self.deal_scope = self.get_deal_scope()

        self.is_public = self.is_public_deal()
        self.save()

    def is_public_deal(self):
        if not self.is_flag_not_public_off():
            return False
        if not self.is_minimum_information_requirement_satisfied():
            return False
        involvements = self.investoractivityinvolvement_set.all()
        if not self.has_valid_investors(involvements):
            return False
        return True

    #def is_high_income_target_country(self):
    #        for tc in self.attributes.filter(name="target_country"):
    #            country = Country.objects.get(id=tc.value)
    #            if country.high_income:
    #                return True
    #        return False


    #def is_mining_deal(self):
    #    mining = A_Key_Value_Lookup.objects.filter(activity_identifier=activity_identifier, key="intention",
    #                                               value="Mining")
    #    intentions = A_Key_Value_Lookup.objects.filter(activity_identifier=activity_identifier, key="intention")
    #    is_mining_deal = len(mining) > 0 and len(intentions) == 1
    #    return is_mining_deal


    def has_valid_investors(self, involvements):
        for i in involvements:
            if not i.fk_investor:
                continue
            investor_name = i.fk_investor.name
            invalid_name = "^(unknown|unnamed)( \(([, ]*(unnamed investor [0-9]+)*)+\))?$"
            if investor_name and not re.match(invalid_name, investor_name.lower()):
                return True
        return False

    #def has_subinvestors(involvements):
    #        if len(involvements) == 1 and not involvements[0].subinvestors.exists():
    #            return False
    #
    #        return len(involvements) > 0

    def is_minimum_information_requirement_satisfied(self):
        target_country = self.attributes.filter(name="target_country")
        ds_type = self.attributes.filter(name="type")
        return len(target_country) > 0 and len(ds_type) > 0


    #def is_size_invalid(self):
    #    intended_size = latest_attribute_value_for_activity(activity_identifier, "intended_size") or 0
    #    contract_size = latest_attribute_value_for_activity(activity_identifier, "contract_size") or 0
    #    production_size = latest_attribute_value_for_activity(activity_identifier, "production_size") or 0
    #    # Filter B2 (area size >= 200ha AND at least one area size is given)
    #    no_size_set = (not intended_size and not contract_size and not production_size)
    #    size_too_small = int(intended_size) < MIN_DEAL_SIZE and int(contract_size) < MIN_DEAL_SIZE and int(production_size) < MIN_DEAL_SIZE
    #    return no_size_set or size_too_small


    def is_flag_not_public_off(self):
        # Filter B1 (flag is unreliable not set):
        not_public = self.attributes.filter(name="not_public")
        not_public = len(not_public) > 0 and not_public[0].value or None
        return (not not_public) or (not_public in ("False", "off"))

    #def is_public_older_y2k(self):
    #    """
    #    Filter B3
    #    Only drop a deal if we have information that initiation years are < 2000.
    #    Deals with missing year values have to cross the filter to the PI
    #    """
    #    negotiation_stati = self.attributes.filter(name="negotiation_status"). \
    #        filter(attributes__contains={
    #                'negotiation_status': [
    #                    "Expression of interest", "Under negotiation", "Oral Agreement",
    #                    "Memorandum of understanding", "Contract signed"
    #                ]
    #            }
    #        ). \
    #        filter(date__lt='2000-01-01')
    #
    #    implementation_stati = self.attributes.filter(name="implementation_status"). \
    #        filter(attributes__contains={
    #            'implementation_status': ["Startup phase (no production)", "In operation (production)"]}
    #        ). \
    #        filter(date__lt='2000-01-01')
    #    return len(negotiation_stati) > 0 or len(implementation_stati) > 0

    def get_deal_scope(self):
        involvements = self.investoractivityinvolvement_set.all()
        target_countries = {c.value for c in self.attributes.filter(name="target_country")}
        investor_countries = {i.fk_investor.fk_country for i in involvements}

        if len(target_countries) > 0 and len(investor_countries) > 0:
            if len(target_countries.symmetric_difference(investor_countries)) == 0:
                return "domestic"
            else:
                return "transnational"
        elif len(target_countries) > 0 and len(investor_countries) == 0:
            # treat deals without investor country as transnational
            return "transnational"
        else:
            return None

    def get_deal_size(self):
        # FIXME: This should probably not sort by -date but by -id (latest element instead of newest)
        intended_size = self.attributes.filter(name="intended_size").order_by("-date")
        intended_size = len(intended_size) > 0 and intended_size[0].value or None
        contract_size = self.attributes.filter(name="contract_size").order_by("-date")
        contract_size = len(contract_size) > 0 and contract_size[0].value or None
        production_size = self.attributes.filter(name="production_size").order_by("-date")
        production_size = len(production_size) > 0 and production_size[0].value or None

        if self.negotiation_status in Activity.NEGOTIATION_STATUSES_INTENDED:
            # intended deal
            if not intended_size and contract_size:
                intended_size = contract_size
            elif not intended_size and not contract_size and production_size:
                intended_size = production_size
            return intended_size
        elif self.negotiation_status in Activity.NEGOTIATION_STATUSES_CONCLUDED:
            # concluded deal
            if not contract_size and production_size:
                contract_size = production_size
            return contract_size
        elif self.negotiation_status == Activity.NEGOTIATION_STATUS_NEGOTIATIONS_FAILED:
            # intended but failed deal
            if not intended_size and contract_size:
                intended_size = contract_size
            elif not intended_size and not contract_size and production_size:
                intended_size = production_size
            return intended_size
        elif self.negotiation_status in Activity.NEGOTIATION_STATUSES_FAILED:
            # concluded but failed
            if not contract_size and production_size:
                contract_size = production_size
            return contract_size

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
        index_together = [
            ['is_public', 'deal_scope'],
            ['is_public', 'deal_scope', 'negotiation_status'],
            ['is_public', 'deal_scope', 'implementation_status'],
            ['is_public', 'deal_scope', 'negotiation_status', 'implementation_status'],
        ]
        permissions = (
            ("review_activity", "Can review activity changes"),
        )


class HistoricalActivityQuerySet(ActivityQuerySet):

    def get_my_deals(self, user):
        return self.filter(history_user=user).\
            filter(fk_status__in=(ActivityBase.STATUS_PENDING, ActivityBase.STATUS_REJECTED))
        #return queryset.values_list('fk_activity_id', flat=True).distinct()


class HistoricalActivity(ActivityBase):
    """All versions (including the current) of activities"""
    history_date = models.DateTimeField(auto_now_add=True)
    history_user = models.ForeignKey('auth.User', blank=True, null=True)
    comment = models.TextField(_('Comment'), blank=True, null=True)

    objects = HistoricalActivityQuerySet.as_manager()

    #@property
    #def attributes(self):
    #    return ActivityAttribute.history.filter(fk_activity_id=self.id).latest()

    def update_public_activity(self):#, user=None):
        """Update public activity based upon newest confirmed historical activity"""
        #user = user or self.history_user
        #if not user.has_perm('landmatrix.change_activity'):
        #    return False
        # Update status of historical activity
        if self.fk_status_id == self.STATUS_PENDING:
            self.fk_status_id = self.STATUS_OVERWRITTEN
        elif self.fk_status_id == self.STATUS_TO_DELETE:
            self.fk_status_id = self.STATUS_DELETED
        self.save()

        # Historical activity already is the newest version of activity?
        #activity = Activity.objects.get(activity_identifier=self.activity_identifier)
        activity = Activity.objects.filter(activity_identifier=self.activity_identifier).order_by('-id').first()
        if activity:
            if self.id == activity.id:
                return False
        else:
            activity = Activity.objects.create(activity_identifier=self.activity_identifier)
        # Activity has been deleted?
        if self.fk_status_id == self.STATUS_DELETED:
            if activity:
                activity.delete()
            return True

        # Update activity (keeping comments)
        #activity.activity_identifier = self.activity_identifier
        activity.availability = self.availability
        activity.fully_updated = self.fully_updated
        activity.fk_status_id = self.fk_status_id
        activity.save()
        # Delete old and create new activity attributes
        if activity:
            activity.attributes.all().delete()
        for hattribute in self.attributes.all():
            attribute = ActivityAttribute.objects.create(
                fk_activity_id = activity.id,
                fk_group_id = hattribute.fk_group_id,
                fk_language_id = hattribute.fk_language_id,
                name = hattribute.name,
                value = hattribute.value,
                value2 = hattribute.value2,
                date = hattribute.date,
                polygon = hattribute.polygon,
            )
        # Confirm pending Investor activity involvement
        involvements = InvestorActivityInvolvement.objects.filter(fk_activity__activity_identifier=activity.activity_identifier)
        if involvements.count() > 0:
            latest = involvements.latest()
            latest.fk_activity_id = activity.id
            if latest.fk_status_id not in (latest.STATUS_ACTIVE, latest.STATUS_OVERWRITTEN):
                latest.fk_status_id = latest.STATUS_OVERWRITTEN
            latest.save()
            # Delete other involvments for activity, since we don't need a history of involvements
            involvements.exclude(id=latest.id).delete()
        activity.refresh_cached_attributes()
        return True

    def get_activity(self):
        return Activity.objects.filter(activity_identifier=self.activity_identifier).first()

    class Meta:
        verbose_name = _('Historical activity')
        verbose_name_plural = _('Historical activities')
        get_latest_by = 'history_date'
        ordering = ('-history_date',)