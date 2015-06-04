from django.db import models
from django.utils.translation import ugettext_lazy as _
from landmatrix.models.default_string_representation import DefaultStringRepresentation

__author__ = 'lene'


class Involvement(DefaultStringRepresentation, models.Model):
    investment_ratio = models.DecimalField(_("Investment ratio"), blank=True, null=True, max_digits=19, decimal_places=2)