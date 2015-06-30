__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.conf import settings


def join_attributes(table_alias, attribute, attribute_table='landmatrix_activityattributegroup', attribute_field='fk_activity_id'):
    from string import Template
    template = Template("""
          LEFT JOIN $table AS $alias ON (a.id = $alias.$field AND $alias.attributes ? '$attr')"""
    )
    return template.substitute(alias=table_alias, attr=attribute, table=attribute_table, field=attribute_field)

class SQLBuilder:
    def __init__(self, columns, group):
        if (settings.DEBUG): print(type(self).__name__)
        self.columns = columns
        self.group = group

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
    def get_name_sql(self):
        return self.GROUP_TO_NAME.get(self.group, "'%s'" % self.group)

    def get_where_sql(self):
        raise RuntimeError('SQLBuilder.get_where_sql() not implemented')

    def get_group_sql(self):
        raise RuntimeError('SQLBuilder.get_group_sql() not implemented')

    def get_inner_group_sql(self):
        return ''

    def get_columns_sql(self):
        raise RuntimeError('SQLBuilder.get_columns_sql() not implemented')

    def get_sub_columns_sql(self):
        return ''

    @classmethod
    def get_base_sql(cls):
        raise RuntimeError('SQLBuilder.get_base_sql() not implemented')

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


class ListSQLBuilder(SQLBuilder):

    def __init__(self, columns, group, group_value):
        super(ListSQLBuilder, self).__init__(columns, group)
        self.group_value = group_value

    GROUP_CONDITIONS = {
        "target_region":    ' AND deal_region.slug = lower(\'%s\') ',
        "target_country":   ' AND deal_country.slug = lower(\'%s\') ',
        "year":             ' AND pi_negotiation_status.year = \'%s\' ',
        "crop":             ' AND crop.slug = lower(\'%s\') ',
        "intention":        ' AND lower(replace(intention.value, \' \', \'-\')) = lower(\'%s\') ',
        "investor_region":  ' AND investor_region.slug = \'%s\' ',
        "investor_country": ' AND investor_country.slug = \'%s\' ',
        "investor_name":    ' AND s.stakeholder_identifier = \'%s\' ',
        "data_source_type": ' AND lower(replace(replace(data_source_type.value, \' \', \'-\'), \'/\', \'+\')) = lower(\'%s\') '
    }
    def get_where_sql(self):
        if self.group != "all"and self.group_value:
            return self.GROUP_CONDITIONS[self.group] % self.group_value
        return ''

    def get_group_sql(self):
        group_by_sql = " GROUP BY a.id "
        additional_group_by = []
        for c in [ col for col in self.columns if not col in ["intended_size", "contract_size", "production_size", "data_source"]]:
            additional_group_by.append("sub.%(name)s" % {"name": c})
        if (settings.DEBUG): print('addnl group by:', additional_group_by)
        if additional_group_by: group_by_sql += ', ' + ', '.join(additional_group_by)

        return group_by_sql

    def get_columns_sql(self):
        columns_sql = ''
        for c in self.columns:
            if c in ("intended_size", "contract_size", "production_size"):
                pass
            elif c == "data_source":
                columns_sql += "                " + self.SQL_COLUMN_MAP.get(c)[0] + "\n"
            else:
                columns_sql += "                " + self.SQL_COLUMN_MAP.get(c)[0] + "\n"
        return columns_sql

    def get_sub_columns_sql(self):
        sub_columns_sql = ''
        for c in self.columns:
            if c in ("intended_size", "contract_size", "production_size"):
                sub_columns_sql += "            ARRAY_AGG(%(name)s.attributes->'%(name)s' ORDER BY %(name)s.date DESC) as %(name)s,\n" % {"name": c}
            elif c == "data_source":
                sub_columns_sql += "            sub.data_source_type as data_source_type, sub.data_source_url as data_source_url, sub.data_source_date data_source_date, sub.data_source_organisation as data_source_organisation,\n"
            else:
                sub_columns_sql += "            sub.%(name)s as %(name)s,\n" % {"name": c}
        return sub_columns_sql

    @classmethod
    def get_base_sql(cls):
        return u"""
        SELECT
            sub.name as name,
%(sub_columns)s            'dummy' as dummy
          FROM
            landmatrix_activity AS a""" \
            + join_attributes('size', 'pi_deal_size') \
            + join_attributes('intended_size', 'intended_size') \
            + join_attributes('contract_size', 'contract_size') \
            + join_attributes('production_size', 'production_size') \
            + \
        """
          JOIN (
            SELECT DISTINCT
              a.id as id,
              %(name)s as name,
%(columns)s                'dummy' as dummy
            FROM
              landmatrix_activity a
            JOIN landmatrix_status ON (landmatrix_status.id = a.fk_status_id)
              %(from)s""" \
            + join_attributes('pi_deal', 'pi_deal') \
            + join_attributes('deal_scope', 'deal_scope') \
            + """
            %(from_filter_activity)s
            %(from_filter_investor)s
          WHERE
            a.version = (
                SELECT max(version)
                FROM landmatrix_activity amax, landmatrix_status st
                WHERE amax.fk_status_id = st.id
                  AND amax.activity_identifier = a.activity_identifier
                  AND st.name IN ('active', 'overwritten', 'deleted')
            )
            AND landmatrix_status.name in ('active', 'overwritten')
            AND pi_deal.attributes->'pi_deal' = 'True'
            AND (NOT DEFINED(intention.attributes, 'intention') OR intention.attributes->'intention' != 'Mining')
            %(where)s
            %(where_filter_investor)s
            %(where_filter_activity)s
            GROUP BY a.id
            ) AS sub ON (sub.id = a.id)
         %(group_by)s, sub.name
         %(order_by)s
         %(limit)s;
    """

class GroupSQLBuilder(SQLBuilder):

    def __init__(self, columns, group, filters):
        super(GroupSQLBuilder, self).__init__(columns, group)
        self.filters = filters

    def get_where_sql(self):
        if not self.filters.get("starts_with", None): return ''

        starts_with = self.filters.get("starts_with", "").lower()
        if self.group == "investor_country":
            return " AND investor_country.slug like '%s%%%%' " % starts_with
        elif self.group == "target_country":
            return " AND deal_country.slug like '%s%%%%' " % starts_with
        return " AND trim(lower(%s.value)) like '%s%%%%' " % (self.group, starts_with)

    def get_group_sql(self):
        if self.group:  return "GROUP BY %s" % self.group
        else:           return 'GROUP BY dummy'

    def get_inner_group_sql(self):
        # query deals grouped by a key
        return ", %s" % self.group

    def get_columns_sql(self):
        columns_sql = ''
        for c in self.columns:
            # get sql for columns
            if c == self.group:
                # use single values for column which gets grouped by
                columns_sql += self.SQL_COLUMN_MAP.get(c)[1] + "\n"
            else:
                columns_sql += self.SQL_COLUMN_MAP.get(c)[0] + "\n"
        return columns_sql

    @classmethod
    def get_base_sql(cls):
        return u"""
        SELECT DISTINCT
              %(name)s as name,
              %(columns)s
              'dummy' as dummy
        FROM
            landmatrix_activity AS a
        JOIN landmatrix_status ON (landmatrix_status.id = a.fk_status_id)
            %(from)s
        LEFT JOIN landmatrix_activityattributegroup AS pi_deal
            ON (a.id = pi_deal.fk_activity_id AND LENGTH(pi_deal.attributes->'pi_deal') > 0)
        LEFT JOIN landmatrix_activityattributegroup AS deal_scope
            ON (a.id = deal_scope.fk_activity_id AND LENGTH(deal_scope.attributes->'deal_scope') > 0)
        %(from_filter_activity)s
        %(from_filter_investor)s
        WHERE
            a.version = (
                SELECT max(version) FROM landmatrix_activity amax, landmatrix_status st
                WHERE amax.fk_status_id = st.id
                  AND amax.activity_identifier = a.activity_identifier
                  AND st.name IN ('active', 'overwritten', 'deleted')
            )
            AND landmatrix_status.name in ('active', 'overwritten')
            AND pi_deal.attributes->'pi_deal' = 'True'
            AND (pi_deal.attributes->'intention' != 'Mining')
            %(where)s
            %(where_filter_investor)s
            %(where_filter_activity)s
         %(group_by)s
         %(order_by)s
         %(limit)s;
    """
