import json

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from django.contrib.gis.geos.prototypes.io import wkt_w
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from apps.landmatrix.models import choices
from apps.landmatrix.models.fields import NanoIDField, LooseDateField
from apps.landmatrix.models.deal.location import Location


class Area(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="areas"
    )
    nid = NanoIDField("ID", max_length=15, db_index=True)
    type = models.CharField(choices=choices.AREA_TYPE_CHOICES)
    current = models.BooleanField(default=False)
    date = LooseDateField(_("Date"), blank=True, null=True)
    area = gis_models.MultiPolygonField()

    def __str__(self):
        return f"{self.location} >> {self.type}"

    # NOTE: Not in use, but would be nice to query features from backend directly
    def to_feature(self):
        return {
            "type": "Feature",
            "geometry": json.loads(self.area.geojson) if self.area else None,
            "properties": {
                "id": self.id,
                "type": self.type,
                "current": self.current,
                "date": self.date,
            },
        }

    @staticmethod
    def geometry_to_multipolygon(geom: GEOSGeometry | str | dict) -> MultiPolygon:
        if isinstance(geom, dict):
            geom = str(geom)
        if isinstance(geom, str):
            geom = GEOSGeometry(geom)
        if geom.hasz:
            wkt = wkt_w(dim=2).write(geom).decode()
            geom = GEOSGeometry(wkt, srid=4674)
        if isinstance(geom, MultiPolygon):
            return geom
        elif isinstance(geom, Polygon):
            return MultiPolygon([geom])

        raise ValidationError

    class Meta:
        # unique_together = ["location", "type", "current"]
        ordering = ["id"]
