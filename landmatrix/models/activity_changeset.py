from django.contrib.auth.models import User
from django.db import models
from django.db.models.manager import Manager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

#from landmatrix.models.activity import HistoricalActivity

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityChangesetManager(models.Manager):

    def get_by_state(self, status):
        #act_ids = self.by_status_query_set(status).values_list('id', flat=True).distinct()
        return self.filter(fk_activity__fk_status_id=status).order_by('-timestamp')

    #def by_status_query_set(self, status):
    #    return HistoricalActivity.objects.filter(fk_status__name__contains=status.lower()).order_by('-history_date')

    #def get_my_deals(self, user):
    #    changesets = ActivityChangeset.objects.filter(fk_activity__history_user=user).\
    #        filter(fk_activity__fk_status__name__in=("pending", "rejected"))
    #    return changesets.order_by('-timestamp').values_list('fk_activity_id', flat=True).distinct()

        #changesets = self.raw("""
        #    SELECT
        #        c.*
        #      FROM
        #        a_changesets c,
        #        activities a,
        #        status s
        #      WHERE
        #        c.fk_activity = a.id
        #        AND a.version = (SELECT max(version) FROM activities amax, status st WHERE amax.fk_status = st.id AND amax.activity_identifier = a.activity_identifier)
        #        AND a.fk_status = s.id
        #        AND c.fk_user = %(user)s
        #        AND s.name in ("pending", "rejected")
        #      ORDER BY timestamp DESC;
        #    """ % {"user": user})

class ReviewDecision(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"))

class ActivityChangeset(models.Model):
    fk_activity = models.ForeignKey('landmatrix.HistoricalActivity', verbose_name=_("Activity"), blank=True, null=True, related_name='changesets')
    fk_country = models.ForeignKey('landmatrix.Country', verbose_name=_("County"), blank=True, null=True)
    #fk_region = models.ForeignKey('landmatrix.Region', verbose_name=_("Region"), blank=True, null=True)

    fk_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), blank=True, null=True)
    timestamp = models.DateTimeField(_("Timestamp"), blank=True, null=True)
    fk_review_decision = models.ForeignKey("ReviewDecision", verbose_name=_("Review decision"), blank=True, null=True)
    comment = models.TextField(_("Comment"), blank=True, null=True)

    objects = ActivityChangesetManager()

    #@classmethod
    #def from_latest(cls, activity_identifier):
    #    most_recent = cls.activity_from_identifier(activity_identifier)
    #    return ActivityChangeset.from_historical_activity(most_recent)
#
    #@classmethod
    #def activity_from_identifier(cls, activity_identifier):
    #    return HistoricalActivity.objects.filter(activity_identifier=activity_identifier).latest()
#
    #@classmethod
    #def from_historical_activity(cls, historical_activity):
    #    changeset = ActivityChangeset()
    #    changeset.timestamp = historical_activity.history_date
    #    changeset.fk_activity = Activity.objects.get(id=historical_activity.id)
    #    return changeset
#
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    #self.historical_activity = None
    #    #if self.fk_activity and self.timestamp:
    #    #    self.historical_activity = self.fk_activity.history.filter(
    #    #        history_date__lte=self.timestamp
    #    #    ).order_by('-history_date').first()
    #    #self.fk_user = None if not self.historical_activity or not self.historical_activity.history_user_id else User.objects.get(pk=self.historical_activity.history_user_id)
    #    #self.previous_version = self._get_previous_version()
#
    #def _get_previous_version(self):
    #    if not ActivityChangeset.implementation_message_printed:
    #        print('ActivityChangeset._get_previous_version(): Implement: point to older version in history')
    #        ActivityChangeset.implementation_message_printed = True
    #    pass

    def __str__(self):
        return str(self.fk_activity)