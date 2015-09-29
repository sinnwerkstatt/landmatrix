from api.query_sets.investor_country_summaries_query_set import InvestorCountrySummariesQuerySet
from api.views.decimal_encoder import DecimalEncoder

from django.http.response import HttpResponse
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class InvestorCountrySummariesJSONView:

    def dispatch(self, request, *args, **kwargs):
        output = self.get_by_investor_country(request.GET)
        return HttpResponse(json.dumps(output, cls=DecimalEncoder), content_type="application/json")

    def get_by_investor_country(self, get):
        queryset = InvestorCountrySummariesQuerySet(get)
        return queryset.all()
