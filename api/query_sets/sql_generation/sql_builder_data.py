__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from api.query_sets.sql_generation.join_functions import *
from landmatrix.models import *


class SQLBuilderData:

    def __init__(self):
        self._setup_column_sql()

    GROUP_TO_NAME = {
        'all':                  "'all deals'",
        'target_region':        'deal_region.name',
        'target_country':       'deal_country.name',
        'year':                 'SUBSTR(negotiation_status.date, 1, 4)',
        'crop':                 'crop.name',
        'intention':            'intention.value',
        'investor_region':      'investor_region.name',
        'investor_country':     'investor_country.name',
        'investor_name':        'stakeholders.name',
        'data_source_type':     'data_source_type.value'
    }

    COLUMNS = { }
    def _setup_column_sql(self):
        if self.COLUMNS: return
        self.COLUMNS = {

            'intended_size': [
                join_attributes('intended_size')
            ],
            'contract_size': [
                join_attributes('contract_size')
            ],
            'production_size': [
                join_attributes('production_size')
            ],

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

            'target_country':     (
                'target_country', [
                    join_attributes('target_country'),
                    join(
                        Country, 'deal_country',
                        on="CAST(target_country.value AS numeric) = deal_country.id"
                    ),
                    join_expression(Region, 'deal_region', 'deal_country.fk_region_id')
                ]
            ),

            'operational_stakeholder': [
                join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
                join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id')
            ],

            'investor_name': [
                join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
                join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
                join(InvestorVentureInvolvement, 'ivi', on='ivi.fk_venture_id = operational_stakeholder.id'),
                join(Investor, 'stakeholders', on='ivi.fk_investor_id = stakeholders.id'),
            ],

            'investor_country': [
                join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
                join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
                join(InvestorVentureInvolvement, 'ivi', on='ivi.fk_venture_id = operational_stakeholder.id'),
                join(Investor, 'stakeholders', on='ivi.fk_investor_id = stakeholders.id'),
                join(Country, 'investor_country', on='investor_country.id = stakeholders.fk_country_id'),
            ],

            'investor_region': [
                join(InvestorActivityInvolvement, 'iai', on='a.id = iai.fk_activity_id'),
                join(Investor, 'operational_stakeholder', on='iai.fk_investor_id = operational_stakeholder.id'),
                join(InvestorVentureInvolvement, 'ivi', on='ivi.fk_venture_id = operational_stakeholder.id'),
                join(Investor, 'stakeholders', on='ivi.fk_investor_id = stakeholders.id'),
                join(Country, 'investor_country', on='investor_country.id = stakeholders.fk_country_id'),
                join(Region, 'investor_region', on='investor_region.id = investor_country.fk_region_id')
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
            # FIXME: The following lines can probably be removed, since this is the default case
            # see also: SQLBuilder._add_join_for_column
            'tg_location_comment': [
                join_attributes('tg_location_comment'),
            ],
            "tg_not_public_comment": [
                join_attributes('tg_not_public_comment'),
            ],
            "tg_feedback_comment": [
                join_attributes('tg_feedback_comment'),
            ],
            "tg_contract_comment": [
                join_attributes('tg_contract_comment'),
            ],
            "tg_data_source_comment": [
                join_attributes('tg_data_source_comment'),
            ],
            "tg_total_number_of_jobs_created_comment": [
                join_attributes('tg_total_number_of_jobs_created_comment'),
            ],
            "tg_foreign_jobs_created_comment": [
                join_attributes('tg_foreign_jobs_created_comment'),
            ],
            "tg_domestic_jobs_created_comment": [
                join_attributes('tg_domestic_jobs_created_comment'),
            ],
            "tg_land_use_comment": [
                join_attributes('tg_land_use_comment'),
            ],
            "tg_gender_specific_info_comment": [
                join_attributes('tg_gender_specific_info_comment'),
            ],
            "tg_land_area_comment": [
                join_attributes('tg_land_area_comment'),
            ],
            "tg_land_cover_comment": [
                join_attributes('tg_land_cover_comment'),
            ],
            "tg_intention_comment": [
                join_attributes('tg_intention_comment'),
            ],
            "tg_nature_comment": [
                join_attributes('tg_nature_comment'),
            ],
            "tg_negotiation_status_comment": [
                join_attributes('tg_negotiation_status_comment'),
            ],
            "tg_implementation_status_comment": [
                join_attributes('tg_implementation_status_comment'),
            ],
            "tg_purchase_price_comment": [
                join_attributes('tg_purchase_price_comment'),
            ],
            "tg_leasing_fees_comment": [
                join_attributes('tg_leasing_fees_comment'),
            ],
            "tg_contract_farming_comment": [
                join_attributes('tg_contract_farming_comment'),
            ],
            "tg_affected_comment": [
                join_attributes('tg_affected_comment'),
            ],
            "tg_recognition_status_comment": [
                join_attributes('tg_recognition_status_comment'),
            ],
            "tg_community_consultation_comment": [
                join_attributes('tg_community_consultation_comment'),
            ],
            "tg_community_reaction_comment": [
                join_attributes('tg_community_reaction_comment'),
            ],
            "tg_land_conflicts_comment": [
                join_attributes('tg_land_conflicts_comment'),
            ],
            "tg_number_of_displaced_people_comment": [
                join_attributes('tg_number_of_displaced_people_comment'),
            ],
            "tg_negative_impacts_comment": [
                join_attributes('tg_negative_impacts_comment'),
            ],
            "tg_promised_benefits_comment": [
                join_attributes('tg_promised_benefits_comment'),
            ],
            "tg_materialized_benefits_comment": [
                join_attributes('tg_materialized_benefits_comment'),
            ],
            "tg_overall_comment": [
                join_attributes('tg_overall_comment'),
            ],
            "tg_crops_comment": [
                join_attributes('tg_crops_comment'),
            ],
            "tg_animals_comment": [
                join_attributes('tg_animals_comment'),
            ],
            "tg_minerals_comment": [
                join_attributes('tg_minerals_comment'),
            ],
            "tg_contract_farming_crops_comment": [
                join_attributes('tg_contract_farming_crops_comment'),
            ],
            "tg_contract_farming_animals_comment": [
                join_attributes('tg_contract_farming_animals_comment'),
            ],
            "tg_use_of_produce_comment": [
                join_attributes('tg_use_of_produce_comment'),
            ],
            "tg_in_country_processing_comment": [
                join_attributes('tg_in_country_processing_comment'),
            ],
            "tg_vggt_applied_comment": [
                join_attributes('tg_vggt_applied_comment'),
            ],
            "tg_prai_applied_comment": [
                join_attributes('tg_prai_applied_comment'),
            ],
            "tg_water_extraction_envisaged_comment": [
                join_attributes('tg_water_extraction_envisaged_comment'),
            ],
            "tg_how_much_do_investors_pay_comment": [
                join_attributes('tg_how_much_do_investors_pay_comment'),
            ],
            "tg_water_extraction_amount_comment": [
                join_attributes('tg_water_extraction_amount_comment'),
            ],
            "tg_use_of_irrigation_infrastructure_comment": [
                join_attributes('tg_use_of_irrigation_infrastructure_comment'),
            ],
            "tg_action_comment": [
                join_attributes('tg_action_comment'),
            ],
            "tg_operational_stakeholder_comment": [
                join_attributes('tg_operational_stakeholder_comment'),
            ],
            "tg_public_user_comment": [
                join_attributes('tg_public_user_comment'),
            ],
        }
        self.COLUMNS['target_region'] = self.COLUMNS['target_country']

    SQL_COLUMN_MAP = {
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
        "data_source_url": [
            "ARRAY_AGG(DISTINCT data_source_url.value) AS data_source_url"#
        ],
        "data_source_date": [
            "ARRAY_AGG(DISTINCT data_source_date.value) as data_source_date"
        ],
        "data_source_organisation": [
            "ARRAY_AGG(DISTINCT data_source_organisation.value) as data_source_organisation"
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
                        SUBSTR(negotiation_status.date, 1, 4)
                )) AS negotiation_status"""
        ],
        "implementation_status": [
            """CASE WHEN (
                ARRAY_AGG(
                    DISTINCT CONCAT(
                        implementation_status.value,
                        '#!#',
                        SUBSTR(implementation_status.date, 1, 4)
                    )
                ) = '{#!#}') THEN NULL
                ELSE ARRAY_AGG(
                    DISTINCT CONCAT(
                        implementation_status.value,
                        '#!#',
                        SUBSTR(implementation_status.date, 1, 4)
                    )
                ) END AS implementation_status"""
        ],
        "nature_of_the_deal": [
            "ARRAY_AGG(DISTINCT nature_of_the_deal.value) AS nature_of_the_deal"
        ],
        "contract_farming": [
            "ARRAY_AGG(DISTINCT contract_farming.value) AS contract_farming"
        ],
        "intended_size": [
            "NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT intended_size.value), ', '), '') AS intended_size",
            "0 AS intended_size"
        ],
        "contract_size": [
            #"NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT contract_size.value), ', '), '') AS contract_size",
            # TODO: This creates the array twice, should be optimized by someone who's more into postgres
            "(ARRAY_AGG(DISTINCT contract_size.value))[ARRAY_LENGTH(ARRAY_AGG(DISTINCT contract_size.value), 1)] AS contract_size",
            "0 AS contract_size"
        ],
        "production_size": [
            #"NULLIF(ARRAY_TO_STRING(ARRAY_AGG(DISTINCT production_size.value), get_group_sql, '), '') AS production_size",
            "(ARRAY_AGG(DISTINCT production_size.value))[ARRAY_LENGTH(ARRAY_AGG(DISTINCT production_size.value), 1)] AS production_size",
            
            "0 AS production_size"
        ],
        "location": [
            "ARRAY_AGG(DISTINCT location.value) AS location"
        ],
        "deal_id": [
            "a.activity_identifier AS deal_id",
            "a.activity_identifier as deal_id"
        ],
        "latlon": [
            "ARRAY_AGG(DISTINCT CONCAT(latitude.value, '#!#', longitude.value, '#!#', level_of_accuracy.value)) AS latlon"
        ],
        # FIXME: The following lines can probably be removed, since this is the default case
        # see also: SubqueryBuilder.column_sql
        "tg_location_comment": [
            "ARRAY_AGG(DISTINCT tg_location_comment.value) AS tg_location_comment"
        ],
        "tg_not_public_comment": [
            "ARRAY_AGG(DISTINCT tg_not_public_comment.value) AS tg_not_public_comment"
        ],
        "tg_feedback_comment": [
            "ARRAY_AGG(DISTINCT tg_feedback_comment.value) AS tg_feedback_comment"
        ],
        "tg_contract_comment": [
            "ARRAY_AGG(DISTINCT tg_contract_comment.value) AS tg_contract_comment"
        ],
        "tg_data_source_comment": [
            "ARRAY_AGG(DISTINCT tg_data_source_comment.value) AS tg_data_source_comment"
        ],
        "tg_total_number_of_jobs_created_comment": [
            "ARRAY_AGG(DISTINCT tg_total_number_of_jobs_created_comment.value) AS tg_total_number_of_jobs_created_comment"
        ],
        "tg_foreign_jobs_created_comment": [
            "ARRAY_AGG(DISTINCT tg_foreign_jobs_created_comment.value) AS tg_foreign_jobs_created_comment"
        ],
        "tg_domestic_jobs_created_comment": [
            "ARRAY_AGG(DISTINCT tg_domestic_jobs_created_comment.value) AS tg_domestic_jobs_created_comment"
        ],
        "tg_land_use_comment": [
            "ARRAY_AGG(DISTINCT tg_land_use_comment.value) AS tg_land_use_comment"
        ],
        "tg_gender_specific_info_comment": [
            "ARRAY_AGG(DISTINCT tg_gender_specific_info_comment.value) AS tg_gender_specific_info_comment"
        ],
        "tg_land_area_comment": [
            "ARRAY_AGG(DISTINCT tg_land_area_comment.value) AS tg_land_area_comment"
        ],
        "tg_land_cover_comment": [
            "ARRAY_AGG(DISTINCT tg_land_cover_comment.value) AS tg_land_cover_comment"
        ],
        "tg_intention_comment": [
            "ARRAY_AGG(DISTINCT tg_intention_comment.value) AS tg_intention_comment"
        ],
        "tg_nature_comment": [
            "ARRAY_AGG(DISTINCT tg_nature_comment.value) AS tg_nature_comment"
        ],
        "tg_negotiation_status_comment": [
            "ARRAY_AGG(DISTINCT tg_negotiation_status_comment.value) AS tg_negotiation_status_comment"
        ],
        "tg_implementation_status_comment": [
            "ARRAY_AGG(DISTINCT tg_implementation_status_comment.value) AS tg_implementation_status_comment"
        ],
        "tg_purchase_price_comment": [
            "ARRAY_AGG(DISTINCT tg_purchase_price_comment.value) AS tg_purchase_price_comment"
        ],
        "tg_leasing_fees_comment": [
            "ARRAY_AGG(DISTINCT tg_leasing_fees_comment.value) AS tg_leasing_fees_comment"
        ],
        "tg_contract_farming_comment": [
            "ARRAY_AGG(DISTINCT tg_contract_farming_comment.value) AS tg_contract_farming_comment"
        ],
        "tg_affected_comment": [
            "ARRAY_AGG(DISTINCT tg_affected_comment.value) AS tg_affected_comment"
        ],
        "tg_recognition_status_comment": [
            "ARRAY_AGG(DISTINCT tg_recognition_status_comment.value) AS tg_recognition_status_comment"
        ],
        "tg_community_consultation_comment": [
            "ARRAY_AGG(DISTINCT tg_community_consultation_comment.value) AS tg_community_consultation_comment"
        ],
        "tg_community_reaction_comment": [
            "ARRAY_AGG(DISTINCT tg_community_reaction_comment.value) AS tg_community_reaction_comment"
        ],
        "tg_land_conflicts_comment": [
            "ARRAY_AGG(DISTINCT tg_land_conflicts_comment.value) AS tg_land_conflicts_comment"
        ],
        "tg_number_of_displaced_people_comment": [
            "ARRAY_AGG(DISTINCT tg_number_of_displaced_people_comment.value) AS tg_number_of_displaced_people_comment"
        ],
        "tg_negative_impacts_comment": [
            "ARRAY_AGG(DISTINCT tg_negative_impacts_comment.value) AS tg_negative_impacts_comment"
        ],
        "tg_promised_benefits_comment": [
            "ARRAY_AGG(DISTINCT tg_promised_benefits_comment.value) AS tg_promised_benefits_comment"
        ],
        "tg_materialized_benefits_comment": [
            "ARRAY_AGG(DISTINCT tg_materialized_benefits_comment.value) AS tg_materialized_benefits_comment"
        ],
        "tg_overall_comment": [
            "ARRAY_AGG(DISTINCT tg_overall_comment.value) AS tg_overall_comment"
        ],
        "tg_crops_comment": [
            "ARRAY_AGG(DISTINCT tg_crops_comment.value) AS tg_crops_comment"
        ],
        "tg_animals_comment": [
            "ARRAY_AGG(DISTINCT tg_animals_comment.value) AS tg_animals_comment"
        ],
        "tg_minerals_comment": [
            "ARRAY_AGG(DISTINCT tg_minerals_comment.value) AS tg_minerals_comment"
        ],
        "tg_contract_farming_crops_comment": [
            "ARRAY_AGG(DISTINCT tg_contract_farming_crops_comment.value) AS tg_contract_farming_crops_comment"
        ],
        "tg_contract_farming_animals_comment": [
            "ARRAY_AGG(DISTINCT tg_contract_farming_animals_comment.value) AS tg_contract_farming_animals_comment"
        ],
        "tg_use_of_produce_comment": [
            "ARRAY_AGG(DISTINCT tg_use_of_produce_comment.value) AS tg_use_of_produce_comment"
        ],
        "tg_in_country_processing_comment": [
            "ARRAY_AGG(DISTINCT tg_in_country_processing_comment.value) AS tg_in_country_processing_comment"
        ],
        "tg_vggt_applied_comment": [
            "ARRAY_AGG(DISTINCT tg_vggt_applied_comment.value) AS tg_vggt_applied_comment"
        ],
        "tg_prai_applied_comment": [
            "ARRAY_AGG(DISTINCT tg_prai_applied_comment.value) AS tg_prai_applied_comment"
        ],
        "tg_water_extraction_envisaged_comment": [
            "ARRAY_AGG(DISTINCT tg_water_extraction_envisaged_comment.value) AS tg_water_extraction_envisaged_comment"
        ],
        "tg_how_much_do_investors_pay_comment": [
            "ARRAY_AGG(DISTINCT tg_how_much_do_investors_pay_comment.value) AS tg_how_much_do_investors_pay_comment"
        ],
        "tg_water_extraction_amount_comment": [
            "ARRAY_AGG(DISTINCT tg_water_extraction_amount_comment.value) AS tg_water_extraction_amount_comment"
        ],
        "tg_use_of_irrigation_infrastructure_comment": [
            "ARRAY_AGG(DISTINCT tg_use_of_irrigation_infrastructure_comment.value) AS tg_use_of_irrigation_infrastructure_comment"
        ],
        "tg_action_comment": [
            "ARRAY_AGG(DISTINCT tg_action_comment.value) AS tg_action_comment"
        ],
        "tg_operational_stakeholder_comment": [
            "ARRAY_AGG(DISTINCT tg_operational_stakeholder_comment.value) AS tg_operational_stakeholder_comment"
        ],
        "tg_public_user_comment": [
            "ARRAY_AGG(DISTINCT tg_public_user_comment.value) AS tg_public_user_comment"
        ],
    }
