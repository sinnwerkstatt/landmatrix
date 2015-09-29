from api.query_sets.agricultural_produce_query_set import AgriculturalProduceQuerySet, AllAgriculturalProduceQuerySet
from api.views.decimal_encoder import DecimalEncoder

import json
from django.http.response import HttpResponse

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class AgriculturalProduceJSONView:

    def dispatch(self, request, *args, **kwargs):
        output = self.get_agricultural_produce(request.GET)
        return HttpResponse(json.dumps(output, cls=DecimalEncoder), content_type="application/json")

    def get_agricultural_produce(self, get):
        queryset = AllAgriculturalProduceQuerySet(get)
        return queryset.all()
