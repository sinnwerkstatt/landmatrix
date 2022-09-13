from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.landmatrix.models.country import Country, Region


class User(AbstractUser):
    full_name = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    information = models.TextField(blank=True)

    email_confirmed = models.BooleanField(default=False)

    country = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.PROTECT
    )
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.PROTECT)

    UserLevelChoices = (
        (0, "---------"),
        (1, "Reporter"),
        (2, "Editor"),
        (3, "Administrator"),
    )
    level = models.IntegerField(default=0, choices=UserLevelChoices)

    class Meta:
        db_table = "auth_user"

    def save(self, *args, **kwargs):
        self.full_name = (
            f"{self.first_name} {self.last_name}".strip()
            if (self.first_name or self.last_name)
            else ""
        )
        super().save(*args, **kwargs)
