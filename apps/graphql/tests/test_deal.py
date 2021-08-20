import pytest
from django.contrib.auth import get_user_model
from graphql import GraphQLError

from apps.graphql.resolvers.generics import object_edit, change_object_status
from apps.landmatrix.models import Deal

User = get_user_model()


def test_create_deal_draft(db):
    land_reporter = User.objects.get(username="land_reporter")
    land_editor = User.objects.get(username="land_editor")
    land_admin = User.objects.get(username="land_admin")

    payload = {
        "country": {"id": 450},
        "locations": [
            {
                "id": 1,
                "point": {"lat": -18.92566, "lng": 47.54364},
                "areas": {"type": "FeatureCollection", "features": []},
                "level_of_accuracy": "APPROXIMATE_LOCATION",
                "name": "Villa Berlin, Lalana Rainmanga Rahanamy, Antananarivo, Madagaskar",
                "description": "villa berlin :)",
            }
        ],
    }

    dealId, dealVersion = object_edit(
        otype="deal",
        user=land_reporter,
        obj_id=-1,
        obj_version_id=None,
        payload=payload,
    )
    # assert dealId == dealVersion == 1
    d1 = Deal.objects.get(id=dealId)
    assert d1.country_id == 450
    d1v = d1.versions.get()
    assert d1v.serialized_data["draft_status"] == 1
    assert d1v.serialized_data["country"] == 450

    # edit draft
    payload = {
        "id": 8895,
        "country": {"id": 450},
        "intended_size": None,
        "contract_size": None,
        "production_size": None,
        "land_area_comment": "",
        "intention_of_investment": None,
        "intention_of_investment_comment": "",
        "nature_of_deal": None,
        "nature_of_deal_comment": "",
        "negotiation_status": None,
        "negotiation_status_comment": "",
        "implementation_status": None,
        "implementation_status_comment": "",
        "purchase_price": None,
        "purchase_price_currency": None,
        "purchase_price_type": None,
        "purchase_price_area": None,
        "purchase_price_comment": "",
        "annual_leasing_fee": None,
        "annual_leasing_fee_currency": None,
        "annual_leasing_fee_type": None,
        "annual_leasing_fee_area": None,
        "annual_leasing_fee_comment": "",
        "contract_farming": None,
        "on_the_lease_state": None,
        "on_the_lease": None,
        "off_the_lease_state": None,
        "off_the_lease": None,
        "contract_farming_comment": "",
        "total_jobs_created": None,
        "total_jobs_planned": None,
        "total_jobs_planned_employees": None,
        "total_jobs_planned_daily_workers": None,
        "total_jobs_current": None,
        "total_jobs_created_comment": "",
        "foreign_jobs_created": None,
        "foreign_jobs_planned": None,
        "foreign_jobs_planned_employees": None,
        "foreign_jobs_planned_daily_workers": None,
        "foreign_jobs_current": None,
        "foreign_jobs_created_comment": "",
        "domestic_jobs_created": None,
        "domestic_jobs_planned": None,
        "domestic_jobs_planned_employees": None,
        "domestic_jobs_planned_daily_workers": None,
        "domestic_jobs_current": None,
        "domestic_jobs_created_comment": "",
        "operating_company": None,
        "involved_actors": None,
        "project_name": "",
        "investment_chain_comment": "",
        "name_of_community": None,
        "name_of_indigenous_people": None,
        "people_affected_comment": "",
        "recognition_status": None,
        "recognition_status_comment": "",
        "community_consultation": None,
        "community_consultation_comment": "",
        "community_reaction": None,
        "community_reaction_comment": "",
        "land_conflicts": None,
        "land_conflicts_comment": "",
        "displacement_of_people": None,
        "displaced_people": None,
        "displaced_households": None,
        "displaced_people_from_community_land": None,
        "displaced_people_within_community_land": None,
        "displaced_households_from_fields": None,
        "displaced_people_on_completion": None,
        "displacement_of_people_comment": "",
        "negative_impacts": None,
        "negative_impacts_comment": "",
        "promised_compensation": "",
        "received_compensation": "",
        "promised_benefits": None,
        "promised_benefits_comment": "",
        "materialized_benefits": None,
        "materialized_benefits_comment": "",
        "presence_of_organizations": "",
        "former_land_owner": None,
        "former_land_owner_comment": "",
        "former_land_use": None,
        "former_land_use_comment": "",
        "former_land_cover": None,
        "former_land_cover_comment": "",
        "crops": None,
        "crops_comment": "",
        "animals": None,
        "animals_comment": "",
        "mineral_resources": None,
        "mineral_resources_comment": "",
        "contract_farming_crops": None,
        "contract_farming_crops_comment": "",
        "contract_farming_animals": None,
        "contract_farming_animals_comment": "",
        "has_domestic_use": None,
        "domestic_use": None,
        "has_export": None,
        "export": None,
        "export_country1": None,
        "export_country1_ratio": None,
        "export_country2": None,
        "export_country2_ratio": None,
        "export_country3": None,
        "export_country3_ratio": None,
        "use_of_produce_comment": "",
        "in_country_processing": None,
        "in_country_processing_comment": "",
        "in_country_processing_facilities": "",
        "in_country_end_products": "",
        "water_extraction_envisaged": None,
        "water_extraction_envisaged_comment": "",
        "source_of_water_extraction": None,
        "source_of_water_extraction_comment": "",
        "how_much_do_investors_pay_comment": "",
        "water_extraction_amount": None,
        "water_extraction_amount_comment": "",
        "use_of_irrigation_infrastructure": None,
        "use_of_irrigation_infrastructure_comment": "",
        "water_footprint": "",
        "gender_related_information": "",
        "vggt_applied": None,
        "vggt_applied_comment": "",
        "prai_applied": None,
        "prai_applied_comment": "",
        "overall_comment": "",
        "created_at": "2021-08-20T21:26:08.692467+00:00",
        "modified_at": "2021-08-20T21:26:08.665Z",
        "fully_updated": False,
        "fully_updated_at": None,
        "confidential": False,
        "confidential_reason": None,
        "confidential_comment": None,
        "is_public": False,
        "not_public_reason": "NO_DATASOURCES",
        "has_known_investor": False,
        "locations": [
            {
                "id": 1,
                "name": "Villa Berlin, Lalana Rainmanga Rahanamy, Antananarivo, Madagaskar",
                "areas": {"type": "FeatureCollection", "features": []},
                "point": {"lat": -18.92566, "lng": 47.54364},
                "description": "",
                "level_of_accuracy": "APPROXIMATE_LOCATION",
                "comment": "KOMMA",
            }
        ],
        "contracts": [],
        "datasources": [],
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [47.54364, -18.92566]},
                    "properties": {
                        "id": 1,
                        "name": "Villa Berlin, Lalana Rainmanga Rahanamy, Antananarivo, Madagaskar",
                        "type": "point",
                        "spatial_accuracy": "APPROXIMATE_LOCATION",
                    },
                }
            ],
        },
        "versions": None,
        "workflowinfos": None,
        "comments": None,
        "status": 1,
        "draft_status": 1,
        "__typename": "Deal",
    }

    newDealId, newDealVersion = object_edit(
        otype="deal",
        user=User.objects.get(username="land_reporter"),
        obj_id=d1.id,
        obj_version_id=d1.versions.get().id,
        payload=payload,
    )
    assert dealId == newDealId
    assert dealVersion == newDealVersion
    d1.refresh_from_db()
    assert d1.locations[0]["description"] == ""
    assert d1.locations[0]["comment"] == "KOMMA"

    # change draft status TO_REVIEW
    dealId, dealVersion = change_object_status(
        otype="deal",
        user=land_reporter,
        obj_id=dealId,
        obj_version_id=dealVersion,
        transition="TO_REVIEW",
        fully_updated=True,
    )
    d1.refresh_from_db()
    assert d1.draft_status == Deal.DRAFT_STATUS_REVIEW
    assert d1.versions.get().serialized_data["draft_status"] == Deal.DRAFT_STATUS_REVIEW

    # change draft status TO_ACTIVATE
    with pytest.raises(GraphQLError):
        change_object_status(
            otype="deal",
            user=land_reporter,
            obj_id=dealId,
            obj_version_id=dealVersion,
            transition="TO_ACTIVATION",
            fully_updated=True,
        )

    change_object_status(
        otype="deal",
        user=land_editor,
        obj_id=dealId,
        obj_version_id=dealVersion,
        transition="TO_ACTIVATION",
        fully_updated=True,
    )
    # change draft status TO_ACTIVATE
    with pytest.raises(GraphQLError):
        change_object_status(
            otype="deal",
            user=land_editor,
            obj_id=dealId,
            obj_version_id=dealVersion,
            transition="ACTIVATE",
            fully_updated=True,
        )

    change_object_status(
        otype="deal",
        user=land_admin,
        obj_id=dealId,
        obj_version_id=dealVersion,
        transition="ACTIVATE",
        fully_updated=True,
    )

    # d1.refresh_from_db()
    # assert d1.draft_status == Deal.DRAFT_STATUS_REVIEW
    # assert d1.versions.get().serialized_data["draft_status"] == Deal.DRAFT_STATUS_REVIEW
