from django.contrib.gis.geos import MultiPolygon
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.grid.gis import *


class GridGISTestCase(TestCase):

    def setUp(self):
        file_names = ['shapefile.cpg', 'shapefile.dbf', 'shapefile.prj', 'shapefile.qpj', 'shapefile.shp',
                      'shapefile.shx']
        files = []
        for file_name in file_names:
            upload_file = open('apps/landmatrix/fixtures/shapefiles/%s' % file_name, 'rb')
            files.append(SimpleUploadedFile(file_name, upload_file.read(), content_type="text/plain"))
        self.files = files

    def test_parse_shapefile(self):
        polygons = parse_shapefile(self.files)
        self.assertIsInstance(polygons, MultiPolygon)

    def test_parse_shapefile_without_shp(self):
        del self.files[4]  # Remove .shp file
        with self.assertRaises(ValueError):
            polygons = parse_shapefile(self.files)

    def test_extract_polygons(self):
        polygons = extract_polygons('apps/landmatrix/fixtures/shapefiles/shapefile.shp')
        self.assertIsInstance(polygons, MultiPolygon)
