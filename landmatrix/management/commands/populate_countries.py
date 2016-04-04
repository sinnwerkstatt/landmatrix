#!/usr/bin/env python
import os
import sys
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Populates the country bounding boxes for zooming in the map'

    def handle(self, *args, **options):
        from landmatrix.models.country import Country
        from country_bounding_boxes import country_subunits_by_iso_code

        def findBounds(boxes, counter, country):
            if len(boxes) > 100:
                counter += 1
                min_lat = 180
                min_lon = 90
                max_lat = -180
                max_lon = -90
                for bb in boxes:
                    if bb[0] < min_lat:
                        min_lat = bb[0]
                    if bb[1] < min_lon:
                        min_lon = bb[1]
                    if bb[2] > max_lat:
                        max_lat = bb[2]
                    if bb[3] > max_lon:
                        max_lon = bb[3]
            else:
                try:
                    bb = boxes[0]
                    min_lat = bb[0]
                    min_lon = bb[1]
                    max_lat = bb[2]
                    max_lon = bb[3]
                except:
                    print(country, "..is bad.")

            try:

                country.point_lat_max = max_lat
                country.point_lon_max = max_lon
                country.point_lat_min = min_lat
                country.point_lon_min = min_lon
                country.save()
            except:
                print(country, "..is bad, too.")
                counter += 1

            return counter

        counter = 0
        whole = 0
        for country in Country.objects.all():
            whole += 1
            boxes = [c.bbox for c in country_subunits_by_iso_code(country.code_alpha3)]
            counter = findBounds(boxes, counter, country)

        print("%i of %i countries with borked borders." % (counter, whole))
