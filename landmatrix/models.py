from django.db import models
from django.utils.translation import ugettext_lazy as _

class Involvement(models.Model):

    investment_ratio = models.DecimalField(_("Investment ratio"), blank=True, null=True, max_digits=19, decimal_places=2)

    def __str__(self):
        return str(dict(filter(lambda item: not item[0].startswith('_'), vars(self).items())))
