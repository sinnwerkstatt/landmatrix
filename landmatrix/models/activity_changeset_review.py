from django.db.models import Model, ForeignKey, DateTimeField, TextField, CharField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ReviewDecision(Model):
    name = CharField(_("Name"), max_length=255)
    description = TextField(_("Description"))


class ActivityChangesetReview(Model):
    fk_activity_changeset = ForeignKey("ActivityChangeset", verbose_name=_("Activity changeset"))
    fk_user = ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"))
    timestamp = DateTimeField(_("Timestamp"), auto_now_add=True)
    fk_review_decision = ForeignKey("ReviewDecision", verbose_name=_("Review decision"))
    comment = TextField(_("Comment"), blank=True, null=True)
