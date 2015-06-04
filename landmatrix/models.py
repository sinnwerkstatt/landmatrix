from django.db import models
from django.utils.translation import ugettext_lazy as _

""" Needs to be the first class inherited from when using it for multiple inheritance,
    if the other classes define a ___str___ method too the implementation of the class
    first in the list of base classes is used.
"""
class DefaultStringRepresentation:
    def __str__(self):
        return str(dict(filter(lambda item: not item[0].startswith('_'), vars(self).items())))

class Involvement(DefaultStringRepresentation, models.Model):
    investment_ratio = models.DecimalField(_("Investment ratio"), blank=True, null=True, max_digits=19, decimal_places=2)

class Activity(DefaultStringRepresentation, models.Model):
    activity_identifier = models.IntegerField(_("Activity identifier"), db_index=True)
    version = models.IntegerField(_("Version"), db_index=True)
    availability = models.FloatField(_("availability"), blank=True, null=True)
    fully_updated = models.DateTimeField(_("Fully updated"), blank=True, null=True)

class Stakeholder(models.Model):
    id = models.AutoField(primary_key=True)
    stakeholder_identifier = models.IntegerField(_("Stakeholder id"), db_index=True)
    version = models.IntegerField(_("Version"), db_index=True)
