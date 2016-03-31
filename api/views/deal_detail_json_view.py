from landmatrix.models.deal import Deal

from django.http.response import HttpResponse
from django.views.generic.base import TemplateView

import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealDetailJSONView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        deal = Deal(request.GET.get('deal_id'))
        attributes = request.GET.getlist('attributes')
        return HttpResponse(json.dumps(deal_to_dict(deal, attributes)))


def deal_to_dict(deal, attributes):
    return {attribute: deal.attributes.get(attribute) for attribute in attributes}
