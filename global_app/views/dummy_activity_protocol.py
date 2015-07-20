__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.http import HttpResponse

import json

from .record_reader import RecordReader



class DummyActivityProtocol:

    def dispatch(self, request, action):

        if request.POST:
            if False and settings.DEBUG: print(request.POST['data'])
            self.data = json.loads(request.POST["data"])

        res = {"errors": [], "activities": []}
        filters = self.data["filters"]
        columns = self.data["columns"]

        res["activities"] = self._get_activities_by_filter_and_grouping(filters, columns)

#        return HttpResponse(json.dumps(res,encoding="cp1251"), mimetype="application/json")#FIXME, utf-8 breaks for get-the-detail view
        return HttpResponse(json.dumps(res))

    def _get_activities_by_filter_and_grouping(self, filters, columns):

        return RecordReader(filters, columns).get_all()
