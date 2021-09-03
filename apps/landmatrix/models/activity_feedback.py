from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ActivityFeedback(models.Model):

    fk_activity = models.ForeignKey(
        "HistoricalActivity", verbose_name=_("Activity"), on_delete=models.CASCADE
    )
    fk_user_assigned = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User assigned"),
        related_name="user_assigned",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    fk_user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User created"),
        related_name="user_created",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    comment = models.TextField(_("Comment"))
    timestamp = models.DateTimeField(_("Timestamp"), default=timezone.now)

    def __str__(self):
        return str(self.fk_activity)

    class Meta:
        verbose_name = _("Activity feedback")
        verbose_name_plural = _("Activity feedbacks")
        ordering = ("-timestamp", "-id")
