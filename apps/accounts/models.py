from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.landmatrix.models.country import Country, Region


class UserRole:
    ANYBODY = 0
    REPORTER = 1
    EDITOR = 2
    ADMINISTRATOR = 3


class User(AbstractUser):
    full_name = models.CharField(blank=True)
    phone = models.CharField(blank=True)
    information = models.TextField(blank=True)

    email_confirmed = models.BooleanField(default=False)

    country = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.PROTECT
    )
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.PROTECT)

    RoleChoices = (
        (UserRole.ANYBODY, "---------"),
        (UserRole.REPORTER, "Reporter"),
        (UserRole.EDITOR, "Editor"),
        (UserRole.ADMINISTRATOR, "Administrator"),
    )
    role = models.IntegerField(default=UserRole.ANYBODY, choices=RoleChoices)

    class Meta:
        db_table = "auth_user"

    def save(self, *args, **kwargs):
        self.full_name = (
            f"{self.first_name} {self.last_name}".strip()
            if (self.first_name or self.last_name)
            else ""
        )
        super().save(*args, **kwargs)
