from django.core.urlresolvers import reverse
from api.query_sets.target_country_summaries_query_set import TargetCountrySummariesQuerySet
from api.views.decimal_encoder import DecimalEncoder

from django.http.response import HttpResponse
import json
from itertools import groupby
from global_app.forms.add_deal_general_form import AddDealGeneralForm

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TargetCountrySummariesJSONView:

    INTENTIONS = filter(lambda k: "Mining" not in k, [str(i[1]) for i in AddDealGeneralForm().fields["intention"].choices])

    def dispatch(self, request, *args, **kwargs):
        countries_summary = self.get_by_target_country(request.GET)
        output = [self.to_json_record(c) for c in countries_summary if c['country_id']]
        return HttpResponse(json.dumps(output, cls=DecimalEncoder), content_type="application/json")

    def to_json_record(self, c):
        c['name'] = c['country']
        c["country_slug"] =c['country'].lower().replace(" ", "-")
        c["region_slug"] =c['region'].lower().replace(" ", "-")
        c["country_url"] = reverse("table_list", kwargs={"group": "by-target-country", "list": c['country'].lower().replace(" ", "-")})

        filtered_intentions = [i for i in c['intentions'] if i]
        sorted_intentions = [self.map_intention(c) for c in sorted(filtered_intentions)]
        c["intentions"] = [
            "%s (%s)" % (key, len(list(group)))
            for key, group in groupby(sorted_intentions)
        ]
        return c

    def get_by_target_country(self, get):
        region = get.get("regions", None)
        country_code = get.get("country_code", None)
        queryset = TargetCountrySummariesQuerySet(get)
        queryset.set_country_region(country_code, region)
        return queryset.all()

    def map_intention(self, intention):
        return intention.split(',')[0] if intention else None
