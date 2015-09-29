from api.query_sets.top_10_countries_query_set import Top10CountriesQuerySet
from api.views.decimal_encoder import DecimalEncoder

from django.http.response import HttpResponse
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class Top10CountriesJSONView:

    def dispatch(self, request, *args, **kwargs):
        output = self.get_top_10_countries(request.GET)
        return HttpResponse(json.dumps(output, cls=DecimalEncoder), content_type="application/json")

    def get_top_10_countries(self, get):
        queryset = Top10CountriesQuerySet(get)
        return queryset.all()
