from django.contrib.auth.models import User
from django.db.models import Model, TextField, ForeignKey, DateTimeField
from django.db.models.manager import Manager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from landmatrix.models.activity import Activity

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityChangesetManager(Manager):

    def filter(self, **kwargs):
        activitiy_identifiers = Activity.history.filter(**kwargs).order_by('-history_date').values_list('activity_identifier', flat=True)
        return [
            ActivityChangeset.from_latest(act_id)
            for act_id in activitiy_identifiers
            if ActivityChangeset.activity_from_identifier(act_id)
        ]

    def get_by_state(self, status):
        activitiy_identifiers = self.by_status_query_set(status).values_list('activity_identifier', flat=True).distinct()
        return [ActivityChangeset.from_latest(act_id) for act_id in activitiy_identifiers]

    def by_status_query_set(self, status):
        return Activity.history.filter(fk_status__name__contains=status.lower()).order_by('-history_date')

    def get_my_deals(self, user):
        pass


class ActivityChangeset(Model):

    comment = TextField(_("Comment"))
    fk_activity = ForeignKey("Activity", verbose_name=_("Activity"))
    timestamp = DateTimeField(_("Timestamp"), auto_now_add=True)
    source = TextField(_("Source"), blank=True, null=True)

    objects = ActivityChangesetManager()

    @classmethod
    def from_latest(cls, activity_identifier):
        most_recent = cls.activity_from_identifier(activity_identifier).history.last()
        return ActivityChangeset(most_recent)

    @classmethod
    def activity_from_identifier(cls, activity_identifier):
        return Activity.objects.filter(activity_identifier=activity_identifier).order_by('id').last()

    def __init__(self, historical_activity=None):
        super().__init__()
        if historical_activity is not None:
            self.historical_activity = historical_activity
            self.timestamp = historical_activity.history_date
            self.fk_activity = Activity.objects.get(id=historical_activity.id)
        else:
            self.historical_activity = self.fk_activity.history.as_of(self.timestamp)

        self.fk_user = None if not historical_activity.history_user_id else User.objects.get(pk=historical_activity.history_user_id)
        self.previous_version = self._get_previous_version()

    def _get_previous_version(self):
        print('Implement: point to older version in history')
        pass

