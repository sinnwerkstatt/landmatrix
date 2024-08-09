from django.conf import settings
from django.db import models
from django.utils import timezone
from wagtail.models import Site

from .version import VersionStatus


class BaseWorkflowInfo(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="+",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
    )
    status_before: VersionStatus | None = models.CharField(
        choices=VersionStatus.choices,
        null=True,
        blank=True,
    )
    status_after: VersionStatus | None = models.CharField(
        choices=VersionStatus.choices,
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True)
    replies = models.JSONField(null=True, default=list)
    resolved = models.BooleanField(default=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
            "status_before": self.status_before,
            "status_after": self.status_after,
            "timestamp": self.timestamp,
            "comment": self.comment,
            "resolved": self.resolved,
            "replies": self.replies,
        }

    def get_object_url(self):
        _site = Site.objects.get(is_default_site=True)
        _port = f":{_site.port}" if _site.port not in [80, 443] else ""
        base_url = f"http{'s' if _site.port == 443 else ''}://{_site.hostname}{_port}"
        return base_url

    class Meta:
        abstract = True
