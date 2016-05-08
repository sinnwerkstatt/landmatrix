from landmatrix.models.country import Country
from landmatrix.models.region import Region

from django.db import models
from django.conf import settings


class UserRegionalInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    super_user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='super_user', blank=True, null=True)
    country = models.ManyToManyField(Country)
    region = models.ManyToManyField(Region)

    class Meta:
	    permissions = (
            ("editor", "Editor"),
            ("editor_filter", "Filter dashboard"),
        )

