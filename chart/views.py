
from grid.views.view_aux_functions import render_to_response

from django.views.generic.base import TemplateView
from django.template import RequestContext


class ChartView(TemplateView):
    template_name = "chart/overview.html"

    def get_context_data(self, **kwargs):
        context = super(ChartView, self).get_context_data(**kwargs)
        context.update({
            "view": "chart view",
        })
        return context