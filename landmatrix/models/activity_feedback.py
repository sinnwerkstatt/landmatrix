from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityFeedbackManager(models.Manager):

    def active(self):
        active_statuses = ('active', 'overwritten')
        return self.filter(fk_activity__fk_status__name__in=active_statuses)


class ActivityFeedback(models.Model):

    fk_activity = models.ForeignKey(
        "HistoricalActivity", verbose_name=_("Activity"))
    fk_user_assigned = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User assigned"),
        related_name="user_assigned")
    fk_user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User created"),
        related_name="user_created")
    comment = models.TextField(_("Comment"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    objects = ActivityFeedbackManager()

    def __str__(self):
        return str(self.fk_activity)

    class Meta:
        verbose_name = _('Activity feedback')
        verbose_name_plural = _('Activity feedbacks')
        ordering = ('-timestamp', '-id')
