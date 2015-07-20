__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.http import HttpResponse
from django.db import connection
from django.conf import settings

import json

from .sql_builder import SQLBuilder



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


        builder = SQLBuilder.create(columns, filters)
        sql = builder.get_base_sql() % {
            "from": builder.get_from_sql(),
            "where": builder.get_where_sql(),
            "limit": builder.get_limit_sql(),
            "order_by": builder.get_order_sql(),
            "from_filter": builder.filter_from(),
            "where_filter": builder.filter_where(),
            "group_by": builder.get_group_sql(),
            "inner_group_by": builder.get_inner_group_sql(),
            "name": builder.get_name_sql(),
            "columns": builder.get_columns_sql(),
            "sub_columns": builder.get_sub_columns_sql()
        }

        if (False and settings.DEBUG): print('*'*80, 'SQL: \n', sql)

        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()






