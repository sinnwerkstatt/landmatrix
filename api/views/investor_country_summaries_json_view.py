from django.core.urlresolvers import reverse
from api.query_sets.investor_country_summaries_query_set import InvestorCountrySummariesQuerySet
from api.views.decimal_encoder import DecimalEncoder
from api.views.json_view_base import JSONViewBase

from django.http.response import HttpResponse
import json
from django.template.defaultfilters import slugify
from itertools import groupby

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class InvestorCountrySummariesJSONView(JSONViewBase):

    def dispatch(self, request, *args, **kwargs):
        filter_sql = self._get_filter(request.GET.getlist("negotiation_status", []), request.GET.getlist("deal_scope", []), request.GET.get("data_source_type"))

        countries_summary = self.get_by_investor_country(filter_sql)

        countries = {}
        for c in countries_summary:
            if not c['country_id']: continue
            country = countries.get(c['country_id'], {"domestic": 0, "transnational": 0})
            country.update(self.to_json_record(c, country))
            countries.update({c['country_id']: country})

        output = [v for k,v in countries.items()]

        return HttpResponse(json.dumps(output, cls=DecimalEncoder), content_type="application/json")

    def to_json_record(self, c, country):
        c['name'] = c['country']
        c["country_slug"] =c['country'].lower().replace(" ", "-")
        c["region_slug"] =c['region'].lower().replace(" ", "-")
        c['url'] = reverse("table_list", kwargs={"group": "by-target-country", "list": c['country'].lower().replace(" ", "-")})
        c[c['deal_scope']] = c['deals'] + country.get(c['deal_scope'], 0)
        c['deals'] = c['deals'] + country.get("deals", 0)

        return c

    def get_by_investor_country(self, filter_sql):

        queryset = InvestorCountrySummariesQuerySet(filter_sql)
        return queryset.all()
