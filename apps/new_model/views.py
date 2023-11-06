import json

from django.http import JsonResponse

from apps.graphql.tools import parse_filters
from apps.new_model.models import DealHull, DealVersion2
from apps.utils import qs_values_to_dict


# class DealViewSet(viewsets.ViewSet):
#     queryset = DealHull.objects.all()
#     serializer_class = DealSerializer
#
#     def list(self, request):
#         return Response(
#             {
#                 "objects": [
#                     {
#                         "id": u.id,
#                         "username": u.username,
#                         "first_name": u.first_name,
#                         "last_name": u.last_name,
#                         "is_staff": u.is_staff,
#                         # "is_impersonate": u.is_impersonate,
#                     }
#                     for u in User.objects.all()
#                 ]
#             }
#         )


def deal_list(request):
    try:
        filters = json.loads(request.GET.get("filters", {}))
    except json.JSONDecodeError:
        return JsonResponse({})
    # filters = """[{"field":"deal__country_id","value":800},{"field":"deal_size","operation":"GE","value":200},{"field":"current_negotiation_status","operation":"IN","value":["ORAL_AGREEMENT","CONTRACT_SIGNED","CHANGE_OF_OWNERSHIP"]},{"field":"current_implementation_status","operation":"IN","value":["PROJECT_NOT_STARTED","STARTUP_PHASE","IN_OPERATION"],"allow_null":false},{"field":"parent_companies","value":42833},{"field":"nature_of_deal","operation":"CONTAINED_BY","value":["PURE_CONTRACT_FARMING","OTHER"],"exclusion":true},{"field":"initiation_year","operation":"GE","value":2000,"allow_null":true},{"field":"current_intention_of_investment","operation":"OVERLAP","value":["BIOFUELS","FOOD_CROPS","FODDER","LIVESTOCK","NON_FOOD_AGRICULTURE","AGRICULTURE_UNSPECIFIED","TIMBER_PLANTATION","FOREST_LOGGING","CARBON","FORESTRY_UNSPECIFIED","MINING","TOURISM","INDUSTRY","CONVERSATION","LAND_SPECULATION","RENEWABLE_ENERGY","OTHER"],"allow_null":false},{"field":"transnational","value":true},{"field":"forest_concession","value":false}]"""
    # filters =  {"field":"deal__country__region_id","value":2},
    # filters =  {"field":"parent_companies","value":42833},

    subset = "PUBLIC"
    sort = "deal_id"
    filtered_fields = [
        "id",
        "deal_id",
        "deal_size",
        "deal__country_id",
        "deal__country__name",
        "deal__country__region__id",
        "current_intention_of_investment",
        "current_negotiation_status",
        "current_contract_size",
        "current_implementation_status",
        "current_crops",
        "current_animals",
        "current_mineral_resources",
        "intended_size",
        "locations",
        # "fully_updated_at",
        "operating_company__id",
        "operating_company__name",
        "top_investors__id",
        "top_investors__name",
        "top_investors__classification",
    ]

    active_version_ids = DealHull.objects.visible(
        user=request.user, subset=subset
    ).values_list("active_version_id", flat=True)
    versions = (
        DealVersion2.objects.filter(id__in=active_version_ids)
        .order_by(sort)
        .prefetch_related("deal__country")
    )

    # qs = DealVersion2.objects.visible(user=request.user, subset=subset).order_by(sort)
    qs = versions.filter(parse_filters(filters)) if filters else versions

    deals = qs_values_to_dict(
        qs,
        filtered_fields,
        ["top_investors", "parent_companies", "workflowinfos"],
    )
    return JsonResponse({"deals": deals})


def deal_detail(request, id, version_id=None):
    dh = DealHull.objects.get(id=id)
    if not version_id:
        version_id = dh.active_version_id or dh.draft_version_id

    if not version_id:
        return
    deal_version = DealVersion2.objects.get(id=version_id)
    # deal = qs_values_to_dict(
    #         visible_deals,
    #         filtered_fields,
    #         ["top_investors", "parent_companies", "workflowinfos"],
    #     )[0]

    detail_fields = [
        "id",
        "deal_id",
        "locations",
        "intended_size",
        "contract_size",
        "production_size",
        "land_area_comment",
        "intention_of_investment",
        "intention_of_investment_comment",
        "nature_of_deal",
        "nature_of_deal_comment",
        "negotiation_status",
        "negotiation_status_comment",
        "implementation_status",
        "implementation_status_comment",
        "purchase_price",
        "purchase_price_currency_id",
        "purchase_price_type",
        "purchase_price_area",
        "purchase_price_comment",
        "annual_leasing_fee",
        "annual_leasing_fee_currency_id",
        "annual_leasing_fee_type",
        "annual_leasing_fee_area",
        "annual_leasing_fee_comment",
        "contract_farming",
        "on_the_lease_state",
        "on_the_lease",
        "off_the_lease_state",
        "off_the_lease",
        "contract_farming_comment",
        "contracts",
        "total_jobs_created",
        "total_jobs_planned",
        "total_jobs_planned_employees",
        "total_jobs_planned_daily_workers",
        "total_jobs_current",
        "total_jobs_created_comment",
        "foreign_jobs_created",
        "foreign_jobs_planned",
        "foreign_jobs_planned_employees",
        "foreign_jobs_planned_daily_workers",
        "foreign_jobs_current",
        "foreign_jobs_created_comment",
        "domestic_jobs_created",
        "domestic_jobs_planned",
        "domestic_jobs_planned_employees",
        "domestic_jobs_planned_daily_workers",
        "domestic_jobs_current",
        "domestic_jobs_created_comment",
        "operating_company_id",
        "involved_actors",
        "project_name",
        "investment_chain_comment",
        "datasources",
        "name_of_community",
        "name_of_indigenous_people",
        "people_affected_comment",
        "recognition_status",
        "recognition_status_comment",
        "community_consultation",
        "community_consultation_comment",
        "community_reaction",
        "community_reaction_comment",
        "land_conflicts",
        "land_conflicts_comment",
        "displacement_of_people",
        "displaced_people",
        "displaced_households",
        "displaced_people_from_community_land",
        "displaced_people_within_community_land",
        "displaced_households_from_fields",
        "displaced_people_on_completion",
        "displacement_of_people_comment",
        "negative_impacts",
        "negative_impacts_comment",
        "promised_compensation",
        "received_compensation",
        "promised_benefits",
        "promised_benefits_comment",
        "materialized_benefits",
        "materialized_benefits_comment",
        "presence_of_organizations",
        "former_land_owner",
        "former_land_owner_comment",
        "former_land_use",
        "former_land_use_comment",
        "former_land_cover",
        "former_land_cover_comment",
        "crops",
        "crops_comment",
        "animals",
        "animals_comment",
        "mineral_resources",
        "mineral_resources_comment",
        "contract_farming_crops",
        "contract_farming_crops_comment",
        "contract_farming_animals",
        "contract_farming_animals_comment",
        "has_domestic_use",
        "domestic_use",
        "has_export",
        "export",
        "export_country1_id",
        "export_country1_ratio",
        "export_country2_id",
        "export_country2_ratio",
        "export_country3_id",
        "export_country3_ratio",
        "use_of_produce_comment",
        "in_country_processing",
        "in_country_processing_comment",
        "in_country_processing_facilities",
        "in_country_end_products",
        "water_extraction_envisaged",
        "water_extraction_envisaged_comment",
        "source_of_water_extraction",
        "source_of_water_extraction_comment",
        "how_much_do_investors_pay_comment",
        "water_extraction_amount",
        "water_extraction_amount_comment",
        "use_of_irrigation_infrastructure",
        "use_of_irrigation_infrastructure_comment",
        "water_footprint",
        "gender_related_information",
        "overall_comment",
        "is_public",
        "has_known_investor",
        # "parent_companies",
        # "top_investors",
        "current_contract_size",
        "current_production_size",
        "current_intention_of_investment",
        "current_negotiation_status",
        "current_implementation_status",
        "current_crops",
        "current_animals",
        "current_mineral_resources",
        "deal_size",
        "initiation_year",
        "forest_concession",
        "transnational",
        "fully_updated",
        "status",
        "created_at",
        "created_by_id",
        "sent_to_review_at",
        "sent_to_review_by_id",
        "reviewed_at",
        "reviewed_by_id",
        "activated_at",
        "activated_by_id",
    ]
    ret_dict = deal_version.to_dict(detail_fields)
    ret_dict["hull"] = {
        "country": {"id": dh.country_id, "name": dh.country.name}
        if dh.country_id
        else None,
        "active_version_id": dh.active_version_id,
        "draft_version_id": dh.draft_version_id,
        "confidential": dh.confidential,
        "confidential_comment": dh.confidential_comment,
        "deleted": dh.deleted,
    }
    ret_dict["versions"] = [
        {
            "id": x.id,
            "created_at": x.created_at,
            "created_by_id": x.created_by_id,
            "sent_to_review_at": x.sent_to_review_at,
            "sent_to_review_by_id": x.sent_to_review_by_id,
            "reviewed_at": x.reviewed_at,
            "reviewed_by_id": x.reviewed_by_id,
            "activated_at": x.activated_at,
            "activated_by_id": x.activated_by_id,
            "fully_updated": x.fully_updated,
            "status": x.status,
        }
        for x in DealVersion2.objects.filter(deal=dh).order_by("-id")
    ]

    return JsonResponse(ret_dict)
