from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

#from simple_history.models import HistoricalRecords

from landmatrix.models.default_string_representation import DefaultStringRepresentation
from landmatrix.models.status import Status
from landmatrix.models.activity_attribute_group import ActivityAttribute, HistoricalActivityAttribute
from landmatrix.models.investor import Investor, InvestorActivityInvolvement, InvestorVentureInvolvement
from landmatrix.models.country import Country


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityManager(models.Manager):
    def public(self):
        return self.filter(fk_status_id__in=(ActivityBase.STATUS_ACTIVE, ActivityBase.STATUS_OVERWRITTEN))

    def public_or_deleted(self):
        return self.filter(fk_status_id__in=(ActivityBase.STATUS_ACTIVE, ActivityBase.STATUS_OVERWRITTEN, ActivityBase.STATUS_DELETED))

    def public_or_pending(self):
        return self.filter(fk_status_id__in=(ActivityBase.STATUS_ACTIVE, ActivityBase.STATUS_OVERWRITTEN, ActivityBase.STATUS_PENDING, ActivityBase.STATUS_TO_DELETE))

    def pending(self):
        return self.filter(fk_status_id__in=(ActivityBase.STATUS_PENDING, ActivityBase.STATUS_TO_DELETE))

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

    objects = ActivityManager()

    class Meta:
        abstract = True

    @classmethod
    def get_latest_activity(cls, activity_identifier):
        return cls.objects.filter(activity_identifier=activity_identifier).order_by('-id').first()

    @classmethod
    def get_latest_active_activity(cls, activity_identifier):
        return cls.objects.filter(activity_identifier=activity_identifier).\
            filter(fk_status__name__in=("active", "overwritten", "deleted")).order_by('-id').first()

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
            raise ObjectDoesNotExist('No OP for activity %s: %s' % (str(self), str(involvement)))
        else:
            involvement = involvement.latest()
        return Investor.objects.get(pk=involvement.fk_investor_id)

    @property
    def stakeholders(self):
        stakeholder_involvements = InvestorVentureInvolvement.objects.filter(fk_venture=self.operational_stakeholder.pk)
        return [Investor.objects.get(pk=involvement.fk_investor_id) for involvement in stakeholder_involvements]

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
    DEAL_SCOPE_CHOICES = (
        ('domestic', _('Domestic')),
        ('transnational', _('Transnational')),
    )
    NEGOTIATION_STATUS_CHOICES = (
        ('', _("---------")),
        ("Expression of interest", _("Intended (Expression of interest)")),
        ("Under negotiation", _("Intended (Under negotiation)")),
        ("Memorandum of understanding", _("Intended (Memorandum of understanding)")),
        ("Oral agreement", _("Concluded (Oral Agreement)")),
        ("Contract signed", _("Concluded (Contract signed)")),
        ("Negotiations failed", _("Failed (Negotiations failed)")),
        ("Contract canceled", _("Failed (Contract canceled)")),
        ("Contract expired", _("Failed (Contract expired)")),
        ("Change of ownership", _("Change of ownership"))
    )
    IMPLEMENTATION_STATUS_CHOICES = (
        ('', _("---------")),
        ("Project not started", _("Project not started")),
        ("Startup phase (no production)", _("Startup phase (no production)")),
        ("In operation (production)", _("In operation (production)")),
        ("Project abandoned", _("Project abandoned")),
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


class HistoricalActivityManager(ActivityManager):

    def get_my_deals(self, user):
        return self.filter(history_user=user).\
            filter(fk_status__in=(ActivityBase.STATUS_PENDING, ActivityBase.STATUS_REJECTED))
        #return queryset.values_list('fk_activity_id', flat=True).distinct()
class HistoricalActivity(ActivityBase):
    """All versions (including the current) of activities"""
    history_date = models.DateTimeField(auto_now_add=True)
    history_user = models.ForeignKey('auth.User', blank=True, null=True)
    comment = models.TextField(_('Comment'), blank=True, null=True)

    objects = HistoricalActivityManager()

    #@property
    #def attributes(self):
    #    return ActivityAttribute.history.filter(fk_activity_id=self.id).latest()

    def update_public_activity(self, user=None):
        """Update public activity based upon newest confirmed historical activity"""
        user = user or self.history_user
        if not user.has_perm('landmatrix.change_activity'):
            return False
        # Update status of historical activity
        if self.fk_status_id == self.STATUS_PENDING:
            self.fk_status_id = self.STATUS_OVERWRITTEN
        elif self.fk_status_id == self.STATUS_TO_DELETE:
            self.fk_status_id = self.STATUS_DELETED
        self.save()

        # Historical activity already is the newest version of activity?
        #old_activity = Activity.objects.get(activity_identifier=self.activity_identifier)
        old_activity = Activity.objects.filter(activity_identifier=self.activity_identifier).order_by('-id').first()
        if old_activity and self.id == old_activity.id:
            return False
        # Activity has been deleted?
        if self.fk_status_id == self.STATUS_DELETED:
            if old_activity:
                old_activity.delete()
            return True

        # Exchange new activity (create new and delete old)
        new_activity = Activity.objects.create(
            id = self.id,
            activity_identifier = self.activity_identifier,
            availability = self.availability,
            fully_updated = self.fully_updated,
            fk_status_id = self.fk_status_id,
        )
        # Delete old and create new activity attributes
        if old_activity:
            old_activity.attributes.all().delete()
        for hattribute in self.attributes.all():
            attribute = ActivityAttribute.objects.create(
                fk_activity_id = self.id,
                fk_group_id = hattribute.fk_group_id,
                fk_language_id = hattribute.fk_language_id,
                name = hattribute.name,
                value = hattribute.value,
                value2 = hattribute.value2,
                date = hattribute.date,
                polygon = hattribute.polygon,
            )
        # Confirm pending Investor activity involvement
        involvements = InvestorActivityInvolvement.objects.filter(fk_activity__activity_identifier=new_activity.activity_identifier)
        if involvements.count() > 0:
            latest = involvements.latest()
            latest.fk_activity_id = new_activity.id
            if latest.fk_status_id not in (latest.STATUS_ACTIVE, latest.STATUS_OVERWRITTEN):
                latest.fk_status_id = latest.STATUS_OVERWRITTEN
            latest.save()
            # Delete other involvments for activity, since we don't need a history of involvements
            involvements.exclude(id=latest.id).delete()
        if old_activity:
            old_activity.delete()
        return True

    class Meta:
        verbose_name = _('Historical activity')
        verbose_name_plural = _('Historical activities')
        get_latest_by = 'history_date'
        ordering = ('-history_date',)