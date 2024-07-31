from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _
from apps.landmatrix.models.country import Country, Region


class UserRole(models.IntegerChoices):
    ANYBODY = 0, _("---------")
    REPORTER = 1, _("Reporter")
    EDITOR = 2, _("Editor")
    ADMINISTRATOR = 3, _("Administrator")


class User(AbstractUser):
    full_name = models.CharField(blank=True)
    phone = models.CharField(blank=True)
    information = models.TextField(blank=True)

    email_confirmed = models.BooleanField(default=False)

    country = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.PROTECT
    )
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.PROTECT)

    role = models.IntegerField(default=UserRole.ANYBODY, choices=UserRole.choices)

    class Meta:
        db_table = "auth_user"

    def save(self, *args, **kwargs):
        self.full_name = (
            f"{self.first_name} {self.last_name}".strip()
            if (self.first_name or self.last_name)
            else self.username
        )
        super().save(*args, **kwargs)
