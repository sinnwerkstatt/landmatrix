from django.contrib.gis.db import models as geomodels
from django.db import models
from django.utils.translation import gettext_lazy as _


class ActivityAttributeGroup(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Activity attribute group")
        verbose_name_plural = _("Activity attribute groups")


class ActivityAttributeBase(geomodels.Model):
    fk_group = models.ForeignKey(
        ActivityAttributeGroup,
        blank=True,
        null=True,
        verbose_name=_("Activity Attribute Group"),
        on_delete=models.SET_NULL,
    )
    fk_language = models.ForeignKey(
        "Language",
        blank=True,
        null=True,
        verbose_name=_("Language"),
        on_delete=models.SET_NULL,
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(max_length=255, blank=True, null=True)
    value2 = models.TextField(max_length=255, blank=True, null=True)
    date = models.CharField(
        _("Year or Date"), max_length=10, blank=True, null=True, db_index=True
    )
    is_current = models.BooleanField(_("Is current"), blank=True, default=False)
    polygon = geomodels.MultiPolygonField(
        dim=2, srid=4326, spatial_index=True, blank=True, null=True
    )

    # objects = hstore.HStoreManager()
    # history = HistoricalRecords(bases=[HistoricalActivityAttribute])

    def __str__(self):
        return "%s: %s" % (self.name, self.value)

    class Meta:
        abstract = True


class HistoricalActivityAttribute(ActivityAttributeBase):
    """All versions (including the current) of activity attributes"""

    fk_activity = models.ForeignKey(
        "HistoricalActivity",
        verbose_name=_("Activity"),
        related_name="attributes",
        on_delete=models.CASCADE,
    )
    # history_date = models.DateTimeField(default=timezone.now)
    # history_user = models.ForeignKey('auth.User', blank=True, null=True)

    class Meta:
        verbose_name = _("Historical activity attribute")
        verbose_name_plural = _("Historical activity attributes")
        get_latest_by = "history_date"

    def to_dict(self):
        return {
            "activity_id": self.fk_activity_id,
            "group_id": self.fk_group_id,
            "name": self.name,
            "value": self.value,
            "value2": self.value2,
            "date": self.date,
            "is_current": self.is_current,
            "polygon": self.polygon,
        }
