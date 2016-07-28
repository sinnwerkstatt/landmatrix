from django.views.generic import TemplateView
from django.template import RequestContext

from grid.views.filter_widget_mixin import FilterWidgetMixin
from landmatrix.models.country import Country
from landmatrix.models.region import Region


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapView(FilterWidgetMixin, TemplateView):
    template_name = 'map/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Target country or region set?
        filters = self.request.session.get('filters')
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

        return context
