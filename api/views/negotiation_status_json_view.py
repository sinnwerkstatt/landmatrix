from api.query_sets.negotiation_status_query_set import NegotiationStatusQuerySet
from api.views.decimal_encoder import DecimalEncoder
from api.views.json_view_base import JSONViewBase

import json
from django.http.response import HttpResponse

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class NegotiationStatusJSONView(JSONViewBase):

    def dispatch(self, request, *args, **kwargs):
        with_names = list(self.get_negotiation_status(request))
        return HttpResponse(json.dumps(with_names, cls=DecimalEncoder))

    def get_negotiation_status(self, request):
        filter_sql = self._get_filter(request.GET.getlist("negotiation_status", []), request.GET.getlist("deal_scope", []), request.GET.get("data_source_type"))
        queryset = NegotiationStatusQuerySet()
        queryset.set_filter_sql(filter_sql)
        return queryset.all()
