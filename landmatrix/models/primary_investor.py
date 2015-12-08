__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from landmatrix.models.default_string_representation import DefaultStringRepresentation
from landmatrix.models.status import Status

# class PrimaryInvestor(DefaultStringRepresentation, models.Model):
#     primary_investor_identifier = models.IntegerField(_("Primary investor id"), db_index=True)
#     name = models.CharField(_("Name"), max_length=1024)
#     version = models.IntegerField(_("Version"), db_index=True)
#     fk_status = models.ForeignKey("Status", verbose_name=_("Status"))
