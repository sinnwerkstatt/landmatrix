from django.db import models
from django.conf import settings

from landmatrix.models import Country, Region


class UserRegionalInfo(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, blank=True, null=True)
    information = models.TextField(blank=True, null=True)
    super_user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='super_user',
        blank=True, null=True)
    country = models.ManyToManyField(Country, blank=True)
    region = models.ManyToManyField(Region, blank=True)

    class Meta:
        permissions = (
            ("editor", "Editor"),
            ("editor_filter", "Filter dashboard"),
        )