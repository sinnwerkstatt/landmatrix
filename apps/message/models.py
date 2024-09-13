from wagtailorderable.models import Orderable

from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.fields import RichTextField


class Message(Orderable):
    class Level(models.TextChoices):
        DEBUG = "debug", _("Debug")
        INFO = "info", _("Info")
        SUCCESS = "success", _("Success")
        WARNING = "warning", _("Warning")
        ERROR = "error", _("Error")

    title = models.CharField(_("Title"))
    text = RichTextField(_("Text"))
    level = models.CharField(
        _("Level"),
        choices=Level.choices,
        default=Level.INFO,
    )
    allow_users_to_hide = models.BooleanField(
        _("Allow users to hide message"),
        help_text=_(
            "Store check off in cookie (expires in 365 days) "
            "so that users can choose to not display the message again."
        ),
        default=False,
    )
    logged_in_only = models.BooleanField(
        _("Only display message to logged-in users"),
        default=False,
    )
    expires_at = models.DateField(
        _("Expiration date"),
        help_text=_("After this date the message will not be displayed anymore"),
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(_("Is active"))

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.get_level_display()} -- {self.title}"
