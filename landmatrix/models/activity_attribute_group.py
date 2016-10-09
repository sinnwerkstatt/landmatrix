from landmatrix.models.default_string_representation import DefaultStringRepresentation

#from simple_history.models import HistoricalRecords

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_hstore import hstore
from django.contrib.gis.db import models as geomodels

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityAttributeGroup(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Activity attribute group')
        verbose_name_plural = _('Activity attribute groups')

class ActivityAttributeBase(DefaultStringRepresentation, geomodels.Model):
    fk_group = models.ForeignKey(ActivityAttributeGroup, blank=True, null=True, verbose_name=_("Activity Attribute Group"))
    fk_language = models.ForeignKey("Language", blank=True, null=True, verbose_name=_("Language"))
    name = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(max_length=255, blank=True, null=True)
    value2 = models.TextField(max_length=255, blank=True, null=True)
    date = models.CharField(_("Year or Date"), max_length=10, blank=True, null=True, db_index=True)
    is_current = models.BooleanField(_("Is current"), blank=True, default=False)
    polygon = geomodels.MultiPolygonField(dim=2, srid=4326, spatial_index=True, blank=True, null=True)

    #objects = hstore.HStoreManager()
    #history = HistoricalRecords(bases=[HistoricalActivityAttribute])
    
    def __str__(self):
        return '%s: %s' % (self.name, self.value)

    class Meta:
        abstract = True

class ActivityAttribute(ActivityAttributeBase):
    """Just the attributes for most recent approved version of activites"""
    fk_activity = models.ForeignKey("Activity", verbose_name=_("Activity"), related_name="attributes")

    class Meta:
        verbose_name = _('Activity attribute')
        verbose_name_plural = _('Activity attributes')

class HistoricalActivityAttribute(ActivityAttributeBase):
    """All versions (including the current) of activity attributes"""
    fk_activity = models.ForeignKey("HistoricalActivity", verbose_name=_("Activity"), related_name="attributes")
    #history_date = models.DateTimeField(auto_now_add=True)
    #history_user = models.ForeignKey('auth.User', blank=True, null=True)

    class Meta:
        verbose_name = _('Historical activity attribute')
        verbose_name_plural = _('Historical activity attributes')
        get_latest_by = 'history_date'
