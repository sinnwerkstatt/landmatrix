import copy

from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic.base import RedirectView

from landmatrix.pdfgen import PDFViewMixin
from grid.views.filter_widget_mixin import FilterWidgetMixin
from grid.views.view_aux_functions import render_to_response


class ChartView(TemplateView, FilterWidgetMixin):
    chart = ""

    def get_context_data(self, **kwargs):
        self._set_filters()

        context = super(ChartView, self).get_context_data(**kwargs)
        context.update({
            "view": "chart view",
            "export_formats": ("XML", "CSV", "XLS"),
            "chart": self.chart,
        })

        self.add_filter_context_data(context, self.request)

        return context

    def _set_filters(self):
        data = self.request.GET.copy()
        self.current_formset_conditions = self.get_formset_conditions(
            self._filter_set(data), data)
        self.filters = self.get_filter_context(self.current_formset_conditions)


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
    def get_redirect_url(self, *args, **kwargs):
        params = self.request.GET
        if 'country' in params or 'region' in params:
            return '%s?%s' % (
                reverse('chart_overview'),
                params.urlencode()
            )
        else:
            return reverse('chart_transnational_deals')


class OverviewChartView(ChartPDFView):
    template_name = "charts/overview.html"
    chart = "chart_overview"
    # This page needs a massive delay for some reason
    pdf_javascript_delay = 4000


class TransnationalDealsChartView(ChartPDFView):
    template_name = "charts/transnational-deals.html"
    chart = "chart_transnational_deals"


class MapOfInvestmentsChartView(ChartPDFView):
    template_name = "charts/investor-target-countries.html"
    chart = "chart_map_of_investments"
    pdf_javascript_delay = 2000


class AgriculturalDriversChartView(ChartPDFView):
    template_name = "charts/agricultural-produce.html"
    chart = "chart_agricultural_drivers"


class PerspectiveChartView(ChartView):
    template_name = "charts/perspective.html"
    chart = "chart_perspective"


class SpecialInterestView(ChartPDFView):
    template_name = "charts/special-interest.html"
    chart = "special_interest"
    pdf_javascript_delay = 10000

    def get_pdf_export_url(self, request, *args, **kwargs):
        '''
        Special handling for the 'variable' switch
        '''
        url = super().get_pdf_export_url(request, *args, **kwargs)
        if 'variable' in request.GET:
            url += '?variable={}'.format(request.GET['variable'])

        return url

    def get_pdf_render_url(self, request, *args, **kwargs):
        '''
        Special handling for the 'variable' switch
        '''
        url = super().get_pdf_render_url(request, *args, **kwargs)
        if 'variable' in request.GET:
            url += '?variable={}'.format(request.GET['variable'])

        return url
