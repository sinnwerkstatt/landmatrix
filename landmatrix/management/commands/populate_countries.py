#!/usr/bin/env python
from django.core.management import BaseCommand
from django.contrib.gis.geos import Polygon, GeometryCollection
from country_bounding_boxes import country_subunits_by_iso_code

from landmatrix.models.country import Country


def find_bounds(country_obj):
    bounding_boxes = [
        c.bbox for c in country_subunits_by_iso_code(country_obj.code_alpha3)]

    if not bounding_boxes:
        message = 'No data found for country code {}'.format(
            country_obj.code_alpha3)
        raise ValueError(message)

    polygons = []
    for box in bounding_boxes:
        x1, y1, x2, y2 = box
        polygon = Polygon.from_bbox((x1, y1, x2, y2))
        polygons.append(polygon)

    collection = GeometryCollection(*polygons)
    return collection.extent


class Command(BaseCommand):
    help = 'Populates the country bounding boxes for zooming in the map'

    def handle(self, *args, **options):
        for country in Country.objects.all():
            try:
                bounds = find_bounds(country)
            except ValueError as exc:
                print(str(exc))
            country.point_lon_min = bounds[0]
            country.point_lat_min = bounds[1]
            country.point_lon_max = bounds[2]
            country.point_lat_max = bounds[3]

            country.save()

            message = "Updated bounds for country {country.name}: ({country.point_lon_min}, {country.point_lat_min}), ({country.point_lon_max}, {country.point_lat_max})".format(country=country)
            print(message)
