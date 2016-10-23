import os
from tempfile import TemporaryDirectory

from django.contrib.gis.gdal import DataSource, GDALException
from django.contrib.gis.gdal.geometries import MultiPolygon as GDALMultiPolygon
from django.contrib.gis.gdal.geomtype import OGRGeomType
from django.contrib.gis.geos import GEOSGeometry


def parse_shapefile(files):
    '''
    Takes shapefiles (in memory or temp) and returns MultiPolygon
    suitable for saving to the DB.

    Any problems with the shapefile raise ValueError.

    We don't check for unknown extensions as there are quite a few optional
    ones.
    '''
    required_extensions = ('shp', 'shx', 'dbf')
    extensions = [file_obj.name[-3:] for file_obj in files]
    if set(required_extensions).difference(set(extensions)):
        raise ValueError('SHP, SHX, and DBF files are required')

    clean_polygons = None

    # we need to preserve the original filenames (or at least make them match)
    # because shapefiles are actually 3 files with different extensions
    with TemporaryDirectory() as temp_dir:
        shapefile_path = None
        for file_obj in files:
            file_name = file_obj.name
            file_extension = file_name[-3:].lower()
            full_path = os.path.join(temp_dir, file_name)

            temp_file = open(full_path, 'wb')
            for chunk in file_obj.chunks():
                temp_file.write(chunk)

            if file_extension == 'shp':
                shapefile_path = full_path

        if shapefile_path is None:
            raise ValueError('A file with the extension shp is required')

        clean_polygons = extract_polygons(shapefile_path)

    if len(clean_polygons) == 0:
        raise ValueError('No polygons found in shapefile.')

    return clean_polygons


def extract_polygons(shapefile_path):
    '''
    Given an (existing, saved to disk) shapefile, retrieve all polygons as
    one MultiPolygon.
    '''
    clean_polygons = GDALMultiPolygon(OGRGeomType('MultiPolygon'))  # empty

    try:
        data_source = DataSource(shapefile_path)

        for layer in data_source:
            if layer.geom_type.name in ('Polygon', 'MultiPolygon'):
                for feature in layer:
                    clean_polygons.add(feature.geom)

    except GDALException as err:
        message = str(err)
        # Make sure we don't expose the confusing file path
        message = message.replace('at "{}"'.format(shapefile_path), '')
        raise ValueError(message)

    # Convert from GDAL MultiPolygon to GEOS MultiPolygon. sheesh.
    geos_polygon = GEOSGeometry(clean_polygons.wkt)

    return geos_polygon
