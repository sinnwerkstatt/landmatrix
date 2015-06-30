__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.conf import settings

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
        columns_sql = ''
        for c in self.columns:
            columns_sql += self.column_sql(c)
        return columns_sql

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

