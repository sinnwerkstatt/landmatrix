import json

import requests
from django.core.management.base import BaseCommand

deal_detail_query = """query Deal($id: Int!, $version: Int)
 { deal(id: $id, version: $version, subset: UNFILTERED) {
    id
    locations
    country {
      id
      name
      code_alpha2
      point_lat_min
      point_lat_max
      point_lon_min
      point_lon_max
    }
    intended_size
    contract_size
    production_size
    land_area_comment
    intention_of_investment
    intention_of_investment_comment
    nature_of_deal
    nature_of_deal_comment
    negotiation_status
    negotiation_status_comment
    implementation_status
    implementation_status_comment
    purchase_price
    purchase_price_currency {
      id
      code
      name
    }
    purchase_price_type
    purchase_price_area
    purchase_price_comment
    annual_leasing_fee
    annual_leasing_fee_currency {
      id
      code
      name
    }
    annual_leasing_fee_type
    annual_leasing_fee_area
    annual_leasing_fee_comment
    contract_farming
    on_the_lease_state
    on_the_lease
    off_the_lease_state
    off_the_lease
    contract_farming_comment
    total_jobs_created
    total_jobs_planned
    total_jobs_planned_employees
    total_jobs_planned_daily_workers
    total_jobs_current
    total_jobs_created_comment
    foreign_jobs_created
    foreign_jobs_planned
    foreign_jobs_planned_employees
    foreign_jobs_planned_daily_workers
    foreign_jobs_current
    foreign_jobs_created_comment
    domestic_jobs_created
    domestic_jobs_planned
    domestic_jobs_planned_employees
    domestic_jobs_planned_daily_workers
    domestic_jobs_current
    domestic_jobs_created_comment
    operating_company {
      id
      name
    }
    involved_actors
    project_name
    investment_chain_comment
    name_of_community
    name_of_indigenous_people
    people_affected_comment
    recognition_status
    recognition_status_comment
    community_consultation
    community_consultation_comment
    community_reaction
    community_reaction_comment
    land_conflicts
    land_conflicts_comment
    displacement_of_people
    displaced_people
    displaced_households
    displaced_people_from_community_land
    displaced_people_within_community_land
    displaced_households_from_fields
    displaced_people_on_completion
    displacement_of_people_comment
    negative_impacts
    negative_impacts_comment
    promised_compensation
    received_compensation
    promised_benefits
    promised_benefits_comment
    materialized_benefits
    materialized_benefits_comment
    presence_of_organizations
    former_land_owner
    former_land_owner_comment
    former_land_use
    former_land_use_comment
    former_land_cover
    former_land_cover_comment
    crops
    crops_comment
    animals
    animals_comment
    mineral_resources
    mineral_resources_comment
    contract_farming_crops
    contract_farming_crops_comment
    contract_farming_animals
    contract_farming_animals_comment
    has_domestic_use
    domestic_use
    has_export
    export
    export_country1 {
      id
      name
    }
    export_country1_ratio
    export_country2 {
      id
      name
    }
    export_country2_ratio
    export_country3 {
      id
      name
    }
    export_country3_ratio
    use_of_produce_comment
    in_country_processing
    in_country_processing_comment
    in_country_processing_facilities
    in_country_end_products
    water_extraction_envisaged
    water_extraction_envisaged_comment
    source_of_water_extraction
    source_of_water_extraction_comment
    how_much_do_investors_pay_comment
    water_extraction_amount
    water_extraction_amount_comment
    use_of_irrigation_infrastructure
    use_of_irrigation_infrastructure_comment
    water_footprint
    gender_related_information
    overall_comment
    created_at
    modified_at
    created_by {
      id
      username
    }
    fully_updated
    fully_updated_at
    confidential
    confidential_comment
    is_public
    not_public_reason
    has_known_investor
    contracts
    datasources
    geojson
    versions {
      id
      deal {
        fully_updated
        status
        draft_status
        confidential
      }
      created_at
      created_by {
        id
        full_name
      }
      object_id
    }
    workflowinfos {
      id
      from_user {
        id
        username
        full_name
      }
      to_user {
        id
        username
        full_name
      }
      draft_status_before
      draft_status_after
      timestamp
      comment
      replies {
        comment
        user_id
        timestamp
      }
      resolved
    }
    status
    draft_status
  }
}"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        DEAL_ID = 2

        self.sess = requests.session()
        self.sess.post(
            "http://localhost:9000/graphql/",
            json={
                "query": """
            mutation Login($username: String!, $password: String!) {
              login(username: $username, password: $password) {
                status error user { id }
              }
            }
            """,
                "operationName": "Login",
                "variables": {
                    "username": "andreas.nuesslein",
                    "password": "HbBEdfH6vG776fB",
                },
            },
        )

        req = self.sess.post(
            "http://localhost:9000/graphql/",
            json={
                "query": deal_detail_query,
                "operationName": "Deal",
                "variables": {"id": DEAL_ID},
            },
            headers={
                "accept": "application/graphql+json, application/json",
                "content-type": "application/json",
            },
        )
        old_answer = req.json()["data"]["deal"]
        req_new = self.sess.get(f"http://localhost:9000/api/deal/{DEAL_ID}/")
        new_answer = req_new.json()

        print(json.dumps(old_answer, indent=2))
        print()
        print()
        print(json.dumps(new_answer, indent=2))
        print()
        print()

        assert old_answer["id"] == new_answer["deal_id"]

        # assert old_answer["locations"] == new_answer["locations"]
        assert old_answer["country_id"] == new_answer["country_id"]
        assert old_answer["intended_size"] == new_answer["intended_size"]
        assert old_answer["contract_size"] == new_answer["contract_size"]
        assert old_answer["production_size"] == new_answer["production_size"]
        assert old_answer["land_area_comment"] == new_answer["land_area_comment"]
        assert (
            old_answer["intention_of_investment"]
            == new_answer["intention_of_investment"]
        )
        assert (
            old_answer["intention_of_investment_comment"]
            == new_answer["intention_of_investment_comment"]
        )
        assert old_answer["nature_of_deal"] == new_answer["nature_of_deal"]
        assert (
            old_answer["nature_of_deal_comment"] == new_answer["nature_of_deal_comment"]
        )
        assert old_answer["negotiation_status"] == new_answer["negotiation_status"]
        assert (
            old_answer["negotiation_status_comment"]
            == new_answer["negotiation_status_comment"]
        )
        assert (
            old_answer["implementation_status"] == new_answer["implementation_status"]
        )
        assert (
            old_answer["implementation_status_comment"]
            == new_answer["implementation_status_comment"]
        )
        assert old_answer["purchase_price"] == new_answer["purchase_price"]
        assert (
            old_answer["purchase_price_currency_id"]
            == new_answer["purchase_price_currency_id"]
        )
        assert old_answer["purchase_price_type"] == new_answer["purchase_price_type"]
        assert old_answer["purchase_price_area"] == new_answer["purchase_price_area"]
        assert (
            old_answer["purchase_price_comment"] == new_answer["purchase_price_comment"]
        )
        assert old_answer["annual_leasing_fee"] == new_answer["annual_leasing_fee"]
        assert (
            old_answer["annual_leasing_fee_currency_id"]
            == new_answer["annual_leasing_fee_currency_id"]
        )
        assert (
            old_answer["annual_leasing_fee_type"]
            == new_answer["annual_leasing_fee_type"]
        )
        assert (
            old_answer["annual_leasing_fee_area"]
            == new_answer["annual_leasing_fee_area"]
        )
        assert (
            old_answer["annual_leasing_fee_comment"]
            == new_answer["annual_leasing_fee_comment"]
        )
        assert old_answer["contract_farming"] == new_answer["contract_farming"]
        assert old_answer["on_the_lease_state"] == new_answer["on_the_lease_state"]
        assert old_answer["on_the_lease"] == new_answer["on_the_lease"]
        assert old_answer["off_the_lease_state"] == new_answer["off_the_lease_state"]
        assert old_answer["off_the_lease"] == new_answer["off_the_lease"]
        assert (
            old_answer["contract_farming_comment"]
            == new_answer["contract_farming_comment"]
        )
        assert old_answer["contracts"] == new_answer["contracts"]
        assert old_answer["total_jobs_created"] == new_answer["total_jobs_created"]
        assert old_answer["total_jobs_planned"] == new_answer["total_jobs_planned"]
        assert (
            old_answer["total_jobs_planned_employees"]
            == new_answer["total_jobs_planned_employees"]
        )
        assert (
            old_answer["total_jobs_planned_daily_workers"]
            == new_answer["total_jobs_planned_daily_workers"]
        )
        assert old_answer["total_jobs_current"] == new_answer["total_jobs_current"]
        assert (
            old_answer["total_jobs_created_comment"]
            == new_answer["total_jobs_created_comment"]
        )
        assert old_answer["foreign_jobs_created"] == new_answer["foreign_jobs_created"]
        assert old_answer["foreign_jobs_planned"] == new_answer["foreign_jobs_planned"]
        assert (
            old_answer["foreign_jobs_planned_employees"]
            == new_answer["foreign_jobs_planned_employees"]
        )
        assert (
            old_answer["foreign_jobs_planned_daily_workers"]
            == new_answer["foreign_jobs_planned_daily_workers"]
        )
        assert old_answer["foreign_jobs_current"] == new_answer["foreign_jobs_current"]
        assert (
            old_answer["foreign_jobs_created_comment"]
            == new_answer["foreign_jobs_created_comment"]
        )
        assert (
            old_answer["domestic_jobs_created"] == new_answer["domestic_jobs_created"]
        )
        assert (
            old_answer["domestic_jobs_planned"] == new_answer["domestic_jobs_planned"]
        )
        assert (
            old_answer["domestic_jobs_planned_employees"]
            == new_answer["domestic_jobs_planned_employees"]
        )
        assert (
            old_answer["domestic_jobs_planned_daily_workers"]
            == new_answer["domestic_jobs_planned_daily_workers"]
        )
        assert (
            old_answer["domestic_jobs_current"] == new_answer["domestic_jobs_current"]
        )
        assert (
            old_answer["domestic_jobs_created_comment"]
            == new_answer["domestic_jobs_created_comment"]
        )
        assert old_answer["operating_company_id"] == new_answer["operating_company_id"]
        assert old_answer["involved_actors"] == new_answer["involved_actors"]
        assert old_answer["project_name"] == new_answer["project_name"]
        assert (
            old_answer["investment_chain_comment"]
            == new_answer["investment_chain_comment"]
        )
        assert old_answer["datasources"] == new_answer["datasources"]
        assert old_answer["name_of_community"] == new_answer["name_of_community"]
        assert (
            old_answer["name_of_indigenous_people"]
            == new_answer["name_of_indigenous_people"]
        )
        assert (
            old_answer["people_affected_comment"]
            == new_answer["people_affected_comment"]
        )
        assert old_answer["recognition_status"] == new_answer["recognition_status"]
        assert (
            old_answer["recognition_status_comment"]
            == new_answer["recognition_status_comment"]
        )
        assert (
            old_answer["community_consultation"] == new_answer["community_consultation"]
        )
        assert (
            old_answer["community_consultation_comment"]
            == new_answer["community_consultation_comment"]
        )
        assert old_answer["community_reaction"] == new_answer["community_reaction"]
        assert (
            old_answer["community_reaction_comment"]
            == new_answer["community_reaction_comment"]
        )
        assert old_answer["land_conflicts"] == new_answer["land_conflicts"]
        assert (
            old_answer["land_conflicts_comment"] == new_answer["land_conflicts_comment"]
        )
        assert (
            old_answer["displacement_of_people"] == new_answer["displacement_of_people"]
        )
        assert old_answer["displaced_people"] == new_answer["displaced_people"]
        assert old_answer["displaced_households"] == new_answer["displaced_households"]
        assert (
            old_answer["displaced_people_from_community_land"]
            == new_answer["displaced_people_from_community_land"]
        )
        assert (
            old_answer["displaced_people_within_community_land"]
            == new_answer["displaced_people_within_community_land"]
        )
        assert (
            old_answer["displaced_households_from_fields"]
            == new_answer["displaced_households_from_fields"]
        )
        assert (
            old_answer["displaced_people_on_completion"]
            == new_answer["displaced_people_on_completion"]
        )
        assert (
            old_answer["displacement_of_people_comment"]
            == new_answer["displacement_of_people_comment"]
        )
        assert old_answer["negative_impacts"] == new_answer["negative_impacts"]
        assert (
            old_answer["negative_impacts_comment"]
            == new_answer["negative_impacts_comment"]
        )
        assert (
            old_answer["promised_compensation"] == new_answer["promised_compensation"]
        )
        assert (
            old_answer["received_compensation"] == new_answer["received_compensation"]
        )
        assert old_answer["promised_benefits"] == new_answer["promised_benefits"]
        assert (
            old_answer["promised_benefits_comment"]
            == new_answer["promised_benefits_comment"]
        )
        assert (
            old_answer["materialized_benefits"] == new_answer["materialized_benefits"]
        )
        assert (
            old_answer["materialized_benefits_comment"]
            == new_answer["materialized_benefits_comment"]
        )
        assert (
            old_answer["presence_of_organizations"]
            == new_answer["presence_of_organizations"]
        )
        assert old_answer["former_land_owner"] == new_answer["former_land_owner"]
        assert (
            old_answer["former_land_owner_comment"]
            == new_answer["former_land_owner_comment"]
        )
        assert old_answer["former_land_use"] == new_answer["former_land_use"]
        assert (
            old_answer["former_land_use_comment"]
            == new_answer["former_land_use_comment"]
        )
        assert old_answer["former_land_cover"] == new_answer["former_land_cover"]
        assert (
            old_answer["former_land_cover_comment"]
            == new_answer["former_land_cover_comment"]
        )
        assert old_answer["crops"] == new_answer["crops"]
        assert old_answer["crops_comment"] == new_answer["crops_comment"]
        assert old_answer["animals"] == new_answer["animals"]
        assert old_answer["animals_comment"] == new_answer["animals_comment"]
        assert old_answer["mineral_resources"] == new_answer["mineral_resources"]
        assert (
            old_answer["mineral_resources_comment"]
            == new_answer["mineral_resources_comment"]
        )
        assert (
            old_answer["contract_farming_crops"] == new_answer["contract_farming_crops"]
        )
        assert (
            old_answer["contract_farming_crops_comment"]
            == new_answer["contract_farming_crops_comment"]
        )
        assert (
            old_answer["contract_farming_animals"]
            == new_answer["contract_farming_animals"]
        )
        assert (
            old_answer["contract_farming_animals_comment"]
            == new_answer["contract_farming_animals_comment"]
        )
        assert old_answer["has_domestic_use"] == new_answer["has_domestic_use"]
        assert old_answer["domestic_use"] == new_answer["domestic_use"]
        assert old_answer["has_export"] == new_answer["has_export"]
        assert old_answer["export"] == new_answer["export"]
        assert old_answer["export_country1_id"] == new_answer["export_country1_id"]
        assert (
            old_answer["export_country1_ratio"] == new_answer["export_country1_ratio"]
        )
        assert old_answer["export_country2_id"] == new_answer["export_country2_id"]
        assert (
            old_answer["export_country2_ratio"] == new_answer["export_country2_ratio"]
        )
        assert old_answer["export_country3_id"] == new_answer["export_country3_id"]
        assert (
            old_answer["export_country3_ratio"] == new_answer["export_country3_ratio"]
        )
        assert (
            old_answer["use_of_produce_comment"] == new_answer["use_of_produce_comment"]
        )
        assert (
            old_answer["in_country_processing"] == new_answer["in_country_processing"]
        )
        assert (
            old_answer["in_country_processing_comment"]
            == new_answer["in_country_processing_comment"]
        )
        assert (
            old_answer["in_country_processing_facilities"]
            == new_answer["in_country_processing_facilities"]
        )
        assert (
            old_answer["in_country_end_products"]
            == new_answer["in_country_end_products"]
        )
        assert (
            old_answer["water_extraction_envisaged"]
            == new_answer["water_extraction_envisaged"]
        )
        assert (
            old_answer["water_extraction_envisaged_comment"]
            == new_answer["water_extraction_envisaged_comment"]
        )
        assert (
            old_answer["source_of_water_extraction"]
            == new_answer["source_of_water_extraction"]
        )
        assert (
            old_answer["source_of_water_extraction_comment"]
            == new_answer["source_of_water_extraction_comment"]
        )
        assert (
            old_answer["how_much_do_investors_pay_comment"]
            == new_answer["how_much_do_investors_pay_comment"]
        )
        assert (
            old_answer["water_extraction_amount"]
            == new_answer["water_extraction_amount"]
        )
        assert (
            old_answer["water_extraction_amount_comment"]
            == new_answer["water_extraction_amount_comment"]
        )
        assert (
            old_answer["use_of_irrigation_infrastructure"]
            == new_answer["use_of_irrigation_infrastructure"]
        )
        assert (
            old_answer["use_of_irrigation_infrastructure_comment"]
            == new_answer["use_of_irrigation_infrastructure_comment"]
        )
        assert old_answer["water_footprint"] == new_answer["water_footprint"]
        assert (
            old_answer["gender_related_information"]
            == new_answer["gender_related_information"]
        )
        assert old_answer["overall_comment"] == new_answer["overall_comment"]
        # for dh in DealHull.objects.all():  # type: DealHull
        #     print(dh)
