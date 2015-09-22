from django.core.urlresolvers import reverse
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

        # process regions
        for r in regions:
            if not r[0]:
                continue
            output.append({
                "region_id": r[0],
                "region": r[1],
                "name": r[1],
                "lat": r[2],
                "lon": r[3],
                "deals": r[4],
                "region_slug": r[1].lower().replace(" ", "-"),
                "hectares": r[5],
                "availability": int(r[7]),
            })
        # process countries
        for c in countries:
            if not c[0]:
                continue
            output.append({
                "country_id":c[0],
                "country":c[1],
                "region":c[2],
                "lat":c[3],
                "lon":c[4],
                "deals":c[5],
                "name":c[1],
                "country_slug":c[1].lower().replace(" ", "-"),
                "region_slug":c[2].lower().replace(" ", "-"),
                "hectares": c[6],
                "availability": int(c[7]),
            })
        countries = {}
        for c in countries_summary:
            if not c[0]:
                continue
            country = countries.get(c[0], {"domestic": 0, "transnational": 0})
            country.update({
                "country_id":c[0],
                "country":c[1],
                "region":c[2],
                "lat":c[3],
                "lon":c[4],
                "deals":c[5] + country.get("deals", 0),
                c[6]: c[5] + country.get(c[6], 0),
                "name":c[1],
                "country_slug":c[1].lower().replace(" ", "-"),
                "region_slug":c[2].lower().replace(" ", "-"),
                "url": reverse("table_list", kwargs={"group": "by-target-country", "list": c[1].lower().replace(" ", "-")}),
            })
            countries.update({c[0]: country})
        for k,v in countries.items():
            output.append(v)

        return HttpResponse(json.dumps(output, cls=DecimalEncoder), content_type="text/plain")

    def get_by_investor_country(self, filter_sql):
        base_filter_sql = ""
        cursor = connection.cursor()
        sql = """
            SELECT DISTINCT
                investor_country.id,
                investor_country.name AS 'country',
                investor_region.name,
                cast(investor_country.point_lat as char),
                cast(investor_country.point_lon as char),
                count(distinct a.activity_identifier) AS deals,
                deal_scope.value
              FROM
                activities a
                %s
              WHERE
                %s
                %s
             GROUP BY investor_country.name, deal_scope.value;
        """ % (self.BASE_JOIN, self.BASE_CONDITON, filter_sql)
        print(sql), cursor.execute(sql)
        return cursor.fetchall()
