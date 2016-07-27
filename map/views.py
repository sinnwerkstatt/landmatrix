from grid.views.view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext

from grid.views.filter_widget_mixin import FilterWidgetMixin
from landmatrix.models.country import Country
from landmatrix.models.region import Region

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapView(TemplateView, FilterWidgetMixin):
    template_name = 'map/map.html'

    def _set_filters(self):
        data = self.request.GET.copy()
        self.current_formset_conditions = self.get_formset_conditions(self._filter_set(data), data)
        self.filters = self.get_filter_context(self.current_formset_conditions)

    def dispatch(self, request, *args, **kwargs):

        self._set_filters()

        context = self.get_context_data(**kwargs)
        self.add_filter_context_data(context, request)

        # Target country or region set?
        filters = request.session.get('filters') or []
        if 'Target country' in filters:
            try:
                context['country'] = Country.objects.get(pk=filters['Target country']['value'])
            except:
                pass
        if 'Target region' in filters:
            try:
                context['region'] = Country.objects.get(pk=filters['Target region']['value'])
            except:
                pass

        return render_to_response(self.template_name, context, RequestContext(request))
