from django.urls import reverse
from django.views.generic.base import RedirectView, TemplateView

from apps.grid.views.filter import FilterWidgetMixin
from apps.landmatrix.pdfgen import PDFViewMixin


class BaseChartView(FilterWidgetMixin, TemplateView):
    chart = ""
    disabled_presets = []
    enabled_presets = []

    def get_context_data(self, **kwargs):
        context = super(BaseChartView, self).get_context_data(**kwargs)
        context.update(
            {
                "view": "chart view",
                "export_formats": ("XML", "CSV", "XLS"),
                "chart": self.chart,
            }
        )

        return context


class BaseChartPDFView(PDFViewMixin, BaseChartView):
    chart = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["export_formats"] = context["export_formats"] + ("PDF",)

        return context

    def get_pdf_filename(self, request, *args, **kwargs):
        return "{}.pdf".format(self.chart)

    def get_pdf_export_url(self, request, *args, **kwargs):
        return reverse("{}_pdf".format(self.chart))

    def get_pdf_render_url(self, request, *args, **kwargs):
        return reverse(self.chart)


class ChartRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if "country" in self.request.GET or "region" in self.request.GET:
            base_url = "chart_intention"
        else:
            base_url = "chart_transnational_deals"

        url = reverse(base_url)
        if self.request.GET:
            url += "?{}".format(self.request.GET.urlencode())

        return url


class IntentionChartView(BaseChartPDFView):
    template_name = "charts/overview/intention.html"
    chart = "chart_intention"
    # This page needs a massive delay for some reason
    pdf_javascript_delay = 4000


class NegotiationStatusChartView(BaseChartPDFView):
    template_name = "charts/overview/negotiation_status.html"
    chart = "chart_negotiation_status"
    # This page needs a massive delay for some reason
    pdf_javascript_delay = 4000
    disabled_presets = [2]


class ImplementationStatusChartView(BaseChartPDFView):
    template_name = "charts/overview/implementation_status.html"
    chart = "chart_implementation_status"
    # This page needs a massive delay for some reason
    pdf_javascript_delay = 4000


class IntentionAgricultureChartView(BaseChartPDFView):
    template_name = "charts/overview/intention-agriculture.html"
    chart = "chart_intention_agriculture"
    # This page needs a massive delay for some reason
    pdf_javascript_delay = 4000


class TransnationalDealsChartView(BaseChartPDFView):
    template_name = "charts/transnational-deals.html"
    chart = "chart_transnational_deals"


class MapOfInvestmentsChartView(BaseChartPDFView):
    template_name = "charts/investor-target-countries.html"
    chart = "chart_map_of_investments"
    pdf_javascript_delay = 2000


class PerspectiveChartView(BaseChartPDFView):
    template_name = "charts/perspective.html"
    chart = "chart_perspective"


class AgriculturalDriversChartView(BaseChartPDFView):
    template_name = "charts/special-interest/agricultural-drivers.html"
    chart = "chart_agricultural_drivers"
    pdf_javascript_delay = 10000


class ProduceInfoChartView(BaseChartPDFView):
    template_name = "charts/special-interest/produce-info.html"
    chart = "chart_produce_info"
    pdf_javascript_delay = 10000


class MiningChartView(BaseChartPDFView):
    template_name = "charts/special-interest/mining.html"
    chart = "chart_mining"
    pdf_javascript_delay = 10000
    disabled_presets = [1, 2]


class LoggingChartView(BaseChartPDFView):
    template_name = "charts/special-interest/logging.html"
    chart = "chart_logging"
    pdf_javascript_delay = 10000
    disabled_presets = [2, 15]


class ContractFarmingChartView(BaseChartPDFView):
    template_name = "charts/special-interest/contract-farming.html"
    chart = "chart_contract_farming"
    pdf_javascript_delay = 10000
