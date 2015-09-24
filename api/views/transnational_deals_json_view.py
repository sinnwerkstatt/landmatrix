from api.query_sets.transnational_deals_query_set import TransnationalDealsQuerySet
from api.views.json_view_base import JSONViewBase

from django.http.response import HttpResponse
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TransnationalDealsJSONView(JSONViewBase):

    def dispatch(self, request, *args, **kwargs):
        filter_sql = self._get_filter(request.GET.getlist("negotiation_status", []), request.GET.getlist("deal_scope", []), request.GET.get("data_source_type"))
        countries = self.get_transnational_deals(filter_sql, request.GET.getlist("region", []))
        return HttpResponse(json.dumps(countries, ensure_ascii=False), content_type="application/json")

    def get_transnational_deals(self, filter_sql, regions=None):
        queryset = TransnationalDealsQuerySet()
        queryset.set_regions(regions)
        queryset.set_filter_sql(filter_sql)
        return queryset.all()


