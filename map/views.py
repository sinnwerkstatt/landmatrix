from grid.views.view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext
from grid.views.filter_widget_mixin import FilterWidgetMixin

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapView(TemplateView, FilterWidgetMixin):
    template_name = 'map/map.html'

    def _set_filters(self, GET):
        self.current_formset_conditions = self.get_formset_conditions(self._filter_set(GET), GET)
        self.filters = self.get_filter_context(self.current_formset_conditions)

    def dispatch(self, request, *args, **kwargs):

        self._set_filters(request.GET)

        context = self.get_context_data(**kwargs)
        self.add_filter_context_data(context, request)

        return render_to_response(self.template_name, context, RequestContext(request))
