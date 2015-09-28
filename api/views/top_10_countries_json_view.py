from django.template.defaultfilters import slugify
from api.query_sets.top_10_countries_query_set import Top10InvestorCountriesQuerySet, Top10TargetCountriesQuerySet
from api.query_sets.transnational_deals_query_set import TransnationalDealsQuerySet
from api.views.decimal_encoder import DecimalEncoder

from django.http.response import HttpResponse
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class Top10CountriesJSONView:

    def dispatch(self, request, *args, **kwargs):
        output = {
            "investor_country": [],
            "target_country": [],
        }
        for c in self.get_top_10_investors(request.GET):
            country = TransnationalDealsQuerySet.LONG_COUNTRIES.get(c['investor_country'], c['investor_country'])
            output["investor_country"].append(
                {"name": country, "slug": slugify(c['investor_country']), "hectares": c['hectares'], "id": c['investor_country_id'], "deals": c['deals']}
            )
        for c in self.get_top_10_target_countries(request.GET):
            country = TransnationalDealsQuerySet.LONG_COUNTRIES.get(c['target_country'], c['target_country'])
            output["target_country"].append(
                {"name": country, "slug": slugify(c['target_country']), "hectares": c['hectares'], "id":c['target_country_id'], "deals": c['deals']}
            )
        return HttpResponse(json.dumps(output, cls=DecimalEncoder), content_type="application/json")

    def get_top_10_investors(self, get):
        queryset = Top10InvestorCountriesQuerySet(get)
        return queryset.all()

    def get_top_10_target_countries(self, get):
        queryset = Top10TargetCountriesQuerySet(get)
        return queryset.all()
