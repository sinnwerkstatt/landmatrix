from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone


class ReviewDecision(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)


class ActivityChangeset(models.Model):
    fk_activity = models.ForeignKey(
        'landmatrix.HistoricalActivity', verbose_name=_("Activity"),
        blank=True, null=True, related_name='changesets', on_delete=models.CASCADE)
    fk_country = models.ForeignKey(
        'landmatrix.Country', verbose_name=_("Country"), blank=True, null=True, on_delete=models.SET_NULL)

    fk_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), blank=True,
        null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(_("Timestamp"), default=timezone.now)
    fk_review_decision = models.ForeignKey(
        ReviewDecision, verbose_name=_("Review decision"), blank=True,
        null=True, on_delete=models.SET_NULL)
    comment = models.TextField(_("Comment"), blank=True, null=True)

    class Meta:
        ordering = ('-timestamp',)
        get_latest_by = 'timestamp'
