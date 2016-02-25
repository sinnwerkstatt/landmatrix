
from grid.views.view_aux_functions import render_to_response

from django.views.generic.base import TemplateView
from django.template import RequestContext


class ChartView(TemplateView):
    chart = ""

    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['request'] = request
        return render_to_response(self.template_name, context, RequestContext(request))

    def get_context_data(self, **kwargs):
        context = super(ChartView, self).get_context_data(**kwargs)
        context.update({
            "view": "chart view",
            "chart": self.chart
        })
        return context


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