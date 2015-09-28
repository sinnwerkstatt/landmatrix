from api.query_sets.agricultural_produce_query_set import AgriculturalProduceQuerySet
from api.views.decimal_encoder import DecimalEncoder
from api.views.json_view_base import JSONViewBase

import json
from django.http.response import HttpResponse

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class AgriculturalProduceJSONView(JSONViewBase):

    REGIONS = {
        'america': ["5","13","21"],
        'africa':  ["11","14","15","17","18"],
        'asia':    ["30","34","35","143","145"],
        'oceania': ["53","54","57","61","29"],
        'europe':  ["151","154","155","39"],
        'overall': None
    }

    def dispatch(self, request, *args, **kwargs):
        filter_sql = self._get_filter(request.GET.getlist("negotiation_status", []), request.GET.getlist("deal_scope", []), request.GET.get("data_source_type"))
        output = []
        for region, value in self.REGIONS.items():
            ap_region = {
                "food_crop": 0,
                "non_food": 0,
                "flex_crop": 0,
                "multiple_use": 0,
            }
            hectares = {
                "food_crop": 0,
                "non_food": 0,
                "flex_crop": 0,
                "multiple_use": 0,
            }
            ap_list = self.get_agricultural_produces(filter_sql, value)

            available_sum, not_available_sum = self.calculate_sums(ap_list)

            for ap in ap_list:
                if ap['agricultural_produce']:
                    ap_name = ap['agricultural_produce'].lower().replace(" ", "_").replace("-", "_")
                    ap_region[ap_name] = round(float(ap['hectares'])/available_sum*100)
                    hectares[ap_name] = ap['hectares']

            output.append({
                "region": region,
                "available": available_sum,
                "not_available": not_available_sum,
                "agricultural_produce": ap_region,
                "hectares": hectares,
            })

        return HttpResponse(json.dumps(output, cls=DecimalEncoder), content_type="application/json")

    def calculate_sums(self, ap_list):
        available_sum, not_available_sum = 0, 0
        for ap in ap_list:
            if ap['agricultural_produce']:
                available_sum += float(ap['hectares'])
            else:
                not_available_sum += float(ap['hectares'])
        return available_sum, not_available_sum

    def get_agricultural_produces(self, filter_sql, region_ids):
        queryset = AgriculturalProduceQuerySet(filter_sql)
        queryset.set_regions(region_ids)
        return queryset.all()
