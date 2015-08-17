from django.shortcuts import render

from global_app.views.view_aux_functions import render_to_response

from django.views.generic.base import TemplateView
from django.template import RequestContext


class ChartsView(TemplateView):
    template_name = "plugins/overview.html"

    def dispatch(self, request, *args, **kwargs):
        print('BOOOOOOOOOOOOOAH ALDA!')
        context = {
            "view": "chart view",


        }
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))
