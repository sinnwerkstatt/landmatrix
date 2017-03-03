import re
from collections import defaultdict

from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.functions import Coalesce
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from landmatrix.models.default_string_representation import DefaultStringRepresentation
from landmatrix.models.status import Status
from landmatrix.models.activity_attribute_group import (
    ActivityAttribute, HistoricalActivityAttribute,
)
from landmatrix.models.investor import (
    Investor, InvestorActivityInvolvement, InvestorVentureInvolvement,
)
from landmatrix.models.country import Country

class ActivityQuerySet(models.QuerySet):
    def public(self):
        '''
        Status public, not to be confused with is_public.
        '''
        return self.filter(fk_status_id__in=ActivityBase.PUBLIC_STATUSES)

    def public_or_deleted(self):
        statuses = ActivityBase.PUBLIC_STATUSES + (
            ActivityBase.STATUS_DELETED,
        )
        return self.filter(fk_status_id__in=statuses)

    def public_or_pending(self):
        statuses = ActivityBase.PUBLIC_STATUSES + (
            ActivityBase.STATUS_PENDING,
        )
        return self.filter(fk_status_id__in=statuses)

    def pending(self):
        statuses = (ActivityBase.STATUS_PENDING, ActivityBase.STATUS_TO_DELETE)
        return self.filter(fk_status_id__in=statuses)

    def pending_only(self):
        return self.filter(fk_status_id=ActivityBase.STATUS_PENDING)

    def active(self):
        return self.filter(fk_status_id=ActivityBase.STATUS_ACTIVE)

    def overwritten(self):
        return self.filter(fk_status_id=ActivityBase.STATUS_OVERWRITTEN)

    def to_delete(self):
        return self.filter(fk_status_id=ActivityBase.STATUS_TO_DELETE)

    def deleted(self):
        return self.filter(fk_status_id=ActivityBase.STATUS_DELETED)

    def rejected(self):
        return self.filter(fk_status_id=ActivityBase.STATUS_REJECTED)

    def activity_identifier_count(self):
        return self.values('activity_identifier').distinct().count()

    def overall_activity_count(self):
        return self.public().activity_identifier_count()

    def public_activity_count(self):
        return self.public().filter(is_public=True).activity_identifier_count()


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
    ACTIVITY_IDENTIFIER_DEFAULT = 2147483647  # Max safe int

    # FIXME: Replace fk_status with Choice Field
    STATUS_PENDING = 1
    STATUS_ACTIVE = 2
    STATUS_OVERWRITTEN = 3
    STATUS_DELETED = 4
    STATUS_REJECTED = 5
    STATUS_TO_DELETE = 6
    PUBLIC_STATUSES = (STATUS_ACTIVE, STATUS_OVERWRITTEN)
    STATUS_CHOICES = (
        (STATUS_PENDING, _('Pending')),
        (STATUS_ACTIVE, _('Active')),
        (STATUS_OVERWRITTEN, _('Overwritten')),
        (STATUS_DELETED, _('Deleted')),
        (STATUS_REJECTED, _('Rejected')),
        (STATUS_TO_DELETE, _('To delete')),
    )

    activity_identifier = models.IntegerField(_("Activity identifier"), db_index=True)
    availability = models.FloatField(_("availability"), blank=True, null=True)
    fully_updated = models.BooleanField(_("Fully updated"), default=False)#, auto_now_add=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"), default=1)

    objects = ActivityQuerySet.as_manager()
    negotiation_status_objects = NegotiationStatusManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        '''
        If there's no identifier, set it to a default, and update it to the id
        post save.

        This is pretty much just for import, which keeps trying to get the
        next id and getting it wrong.
        '''
        if self.activity_identifier is None:
            self.activity_identifier = self.ACTIVITY_IDENTIFIER_DEFAULT

        super().save(*args, **kwargs)

        if self.activity_identifier == self.ACTIVITY_IDENTIFIER_DEFAULT:
            kwargs['update_fields'] = ['activity_identifier']
            self.activity_identifier = self.id
            # re-save
            self.save(*args, **kwargs)

    @classmethod
    def get_latest_activity(cls, activity_identifier):
        return cls.objects.filter(activity_identifier=activity_identifier).order_by('-id').first()

    @classmethod
    def get_latest_active_activity(cls, activity_identifier):
        queryset = cls.objects.public_or_deleted()
        queryset = queryset.filter(activity_identifier=activity_identifier)
        item = queryset.order_by('-id').first()

        return item

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
            except Country.DoesNotExist:
                return None
        else:
            return None

    @property
    def attributes_as_dict(self):
        '''
        Returns all attributes, *grouped* as a nested dict.
        '''
        attrs = defaultdict(dict)
        for attr in self.attributes.select_related('fk_group'):
            attrs[attr.fk_group.name][attr.name] = attr.value

        return attrs


class Activity(ActivityBase):
    """
    Just the most recent approved version of an activity
    (for simple queries in the public interface).

    There should only be one activity per activity_identifier.
    """
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
        if not self.has_subinvestors(involvements):
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

    def has_subinvestors(self, involvements):
        for i in involvements:
            if i.fk_investor.venture_involvements.count() > 0:
                return True
            return False
    
        return len(involvements) > 0

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
            return intended_size or contract_size or production_size or 0
        elif self.negotiation_status in Activity.NEGOTIATION_STATUSES_CONCLUDED:
            # concluded deal
            return contract_size or production_size or 0
        elif self.negotiation_status == Activity.NEGOTIATION_STATUS_NEGOTIATIONS_FAILED:
            # intended but failed deal
            return intended_size or contract_size or production_size or 0
        elif self.negotiation_status in Activity.NEGOTIATION_STATUSES_FAILED:
            # concluded but failed
            return contract_size or production_size or 0
        else:
            return 0

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

    def _single_revision_identifiers(self):
        '''
        Get all activity identifiers (as values) that only have a single
        revision.

        This query looks a bit strange, but the order of operations is required
        in order to construct the group by correctly.
        '''
        queryset = HistoricalActivity.objects.values('activity_identifier') # don't use 'self' here
        queryset = queryset.annotate(
            revisions_count=models.Count('activity_identifier'))
        queryset = queryset.order_by('activity_identifier')
        queryset = queryset.exclude(revisions_count__gt=1)
        queryset = queryset.values_list('activity_identifier', flat=True)

        return queryset

    def with_multiple_revisions(self):
        '''
        Get only new activities (without any other historical instances).
        '''
        subquery = self._single_revision_identifiers()
        return self.exclude(activity_identifier__in=subquery)

    def without_multiple_revisions(self):
        '''
        Get only new activities (without any other historical instances).
        '''
        subquery = self._single_revision_identifiers()
        return self.filter(activity_identifier__in=subquery)


class HistoricalActivity(ActivityBase):
    """
    All versions (including the current) of activities
    
    Only the current historical activity should have a public version set.
    """
    public_version = models.OneToOneField(
        Activity, blank=True, null=True, related_name='historical_version')
    history_date = models.DateTimeField(auto_now_add=True)
    history_user = models.ForeignKey('auth.User', blank=True, null=True)
    comment = models.TextField(_('Comment'), blank=True, null=True)

    objects = HistoricalActivityQuerySet.as_manager()

    def approve_change(self, user=None, comment=None):
        assert self.fk_status_id == HistoricalActivity.STATUS_PENDING

        # Only approvals of administrators should go public
        if user.has_perm('landmatrix.change_activity'):
            # TODO: this logic is taken from changeset protocol
            # but it won't really work properly. We need to determine behaviour
            # when updates happen out of order. There can easily be many edits,
            # and not the latest one is approved.
            latest_public_version = self.__class__.get_latest_active_activity(
                self.activity_identifier)
            if latest_public_version:
                self.fk_status_id = HistoricalActivity.STATUS_OVERWRITTEN
            else:
                self.fk_status_id = HistoricalActivity.STATUS_ACTIVE
            self.save(update_fields=['fk_status'])

            try:
                investor = InvestorActivityInvolvement.objects.get(
                    fk_activity_id=self.pk).fk_investor
            except InvestorActivityInvolvement.DoesNotExist:
                pass
            else:
                investor.approve()

            self.update_public_activity()

        self.changesets.create(fk_user=user, comment=comment)

    def reject_change(self, user=None, comment=None):
        assert self.fk_status_id == HistoricalActivity.STATUS_PENDING
        self.fk_status_id = HistoricalActivity.STATUS_REJECTED
        self.save(update_fields=['fk_status'])

        try:
            investor = InvestorActivityInvolvement.objects.get(
                fk_activity_id=self.pk).fk_investor
        except InvestorActivityInvolvement.DoesNotExist:
            pass
        else:
            investor.reject()

        self.changesets.create(fk_user=user, comment=comment)

    def approve_delete(self, user=None, comment=None):
        assert self.fk_status_id == HistoricalActivity.STATUS_TO_DELETE

        # Only approvals of administrators should go public
        if user.has_perm('landmatrix.change_activity'):
            self.fk_status_id = HistoricalActivity.STATUS_DELETED
            self.save(update_fields=['fk_status'])

            # TODO: this seems weird to me, but I just moved the logic over
            # Wouldn't it make sense to delete here?
            try:
                investor = InvestorActivityInvolvement.objects.get(
                    fk_activity_id=self.pk).fk_investor
            except InvestorActivityInvolvement.DoesNotExist:
                pass
            else:
                investor.approve()
            self.update_public_activity()

        self.changesets.create(fk_user=user, comment=comment)

    def reject_delete(self, user=None, comment=None):
        assert self.fk_status_id == HistoricalActivity.STATUS_TO_DELETE
        self.fk_status_id = HistoricalActivity.STATUS_REJECTED
        self.save(update_fields=['fk_status'])

        try:
            investor = InvestorActivityInvolvement.objects.get(
                fk_activity_id=self.pk).fk_investor
        except InvestorActivityInvolvement.DoesNotExist:
            pass
        else:
            investor.reject()

        self.changesets.create(fk_user=user, comment=comment)

    def compare_attributes_to(self, version):
        changed_attrs = []  # (group_id, key, current_val, other_val)

        def get_lookup(attr):
            return (attr.fk_group_id, attr.name)

        current_attrs = list(self.attributes.all())
        current_lookups = {
            get_lookup(attr) for attr in current_attrs
        }
        # Build a dict of attrs for quick lookup with one query
        other_attrs = {}
        if version:
            for attr in version.attributes.all():
                other_attrs[get_lookup(attr)] = attr.value

        for attr in current_attrs:
            lookup = get_lookup(attr)
            if lookup not in other_attrs:
                changes = (attr.fk_group_id, attr.name, attr.value, None)
                changed_attrs.append(changes)
            elif lookup in other_attrs and attr.value != other_attrs[lookup]:
                other_val = other_attrs[lookup]
                changes = (attr.fk_group_id, attr.name, attr.value, other_val)
                changed_attrs.append(changes)

        # Check attributes that are not in this version
        for lookup in set(other_attrs.keys()) - current_lookups:
            group_id, key = lookup
            changes = (group_id, key, None, other_attrs[lookup])
            changed_attrs.append(changes)

        return changed_attrs

    def update_public_activity(self):
        """Update public activity based upon newest confirmed historical activity"""
        #user = user or self.history_user
        # Update status of historical activity
        if self.fk_status_id == self.STATUS_PENDING:
            self.fk_status_id = self.STATUS_OVERWRITTEN
        elif self.fk_status_id == self.STATUS_TO_DELETE:
            self.fk_status_id = self.STATUS_DELETED
        self.save()

        # Historical activity already is the newest version of activity?
        if self.public_version:
            return False

        activity = Activity.objects.filter(
            activity_identifier=self.activity_identifier).order_by(
            '-id').first()

        # Activity has been deleted?
        if self.fk_status_id == self.STATUS_DELETED:
            if activity:
                activity.delete()
            return True

        if not activity:
            activity = Activity.objects.create(
                activity_identifier=self.activity_identifier)

        # Update activity (keeping comments)
        activity.availability = self.availability
        activity.fully_updated = self.fully_updated
        activity.fk_status_id = self.fk_status_id
        activity.save()

        # Delete old and create new activity attributes
        activity.attributes.all().delete()

        for hattribute in self.attributes.all():
            ActivityAttribute.objects.create(
                fk_activity_id=activity.id,
                fk_group_id=hattribute.fk_group_id,
                fk_language_id=hattribute.fk_language_id,
                name=hattribute.name,
                value=hattribute.value,
                value2=hattribute.value2,
                date=hattribute.date,
                is_current=hattribute.is_current,
                polygon=hattribute.polygon)
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

        # Keep public version relation up to date
        HistoricalActivity.objects.filter(public_version=activity).update(
            public_version=None)
        self.public_version = activity
        self.save(update_fields=['public_version'])

        return True

    @property
    def changeset_comment(self):
        '''
        Previously in changeset protocol there was some voodoo around getting
        a changeset with the same datetime as history_date. That doesn't work,
        because history_date is set when the activity is revised, and the
        changeset is timestamped when it is reviewed.

        So, just grab the most recent one.
        '''

        changeset = self.changesets.first()
        comment = changeset.comment if changeset else ''

        return comment

    class Meta:
        verbose_name = _('Historical activity')
        verbose_name_plural = _('Historical activities')
        get_latest_by = 'history_date'
        ordering = ('-history_date',)

