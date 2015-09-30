from api.query_sets.hectares_query_set import HectaresQuerySet
from api.views.decimal_encoder import DecimalEncoder

import json
from django.http.response import HttpResponse

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class HectaresJSONView:

    def dispatch(self, request):
        data = self.get_json(request.GET)
        return HttpResponse(json.dumps(data[0] if data else {}, cls=DecimalEncoder), content_type="application/json")

    def get_json(self, get):
        return HectaresQuerySet(get).all()
