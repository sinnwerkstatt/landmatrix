__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .record_reader import RecordReader

from django.http import HttpResponse
from django.conf import settings

import json


class DummyActivityProtocol:

    def dispatch(self, request, action):

        if request.POST:
            if False and settings.DEBUG: print(request.POST['data'])
            self.data = json.loads(request.POST["data"])

        res = {"errors": [], "activities": []}
        res["activities"] = self._get_activities_by_filter_and_grouping(self.data["filters"], self.data["columns"])

#        return HttpResponse(json.dumps(res,encoding="cp1251"), mimetype="application/json")#FIXME, utf-8 breaks for get-the-detail view
        return HttpResponse(json.dumps(res))

    def _get_activities_by_filter_and_grouping(self, filters, columns):

        # if filters.get('group_value') == '':
        #     return RecordReader(filters, columns).slap_columns_together()
        return RecordReader(filters, columns).get_all()
