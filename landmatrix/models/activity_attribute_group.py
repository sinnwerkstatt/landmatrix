__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_hstore import hstore
from landmatrix.models.default_string_representation import DefaultStringRepresentation

class ActivityAttributeGroup(DefaultStringRepresentation, models.Model):
    fk_activity = models.ForeignKey("Activity", verbose_name=_("Activity"))
#    fk_language = models.ForeignKey("Language", verbose_name=_("Language"))
    year = models.PositiveIntegerField(_("Year"), blank=True, null=True, db_index=True)
    attributes = hstore.DictionaryField(db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    # TODO: Add geometry (location point)

    objects = hstore.HStoreManager()
