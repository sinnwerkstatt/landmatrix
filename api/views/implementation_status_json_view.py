from api.views.json_view_base import JSONViewBase
from api.query_sets.implementation_status_query_set import ImplementationStatusQuerySet
from api.views.decimal_encoder import DecimalEncoder

from django.http.response import HttpResponse
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ImplementationStatusJSONView(JSONViewBase):

    def dispatch(self, request, *args, **kwargs):
        with_names = list(self.get_implementation_status(request))
        return HttpResponse(json.dumps(with_names, cls=DecimalEncoder), content_type="application/json")

    def get_implementation_status(self, request):
        filter_sql = self._get_filter(request.GET.getlist("negotiation_status", []), request.GET.getlist("deal_scope", []), request.GET.get("data_source_type"))
        queryset = ImplementationStatusQuerySet()
        queryset.set_filter_sql(filter_sql)
        return queryset.all()

