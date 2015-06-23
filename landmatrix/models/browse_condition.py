__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from landmatrix.models import DefaultStringRepresentation, BrowseRule

class BrowseCondition(models.Model, DefaultStringRepresentation):
    rule = models.ForeignKey(BrowseRule)
    variable = models.CharField(_("Variable"), max_length=20, choices=())
    operator = models.CharField(_("Operator"), max_length=20, choices=())
    value = models.CharField(_("Variable"), max_length=1024)
