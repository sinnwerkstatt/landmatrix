from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

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
        on_delete=models.SET_NULL,
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
        super().save(*args, **kwargs)

    @classmethod
    def from_object(cls, obj, created_at=None, created_by=None):
        version, _ = cls.objects.get_or_create(
            created_at=created_at,
            created_by=created_by,
            object_id=obj.pk,
            serialized_data=obj.serialize_for_version(),
        )
        return version

    def enriched_dict(self) -> dict:
        edict = self.serialized_data
        edict["id"] = self.object_id
        for x in self.object._meta.fields:
            if x.__class__.__name__ == "ForeignKey":
                if edict.get(x.name):
                    edict[x.name] = x.related_model.objects.get(pk=edict[x.name])
        edict["created_at"] = self.created_at
        edict["created_by"] = self.created_by
        return edict


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
    processed_by_receiver = models.BooleanField(default=False)

    # watch out: ignore the draft_status within this DealVersion object, it will change
    # when the workflow moves along. the payload will remain consistent though.

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "from_user": self.from_user,
            "to_user": self.to_user,
            "draft_status_before": self.draft_status_before,
            "draft_status_after": self.draft_status_after,
            "timestamp": self.timestamp,
            "comment": self.comment,
            "processed_by_receiver": self.processed_by_receiver,
        }

    class Meta:
        abstract = True
