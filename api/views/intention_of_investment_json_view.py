from api.query_sets.intention_query_set import IntentionQuerySet
from api.views.decimal_encoder import DecimalEncoder
from api.views.json_view_base import JSONViewBase

from django.http.response import HttpResponse
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class IntentionOfInvestmentJSONView(JSONViewBase):

    def dispatch(self, request, *args, **kwargs):
        filter_sql = self._get_filter(request.GET.getlist("negotiation_status", []), request.GET.getlist("deal_scope", []), request.GET.get("data_source_type"))
        found = self.get_intention(filter_sql, request.GET.get("intention", ""))
        return HttpResponse(json.dumps(found, cls=DecimalEncoder), content_type="application/json")

    def get_intention(self, filter_sql, parent_intention):
        queryset = IntentionQuerySet()
        queryset.set_intention(parent_intention)
        queryset.set_filter_sql(filter_sql)
        return queryset.all()
