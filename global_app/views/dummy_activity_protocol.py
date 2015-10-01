__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

import json

from django.http import HttpResponse
from django.conf import settings

from global_app.views.sql_generation.record_reader import RecordReader


class DummyActivityProtocol:

    DEBUG = False

    def dispatch(self, request, action):

        if request.POST:
            if False and settings.DEBUG: print(request.POST['data'])
            data = json.loads(request.POST["data"])

        res = {
            "errors": [],
            "activities":  self._get_activities_by_filter_and_grouping(data["filters"], data["columns"])
        }

#        return HttpResponse(json.dumps(res,encoding="cp1251"), mimetype="application/json")#FIXME, utf-8 breaks for get-the-detail view
        return HttpResponse(json.dumps(res), content_type="application/json")

    def _get_activities_by_filter_and_grouping(self, filters, columns):

        # if filters.get('group_value') == '':
        reader = RecordReader(filters, columns)
        if self.DEBUG:
            print(reader.get_all_sql())
        return reader.get_all(assemble=reader._make_padded_record_from_column_data)
