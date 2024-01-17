from wagtailorderable.models import Orderable

from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.fields import RichTextField
from wagtail.rich_text import expand_db_html


class Message(Orderable, models.Model):
    LEVEL_CHOICES = (
        ("debug", _("Debug")),
        ("info", _("Info")),
        ("success", _("Success")),
        ("warning", _("Warning")),
        ("error", _("Error")),
    )

    title = models.CharField(_("Title"), blank=True, null=True)
    text = RichTextField(_("Text"))
    level = models.CharField(_("Level"), choices=LEVEL_CHOICES, default="info")
    allow_users_to_hide = models.BooleanField(
        _("Allow users to hide message"),
        help_text=_(
            "Store check off in cookie (expires in 365 days) so that users can choose to not display the messagea again."
        ),
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
        return self.title
