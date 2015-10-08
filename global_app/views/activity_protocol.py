from api.query_sets.activity_query_set import ActivityQuerySet

from django.http import HttpResponse
import json
from api.query_sets.sql_generation.record_reader import RecordReader

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityProtocol:

    def dispatch(self, request, action):
        queryset = ActivityQuerySet(request.POST)
        res = queryset.all()
        output = json.dumps(res)

        # return HttpResponse(json.dumps(res,encoding="cp1251"), mimetype="application/json")#FIXME, utf-8 breaks for get-the-detail view
        return HttpResponse(output, content_type="application/json")


