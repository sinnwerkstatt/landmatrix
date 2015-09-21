from api.query_sets.transnational_deals_by_country_query_set import TransnationalDealsByTargetCountryQuerySet, \
    TransnationalDealsByInvestorCountryQuerySet
from api.views.decimal_encoder import DecimalEncoder
from api.views.json_view_base import JSONViewBase

from django.http.response import HttpResponse
import json
from django.template.defaultfilters import slugify

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TransnationalDealsByCountryJSONView(JSONViewBase):

    def dispatch(self, request, *args, **kwargs):
        filter_sql = self._get_filter(request.GET.getlist("negotiation_status", []), request.GET.getlist("deal_scope", []), request.GET.get("data_source_type"))
        country = request.GET.get("country", None)
        output = {
            'target_country': aggregate_regions(self.get_transnational_deals_by_target_country(filter_sql, country)),
            'investor_country': aggregate_regions(self.get_transnational_deals_by_investor_country(filter_sql, country))
        }
        return HttpResponse(json.dumps(output, cls=DecimalEncoder), content_type="text/plain")

    def get_transnational_deals_by_target_country(self, filter_sql, country):
        queryset = TransnationalDealsByTargetCountryQuerySet()
        queryset.set_country(country)
        queryset.set_filter_sql(filter_sql)
        return queryset.all()

    def get_transnational_deals_by_investor_country(self, filter_sql, country):
        queryset = TransnationalDealsByInvestorCountryQuerySet()
        queryset.set_country(country)
        queryset.set_filter_sql(filter_sql)
        return queryset.all()


def aggregate_regions(t_deals):
    sum_deals, sum_hectares = 0, 0
    output = []
    for d in t_deals:
        output.append({
            "region_id": d['region_id'],
            "region": d['region'],
            "deals": d['deals'] or 0,
            "hectares": d['hectares'] or 0,
            "slug": slugify(d['region']),
        })
        sum_deals += d['deals'] or 0
        sum_hectares += float(d['hectares'] or 0)
    output.append({
        "region_id": 0,
        "region": "Total",
        "deals": sum_deals,
        "hectares": sum_hectares,
    })
    return output
