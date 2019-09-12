#!/usr/bin/env python
import os
import sys
import zipfile
from io import BytesIO

import errno
import requests
import shutil

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon
from django.core.management import BaseCommand

from apps.landmatrix import settings
from apps.landmatrix.models import Country


class Command(BaseCommand):
    help = 'Populates the countries with shape geometries (from biogeo.ucdavis.edu)'

    def handle(self, *args, **options):

        countries = Country.objects.all()
        shp_base_url = 'http://biogeo.ucdavis.edu/data/gadm2.8/shp/{}_adm_shp.zip'
        shp_base_filename = '{}_adm0.shp'

        temp_dir_path = os.path.join(settings.BASE_DIR, 'temp_geom_import')
        create_folder(temp_dir_path)

        for country in countries:
            if not country.code_alpha3:
                continue

            print("\n\n*** Currently processing country {} ...".format(country))
            response = requests.get(shp_base_url.format(country.code_alpha3.upper()))
            file = zipfile.ZipFile(BytesIO(response.content))
            file.extractall(path=temp_dir_path)

            shp_filename = shp_base_filename.format(country.code_alpha3.upper())
            ds = DataSource(os.path.join(temp_dir_path, shp_filename))
            if ds.layer_count != 1:
                raise Exception('There should be exactly 1 layer in the SHP file!')

            layer = ds[0]

            geoms = layer.get_geoms(geos=True)
            if len(geoms) != 1:
                raise Exception('There should be exactly one geometry')

            # Geometry is either a MultiPolygon already. Or it is a Polygon, in
            # which case it needs to be transferred to a MultiPolygon
            geometry = geoms[0]
            if geometry.geom_type == 'Polygon':
                geometry = MultiPolygon(geometry)

            country.geom = geometry
            country.save()

            delete_all_files_in_folder(temp_dir_path)

        delete_folder(temp_dir_path)


def create_folder(folder_path):
    # http://stackoverflow.com/a/600612/841644
    try:
        os.makedirs(folder_path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(folder_path):
            pass
        else:
            raise


def delete_folder(folder_path):
    # http://stackoverflow.com/a/303225/841644
    shutil.rmtree(folder_path)


def delete_all_files_in_folder(folder_path):
    # http://stackoverflow.com/a/185941/841644
    for the_file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
