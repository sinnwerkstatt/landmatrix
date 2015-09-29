from api.query_sets.target_country_summaries_query_set import TargetCountrySummariesQuerySet
from api.views.decimal_encoder import DecimalEncoder

from django.http.response import HttpResponse
import json
from global_app.forms.add_deal_general_form import AddDealGeneralForm

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TargetCountrySummariesJSONView:

    def dispatch(self, request, *args, **kwargs):
        output = self.get_by_target_country(request.GET)
        return HttpResponse(json.dumps(output, cls=DecimalEncoder), content_type="application/json")

    def get_by_target_country(self, get):
        queryset = TargetCountrySummariesQuerySet(get)
        return queryset.all()

