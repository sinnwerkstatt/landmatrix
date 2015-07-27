__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.views.sql_generation.join_functions import *
from landmatrix.models import *

class SQLBuilderData:

    def __init__(self):
        self._setup_column_sql()

    GROUP_TO_NAME = {
        'all':              "'all deals'",
        'target_region':    'deal_region.name',
        'target_country':   'deal_country.name',
        'year':             'EXTRACT(YEAR FROM pi_negotiation_status.date)',
        'crop':             'crop.name',
        'intention':        "intention.attributes->'intention'",
        'investor_region':  'investor_region.name',
        'investor_country': 'investor_country.name',
        'investor_name':    "investor_name.attributes->'investor_name'",
        'data_source_type': "data_source_type.attributes->'type'"
    }

    COLUMNS = { }
    def _setup_column_sql(self):
        if self.COLUMNS: return
        self.COLUMNS = {

            'intended_size': [join_attributes('intended_size')],
            'contract_size': [join_attributes('contract_size')],
            'production_size': [],

            'investor_country':   (
                'investor_country', [
                    join_attributes(
                        'skvl1', 'country',
                        attributes_model=StakeholderAttributeGroup, attribute_field='fk_stakeholder_id'
                    ),
                    join(
                        Country, 'investor_country',
                        on="investor_country.id = CAST(skvl1.attributes->'country' AS numeric)"
                    ),
                    join_expression(Region, 'investor_region', 'investor_country.fk_region_id')
                ]
            ),

            'investor_name':      [
                join(PrimaryInvestor, 'pi', 'i.fk_primary_investor_id = pi.id'),
                join(Status, 'pi_st', 'pi.fk_status_id = pi_st.id'),
                join_attributes(
                    'investor_name',
                    attributes_model=StakeholderAttributeGroup, attribute_field='fk_stakeholder_id'
                )
            ],

            'year': [ join_attributes('pi_negotiation_status') ],

            'crop':               [
                join_attributes('akvl1', 'crops'),
                join_expression(Crop, 'crop', "CAST(akvl1.attributes->'crops' AS NUMERIC)")
            ],

            'target_country':     (
                'target_country', [
                    join_attributes('target_country'),
                    join(
                        Country, 'deal_country',
                        on="CAST(target_country.attributes->'target_country' AS numeric) = deal_country.id"
                    ),
                    join_expression(Region, 'deal_region', 'deal_country.fk_region_id')
                ]
            ),

            'primary_investor':   [ join_expression(PrimaryInvestor, 'p', 'i.fk_primary_investor_id') ],

            'data_source_type':   ( 'data_source', [ join_attributes('data_source_type', 'type') ] ),

            'data_source':        [
                join_activity_attributes('data_source_type', 'type'),
                join_activity_attributes('data_source_url', 'url'),
                join_activity_attributes('data_source_organisation', 'company'),
                join_activity_attributes('data_source_date', 'date'),
            ],

            'contract_farming':   [ join_activity_attributes('contract_farming', 'off_the_lease'), ],

            'nature_of_the_deal': [ join_activity_attributes('nature_of_the_deal', 'nature'), ],

            'latlon':             [
                join_activity_attributes('latitude', 'point_lat'),
                join_activity_attributes('longitude', 'point_lon'),
                join_activity_attributes('level_of_accuracy', 'level_of_accuracy'),
            ],
        }
        self.COLUMNS['investor_region'] = self.COLUMNS['investor_country']
        self.COLUMNS['target_region'] = self.COLUMNS['target_country']

    SQL_COLUMN_MAP = {
        "investor_name": [
            "ARRAY_AGG(DISTINCT CONCAT(investor_name.attributes->'investor_name', '#!#', s.stakeholder_identifier)) AS investor_name",
            "CONCAT(investor_name.attributes->'investor_name', '#!#', s.stakeholder_identifier) AS investor_name"
        ],
        "investor_country": [
            "ARRAY_AGG(DISTINCT CONCAT(investor_country.name, '#!#', investor_country.code_alpha3)) AS investor_country",
            "CONCAT(investor_country.name, '#!#', investor_country.code_alpha3) AS investor_country"
        ],
        "investor_region": [
            "ARRAY_TO_STRING(ARRAY_AGG(DISTINCT CONCAT(investor_region.name, '#!#', investor_region.id)), '##!##') AS investor_region",
            "CONCAT(investor_region.name, '#!#', investor_region.id) AS investor_region"
        ],
        "intention": [
            "ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intention.attributes->'intention' ORDER BY intention.attributes->'intention'), '##!##') AS intention",
            "intention.attributes->'intention' AS intention"
        ],
        "crop": [
            "ARRAY_TO_STRING(ARRAY_AGG(DISTINCT CONCAT(crop.name, '#!#', crop.code )), '##!##') AS crop",
            "CONCAT(crop.name, '#!#', crop.code ) AS crop"
        ],
        "deal_availability": ["a.availability AS availability", "a.availability AS availability"],
        "data_source_type": [
#            "ARRAY_TO_STRING(ARRAY_AGG(DISTINCT CONCAT(data_source_type.attributes->'type', '#!#', data_source_type.group)), '##!##') AS data_source_type",
            "ARRAY_TO_STRING(ARRAY_AGG(DISTINCT data_source_type.attributes->'type'), '##!##') AS data_source_type",
            "data_source_type.attributes->'type' AS data_source_type"
        ],
        "target_country": ["ARRAY_TO_STRING(ARRAY_AGG(DISTINCT deal_country.name), '##!##') AS target_country",
                           "deal_country.name AS target_country"],
        "target_region": ["ARRAY_TO_STRING(ARRAY_AGG(DISTINCT deal_region.name), '##!##') AS target_region",
                          " deal_region.name AS target_region"],
        "deal_size": ["IFNULL(pi_deal_size.value, 0) + 0 AS deal_size",
                      "IFNULL(pi_deal_size.value, 0) + 0 AS deal_size"],
        "year": ["EXTRACT(YEAR FROM pi_negotiation_status.date) AS year",
                 "EXTRACT(YEAR FROM pi_negotiation_status.date) AS year"],
        "deal_count": ["COUNT(DISTINCT a.activity_identifier) as deal_count",
                       "COUNT(DISTINCT a.activity_identifier) as deal_count"],
        "availability": ["SUM(a.availability) / COUNT(a.activity_identifier) AS availability",
                         "SUM(a.availability) / COUNT(a.activity_identifier) AS availability"],
        "primary_investor": ["ARRAY_TO_STRING(ARRAY_AGG(DISTINCT p.name), '##!##') AS primary_investor",
                             "ARRAY_TO_STRING(ARRAY_AGG(DISTINCT p.name), '##!##') AS primary_investor"],
        "negotiation_status": [
            """ARRAY_TO_STRING(ARRAY_AGG(
                    DISTINCT CONCAT(
                        negotiation_status.attributes->'negotiation_status',        '#!#',
                        EXTRACT(YEAR FROM negotiation_status.date)
                    )), '##!##'
                ) AS negotiation_status"""
        ],
        "implementation_status": [
            """CASE WHEN (
                ARRAY_TO_STRING(ARRAY_AGG(
                    DISTINCT CONCAT(
                        implementation_status.attributes->'implementation_status',  '#!#',
                        EXTRACT(YEAR FROM implementation_status.date)
                    )), '##!##'
                ) = '#!#') THEN NULL
                ELSE ARRAY_TO_STRING(ARRAY_AGG(
                    DISTINCT CONCAT(
                        implementation_status.attributes->'implementation_status',  '#!#',
                        EXTRACT(YEAR FROM implementation_status.date)
                    )), '##!##'
                ) END AS implementation_status"""
        ],
        "nature_of_the_deal": ["ARRAY_TO_STRING(ARRAY_AGG(DISTINCT nature_of_the_deal.value), '##!##') AS nature_of_the_deal"],
        "data_source": [
            """GROUP_CONCAT(DISTINCT CONCAT(data_source_type.value, '#!#', data_source_type.group) SEPARATOR '##!##') AS data_source_type,
GROUP_CONCAT(DISTINCT CONCAT(data_source_url.value, '#!#', data_source_url.group) SEPARATOR '##!##') as data_source_url,
GROUP_CONCAT(DISTINCT CONCAT(data_source_date.value, '#!#', data_source_date.group) SEPARATOR '##!##') as data_source_date,
GROUP_CONCAT(DISTINCT CONCAT(data_source_organisation.value, '#!#', data_source_organisation.group) SEPARATOR '##!##') as data_source_organisation"""
        ],
        "contract_farming": ["ARRAY_TO_STRING(ARRAY_AGG(DISTINCT contract_farming.value), '##!##') AS contract_farming"],
        "intended_size": ["0 AS intended_size"],
        "contract_size": ["0 AS contract_size"],
        "production_size": ["0 AS production_size"],
        "location": ["ARRAY_TO_STRING(ARRAY_AGG(DISTINCT location.value), '##!##') AS location"],
        "deal_id": ["a.activity_identifier AS deal_id", "a.activity_identifier as deal_id"],
        "latlon": [
            "GROUP_CONCAT(DISTINCT CONCAT(latitude.value, '#!#', longitude.value, '#!#', level_of_accuracy.value) SEPARATOR '##!##') AS latlon"
        ],
    }
