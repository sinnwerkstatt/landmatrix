__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_hstore import hstore
from landmatrix.models.default_string_representation import DefaultStringRepresentation

class StakeholderAttributeGroup(DefaultStringRepresentation, models.Model):
    fk_stakeholder = models.ForeignKey("Stakeholder", verbose_name=_("Stakeholder"))
#    fk_language = models.ForeignKey("Language", verbose_name=_("Language"))
    attributes = hstore.DictionaryField(db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    objects = hstore.HStoreManager()
