from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter
from rest_framework.request import Request

from apps.landmatrix.models import choices

openapi_filters_parameters_scoring = [
    OpenApiParameter(
        name="region_id", description="Filter by region", type=int, many=True
    ),
    OpenApiParameter(
        name="country_id", description="Filter by country", type=int, many=True
    ),
    OpenApiParameter(name="area_min", description="Minimum deal area", type=int),
    OpenApiParameter(name="area_max", description="Maximum deal area", type=int),
    OpenApiParameter(
        name="negotiation_status",
        description="Negotiation status",
        type=str,
        enum=[x["value"] for x in choices.NEGOTIATION_STATUS_ITEMS],
        many=True,
    ),
    OpenApiParameter(
        name="nature_of_deal",
        description="Nature of the deal",
        type=str,
        enum=[x["value"] for x in choices.NATURE_OF_DEAL_ITEMS],
        many=True,
    ),
    OpenApiParameter(
        name="parent_company",
        description="ID of the parent company",
        type=int,
        many=True,
    ),
    OpenApiParameter(
        name="parent_company_country_id",
        description="ID of the parent company's country",
        type=int,
        many=True,
    ),
    OpenApiParameter(
        "initiation_year_min", description="Minimum year of initiation", type=int
    ),
    OpenApiParameter(
        "initiation_year_max", description="Maximum year of initiation", type=int
    ),
    OpenApiParameter(
        "initiation_year_unknown", description="Include unknown years", type=bool
    ),
    OpenApiParameter(
        name="implementation_status",
        description="Implementation status",
        type=str,
        enum=[x["value"] for x in choices.IMPLEMENTATION_STATUS_ITEMS] + ["UNKNOWN"],
        many=True,
    ),
    OpenApiParameter(
        name="intention_of_investment",
        description="",
        type=str,
        enum=[x["value"] for x in choices.INTENTION_OF_INVESTMENT_ITEMS] + ["UNKNOWN"],
        many=True,
    ),
    OpenApiParameter(
        name="crops",
        type=str,
        enum=[x["value"] for x in choices.CROPS_ITEMS],
        many=True,
    ),
    OpenApiParameter(
        name="animals",
        type=str,
        enum=[x["value"] for x in choices.ANIMALS_ITEMS],
        many=True,
    ),
    OpenApiParameter(
        name="minerals",
        type=str,
        enum=[x["value"] for x in choices.MINERALS_ITEMS],
        many=True,
    ),
    OpenApiParameter(
        name="transnational",
        description="Scope. true: Transnational, false: Domestic, not set: both",
        type=bool,
    ),
    OpenApiParameter(
        name="forest_concession",
        description="not set: Included, true: Only false: Excluded",
        type=bool,
    ),
]


def parse_filters(request: Request):
    res = Q()

    if region_id := request.GET.getlist("region_id"):
        res &= Q(deal__country__region_id__in=region_id)
    if country_id := request.GET.getlist("country_id"):
        res &= Q(deal__country_id__in=country_id)

    if area_min := request.GET.get("area_min"):
        res &= Q(deal__active_version__deal_size__gte=area_min)
    if area_max := request.GET.get("area_max"):
        res &= Q(deal__active_version__deal_size__lte=area_max)

    if neg_status := request.GET.getlist("negotiation_status"):
        res &= Q(deal__active_version__current_negotiation_status__in=neg_status)

    if nature := request.GET.getlist("nature_of_deal"):
        all_nature = {x["value"] for x in choices.NATURE_OF_DEAL_ITEMS}
        res &= ~Q(
            deal__active_version__nature_of_deal__contained_by=list(
                all_nature - set(nature)
            )
        )

    if parents := request.GET.getlist("parent_company"):
        res &= Q(deal__active_version__parent_companies__id__in=parents)
    if parents_c_id := request.GET.getlist("parent_company_country_id"):
        res &= Q(
            deal__active_version__parent_companies__active_version__country_id__in=parents_c_id
        )

    if request.GET.get("initiation_year_unknown") == "false":
        res &= Q(deal__active_version__initiation_year__isnull=False)
    if init_year_min := request.GET.get("initiation_year_min"):
        res &= Q(deal__active_version__initiation_year__gte=init_year_min)
    if init_year_max := request.GET.get("initiation_year_max"):
        res &= Q(deal__active_version__initiation_year_max__lte=init_year_max)

    if imp_status := request.GET.getlist("implementation_status"):
        unknown = (
            Q(deal__active_version__current_implementation_status=None)
            if "UNKNOWN" in imp_status
            else Q()
        )
        res &= (
            Q(deal__active_version__current_implementation_status__in=imp_status)
            | unknown
        )

    if int_of_inv := request.GET.getlist("intention_of_investment"):
        unknown = (
            Q(deal__active_version__current_intention_of_investment=[])
            if "UNKNOWN" in int_of_inv
            else Q()
        )
        res &= (
            Q(deal__active_version__current_intention_of_investment__overlap=int_of_inv)
            | unknown
        )

    if crops := request.GET.getlist("crops"):
        res &= Q(deal__active_version__current_crops__overlap=crops)
    if animals := request.GET.getlist("animals"):
        res &= Q(deal__active_version__current_animals__overlap=animals)
    if minerals := request.GET.getlist("minerals"):
        res &= Q(deal__active_version__current_minerals__overlap=minerals)

    if trans := request.GET.get("transnational"):
        res &= Q(deal__active_version__transnational=trans == "true")

    if for_con := request.GET.get("forest_concession"):
        res &= Q(deal__active_version__forest_concession=for_con == "true")

    return res
