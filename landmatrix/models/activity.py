from django.db import models
from django.utils.translation import ugettext_lazy as _

from simple_history.models import HistoricalRecords

from landmatrix.models.default_string_representation import DefaultStringRepresentation
from landmatrix.models.status import Status

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class Activity(DefaultStringRepresentation, models.Model):
    activity_identifier = models.IntegerField(_("Activity identifier"), db_index=True)
    availability = models.FloatField(_("availability"), blank=True, null=True)
    fully_updated = models.DateTimeField(_("Fully updated"), blank=True, null=True, auto_now_add=True)
    fk_status = models.ForeignKey("Status", verbose_name=_("Status"))

    history = HistoricalRecords()

    # http://django-simple-history.readthedocs.io/en/latest/advanced.html#recording-which-user-changed-a-model
    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    @classmethod
    def get_latest_activity(cls, activity_identifier):
        return cls.objects.filter(activity_identifier=activity_identifier).order_by('-id').first()

    @classmethod
    def get_latest_active_activity(cls, activity_identifier):
        return cls.objects.filter(activity_identifier=activity_identifier).\
            filter(fk_status__name__in=("active", "overwritten", "deleted")).order_by('-id').first()

