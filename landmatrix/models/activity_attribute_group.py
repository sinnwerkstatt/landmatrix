from landmatrix.models.default_string_representation import DefaultStringRepresentation

from simple_history.models import HistoricalRecords

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_hstore import hstore
from django.contrib.gis.db import models as geomodels

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityAttributeGroup(DefaultStringRepresentation, models.Model):
    fk_activity = models.ForeignKey("Activity", verbose_name=_("Activity"))
    fk_language = models.ForeignKey("Language", verbose_name=_("Language"))
    date = models.DateField(_("Date"), blank=True, null=True, db_index=True)
    attributes = hstore.DictionaryField(db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    polygon = geomodels.MultiPolygonField(dim=2, srid=4326, spatial_index=True, blank=True, null=True)

    objects = hstore.HStoreManager()
    history = HistoricalRecords()
