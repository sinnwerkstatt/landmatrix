from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.new_model.models import DealHull
from apps.new_model.serializers import Deal2Serializer


class Deal2ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DealHull.objects.all()
    serializer_class = Deal2Serializer

    @action(
        name="Deal Instance",
        methods=["get"],
        url_path="(?P<version_id>\d+)",
        detail=True,
    )
    def retrieve_version(self, request, pk=None, version_id=None):
        instance = self.get_object()
        if version_id:
            instance._selected_version_id = version_id
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# def deal_list(request):
#     try:
#         filters = json.loads(request.GET.get("filters", {}))
#     except json.JSONDecodeError:
#         return JsonResponse({})
#     # filters = """[{"field":"deal__country_id","value":800},{"field":"deal_size","operation":"GE","value":200},{"field":"current_negotiation_status","operation":"IN","value":["ORAL_AGREEMENT","CONTRACT_SIGNED","CHANGE_OF_OWNERSHIP"]},{"field":"current_implementation_status","operation":"IN","value":["PROJECT_NOT_STARTED","STARTUP_PHASE","IN_OPERATION"],"allow_null":false},{"field":"parent_companies","value":42833},{"field":"nature_of_deal","operation":"CONTAINED_BY","value":["PURE_CONTRACT_FARMING","OTHER"],"exclusion":true},{"field":"initiation_year","operation":"GE","value":2000,"allow_null":true},{"field":"current_intention_of_investment","operation":"OVERLAP","value":["BIOFUELS","FOOD_CROPS","FODDER","LIVESTOCK","NON_FOOD_AGRICULTURE","AGRICULTURE_UNSPECIFIED","TIMBER_PLANTATION","FOREST_LOGGING","CARBON","FORESTRY_UNSPECIFIED","MINING","TOURISM","INDUSTRY","CONVERSATION","LAND_SPECULATION","RENEWABLE_ENERGY","OTHER"],"allow_null":false},{"field":"transnational","value":true},{"field":"forest_concession","value":false}]"""
#     # filters =  {"field":"deal__country__region_id","value":2},
#     # filters =  {"field":"parent_companies","value":42833},
#
#     subset = "PUBLIC"
#     sort = "deal_id"
#     filtered_fields = [
#         "id",
#         "deal_id",
#         "deal_size",
#         "deal__country_id",
#         "deal__country__name",
#         "deal__country__region__id",
#         "current_intention_of_investment",
#         "current_negotiation_status",
#         "current_contract_size",
#         "current_implementation_status",
#         "current_crops",
#         "current_animals",
#         "current_mineral_resources",
#         "intended_size",
#         "locations",
#         # "fully_updated_at",
#         "operating_company__id",
#         "operating_company__name",
#         "top_investors__id",
#         "top_investors__name",
#         "top_investors__classification",
#     ]
#
#     active_version_ids = DealHull.objects.visible(
#         user=request.user, subset=subset
#     ).values_list("active_version_id", flat=True)
#     versions = (
#         DealVersion2.objects.filter(id__in=active_version_ids)
#         .order_by(sort)
#         .prefetch_related("deal__country")
#     )
#
#     # qs = DealVersion2.objects.visible(user=request.user, subset=subset).order_by(sort)
#     qs = versions.filter(parse_filters(filters)) if filters else versions
#
#     deals = qs_values_to_dict(
#         qs,
#         filtered_fields,
#         ["top_investors", "parent_companies", "workflowinfos"],
#     )
#     return JsonResponse({"deals": deals})
#
#
# def deal_detail(request, id, version_id=None):
#     deal = DealHull.objects.get(id=id)
#     if not version_id:
#         version_id = deal.active_version_id or deal.draft_version_id
#         if not version_id:
#             raise Http404
#
#     return JsonResponse(deal.to_detail_dict(version_id))
