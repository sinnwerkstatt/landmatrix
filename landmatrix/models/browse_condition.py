from django.db import models
from django.utils.translation import ugettext_lazy as _
from landmatrix.models.browse_rule import BrowseRule

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class BrowseCondition(models.Model):
    rule = models.ForeignKey(BrowseRule)
    variable = models.CharField(_("Variable"), max_length=20, choices=())
    operator = models.CharField(_("Operator"), max_length=20, choices=())
    value = models.CharField(_("Value"), max_length=1024)

    def __str__(self):
        return '{} {} {}'.format(self.variable, self.operator, self.value)