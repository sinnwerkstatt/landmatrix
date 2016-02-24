
from grid.views.view_aux_functions import render_to_response

from django.views.generic.base import TemplateView
from django.template import RequestContext


class ChartView(TemplateView):
    template_name = "chart/overview.html"

    def dispatch(self, request, *args, **kwargs):
        context = {
            "view": "chart view",
        }
        return render_to_response(self.template_name, context, RequestContext(request))
