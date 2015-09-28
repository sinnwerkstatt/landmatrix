from api.query_sets.negotiation_status_query_set import NegotiationStatusQuerySet
from api.views.decimal_encoder import DecimalEncoder

import json
from django.http.response import HttpResponse

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class NegotiationStatusJSONView:

    def dispatch(self, request, *args, **kwargs):
        with_names = list(self.get_negotiation_status(request))
        return HttpResponse(json.dumps(with_names, cls=DecimalEncoder), content_type="application/json")

    def get_negotiation_status(self, request):
        queryset = NegotiationStatusQuerySet(request.GET)
        return queryset.all()
