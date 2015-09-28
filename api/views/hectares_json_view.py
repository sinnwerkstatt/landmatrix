from api.query_sets.hectares_query_set import HectaresQuerySet
from api.views.decimal_encoder import DecimalEncoder

import json
from django.http.response import HttpResponse

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class HectaresJSONView:

    def dispatch(self, request, *args, **kwargs):
        h = self.get_hectares(request.GET)
        return HttpResponse(json.dumps(h[0] if h else {}, cls=DecimalEncoder), content_type="application/json")

    def get_hectares(self, get):
        queryset = HectaresQuerySet(get)
        return queryset.all()
