from api.query_sets.intention_query_set import IntentionQuerySet
from api.views.decimal_encoder import DecimalEncoder

from django.http.response import HttpResponse
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class IntentionOfInvestmentJSONView:

    def dispatch(self, request, *args, **kwargs):
        found = self.get_intention(request.GET)
        return HttpResponse(json.dumps(found, cls=DecimalEncoder), content_type="application/json")

    def get_intention(self, get):
        queryset = IntentionQuerySet(get)
        queryset.set_intention(get.get("intention", ""))
        return queryset.all()
