from __future__ import unicode_literals

import logging

from django.conf import settings
from django.contrib.gis import gdal
from django.contrib.gis.geos import GEOSException, GEOSGeometry
from django.forms.widgets import Widget, TextInput
from django.template import loader
from django.utils import six, translation

logger = logging.getLogger('django.contrib.gis')


class BaseGeometryWidget(Widget):
    """
    The base class for rich geometry widgets.
    Renders a map using the WKT of the geometry.
    """
    geom_type = 'GEOMETRY'
    map_srid = 4326
    map_width = 600
    map_height = 400
    display_raw = False

    supports_3d = False
    toggle_map_display = False
    template_name = ''  # set on subclasses

    def __init__(self, attrs=None):
        self.attrs = {}
        defaults = (
            'geom_type', 'map_srid', 'map_width', 'map_height', 'display_raw',
            'toggle_map_display',
        )
        for key in defaults:
            self.attrs[key] = getattr(self, key)
        if attrs:
            self.attrs.update(attrs)

    def serialize(self, value):
        return value.wkt if value else ''

    def deserialize(self, value):
        try:
            return GEOSGeometry(value, self.map_srid)
        except (GEOSException, ValueError) as err:
            logger.error(
                "Error creating geometry from value '%s' (%s)", value, err)
        return None

    def get_context(self, name, value, attrs=None):
        # If a string reaches here (via a validation error on another
        # field) then just reconstruct the Geometry.
        if isinstance(value, six.string_types):
            value = self.deserialize(value)

        if value:
            # Check that srid of value and map match
            if value.srid != self.map_srid:
                try:
                    ogr = value.ogr
                    ogr.transform(self.map_srid)
                    value = ogr
                except gdal.GDALException as err:
                    logger.error(
                        "Error transforming geometry from srid '%s' to srid "
                        "'%s' (%s)", value.srid, self.map_srid, err)

        context = self.build_attrs(
            attrs,
            name=name,
            module='geodjango_%s' % name.replace('-', '_'),  # JS-safe
            serialized=self.serialize(value),
            geom_type=gdal.OGRGeomType(self.attrs['geom_type']),
            STATIC_URL=settings.STATIC_URL,
            LANGUAGE_BIDI=translation.get_language_bidi(),
        )

        # fallback if no id
        if 'id' not in context:
            context['id'] = name

        return context

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs=attrs)

        return loader.render_to_string(self.template_name, context)


class OpenLayersWidget(BaseGeometryWidget):
    template_name = 'gis/openlayers.html'

    class Media:
        css = {
            'all': (
                'css/ol.css',
            )
        }
        js = (
            'js/ol.js',
            'gis/js/OLMapWidget.js',
        )

    def serialize(self, value):
        return value.json if value else ''


class OSMWidget(OpenLayersWidget):
    """
    An OpenLayers/OpenStreetMap-based widget.
    """
    template_name = 'gis/openlayers-osm.html'
    default_lon = 5
    default_lat = 47
    default_zoom = 8

    def __init__(self, attrs=None):
        super(OSMWidget, self).__init__()
        for key in ('default_lon', 'default_lat', 'default_zoom'):
            self.attrs[key] = getattr(self, key)
        if attrs:
            self.attrs.update(attrs)

    @property
    def map_srid(self):
        # Use the official spherical mercator projection SRID when GDAL is
        # available; otherwise, fallback to 900913.
        if gdal.HAS_GDAL:
            return 3857
        else:
            return 900913


class MapWidget(OSMWidget):
    template_name = 'map_widget.html'
    default_lon = 0
    default_lat = 0
    default_zoom = 5
    geom_type = 'POINT'

    show_controls = True
    show_deals = False
    bound_location_field_id = None
    bound_target_country_field_id = None
    bound_lat_field_id = None
    bound_lon_field_id = None
    bound_level_of_accuracy_field_id = None

    def __init__(self, attrs=None):
        super().__init__(attrs=attrs)
        defaults = (
            'show_controls', 'show_deals', 'bound_location_field_id',
            'bound_lat_field_id', 'bound_lon_field_id',
            'bound_level_of_accuracy_field_id',
            'bound_target_country_field_id',
        )
        for key in defaults:
            self.attrs[key] = getattr(self, key)
        if attrs:
            self.attrs.update(attrs)

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs=attrs)
        if not self.attrs['show_controls']:
            context['disabled'] = True

        return context


class LocationWidget(TextInput):
    '''
    LocationWidget combines a map and a Google autocomplete location field.
    '''

    def __init__(self, *args, **kwargs):
        map_attrs = {}
        if 'map_attrs' in kwargs:
            map_attrs = kwargs.pop('map_attrs')

        super().__init__(*args, **kwargs)
        self.map_attrs = map_attrs

    def render(self, name, value, attrs=None):
        map_widget = MapWidget(attrs=self.map_attrs)
        map_name = '{}-map'.format(name)

        rendered_location = super().render(name, value, attrs=attrs)
        rendered_map = map_widget.render(map_name, None)
        output = '<div>{}</div><div>{}</div>'.format(
            rendered_location, rendered_map)

        return output
