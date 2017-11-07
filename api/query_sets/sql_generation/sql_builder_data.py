import collections

from api.query_sets.sql_generation.join_functions import *
from landmatrix.models.country import Country
from landmatrix.models.region import Region
from landmatrix.models.investor import Investor, InvestorActivityInvolvement, InvestorVentureInvolvement
from landmatrix.models.crop import Crop


class DefaultDict(collections.defaultdict):
    '''
    defaultdict that passes the key name to the default value factory.
    '''
    def __missing__(self, key):
        return self.default_factory(key)


def default_column_map(column_name):
    '''
    Fallback value for any column without explicit sql.
    '''
    column_sql = 'ARRAY_AGG(DISTINCT {column}.value) AS {column}'.format(
        column=column_name)

    return [column_sql]


def default_column(column_name):
    '''
    Fallback value for any column without explicit joins.
    '''
    return [join_attributes(column_name)]


class SQLBuilderData:
    GROUP_TO_NAME = {
        'all':                  "'all deals'",
        'target_region':        'deal_region.name',
        'target_country':       'deal_country.name',
        'year':                 'SUBSTR(negotiation_status.date, 1, 4)',
        #'crop':                 'crop.name', # breaks table group view "by crop"
        'intention':            'intention.value',
        'operational_stakeholder_region':      'operational_stakeholder_region.name',
        #'parent_stakeholder_country':     'parent_stakeholder_country.name',
        #'parent_stakeholder_name':        'parent_stakeholder.name',
        #'investor_region':      'investor_region.name',
        #'investor_country':     'investor_country.name',
        'data_source_type':     'data_source_type.value'
    }
    # TODO: should country actually join region?
    TARGET_COUNTRY_COLUMNS = (
        'target_country', [
            join_attributes('target_country'),
            join(
                Country, 'deal_country',
                on="CAST(target_country.value AS numeric) = deal_country.id"
            ),
            join_expression(Region, 'deal_region', 'deal_country.fk_region_id')
        ]
    )
    INVESTOR_COLUMNS = [
        join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
        join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
        join(InvestorVentureInvolvement, 'ivi', on="ivi.fk_venture_id = operational_stakeholder.id AND ivi.role = 'ST'"),
        join(Investor, 'stakeholders', on='ivi.fk_investor_id = stakeholders.id'),
    ]
    COLUMNS = DefaultDict(default_column, {
        # Operational stakeholders (= Operating companies)
        'operational_stakeholder': [
            join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
            join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id')
        ],
        'operating_company_country': [
            join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
            join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
            join(Country, 'operational_stakeholder_country', on='operational_stakeholder_country.id = operational_stakeholder.fk_country_id'),
        ],
        'operating_company_region': [
            join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
            join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
            join(Country, 'operational_stakeholder_country', on='operational_stakeholder_country.id = operational_stakeholder.fk_country_id'),
            join(Region, 'operational_stakeholder_region', on='operational_stakeholder_region.id = operational_stakeholder_country.fk_region_id')
        ],
        "operating_company_classification": [
            join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
            join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
        ],
        "operating_company_homepage": [
            join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
            join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
        ],
        "operating_company_opencorporates_link": [
            join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
            join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
        ],
        "operating_company_comment": [
            join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
            join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
        ],
        # Parent stakeholders (= Parent companies and investors of Operating company)
        'investor_name': INVESTOR_COLUMNS,
        'investor_country': INVESTOR_COLUMNS + [
            join(Country, 'investor_country', on='investor_country.id = stakeholders.fk_country_id'),
        ],
        'investor_region': INVESTOR_COLUMNS + [
            join(Country, 'investor_country', on='investor_country.id = stakeholders.fk_country_id'),
            join(Region, 'investor_region', on='investor_region.id = investor_country.fk_region_id')
        ],
        'parent_stakeholder': INVESTOR_COLUMNS,
        'parent_stakeholder_percentage': [
            join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
            join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
            join(InvestorVentureInvolvement, 'ivi', on='ivi.fk_venture_id = operational_stakeholder.id AND ivi.role = "ST"'),
        ],
        'parent_stakeholder_classification': INVESTOR_COLUMNS,
        'parent_stakeholder_country': INVESTOR_COLUMNS + [
            join(Country, 'parent_stakeholder_country', on='parent_stakeholder_country.id = stakeholders.fk_country_id'),
        ],
        'parent_stakeholder_region': INVESTOR_COLUMNS + [
            join(Country, 'parent_stakeholder_country', on='parent_stakeholder_country.id = stakeholders.fk_country_id'),
            join(Region, 'parent_stakeholder_region', on='parent_stakeholder_region.id = parent_stakeholder_country.fk_region_id')
        ],
        'parent_stakeholder_homepage': INVESTOR_COLUMNS,
        'parent_stakeholder_opencorporates_link': INVESTOR_COLUMNS,
        'parent_stakeholder_comment': INVESTOR_COLUMNS,
        # Deal variables
        'deal_count': [],
        'availability': [],
        'year': [ join_attributes('negotiation_status') ],
        'crop':               [
            join_attributes('akvl1', 'crops'),
            join_expression(Crop, 'crop', "CAST(akvl1.value AS NUMERIC)")
        ],
        'crops':               [
            join_attributes('akvl1', 'crops'),
            join_expression(Crop, 'crops', "CAST(akvl1.value AS NUMERIC)")
        ],
        'target_country': TARGET_COUNTRY_COLUMNS,
        'target_region': TARGET_COUNTRY_COLUMNS,
        'data_source_type':   (
            'data_source',
            [join_attributes('data_source_type', 'type')],
        ),
        'data_source':        [
            join_attributes('data_source_type', 'type'),
            join_attributes('data_source_url', 'url'),
            join_attributes('data_source_organisation', 'company'),
            join_attributes('data_source_date', 'date'),
        ],
        'contract_farming':   [join_attributes('contract_farming', 'off_the_lease'),],
        'nature_of_the_deal': [join_attributes('nature_of_the_deal', 'nature')],
        'latlon':             [
            join_activity_attributes('latitude', 'point_lat'),
            join_activity_attributes('longitude', 'point_lon'),
            join_activity_attributes('level_of_accuracy', 'level_of_accuracy'),
        ],
    })
    SQL_COLUMN_MAP = DefaultDict(default_column_map, {
        # Operational stakeholder (= Operating company)
        #"operational_stakeholder_name": [
        #    "ARRAY_AGG(DISTINCT CONCAT(stakeholders.name, '#!#', stakeholders.investor_identifier)) AS operational_stakeholder_name",
        #    "CONCAT(stakeholders.name, '#!#', stakeholders.investor_identifier) AS operational_stakeholder_name"
        #],
        "operational_stakeholder_name": [
            "ARRAY_AGG(DISTINCT operational_stakeholder.name) AS operational_stakeholder_name",
        ],
        "operating_company_country": [
            "ARRAY_AGG(DISTINCT CONCAT(operational_stakeholder_country.name, '#!#', operational_stakeholder_country.code_alpha3)) AS operating_company_country",
            "CONCAT(operational_stakeholder_country.name, '#!#', operational_stakeholder_country.code_alpha3) AS operating_company_country"
        ],
        "operating_company_region": [
            "ARRAY_AGG(DISTINCT CONCAT(operational_stakeholder_region.name, '#!#', operational_stakeholder_region.id)) AS operating_company_region",
            "CONCAT(operational_stakeholder_region.name, '#!#', operational_stakeholder_region.id) AS operating_company_region"
        ],
        "operating_company_classification": [
            "ARRAY_AGG(DISTINCT operational_stakeholder.classification) AS operating_company_classification",
        ],
        "operating_company_homepage": [
            "ARRAY_AGG(DISTINCT operational_stakeholder.homepage) AS operating_company_homepage",
        ],
        "operating_company_opencorporates_link": [
            "ARRAY_AGG(DISTINCT operational_stakeholder.opencorporates_link) AS operating_company_opencorporates_link",
        ],
        "operating_company_comment": [
            "ARRAY_AGG(DISTINCT operational_stakeholder.comment) AS operating_company_comment",
        ],
        # Parent stakeholders (= Parent companies and investors of Operating company)
        "investor_id": [
            "ARRAY_AGG(DISTINCT stakeholders.investor_identifier) AS investor_id",
            "stakeholders.investor_identifier AS investor_id"
        ],
        "investor_name": [
            "ARRAY_AGG(DISTINCT CONCAT(stakeholders.name, '#!#', stakeholders.investor_identifier)) AS investor_name",
            "CONCAT(stakeholders.name, '#!#', stakeholders.investor_identifier) AS investor_name"
        ],
        "investor_country": [
            "ARRAY_AGG(DISTINCT CONCAT(investor_country.name, '#!#', investor_country.code_alpha3)) AS investor_country",
            "CONCAT(investor_country.name, '#!#', investor_country.code_alpha3) AS investor_country"
        ],
        "investor_region": [
            "ARRAY_AGG(DISTINCT CONCAT(investor_region.name, '#!#', investor_region.id)) AS investor_region",
            "CONCAT(investor_region.name, '#!#', investor_region.id) AS investor_region"
        ],
        "parent_stakeholder": [
            "ARRAY_AGG(stakeholders.name) AS parent_stakeholder",
            "stakeholders.name AS parent_stakeholder",
        ],
        "parent_stakeholder_percentage": [
            "ARRAY_AGG(ivi.percentage) AS parent_stakeholder_percentage",
            "ivi.percentage AS parent_stakeholder_percentage",
        ],
        "parent_stakeholder_country": [
            "ARRAY_AGG(DISTINCT CONCAT(parent_stakeholder_country.name, '#!#', parent_stakeholder_country.code_alpha3)) AS parent_stakeholder_country",
            "CONCAT(parent_stakeholder_country.name, '#!#', parent_stakeholder_country.code_alpha3) AS parent_stakeholder_country"
        ],
        "parent_stakeholder_region": [
            "ARRAY_AGG(DISTINCT CONCAT(parent_stakeholder_region.name, '#!#', parent_stakeholder_region.id)) AS parent_stakeholder_region",
            "CONCAT(parent_stakeholder_region.name, '#!#', parent_stakeholder_region.id) AS parent_stakeholder_region"
        ],
        "parent_stakeholder_classification": [
            "ARRAY_AGG(stakeholders.classification) AS parent_stakeholder_classification",
            "stakeholders.classification AS parent_stakeholder_classification",
        ],
        "parent_stakeholder_homepage": [
            "ARRAY_AGG(stakeholders.homepage) AS parent_stakeholder_homepage",
            "stakeholders.homepage AS parent_stakeholder_homepage",
        ],
        "parent_stakeholder_opencorporates_link": [
            "ARRAY_AGG(stakeholders.opencorporates_link) AS parent_stakeholder_opencorporates_link",
            "stakeholders.opencorporates_link AS parent_stakeholder_opencorporates_link",
        ],
        "parent_stakeholder_comment": [
            "ARRAY_AGG(stakeholders.comment) AS parent_stakeholder_comment",
            "stakeholders.comment AS parent_stakeholder_comment",
        ],
        # Deal variables
        "intention": [
            "ARRAY_AGG(DISTINCT intention.value ORDER BY intention.value) AS intention",
            "intention.value AS intention"
        ],
        "crop": [
            "ARRAY_AGG(DISTINCT CONCAT(crop.name, '#!#', crop.code )) AS crop",
            "CONCAT(crop.name, '#!#', crop.code ) AS crop"
        ],
        "crops": [
            "ARRAY_AGG(DISTINCT crops.name) AS crops",
        ],
        "deal_availability": ["a.availability AS availability", "a.availability AS availability"],
        "data_source_type": [
            "ARRAY_AGG(DISTINCT data_source_type.value) AS data_source_type",
            "data_source_type.value AS data_source_type"
        ],
        "target_country": [
            "ARRAY_AGG(DISTINCT deal_country.name) AS target_country",
            "deal_country.name AS target_country"
        ],
        "target_region": [
            "ARRAY_AGG(DISTINCT deal_region.name) AS target_region",
            " deal_region.name AS target_region"
        ],
        "deal_size": [
            "IFNULL(a.deal_size, 0) + 0 AS deal_size",
            "IFNULL(a.deal_size, 0) + 0 AS deal_size"
        ],
        "year": [
            "SUBSTR(negotiation_status.date, 1, 4) AS year",
            "SUBSTR(negotiation_status.date, 1, 4) AS year"
        ],
        "deal_count": [
            "COUNT(DISTINCT a.activity_identifier) as deal_count",
            "COUNT(DISTINCT a.activity_identifier) as deal_count"
        ],
        "availability": [
            "SUM(a.availability) / COUNT(a.activity_identifier) AS availability",
            "SUM(a.availability) / COUNT(a.activity_identifier) AS availability"
        ],
        "operational_stakeholder": [
            "ARRAY_AGG(DISTINCT operational_stakeholder.name) AS operational_stakeholder",
            "ARRAY_AGG(DISTINCT operational_stakeholder.name) AS operational_stakeholder"
        ],
        "negotiation_status": [
            """ARRAY_AGG(DISTINCT CONCAT(
                        negotiation_status.value,
                        '#!#',
                        negotiation_status.date,
                        '#!#',
                        negotiation_status.is_current
                )) AS negotiation_status"""
        ],
        "implementation_status": [
            """CASE WHEN (
                ARRAY_AGG(
                    DISTINCT CONCAT(
                        implementation_status.value,
                        '#!#',
                        implementation_status.date,
                        '#!#',
                        implementation_status.is_current
                    )
                ) = '{#!##!#}') THEN NULL
                ELSE ARRAY_AGG(
                    DISTINCT CONCAT(
                        implementation_status.value,
                        '#!#',
                        implementation_status.date,
                        '#!#',
                        implementation_status.is_current
                    )
                ) END AS implementation_status"""
        ],
        "intended_size": [
            "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intended_size.value), ', '), '') AS intended_size",
            "0 AS intended_size"
        ],
        # TODO: surely 0 as contract_size, etc. isn't right
        "contract_size": [
            # TODO: This creates the array twice, should be optimized by someone who's more into postgres
            "(ARRAY_AGG(DISTINCT contract_size.value))[ARRAY_LENGTH(ARRAY_AGG(DISTINCT contract_size.value), 1)] AS contract_size",
            "0 AS contract_size"
        ],
        "production_size": [
            #"NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT production_size.value), get_group_sql, '), '') AS production_size",
            "(ARRAY_AGG(DISTINCT production_size.value))[ARRAY_LENGTH(ARRAY_AGG(DISTINCT production_size.value), 1)] AS production_size",
            "0 AS production_size"
        ],
        "deal_id": [
            "a.activity_identifier AS deal_id",
            "a.activity_identifier as deal_id"
        ],
        "latlon": [
            "ARRAY_AGG(DISTINCT CONCAT(latitude.value, '#!#', longitude.value, '#!#', level_of_accuracy.value)) AS latlon"
        ],
    })
