from grid.views.view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapView(TemplateView):
    template_name = 'map/map.html'

    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['request'] = request
        return render_to_response(self.template_name, context, RequestContext(request))

