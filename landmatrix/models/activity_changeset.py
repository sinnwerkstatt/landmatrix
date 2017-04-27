from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone



class ActivityChangesetManager(models.Manager):

    def get_by_state(self, status):
        return self.filter(fk_activity__fk_status_id=status)


class ReviewDecision(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)


class ActivityChangeset(models.Model):
    fk_activity = models.ForeignKey(
        'landmatrix.HistoricalActivity', verbose_name=_("Activity"),
        blank=True, null=True, related_name='changesets')
    fk_country = models.ForeignKey(
        'landmatrix.Country', verbose_name=_("County"), blank=True, null=True)

    fk_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), blank=True,
        null=True)
    timestamp = models.DateTimeField(_("Timestamp"), default=timezone.now)
    fk_review_decision = models.ForeignKey(
        ReviewDecision, verbose_name=_("Review decision"), blank=True,
        null=True)
    comment = models.TextField(_("Comment"), blank=True, null=True)

    objects = ActivityChangesetManager()

    class Meta:
        ordering = ('-timestamp',)
