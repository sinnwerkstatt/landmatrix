from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseHull(models.Model):
    deleted = models.BooleanField(default=False)
    deleted_comment = models.TextField(blank=True)

    # mainly for management/case_statistics
    first_created_at = models.DateTimeField()
    first_created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding and not self.first_created_at:
            self.first_created_at = timezone.now()
        super().save(*args, **kwargs)
