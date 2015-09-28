from api.query_sets.implementation_status_query_set import ImplementationStatusQuerySet
from api.views.decimal_encoder import DecimalEncoder

from django.http.response import HttpResponse
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ImplementationStatusJSONView:

    def dispatch(self, request, *args, **kwargs):
        with_names = list(self.get_implementation_status(request))
        return HttpResponse(json.dumps(with_names, cls=DecimalEncoder), content_type="application/json")

    def get_implementation_status(self, request):
        queryset = ImplementationStatusQuerySet(request.GET)
        return queryset.all()

