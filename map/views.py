from grid.views.view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext
from grid.views.filter_widget_mixin import FilterWidgetMixin

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapView(TemplateView, FilterWidgetMixin):
    template_name = 'map/map.html'

    def _set_filters(self):
        self.current_formset_conditions = self.get_formset_conditions(
                self._filter_set(self.GET), self.GET, self.group, self.rules
        )

        self.filters = self.get_filter_context(
                self.current_formset_conditions, self._order_by(), self.group, self.group_value,
                self.GET.get("starts_with", None)
        )

    def _order_by(self, x=None):
        return x

    def dispatch(self, request, *args, **kwargs):

        self.request = request
        self.GET = request.GET
        self.group = []
        self.group_value = ""

        self._set_filters()

        context = self.get_context_data(**kwargs)
        context['request'] = request
        context['filters'] = self.filters
        return render_to_response(self.template_name, context, RequestContext(request))
