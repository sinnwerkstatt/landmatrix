from pprint import pprint
from django.template.defaultfilters import slugify
from api.query_sets.top_10_countries_query_set import Top10InvestorCountriesQuerySet, Top10TargetCountriesQuerySet
from api.query_sets.transnational_deals_query_set import TransnationalDealsQuerySet
from api.views.decimal_encoder import DecimalEncoder
from api.views.json_view_base import JSONViewBase

from django.http.response import HttpResponse
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class Top10CountriesJSONView(JSONViewBase):

    def dispatch(self, request, *args, **kwargs):
        filter_sql = self._get_filter(request.GET.getlist("negotiation_status", []), request.GET.getlist("deal_scope", []), request.GET.get("data_source_type"))

        output = {
            "investor_country": [],
            "target_country": [],
        }
        for c in self.get_top_10_investors(filter_sql):
            country = " %s" % TransnationalDealsQuerySet.LONG_COUNTRIES.get(c['investor_country'], c['investor_country'])
            output["investor_country"].append(
                {"name": country, "slug": slugify(c['investor_country']), "hectares": c['hectares'], "id": c['investor_country_id'], "deals": c['deals']}
            )
        for c in self.get_top_10_target_countries(filter_sql):
            country = " %s" % TransnationalDealsQuerySet.LONG_COUNTRIES.get(c['target_country'], c['target_country'])
            output["target_country"].append(
                {"name": country, "slug": slugify(c['target_country']), "hectares": c['hectares'], "id":c['target_country_id'], "deals": c['deals']}
            )
        return HttpResponse(json.dumps(output, cls=DecimalEncoder), content_type="text/plain")

    def get_top_10_investors(self, filter_sql):
        queryset = Top10InvestorCountriesQuerySet()
        queryset.set_filter_sql(filter_sql)
        return queryset.all()

    def get_top_10_target_countries(self, filter_sql):
        queryset = Top10TargetCountriesQuerySet()
        queryset.set_filter_sql(filter_sql)
        return queryset.all()
