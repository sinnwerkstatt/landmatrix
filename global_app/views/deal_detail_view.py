__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from landmatrix.models import Deal
from .view_aux_functions import render_to_response

from django.views.generic import TemplateView
from django.template import RequestContext


class DealDetailView(TemplateView):

    template_name = 'deal-detail.html'

    def dispatch(self, request, *args, **kwargs):

        deal = Deal(kwargs["deal_id"])
        context = {
            "deal": {
                'attributes': deal.attributes,
                'primary_investor': deal.primary_investor,
                'stakeholder': deal.stakeholder,
            }
        }
        return render_to_response(self.template_name, context, RequestContext(request))


