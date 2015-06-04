from django.db import models
from django.utils.translation import ugettext_lazy as _

__author__ = 'lene'


class Stakeholder(models.Model):
    stakeholder_identifier = models.IntegerField(_("Stakeholder id"), db_index=True)
    version = models.IntegerField(_("Version"), db_index=True)