from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.translation import gettext as _
from nanoid import generate

from apps.landmatrix.models import choices
from apps.landmatrix.models.fields import NanoIDField
from apps.landmatrix.models.deal import DealVersion


class Location(models.Model):
    dealversion = models.ForeignKey(
        DealVersion, on_delete=models.CASCADE, related_name="locations"
    )
    nid = NanoIDField("ID", max_length=15, db_index=True)
    level_of_accuracy = models.CharField(
        _("Spatial accuracy level"),
        blank=True,
        choices=choices.LOCATION_ACCURACY_CHOICES,
    )
    name = models.CharField(_("Location"), blank=True)
    point = gis_models.PointField(_("Point"), blank=True, null=True)
    description = models.TextField(_("Description"), blank=True)
    facility_name = models.CharField(_("Facility name"), blank=True)
    comment = models.TextField(_("Comment"), blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding and not self.nid:
            self.nid = generate(size=8)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]

    def __str__(self):
        return f"{self.nid} @ {self.dealversion}"
