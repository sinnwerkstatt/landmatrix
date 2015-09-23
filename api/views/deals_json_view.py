import timeit
from api.query_sets.deals_query_set import DealsQuerySet
from api.query_sets.negotiation_status_query_set import NegotiationStatusQuerySet
from api.views.decimal_encoder import DecimalEncoder
from api.views.json_view_base import JSONViewBase

import json
from django.http.response import HttpResponse
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealsJSONView(JSONViewBase):

    def dispatch(self, request, *args, **kwargs):
        start_time = timeit.default_timer()
        deals = list(self.get_deals(request))
        print(deals[:10], len(deals), timeit.default_timer() - start_time)
        return HttpResponse(json.dumps(deals, cls=DecimalEncoder), content_type='text/plain')

    def get_deals(self, request):
        filter_sql = self._get_filter(request.GET.getlist("negotiation_status", []), request.GET.getlist("deal_scope", []), request.GET.get("data_source_type"))
        queryset = DealsQuerySet()
#        queryset.set_filter_sql(filter_sql)
        return queryset.all()
