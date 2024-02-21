from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

STATUS = {"DRAFT": 1, "LIVE": 2, "UPDATED": 3, "DELETED": 4}
STATUS_CHOICES = (
    (STATUS["DRAFT"], _("Draft")),
    (STATUS["LIVE"], _("Live")),
    (STATUS["UPDATED"], _("Updated")),
    (STATUS["DELETED"], _("Deleted")),
)

DRAFT_STATUS = {
    "DRAFT": 1,
    "REVIEW": 2,
    "ACTIVATION": 3,
    "REJECTED": 4,
    "TO_DELETE": 5,
}
DRAFT_STATUS_CHOICES = (
    (DRAFT_STATUS["DRAFT"], _("Draft")),
    (DRAFT_STATUS["REVIEW"], _("Review")),
    (DRAFT_STATUS["ACTIVATION"], _("Activation")),
    (DRAFT_STATUS["REJECTED"], _("Rejected")),
    (DRAFT_STATUS["TO_DELETE"], _("To Delete")),
)


class Version(models.Model):
    created_at = models.DateTimeField(db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    modified_at = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    serialized_data = models.JSONField()

    class Meta:
        abstract = True
        ordering = ["-pk"]

    def __str__(self):
        return f"#{self.object_id} v{self.id} @{self.created_at.date()}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
        # It's not very nice to just strip the modified_at timestamp out of
        # the serialized data :S
        self.modified_at = self.serialized_data["modified_at"]
        self.modified_by_id = self.serialized_data["modified_by"]
        super().save(*args, **kwargs)


class WorkflowInfo(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
    )
    draft_status_before = models.IntegerField(
        choices=DRAFT_STATUS_CHOICES, null=True, blank=True
    )
    draft_status_after = models.IntegerField(
        choices=DRAFT_STATUS_CHOICES, null=True, blank=True
    )
    timestamp = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)
    replies = models.JSONField(null=True, blank=True)
    resolved = models.BooleanField(default=False)

    # watch out: ignore the draft_status within this DealVersion object, it will change
    # when the workflow moves along. the payload will remain consistent though.

    class Meta:
        abstract = True
