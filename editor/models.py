from landmatrix.models.country import Country
from landmatrix.models.region import Region

from django.db import models
from django.contrib.auth.models import User


class UserRegionalInfo(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
#    super_user = models.OneToOneField(User, related_name='super_user', blank=True, null=True)
    country = models.ManyToManyField(Country)
    region = models.ManyToManyField(Region)

