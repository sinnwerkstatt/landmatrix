import contextlib

import collections
import json

from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from grid.views.filter import FilterWidgetMixin
from landmatrix.models.country import Country
from landmatrix.models.region import Region
from wagtailcms.models import WagtailRootPage


class MapSettingsMixin:

    @staticmethod
    def get_legend():

        return collections.OrderedDict({
            'implementation': {
                'label': _('Implementation status'),
                'attributes': [
                    {
                        'label': _('Project not started'),
                        'id': 'Project not started',
                        'color': '#1D6914'
                    },
                    {
                        'label': _('Startup phase (no production)'),
                        'id': 'Startup phase (no production)',
                        'color': '#2A4BD7'
                    },
                    {
                        'label': _('In operation (production)'),
                        'id': 'In operation (production)',
                        'color': '#575757'
                    },
                    {
                        'label': _('Project abandoned'),
                        'id': 'Project abandoned',
                        'color': '#AD2323'
                    },
                    {
                        'label': _('Unknown'),
                        'id': 'Unknown',
                        'color': '#bab8b8'
                    }
                ]
            },
            'intention': {
                'label': _('Intention of investment'),
                'attributes': [
                    {
                        'label': _('Agriculture'),
                        'id': 'Agriculture',
                        'color': '#1D6914'
                    },
                    {
                        'label': _('Forestry'),
                        'id': 'Forestry',
                        'color': '#2A4BD7'
                    },
                    {
                        'label': _('Mining'),
                        'id': 'Mining',
                        'color': '#814A19'
                    },
                    {
                        'label': _('Tourism'),
                        'id': 'Tourism',
                        'color': '#9DAFFF'
                    },
                    {
                        'label': _('Industry'),
                        'id': 'Industry',
                        'color': '#AD2323'
                    },
                    {
                        'label': _('Conservation'),
                        'id': 'Conservation',
                        'color': '#575757'
                    },
                    {
                        'label': _('Renewable Energy'),
                        'id': 'Renewable Energy',
                        'color': '#81C57A'
                    },
                    {
                        'label': _('Other'),
                        'id': 'Other',
                        'color': '#8126C0'
                    },
                    {
                        'label': _('Unknown'),
                        'id': 'Unknown',
                        'color': '#bab8b8'
                    }
                ]
            },
            'level_of_accuracy': {
                'label': _('Spatial accuracy'),
                'attributes': [
                    {
                        'label': _('Country'),
                        'id': 'Country',
                        'color': '#1D6914'
                    },
                    {
                        'label': _('Administrative region'),
                        'id': 'Administrative region',
                        'color': '#8126C0'
                    },
                    {
                        'label': _('Approximate location'),
                        'id': 'Approximate location',
                        'color': '#575757'
                    },
                    {
                        'label': _('Exact location'),
                        'id': 'Exact location',
                        'color': '#AD2323'
                    },
                    {
                        'label': _('Coordinates'),
                        'id': 'Coordinates',
                        'color': '#814A19'
                    },
                    {
                        'label': _('Unknown'),
                        'id': 'Unknown',
                        'color': '#bab8b8'
                    }
                ]
            }
        })

    @staticmethod
    def get_polygon_layers():
        return collections.OrderedDict({
            'contract_area': {
                'label': _('Contract area'),
                'color': '#575757',
                'url': reverse('polygon_geom_api', kwargs={
                    'polygon_field': 'contract_area'}),
            },
            'intended_area': {
                'label': _('Intended area'),
                'color': '#AD2323',
                'url': reverse('polygon_geom_api', kwargs={
                    'polygon_field': 'intended_area'}),
            },
            'production_area': {
                'label': _('Area in production'),
                'color': '#1D6914',
                'url': reverse('polygon_geom_api', kwargs={
                    'polygon_field': 'production_area'}),
            },
        })


class MapView(MapSettingsMixin, FilterWidgetMixin, TemplateView):

    template_name = 'map/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'legend': self.get_legend(),
            'legend_json': json.dumps(self.get_legend()),
            'polygon_layers': self.get_polygon_layers(),
            'polygon_layers_json': json.dumps(self.get_polygon_layers()),
        })

        # Target country or region set?
        filters = self.request.session.get('deal:filters', {})
        if 'country' in filters:
            target_country_id = filters['country']['value']
            with contextlib.suppress(Country.DoesNotExist, ValueError):
                context['map_object'] = Country.objects.defer('geom').get(pk=target_country_id)
                context['is_country'] = True

        if 'region' in filters:
            target_region_id = filters['region']['value']
            with contextlib.suppress(Region.DoesNotExist, ValueError):
                context['map_object'] = Region.objects.get(pk=target_region_id)

        root = WagtailRootPage.objects.first()
        if root.map_introduction:
            context['introduction'] = root.map_introduction

        return context
