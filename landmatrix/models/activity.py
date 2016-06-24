from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

#from simple_history.models import HistoricalRecords

from landmatrix.models.default_string_representation import DefaultStringRepresentation
from landmatrix.models.status import Status
from landmatrix.models.activity_attribute_group import ActivityAttribute
from landmatrix.models.investor import Investor, InvestorActivityInvolvement, InvestorVentureInvolvement


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

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
    fully_updated = models.DateTimeField(_("Fully updated"), blank=True, null=True)#, auto_now_add=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"), default=1)

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

class Activity(ActivityBase):
    """Just the most recent approved version of an activity (for simple queries in the public interface)"""
    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

class HistoricalActivity(ActivityBase):
    """All versions (including the current) of activities"""
    history_date = models.DateTimeField(auto_now_add=True)
    history_user = models.ForeignKey('auth.User', blank=True, null=True)

    #@property
    #def attributes(self):
    #    return ActivityAttribute.history.filter(fk_activity_id=self.id).latest()

    class Meta:
        verbose_name = _('Historical activity')
        verbose_name_plural = _('Historical activities')
        get_latest_by = 'history_date'
        ordering = ('-history_date',)
