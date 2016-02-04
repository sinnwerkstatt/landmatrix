from django.contrib.auth.models import User
from django.db.models import Model, TextField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from landmatrix.models.activity import Activity

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityChangeset:

    class Manager:

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

    comment = TextField(_("Comment"))

    @classmethod
    def from_latest(cls, activity_identifier):
        # print('from_latest:', activity_identifier)
        most_recent = cls.activity_from_identifier(activity_identifier).history.last()
        return ActivityChangeset(most_recent)

    @classmethod
    def activity_from_identifier(cls, activity_identifier):
        return Activity.objects.filter(activity_identifier=activity_identifier).order_by('id').last()

    def __init__(self, historical_activity):
        self.activity = historical_activity
        self.fk_user = None if not historical_activity.history_user_id else User.objects.get(pk=historical_activity.history_user_id)
        self.timestamp = historical_activity.history_date
        self.source = None  # models.TextField(_("Source"), blank=True, null=True)
        self.fk_activity = self.activity
        self.previous_version = None  # models.IntegerField(_("Previous version"), blank=True, null=True)
        super().__init__()

    objects = Manager()
