from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.landmatrix.models.browse_rule import BrowseRule


class BrowseCondition(models.Model):

    rule = models.ForeignKey(BrowseRule, on_delete=models.CASCADE)
    variable = models.CharField(_("Variable"), max_length=20, choices=())
    operator = models.CharField(_("Operator"), max_length=20, choices=())
    value = models.CharField(_("Value"), max_length=1024)

    def __str__(self):
        return '{} {} {}'.format(self.variable, self.operator, self.value)
