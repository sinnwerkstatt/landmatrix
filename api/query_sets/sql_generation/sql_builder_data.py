__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.sql_generation.join_functions import *
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
        'stakeholder_country': 'stakeholder_country.name',
        'investor_name':    "investor_name.attributes->'investor_name'",
        'stakeholder_name': 'stakeholders.name',
        'data_source_type': "data_source_type.attributes->'type'"
    }

    COLUMNS = { }
    def _setup_column_sql(self):
        if self.COLUMNS: return
        self.COLUMNS = {

            'intended_size': [join_attributes('intended_size')],
            'contract_size': [join_attributes('contract_size')],
            'production_size': [join_attributes('production_size')],

            'deal_count': [],
            'availability': [],

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

            'operational_stakeholder': [
                join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
                join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id')
            ],

            'stakeholder_name': [
                join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
                join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
                join(InvestorVentureInvolvement, 'ivi', on='ivi.fk_venture_id = operational_stakeholder.id'),
                join(Investor, 'stakeholders', on='ivi.fk_investor_id = stakeholders.id'),
            ],

            'stakeholder_country': [
                join(Country, 'stakeholder_country', on='stakeholder_country.id = stakeholders.fk_country_id'),
            ],

            'data_source_type':   ( 'data_source', [ join_attributes('data_source_type', 'type') ] ),

            'data_source':        [
                join_attributes('data_source_type', 'type'),
                join_attributes('data_source_url', 'url'),
                join_attributes('data_source_organisation', 'company'),
                join_attributes('data_source_date', 'date'),
            ],

            'contract_farming':   [ join_attributes('contract_farming', 'off_the_lease'), ],

            'nature_of_the_deal': [join_attributes('nature_of_the_deal', 'nature')],

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
        "stakeholder_name": [
            "ARRAY_AGG(DISTINCT stakeholders.name) AS stakeholder_name",
            "stakeholders.name AS stakeholder_name"
        ],
        "investor_country": [
            "ARRAY_AGG(DISTINCT CONCAT(investor_country.name, '#!#', investor_country.code_alpha3)) AS investor_country",
            "CONCAT(investor_country.name, '#!#', investor_country.code_alpha3) AS investor_country"
        ],
        "stakeholder_country": [
            "ARRAY_AGG(DISTINCT stakeholder_country.name) AS stakeholder_country",
            "stakeholder_country.name AS stakeholder_country"
        ],
        "investor_region": [
            "ARRAY_AGG(DISTINCT CONCAT(investor_region.name, '#!#', investor_region.id)) AS investor_region",
            "CONCAT(investor_region.name, '#!#', investor_region.id) AS investor_region"
        ],
        "intention": [
            "ARRAY_AGG(DISTINCT intention.attributes->'intention' ORDER BY intention.attributes->'intention') AS intention",
            "intention.attributes->'intention' AS intention"
        ],
        "crop": [
            "ARRAY_AGG(DISTINCT CONCAT(crop.name, '#!#', crop.code )) AS crop",
            "CONCAT(crop.name, '#!#', crop.code ) AS crop"
        ],
        "deal_availability": ["a.availability AS availability", "a.availability AS availability"],
        "data_source_type": [
#            "ARRAY_AGG(DISTINCT CONCAT(data_source_type.attributes->'type', '#!#', data_source_type.group)) AS data_source_type",
            "ARRAY_AGG(DISTINCT data_source_type.attributes->'type') AS data_source_type",
            "data_source_type.attributes->'type' AS data_source_type"
        ],
        "data_source_url": ["ARRAY_AGG(DISTINCT data_source_url.attributes->'url') AS data_source_url"],
        "data_source_date": ["ARRAY_AGG(DISTINCT data_source_date.attributes->'date') as data_source_date"],
        "data_source_organisation": [
            "ARRAY_AGG(DISTINCT data_source_organisation.attributes->'company') as data_source_organisation"
        ],
        "target_country": ["ARRAY_AGG(DISTINCT deal_country.name) AS target_country",
                           "deal_country.name AS target_country"],
        "target_region": ["ARRAY_AGG(DISTINCT deal_region.name) AS target_region",
                          " deal_region.name AS target_region"],
        "deal_size": ["IFNULL(pi_deal_size.value, 0) + 0 AS deal_size",
                      "IFNULL(pi_deal_size.value, 0) + 0 AS deal_size"],
        "year": ["EXTRACT(YEAR FROM pi_negotiation_status.date) AS year",
                 "EXTRACT(YEAR FROM pi_negotiation_status.date) AS year"],
        "deal_count": ["COUNT(DISTINCT a.activity_identifier) as deal_count",
                       "COUNT(DISTINCT a.activity_identifier) as deal_count"],
        "availability": ["SUM(a.availability) / COUNT(a.activity_identifier) AS availability",
                         "SUM(a.availability) / COUNT(a.activity_identifier) AS availability"],
        "primary_investor": ["ARRAY_AGG(DISTINCT p.name) AS primary_investor",
                             "ARRAY_AGG(DISTINCT p.name) AS primary_investor"],
        "operational_stakeholder": ["ARRAY_AGG(DISTINCT operational_stakeholder.name) AS investor",
                                    "ARRAY_AGG(DISTINCT operational_stakeholder.name) AS investor"],
        "negotiation_status": [
            """ARRAY_AGG(DISTINCT CONCAT(
                        negotiation_status.attributes->'negotiation_status',        '#!#',
                        EXTRACT(YEAR FROM negotiation_status.date)
                )) AS negotiation_status"""
        ],
        "implementation_status": [
            """CASE WHEN (
                ARRAY_AGG(
                    DISTINCT CONCAT(
                        implementation_status.attributes->'implementation_status',  '#!#',
                        EXTRACT(YEAR FROM implementation_status.date)
                    )
                ) = '{#!#}') THEN NULL
                ELSE ARRAY_AGG(
                    DISTINCT CONCAT(
                        implementation_status.attributes->'implementation_status',  '#!#',
                        EXTRACT(YEAR FROM implementation_status.date)
                    )
                ) END AS implementation_status"""
        ],
        "nature_of_the_deal": ["ARRAY_AGG(DISTINCT nature_of_the_deal.attributes->'nature') AS nature_of_the_deal"],
        "contract_farming": ["ARRAY_AGG(DISTINCT contract_farming.attributes->'off_the_lease') AS contract_farming"],
        "intended_size": [
            "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intended_size.attributes->'intended_size'), ', '), '') AS intended_size",
            "0 AS intended_size"
        ],
        "contract_size": [
            "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT contract_size.attributes->'contract_size'), ', '), '') AS contract_size",
            "0 AS contract_size"
        ],
        "production_size": [
            "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT production_size.attributes->'production_size'), ', '), '') AS production_size",
            "0 AS production_size"
        ],
        "location": ["ARRAY_AGG(DISTINCT location.attributes->'location') AS location"],
        "deal_id": ["a.activity_identifier AS deal_id", "a.activity_identifier as deal_id"],
        "latlon": [
            "ARRAY_AGG(DISTINCT CONCAT(latitude.value, '#!#', longitude.value, '#!#', level_of_accuracy.value)) AS latlon"
        ],
    }
