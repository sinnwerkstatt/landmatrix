from api.query_sets.agricultural_produce_query_set import AgriculturalProduceQuerySet
from api.query_sets.hectares_query_set import HectaresQuerySet
from api.views.decimal_encoder import DecimalEncoder
from api.views.json_view_base import JSONViewBase

import json
from django.http.response import HttpResponse

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class HectaresJSONView(JSONViewBase):

    def dispatch(self, request, *args, **kwargs):
        filter_sql = self._get_filter(request.GET.getlist("negotiation_status", []), request.GET.getlist("deal_scope", []), request.GET.get("data_source_type"))
        h = self.get_hectares(filter_sql)
        return HttpResponse(json.dumps(h[0] if h else {}, cls=DecimalEncoder), content_type="application/json")

    def get_hectares(self, filter_sql):
        queryset = HectaresQuerySet(filter_sql)
        return queryset.all()
