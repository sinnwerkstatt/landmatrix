from grid.views.filter_widget_mixin import FilterWidgetMixin
from grid.views.view_aux_functions import render_to_response

from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.template import RequestContext

from charts.pdfgen import pdfize_url


class ChartView(TemplateView, FilterWidgetMixin):
    chart = ""

    def dispatch(self, request, *args, **kwargs):
        self._set_filters(request.GET)
        context = self.get_context_data(**kwargs)
        self.add_filter_context_data(context, request)

        if 'is_pdf_export' in kwargs and kwargs['is_pdf_export'] is True:
            chart_url = request.build_absolute_uri(reverse(self.chart))
            pdf_filename = "{}.pdf".format(self.chart)
            response = pdfize_url(chart_url, pdf_filename)
        else:
            response = render_to_response(self.template_name, context,
                                          RequestContext(request))

        return response

    def get_context_data(self, **kwargs):
        context = super(ChartView, self).get_context_data(**kwargs)
        context.update({
            "view": "chart view",
            "export_formats": ("XML", "CSV", "XLS", "PDF"),
            "chart": self.chart,
            # Use the convention 'chart_name_pdf' for PDF exports
            "pdf_chart_url": "{}_pdf".format(self.chart),
        })
        return context

    def _set_filters(self, GET):
        self.current_formset_conditions = self.get_formset_conditions(
            self._filter_set(GET), GET)
        self.filters = self.get_filter_context(self.current_formset_conditions)


class OverviewChartView(ChartView):
    template_name = "charts/overview.html"
    chart = "chart_overview"


class TransnationalDealsChartView(ChartView):
    template_name = "charts/transnational-deals.html"
    chart = "chart_transnational_deals"


class MapOfInvestmentsChartView(ChartView):
    template_name = "charts/investor-target-countries.html"
    chart = "chart_map_of_investments"


class AgriculturalDriversChartView(ChartView):
    template_name = "charts/agricultural-produce.html"
    chart = "chart_agricultural_drivers"


class PerspectiveChartView(ChartView):
    template_name = "charts/perspective.html"
    chart = "chart_perspective"
