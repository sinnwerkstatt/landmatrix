from django.conf import settings
from django.db import models

from apps.landmatrix.models.country import Country, Region


class UserRegionalInfo(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, blank=True, null=True)
    information = models.TextField(blank=True, null=True)
    country = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.SET_NULL
    )
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (("editor", "Editor"), ("editor_filter", "Filter dashboard"))
