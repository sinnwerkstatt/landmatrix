__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import Activity
from .view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext


class DealDetailView(TemplateView):

    template_name = 'deal-detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.deal_id = kwargs["deal_id"]
        items = Activity.objects.filter(activity_identifier=3)
        print(items)
        context = {
            "data": {
                "items": items,
            }
        }
        return render_to_response(self.template_name, context, RequestContext(self.request))