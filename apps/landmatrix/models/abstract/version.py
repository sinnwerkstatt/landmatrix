from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.exceptions import PermissionDenied, ParseError

from apps.accounts.models import User
from apps.landmatrix.permissions import is_editor_or_higher, is_admin


VERSION_STATUS_CHOICES = (
    ("DRAFT", _("Draft")),
    ("REVIEW", _("Review")),
    ("ACTIVATION", _("Activation")),
    ("ACTIVATED", _("Activated")),
)


class BaseVersion(models.Model):
    created_at = models.DateTimeField(_("Created at"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    modified_at = models.DateTimeField(_("Modified at"), blank=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    sent_to_review_at = models.DateTimeField(
        _("Sent to review at"), null=True, blank=True
    )
    sent_to_review_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    sent_to_activation_at = models.DateTimeField(
        _("Reviewed at"), null=True, blank=True
    )
    sent_to_activation_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    activated_at = models.DateTimeField(_("Activated at"), null=True, blank=True)
    activated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    status = models.CharField(choices=VERSION_STATUS_CHOICES, default="DRAFT")

    def save(self, *args, **kwargs):
        if self._state.adding and not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def change_status(
        self,
        new_status: str,
        user: User,
        to_user_id: int = None,
    ):
        if new_status == "TO_REVIEW":
            if not (self.created_by == user or is_editor_or_higher(user)):
                raise PermissionDenied("MISSING_AUTHORIZATION")
            self.status = "REVIEW"
            self.sent_to_review_at = timezone.now()
            self.sent_to_review_by = user
            self.save()
        elif new_status == "TO_ACTIVATION":
            if not is_editor_or_higher(user):
                raise PermissionDenied("MISSING_AUTHORIZATION")
            self.status = "ACTIVATION"
            self.sent_to_activation_at = timezone.now()
            self.sent_to_activation_by = user
            self.save()
        elif new_status == "ACTIVATE":
            if not is_admin(user):
                raise PermissionDenied("MISSING_AUTHORIZATION")
            self.status = "ACTIVATED"
            self.activated_at = timezone.now()
            self.activated_by = user
            self.save()
        elif new_status == "TO_DRAFT":
            if not is_editor_or_higher(user):
                raise PermissionDenied("MISSING_AUTHORIZATION")
            self.copy_to_new_draft(to_user_id)

        else:
            raise ParseError("Invalid transition")

    class Meta:
        abstract = True

    def copy_to_new_draft(self, created_by_id):
        self.id = None
        self.status = "DRAFT"
        self.created_at = timezone.now()
        self.created_by_id = created_by_id
        self.modified_at = None
        self.modified_by = None
        self.sent_to_review_at = None
        self.sent_to_review_by = None
        self.sent_to_activation_at = None
        self.sent_to_activation_by = None
        self.activated_at = None
        self.activated_by = None
