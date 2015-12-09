__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models.status import Status
from landmatrix.managers.stakeholder_manager import StakeholderManager

from django.db import models
from django.utils.translation import ugettext_lazy as _


# class Stakeholder(models.Model):
#
#     stakeholder_identifier = models.IntegerField(_("Stakeholder id"), db_index=True)
#     version = models.IntegerField(_("Version"), db_index=True)
#     fk_status = models.ForeignKey("Status", verbose_name=_("status"))
#
#     objects = StakeholderManager()
