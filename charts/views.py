import copy

from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic.base import RedirectView

from landmatrix.pdfgen import PDFViewMixin
from grid.views.filter_widget_mixin import FilterWidgetMixin


class ChartView(FilterWidgetMixin, TemplateView):
    chart = ""
    disabled_presets = []
    enabled_presets = []

    def get_context_data(self, **kwargs):
        context = super(ChartView, self).get_context_data(**kwargs)
        context.update({
            "view": "chart view",
            "export_formats": ("XML", "CSV", "XLS"),
            "chart": self.chart,
        })

        return context


class ChartPDFView(PDFViewMixin, ChartView):
    chart = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['export_formats'] = context['export_formats'] + ('PDF',)

        return context

    def get_pdf_filename(self, request, *args, **kwargs):
        return '{}.pdf'.format(self.chart)

    def get_pdf_export_url(self, request, *args, **kwargs):
        return reverse('{}_pdf'.format(self.chart))

    def get_pdf_render_url(self, request, *args, **kwargs):
        return reverse(self.chart)


class ChartRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if 'country' in self.request.GET or 'region' in self.request.GET:
            base_url = 'chart_intention'
        else:
            base_url = 'chart_transnational_deals'

        url = reverse(base_url)
        if self.request.GET:
            url += '?{}'.format(self.request.GET.urlencode())

        return url


class IntentionChartView(ChartPDFView):
    template_name = "charts/overview/intention.html"
    chart = "chart_intention"
    # This page needs a massive delay for some reason
    pdf_javascript_delay = 4000


class NegotiationStatusChartView(ChartPDFView):
    template_name = "charts/overview/negotiation_status.html"
    chart = "chart_negotiation_status"
    # This page needs a massive delay for some reason
    pdf_javascript_delay = 4000


class ImplementationStatusChartView(ChartPDFView):
    template_name = "charts/overview/implementation_status.html"
    chart = "chart_implementation_status"
    # This page needs a massive delay for some reason
    pdf_javascript_delay = 4000


class IntentionAgricultureChartView(ChartPDFView):
    template_name = "charts/overview/intention-agriculture.html"
    chart = "chart_intention_agriculture"
    # This page needs a massive delay for some reason
    pdf_javascript_delay = 4000


class TransnationalDealsChartView(ChartPDFView):
    template_name = "charts/transnational-deals.html"
    chart = "chart_transnational_deals"


class MapOfInvestmentsChartView(ChartPDFView):
    template_name = "charts/investor-target-countries.html"
    chart = "chart_map_of_investments"
    pdf_javascript_delay = 2000


class PerspectiveChartView(ChartView):
    template_name = "charts/perspective.html"
    chart = "chart_perspective"


#class SpecialInterestView(ChartPDFView):
#    template_name = "charts/special-interest.html"
#    chart = "special_interest"
#    pdf_javascript_delay = 10000
#
#    def get_pdf_export_url(self, request, *args, **kwargs):
#        '''
#        Special handling for the 'variable' switch
#        '''
#        url = super().get_pdf_export_url(request, *args, **kwargs)
#        if 'variable' in request.GET:
#            url += '?variable={}'.format(request.GET['variable'])
#
#        return url
#
#    def get_pdf_render_url(self, request, *args, **kwargs):
#        '''
#        Special handling for the 'variable' switch
#        '''
#        url = super().get_pdf_render_url(request, *args, **kwargs)
#        if 'variable' in request.GET:
#            url += '?variable={}'.format(request.GET['variable'])
#
#        return url

class AgriculturalDriversChartView(ChartPDFView):
    template_name = "charts/special-interest/agricultural-drivers.html"
    chart = "chart_agricultural_drivers"
    pdf_javascript_delay = 10000

class ProduceInfoChartView(ChartPDFView):
    template_name = "charts/special-interest/produce-info.html"
    chart = "chart_produce_info"
    pdf_javascript_delay = 10000

class MiningChartView(ChartPDFView):
    template_name = "charts/special-interest/mining.html"
    chart = "chart_mining"
    pdf_javascript_delay = 10000
    disabled_presets = [1,2]

class LoggingChartView(ChartPDFView):
    template_name = "charts/special-interest/logging.html"
    chart = "chart_logging"
    pdf_javascript_delay = 10000
    disabled_presets = [2,15]

class ContractFarmingChartView(ChartPDFView):
    template_name = "charts/special-interest/contract-farming.html"
    chart = "chart_contract_farming"
    pdf_javascript_delay = 10000
