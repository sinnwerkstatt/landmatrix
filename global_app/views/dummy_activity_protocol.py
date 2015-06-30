__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.http import HttpResponse
from django.db import connection
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import json

from .sql_builder import GroupSQLBuilder, ListSQLBuilder, join_attributes


def get_join_columns(columns, group, group_value):
    if group_value and group not in columns:
        join_columns = columns[:]
        join_columns.append(group)
    else:
        join_columns = columns
    return join_columns

def get_limit_sql(limit):
    if limit: return " LIMIT %s " % limit
    return ''

def get_order_sql(order_by):
    order_by_sql = ''
    if order_by:
        for field in order_by:
            if not order_by_sql:
                order_by_sql = "ORDER BY "
            else:
                order_by_sql += ", "
            natural_sort = ""
            if "+0" in field:
                natural_sort = "+0"
                field = field.split("+0")[0]
            if field[0] == "-":
                field = field[1:]
                order_by_sql += "%s %s DESC" % (field, natural_sort)
            else:
                order_by_sql += "%s %s ASC" % (field, natural_sort)

    return order_by_sql

def list_view_wanted(group, group_value):
    return group == "all" or group_value


class DummyActivityProtocol:

    def dispatch(self, request, action):

        if request.POST:
            self.data = json.loads(request.POST["data"])

        res = {"errors": [], "activities": []}
        filters = self.data["filters"]
        columns = self.data["columns"]

        res["activities"] = self._get_activities_by_filter_and_grouping(filters, columns)

#        return HttpResponse(json.dumps(res,encoding="cp1251"), mimetype="application/json")#FIXME, utf-8 breaks for get-the-detail view
        return HttpResponse(json.dumps(res))


    def _get_activities_by_filter_and_grouping(self, filters, columns):

        self.where_sql, self.inner_group_by_sql, self.columns_sql, self.sub_columns_sql = '', '', '', ''
        group, group_value = filters.get("group_by", ""), filters.get("group_value", "")

        filter_sql = self._browse_filters_to_sql(filters)
        from_sql = self.get_from_sql(filters, get_join_columns(columns, group, group_value), columns)

        self.name_sql = self.get_name_sql(group)

        if list_view_wanted(group, group_value):
            creator = ListSQLBuilder(columns, group, group_value)
            self.prepare_list_sql(columns, group, group_value)
        else:
            creator = GroupSQLBuilder(columns, group, filters)
            self.prepare_group_sql(columns, filters, group)

        self.group_by_sql = creator.get_group_sql()
        sql = creator.get_base_sql()

        sql = sql % {
            "from": from_sql,
            "where": self.where_sql,
            "limit": (get_limit_sql(filters.get("limit"))),
            "order_by": (get_order_sql(filters.get("order_by"))),
            "from_filter_activity": filter_sql["activity"]["from"],
            "where_filter_activity": filter_sql["activity"]["where"],
            "from_filter_investor": filter_sql["investor"]["from"],
            "where_filter_investor": filter_sql["investor"]["where"],
            "group_by": self.group_by_sql,
            "inner_group_by": self.inner_group_by_sql,
            "name": self.name_sql,
            "columns": self.columns_sql,
            "sub_columns": self.sub_columns_sql,
        }

        if (settings.DEBUG):
            print('from_sql:', from_sql)
            print('group_sql:', self.group_by_sql)
            print('SQL: ', sql)

        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def prepare_group_sql(self, columns, filters, group):

        if (settings.DEBUG): print('GROUP_SQL')

        # query deals grouped by a key
        self.inner_group_by_sql = ", %s" % group

        for c in columns:
            # get sql for columns
            if c == group:
                # use single values for column which gets grouped by
                self.columns_sql += self.SQL_COLUMN_MAP.get(c)[1] + "\n"
            else:
                self.columns_sql += self.SQL_COLUMN_MAP.get(c)[0] + "\n"
        if filters.get("starts_with", None):
            starts_with = filters.get("starts_with", "").lower()
            if group == "investor_country":
                self.where_sql += " AND investor_country.slug like '%s%%%%' " % starts_with
            elif group == "target_country":
                self.where_sql += " AND deal_country.slug like '%s%%%%' " % starts_with
            else:
                self.where_sql += " AND trim(lower(%s.value)) like '%s%%%%' " % (group, starts_with)

    def prepare_list_sql(self, columns, group, group_value):

        if (settings.DEBUG): print('LIST_SQL')

        for c in columns:
            if c in ("intended_size", "contract_size", "production_size"):
                self.sub_columns_sql += "            ARRAY_AGG(%(name)s.attributes->'%(name)s' ORDER BY %(name)s.date DESC) as %(name)s,\n" % {
                "name": c}
            elif c == "data_source":
                self.sub_columns_sql += "            sub.data_source_type as data_source_type, sub.data_source_url as data_source_url, sub.data_source_date data_source_date, sub.data_source_organisation as data_source_organisation,\n"
                self.columns_sql += "                " + self.SQL_COLUMN_MAP.get(c)[0] + "\n"
            else:
                self.columns_sql += "                " + self.SQL_COLUMN_MAP.get(c)[0] + "\n"
                self.sub_columns_sql += "            sub.%(name)s as %(name)s,\n" % {"name": c}
        if (settings.DEBUG): print('sub_columns:', self.sub_columns_sql)

        if group == "all":
            # show all deals not grouped
            pass
        elif group_value:
            # query deals not grouped by any key
            # parse group conditions
            if group == "target_region":
                self.where_sql += ' AND deal_region.slug = lower(\'%s\') ' % group_value
            elif group == "target_country":
                self.where_sql += ' AND deal_country.slug = lower(\'%s\') ' % group_value
            elif group == "year":
                self.where_sql += ' AND pi_negotiation_status.year = \'%s\' ' % group_value
            elif group == "crop":
                self.where_sql += ' AND crop.slug = lower(\'%s\') ' % group_value
            elif group == "intention":
                self.where_sql += ' AND lower(replace(intention.value, \' \', \'-\')) = lower(\'%s\') ' % group_value
            elif group == "investor_region":
                self.where_sql += ' AND investor_region.slug = \'%s\' ' % group_value
            elif group == "investor_country":
                self.where_sql += ' AND investor_country.slug = \'%s\' ' % group_value
            elif group == "investor_name":
                self.where_sql += ' AND s.stakeholder_identifier = \'%s\' ' % group_value
            elif group == "data_source_type":
                self.where_sql += ' AND lower(replace(replace(data_source_type.value, \' \', \'-\'), \'/\', \'+\')) = lower(\'%s\') ' % group_value

    GROUP_TO_NAME = {
        'all':              "'all deals'",
        'target_region':    'deal_region.name',
        'target_country':   'deal_country.name',
        'year':             'pi_negotiation_status.year',
        'crop':             'crop.name',
        'intention':        'intention.value',
        'investor_region':  'investor_region.name',
        'investor_country': 'investor_country.name',
        'investor_name':    'investor_name.value',
        'data_source_type': 'data_source_type.value'
    }
    def get_name_sql(self, group):
        return self.GROUP_TO_NAME.get(group, "'%s'" % group)

    def get_from_sql(self, filters, join_columns, columns):

        from_sql = ''

        if filters.get("investor", None) or any(x in ("investor_country","investor_region", "investor_name", 'primary_investor', "primary_investor_name") for x in columns):
            # is join of invovlements and stakeholders necessary?
            from_sql += """
            LEFT JOIN landmatrix_involvement AS i ON (i.fk_activity_id = a.id)
            LEFT JOIN landmatrix_stakeholder AS s ON (i.fk_stakeholder_id = s.id)"""

        for c in join_columns:
            if c in ("intended_size", "contract_size", "production_size"):
                # skip size rows
                continue
            elif c == "investor_country" or c == "investor_region":
                if "investor_country" not in from_sql:
                    from_sql += \
                        join_attributes('skvl1', 'country', attribute_table='landmatrix_stakeholderattributegroup', attribute_field='fk_stakeholder_id') + """
            LEFT JOIN landmatrix_country AS investor_country ON (investor_country.id = CAST(skvl1.attributes->'country' AS numeric))
            LEFT JOIN landmatrix_region AS investor_region ON (investor_region.id = investor_country.fk_region_id)"""
            elif c == "investor_name":
                from_sql += join_attributes('investor_name', 'investor_name',
                                            attribute_table='landmatrix_stakeholderattributegroup',
                                            attribute_field='fk_stakeholder_id')
                """
                LEFT JOIN sh_key_value_lookup investor_name
                    ON (s.stakeholder_identifier = investor_name.stakeholder_identifier AND investor_name.key = 'investor_name')
                """
            elif c == "crop":
                from_sql += join_attributes('akvl1', 'crops') + """
            LEFT JOIN crops crop ON (crop.id = akvl1.value)"""
            elif c == "target_country" or c == "target_region":
                if "target_country" not in from_sql:
                    from_sql += \
                        join_attributes('target_country', 'target_country') + """
            LEFT JOIN landmatrix_country AS deal_country ON (CAST(target_country.attributes->'target_country' AS numeric) = deal_country.id)
            LEFT JOIN landmatrix_region AS deal_region ON (deal_country.fk_region_id = deal_region.id)
            """

            elif c == "primary_investor":
                from_sql += """
            LEFT JOIN landmatrix_primaryinvestor AS p ON (i.fk_primary_investor_id = p.id)
            """
            elif c == "data_source_type":
                # only add data_source_type if not data_source added
                if "data_source" not in join_columns:
                    from_sql += "LEFT JOIN landmatrix_activityattributegroup AS data_source_type ON (a.activity_identifier = data_source_type.activity_identifier AND data_source_type.key = 'type') "
            elif c == "data_source":
                from_sql += """ LEFT JOIN landmatrix_activityattributegroup AS data_source_type ON (a.activity_identifier = data_source_type.activity_identifier AND data_source_type.key = 'type')
                                 LEFT JOIN landmatrix_activityattributegroup AS data_source_url ON (a.activity_identifier = data_source_url.activity_identifier AND data_source_url.key = 'url')
                                 LEFT JOIN landmatrix_activityattributegroup AS data_source_organisation ON (a.activity_identifier = data_source_organisation.activity_identifier AND data_source_organisation.key = 'company')
                                 LEFT JOIN landmatrix_activityattributegroup AS data_source_date ON (a.activity_identifier = data_source_date.activity_identifier AND data_source_date.key = 'date') """
            elif c == "contract_farming":
                from_sql += "LEFT JOIN landmatrix_activityattributegroup AS contract_farming ON (a.activity_identifier = contract_farming.activity_identifier AND contract_farming.key = 'off_the_lease') "
            elif c == "nature_of_the_deal":
                from_sql += "LEFT JOIN landmatrix_activityattributegroup AS nature_of_the_deal ON (a.activity_identifier = nature_of_the_deal.activity_identifier AND nature_of_the_deal.key = 'nature') "
            elif c == "latlon":
                from_sql += "LEFT JOIN landmatrix_activityattributegroup AS latitude ON (a.activity_identifier = latitude.activity_identifier AND latitude.key = 'point_lat') "
                from_sql += "LEFT JOIN landmatrix_activityattributegroup AS longitude ON (a.activity_identifier = longitude.activity_identifier AND longitude.key = 'point_lon') "
                from_sql += "LEFT JOIN landmatrix_activityattributegroup AS level_of_accuracy ON (a.activity_identifier = level_of_accuracy.activity_identifier AND level_of_accuracy.key = 'level_of_accuracy') "
            else:
                from_sql += '    ' + join_attributes(c, c)

        return from_sql

    def _browse_filters_to_sql(self, filters):
        sql = {
            "activity": {
                "where": "",
                "from": "",
            },
            "investor": {
                "where": "",
                "from": "",
            }
        }
        if not filters:
            return sql
        tables_from_act, where_act, tables_from_inv, where_inv = "", "", "", ""
        if filters.get("activity", {}).get("identifier"):
            for f in filters.get("activity").get("identifier"):
                operation = f.get("op")
                value = ",".join(filter(None, [s.strip() for s in f.get("value").split(",")]))
                where_act += "AND a.activity_identifier %s " % DummyActivityProtocol.OPERATION_MAP[operation][0] % value
        if filters.get("deal_scope") and filters.get("deal_scope") != "all":
            where_act += " AND deal_scope.value = '%s' " % filters.get("deal_scope")
        if filters.get("activity", {}).get("tags"):
            tags = filters.get("activity").get("tags")
            for i, (tag, value) in enumerate(tags.items()):
                variable_operation = tag.split("__")
                variable = variable_operation[0]
                # choose operation depending on variable type default 0(int)
                operation = ""
                if len(variable_operation) > 1:
                    operation = variable_operation[1]
                # empty as operation or no value given
                if operation == "is_empty" or not value or (value and not value[0]):
                    where_act += " AND akv%(count)i.value IS NULL " % {
                        "count": i,
                    }
                elif operation in ("in", "not_in"):
                    # value = value[0].split(",")
                    in_values = ",".join(["'%s'" % v.strip().replace("'", "\\'") for v in value])
                    if variable == "region":
                        where_act += " AND ar%(count)i.name %(op)s " % {
                            "count": i,
                            "op": DummyActivityProtocol.OPERATION_MAP[operation][0] % in_values,
                        }
                    else:
                        where_act += " AND akv%(count)i.value %(op)s " % {
                            "count": i,
                            "op": DummyActivityProtocol.OPERATION_MAP[operation][0] % in_values,
                        }
                else:
                    for v in value:
                        year = None
                        if "##!##" in v:
                            v,year =  v.split("##!##")[0], v.split("##!##")[1]
                        operation_type = not v.isdigit() and 1 or 0
                        if variable == "region":
                            where_act += " AND ar%(count)i.name %(op)s " % { "count": i, "op": DummyActivityProtocol.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'")}
                        else:
                            where_act += "  %(value)s  %(year)s " % {
                                "value": v and " AND akv%(count)i.value %(op)s " % { "count": i, "op": DummyActivityProtocol.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'")}  or "",
                                "year": year and " AND akv%i.year = '%s' " % (i, year) or ""
                            }
                # join tag tables for each condition
                if variable == "region":
                    tables_from_act += "LEFT JOIN landmatrix_activityattributegroup AS akv%(count)i, countries AS ac%(count)i, regions AS ar%(count)i \n" % {"count": i}
                    tables_from_act += " ON (a.activity_identifier = akv%(count)i.activity_identifier AND akv%(count)i.key = 'target_country' AND akv%(count)i.value = ac%(count)i.name AND ar%(count)i.id = ac%(count)i.fk_region)"%{"count": i, "key": variable}
                if variable.isdigit():
                    tables_from_act += "LEFT JOIN landmatrix_activityattributegroup AS akv%(count)i\n" % {"count": i}
                    tables_from_act += " ON (a.activity_identifier = akv%(count)i.activity_identifier AND akv%(count)i.key_id = '%(key)s')"%{"count": i, "key": variable}
                else:
                    tables_from_act += "LEFT JOIN landmatrix_activityattributegroup AS akv%(count)i\n" % {"count": i}
                    tables_from_act += " ON (a.activity_identifier = akv%(count)i.activity_identifier AND akv%(count)i.key = '%(key)s')"%{"count": i, "key": variable}
        sql["activity"]["from"] = tables_from_act
        sql["activity"]["where"] = where_act
        if filters.get("investor", {}).get("tags"):
            tags = filters.get("investor").get("tags")
            for i, (tag, value) in enumerate(tags.items()):
                if not value:
                    continue
                variable_operation = tag.split("__")
                variable = variable_operation[0]
                # choose operation depending on variable type default 0(int)
                operation = ""
                if len(variable_operation) > 1:
                    operation = variable_operation[1]
                if operation == "is_empty" or not value or (value and not value[0]):
                    where_inv += " AND skv%(count)i.value IS NULL " % {
                        "count": i,
                    }
                elif operation in ("in", "not_in"):
                    value = value[0].split(",")
                    in_values = ",".join(["'%s'" % v.strip().replace("'", "\\'") for v in value])
                    if variable == "region":
                        where_inv += " AND skvr%(count)i.name %(op)s" % {
                            "count": i,
                            "op": DummyActivityProtocol.OPERATION_MAP[operation][0] % in_values
                        }
                    else:
                        where_inv += " AND skv%(count)i.value %(op)s" % {
                            "count": i,
                            "op": DummyActivityProtocol.OPERATION_MAP[operation][0] % in_values
                        }
                else:
                    for v in value:
                        operation_type = not v.isdigit() and 1 or 0
                        if variable == "region":
                            where_inv += " AND skvr%i.name %s" % (i, DummyActivityProtocol.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"))
                        else:
                            where_inv += " AND skv%i.value %s" % (i, DummyActivityProtocol.OPERATION_MAP[operation][operation_type] % v.replace("'", "\\'"))
                        #query_params.append(v)
                # join tag tables for each condition
                if variable == "region":
                    tables_from_inv += "LEFT JOIN (sh_key_value_lookup skv%(count)i, countries skvc%(count)i, regions skvr%(count)i) \n" % {"count": i}
                    tables_from_inv += " ON (skv%(count)i.stakeholder_identifier = s.stakeholder_identifier AND skv%(count)i.key = 'country' AND skv%(count)i.value = skvc%(count)i.name AND skvr%(count)i.id = skvc%(count)i.fk_region)"%{"count": i, "key": variable}
                else:
                    tables_from_inv += "LEFT JOIN (sh_key_value_lookup skv%(count)i)\n" % {"count": i}
                    tables_from_inv += " ON (skv%(count)i.stakeholder_identifier = s.stakeholder_identifier AND skv%(count)i.key_id = '%(key)s')\n" % {"count": i, "key": variable}
            sql["investor"]["from"] = tables_from_inv
            sql["investor"]["where"] = where_inv
        return sql



    SQL_COLUMN_MAP = {
        "investor_name": ["array_to_string(array_agg(DISTINCT concat(investor_name.attributes->'investor_name', '#!#', s.stakeholder_identifier)), '##!##') as investor_name,",
                          "CONCAT(investor_name.value, '#!#', s.stakeholder_identifier) as investor_name,"],
        "investor_country": ["array_to_string(array_agg(DISTINCT concat(investor_country.name, '#!#', investor_country.code_alpha3)), '##!##') as investor_country,",
                             "CONCAT(investor_country.name, '#!#', investor_country.code_alpha3) as investor_country,"],
        "investor_region": ["GROUP_CONCAT(DISTINCT CONCAT(investor_region.name, '#!#', investor_region.id) SEPARATOR '##!##') as investor_region,",
                            "CONCAT(investor_region.name, '#!#', investor_region.id) as investor_region,"],
        "intention": ["array_to_string(array_agg(DISTINCT intention.attributes->'intention' ORDER BY intention.attributes->'intention'), '##!##') AS intention,",
                      "intention.value AS intention,"],
        "crop": ["GROUP_CONCAT(DISTINCT CONCAT(crop.name, '#!#', crop.code ) SEPARATOR '##!##') AS crop,",
                 "CONCAT(crop.name, '#!#', crop.code ) AS crop,"],
        "deal_availability": ["a.availability AS availability, ", "a.availability AS availability, "],
        "data_source_type": ["GROUP_CONCAT(DISTINCT CONCAT(data_source_type.value, '#!#', data_source_type.group) SEPARATOR '##!##') AS data_source_type, ",
                             " data_source_type.value AS data_source_type, "],
        "target_country": [" array_to_string(array_agg(DISTINCT deal_country.id), '##!##') as target_country, ",
                           " deal_country.id as target_country, "],
        "target_region": ["GROUP_CONCAT(DISTINCT deal_region.name SEPARATOR '##!##') as target_region, ",
                          " deal_region.name as target_region, "],
        "deal_size": ["IFNULL(pi_deal_size.value, 0) + 0 AS deal_size,",
                      "IFNULL(pi_deal_size.value, 0) + 0 AS deal_size,"],
        "year": ["pi_negotiation_status.year AS year, ", "pi_negotiation_status.year AS year, "],
        "deal_count": ["COUNT(DISTINCT a.activity_identifier) as deal_count,",
                       "COUNT(DISTINCT a.activity_identifier) as deal_count,"],
        "availability": ["SUM(a.availability) / COUNT(a.activity_identifier) as availability,",
                         "SUM(a.availability) / COUNT(a.activity_identifier) as availability,"],
        "primary_investor": ["array_to_string(array_agg(DISTINCT p.name), '##!##') as primary_investor,",
                             "array_to_string(array_agg(DISTINCT p.name), '##!##') as primary_investor,"],
        "negotiation_status": [
            """array_to_string(
                    array_agg(
                        DISTINCT concat(
                            negotiation_status.attributes->'negotiation_status',
                            '#!#',
                            COALESCE(EXTRACT(YEAR FROM negotiation_status.date), 0)
                        )
                    ),
                    '##!##'
                ) as negotiation_status,"""
        ],
        "implementation_status": [
            """array_to_string(
                    array_agg(
                        DISTINCT concat(
                            implementation_status.attributes->'implementation_status',
                            '#!#',
                            COALESCE(EXTRACT(YEAR FROM implementation_status.date), 0)
                        )
                    ),
                    '##!##'
                ) as implementation_status,"""
        ],
        "nature_of_the_deal": ["array_to_string(array_agg(DISTINCT nature_of_the_deal.value), '##!##') as nature_of_the_deal,"],
        "data_source": ["GROUP_CONCAT(DISTINCT CONCAT(data_source_type.value, '#!#', data_source_type.group) SEPARATOR '##!##') AS data_source_type, GROUP_CONCAT(DISTINCT CONCAT(data_source_url.value, '#!#', data_source_url.group) SEPARATOR '##!##') as data_source_url, GROUP_CONCAT(DISTINCT CONCAT(data_source_date.value, '#!#', data_source_date.group) SEPARATOR '##!##') as data_source_date, GROUP_CONCAT(DISTINCT CONCAT(data_source_organisation.value, '#!#', data_source_organisation.group) SEPARATOR '##!##') as data_source_organisation,"],
        "contract_farming": ["array_to_string(array_agg(DISTINCT contract_farming.value), '##!##') as contract_farming,"],
        "intended_size": ["0 AS intended_size,"],
        "contract_size": ["0 AS contract_size,"],
        "production_size": ["0 AS production_size,"],
        "location": ["array_to_string(array_agg(DISTINCT location.value), '##!##') AS location,"],
        "deal_id": ["a.activity_identifier as deal_id,", "a.activity_identifier as deal_id,"],
        "latlon": ["GROUP_CONCAT(DISTINCT CONCAT(latitude.value, '#!#', longitude.value, '#!#', level_of_accuracy.value) SEPARATOR '##!##') as latlon,"],
    }
#             AND (intention.value IS NULL OR intention.value != 'Mining')

    ## operation => (numeric operand, character operand, description )
    OPERATION_MAP = {
        "is" :      ("= %s", "= '%s'", _("is")),
        "in":       ("IN (%s)", "IN (%s)", _("is one of")),
        "not_in":   ("NOT IN (%s)", "NOT IN (%s)", _("isn't any of")),
        "gte":      (">= %s", ">= %s", _("is >=")),
        "gt":       ("> %s", "> '%s'", _("is >")),
        "lte":      ("<= %s", "<= '%s'", _("is <=")),
        "lt":       ("< %s", "< '%s'", _("is <")),
        "contains": ("LIKE '%%%%%%%%%s%%%%%%%%'", "LIKE '%%%%%%%%%s%%%%%%%%'", _("contains")),
        "is_empty": ("IS NULL", "IS NULL", _("is empty")),
    }


