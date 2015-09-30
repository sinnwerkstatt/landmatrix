import timeit
from api.query_sets.deals_query_set import DealsQuerySet
from api.query_sets.negotiation_status_query_set import NegotiationStatusQuerySet
from api.views.decimal_encoder import DecimalEncoder

import json
from django.http.response import HttpResponse
from landmatrix.models.activity_attribute_group import ActivityAttributeGroup

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealsJSONView():

    def dispatch(self, request):
        start_time = timeit.default_timer()
        data = list(self.get_json(request))
        print(data[:10], len(data), timeit.default_timer() - start_time)
        return HttpResponse(json.dumps(data, cls=DecimalEncoder), content_type='application/json')

    def get_json(self, request):
        queryset = DealsQuerySet()
        queryset.set_limit(request.GET.get('limit', None))
        queryset.set_investor_country(request.GET.get('investor_country', None))
        queryset.set_investor_region(request.GET.get('investor_region', None))
        queryset.set_target_country(request.GET.get('target_country', None))
        queryset.set_target_region(request.GET.get('target_region', None))
        if request.GET.get('window'):
            lat_min, lat_max, lon_min, lon_max = request.GET.get('window').split(',')
            queryset.set_window(lat_min, lat_max, lon_min, lon_max)
        return queryset.all()
