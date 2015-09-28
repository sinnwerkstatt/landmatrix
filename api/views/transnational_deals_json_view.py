from api.query_sets.transnational_deals_query_set import TransnationalDealsQuerySet

from django.http.response import HttpResponse
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TransnationalDealsJSONView:

    def dispatch(self, request, *args, **kwargs):
        countries = self.get_transnational_deals(request.GET)
        return HttpResponse(json.dumps(countries, ensure_ascii=False), content_type="application/json")

    def get_transnational_deals(self, get):
        queryset = TransnationalDealsQuerySet(get)
        queryset.set_regions(get.getlist("region", []))
        return queryset.all()


