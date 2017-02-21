import collections
import json

from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from grid.views.filter_widget_mixin import FilterWidgetMixin
from landmatrix.models.country import Country
from landmatrix.models.region import Region
from wagtailcms.models import WagtailRootPage


class GlobalView(FilterWidgetMixin, RedirectView):
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        self.remove_country_region_filter()
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        return '/'


class MapSettingsMixin:

    @staticmethod
    def get_legend():

        return collections.OrderedDict({
            'implementation': {
                'label': _('Implementation status'),
                'attributes': [
                    {
                        'label': _('Project not started'),
                        'id': 'not_started',
                        'color': '#1D6914'
                    },
                    {
                        'label': _('Startup phase (no production)'),
                        'id': 'startup',
                        'color': '#2A4BD7'
                    },
                    {
                        'label': _('In operation (production)'),
                        'id': 'in_operation',
                        'color': '#575757'
                    },
                    {
                        'label': _('Project abandoned'),
                        'id': 'abandoned',
                        'color': '#AD2323'
                    },
                    {
                        'label': _('Unknown'),
                        'id': 'unknown',
                        'color': '#81C57A'
                    }
                ]
            },
            'intention': {
                'label': _('Intention of investment'),
                'attributes': [
                    {
                        'label': _('Agriculture'),
                        'id': 'agriculture',
                        'color': '#1D6914'
                    },
                    {
                        'label': _('Forestry'),
                        'id': 'forestry',
                        'color': '#2A4BD7'
                    },
                    {
                        'label': _('Mining'),
                        'id': 'mining',
                        'color': '#814A19'
                    },
                    {
                        'label': _('Tourism'),
                        'id': 'tourism',
                        'color': '#9DAFFF'
                    },
                    {
                        'label': _('Industry'),
                        'id': 'industry',
                        'color': '#AD2323'
                    },
                    {
                        'label': _('Conservation'),
                        'id': 'conservation',
                        'color': '#575757'
                    },
                    {
                        'label': _('Renewable Energy'),
                        'id': 'renewable_energy',
                        'color': '#81C57A'
                    },
                    {
                        'label': _('Other'),
                        'id': 'other',
                        'color': '#8126C0'
                    }
                ]
            }
        })


class MapView(MapSettingsMixin, FilterWidgetMixin, TemplateView):
    template_name = 'map/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'legend': self.get_legend(),
            'legend_json': json.dumps(self.get_legend())
        })

        # Target country or region set?
        filters = self.request.session.get('filters', {})
        if 'Target country' in filters:
            target_country_id = filters['Target country']['value']
            try:
                context['country'] = Country.objects.get(pk=target_country_id)
            except (Country.DoesNotExist, ValueError):
                pass
        if 'Target region' in filters:
            target_region_id = filters['Target region']['value']
            try:
                context['region'] = Region.objects.get(pk=target_region_id)
            except (Region.DoesNotExist, ValueError):
                pass
        root = WagtailRootPage.objects.first()
        if root.map_introduction:
            context['introduction'] = root.map_introduction

        return context
