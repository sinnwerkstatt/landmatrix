from drf_spectacular.utils import OpenApiParameter

from django.db.models import Q
from rest_framework.request import Request

from apps.landmatrix.models import choices

openapi_filters_parameters = [
    OpenApiParameter("region_id", description="See /api/regions/ for IDs", type=int),
    OpenApiParameter("country_id", description="See /api/countries/ for IDs", type=int),
    OpenApiParameter("area_min", description="Minimum deal area", type=int),
    OpenApiParameter("area_max", description="Maximum deal area", type=int),
    OpenApiParameter(
        "negotiation_status",
        description="",
        type=str,
        enum=[x["value"] for x in choices.NEGOTIATION_STATUS_ITEMS],
        many=True,
    ),
    OpenApiParameter(
        "implementation_status",
        description="",
        type=str,
        enum=[x["value"] for x in choices.IMPLEMENTATION_STATUS_ITEMS] + ["UNKNOWN"],
        many=True,
    ),
    OpenApiParameter(
        "parent_company", description="ID of the parent company", type=int
    ),
    OpenApiParameter(
        "parent_company_country_id",
        description="ID of the parent company's country",
        type=int,
    ),
    OpenApiParameter(
        "nature",
        description="",
        type=str,
        enum=[x["value"] for x in choices.NATURE_OF_DEAL_ITEMS],
        many=True,
    ),
    OpenApiParameter(
        "initiation_year_null", description="Include unknown years", type=bool
    ),
    OpenApiParameter(
        "initiation_year_min", description="Minimum year of initiation", type=int
    ),
    OpenApiParameter(
        "initiation_year_max", description="Maximum year of initiation", type=int
    ),
    OpenApiParameter(
        "intention_of_investment",
        description="",
        type=str,
        enum=[x["value"] for x in choices.INTENTION_OF_INVESTMENT_ITEMS],
        many=True,
    ),
    OpenApiParameter(
        "crops",
        type=str,
        enum=[x["value"] for x in choices.CROPS_ITEMS],
        many=True,
    ),
    OpenApiParameter(
        "animals",
        type=str,
        enum=[x["value"] for x in choices.ANIMALS_ITEMS],
        many=True,
    ),
    OpenApiParameter(
        "minerals",
        type=str,
        enum=[x["value"] for x in choices.MINERALS_ITEMS],
        many=True,
    ),
    OpenApiParameter(
        "transnational",
        description="Scope. true: Transnational, false: Domestic, not set: both",
        type=bool,
    ),
    OpenApiParameter(
        "forest_concession",
        description="not set: Included, true: Only false: Excluded",
        type=bool,
    ),
]


def parse_filters(request: Request):
    ret = Q()

    if region_id := request.GET.get("region_id"):
        ret &= Q(country__region_id=region_id)
    if country_id := request.GET.get("country_id"):
        ret &= Q(country_id=country_id)

    if area_min := request.GET.get("area_min"):
        ret &= Q(active_version__deal_size__gte=area_min)
    if area_max := request.GET.get("area_max"):
        ret &= Q(active_version__deal_size__lte=area_max)

    if neg_list := request.GET.getlist("negotiation_status"):
        ret &= Q(active_version__current_negotiation_status__in=neg_list)

    if imp_list := request.GET.getlist("implementation_status"):
        unknown = (
            Q(active_version__current_implementation_status=None)
            if "UNKNOWN" in imp_list
            else Q()
        )
        ret &= Q(active_version__current_implementation_status__in=imp_list) | unknown

    if parents := request.GET.get("parent_company"):
        ret &= Q(active_version__parent_companies__id=parents)
    if parents_c_id := request.GET.get("parent_company_country_id"):
        ret &= Q(
            active_version__parent_companies__active_version__country_id=parents_c_id
        )

    if nature := request.GET.getlist("nature"):
        all_nature = set([x["value"] for x in choices.NATURE_OF_DEAL_ITEMS])
        ret &= ~Q(
            active_version__nature_of_deal__contained_by=list(all_nature - set(nature))
        )

    iy_null = (
        Q(active_version__initiation_year=None)
        if request.GET.get("initiation_year_null")
        else Q()
    )
    if iy_min := request.GET.get("initiation_year_min"):
        ret &= Q(active_version__initiation_year__gte=iy_min) | iy_null
    if iy_max := request.GET.get("initiation_year_max"):
        ret &= Q(active_version__initiation_year__lte=iy_max) | iy_null

    if ioi_list := request.GET.getlist("intention_of_investment"):
        unknown = (
            Q(active_version__current_intention_of_investment=[])
            if "UNKNOWN" in ioi_list
            else Q()
        )
        ret &= (
            Q(active_version__current_intention_of_investment__overlap=ioi_list)
            | unknown
        )

    if crops := request.GET.getlist("crops"):
        ret &= Q(active_version__current_crops__overlap=crops)
    if animals := request.GET.getlist("animals"):
        ret &= Q(active_version__current_animals__overlap=animals)
    if minerals := request.GET.getlist("minerals"):
        ret &= Q(active_version__current_minerals__overlap=minerals)

    if trans := request.GET.get("transnational"):
        ret &= Q(active_version__transnational=trans == "true")

    if for_con := request.GET.get("forest_concession"):
        ret &= Q(active_version__forest_concession=for_con == "true")

    return ret
