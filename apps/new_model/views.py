from django.db.models import Prefetch, Q
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.landmatrix.models.choices import (
    INVESTOR_CLASSIFICATION_ITEMS,
    INTENTION_OF_INVESTMENT_ITEMS,
    NEGOTIATION_STATUS_ITEMS,
    IMPLEMENTATION_STATUS_ITEMS,
    LOCATION_ACCURACY_ITEMS,
    INVESTMENT_TYPE_ITEMS,
    NATURE_OF_DEAL_ITEMS,
)
from apps.new_model.models import DealHull, InvestorHull, DealVersion2, InvestorVersion2
from apps.new_model.serializers import (
    Deal2Serializer,
    Investor2Serializer,
)


class Deal2ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DealHull.objects.all().prefetch_related(
        Prefetch("versions", queryset=DealVersion2.objects.order_by("-id"))
    )
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

    @staticmethod
    def _parse_filter(request: Request):
        ret = Q()

        print(request.GET)
        if subset := request.GET.get("subset"):
            # TODO
            ret &= Q(active_version__is_public=True)

        if r_id := request.GET.get("r_id"):
            ret &= Q(country__region_id=r_id)
        if c_id := request.GET.get("c_id"):
            ret &= Q(country_id=c_id)

        if ds_min := request.GET.get("ds_min"):
            ret &= Q(active_version__deal_size__gte=ds_min)
        if ds_max := request.GET.get("ds_max"):
            ret &= Q(active_version__deal_size__lte=ds_max)

        if neg_list := request.GET.getlist("cur_neg_stat"):
            ret &= Q(active_version__current_negotiation_status__in=neg_list)

        if imp_list := request.GET.getlist("cur_imp_stat"):
            unknown = (
                Q(active_version__current_implementation_status__isnull=True)
                if "UNKNOWN" in imp_list
                else Q()
            )
            ret &= (
                Q(active_version__current_implementation_status__in=imp_list) | unknown
            )

        if parents := request.GET.get("parents"):
            ret &= Q(active_version__parent_companies__id=parents)
        if parents_c_id := request.GET.get("parents_c_id"):
            ret &= Q(active_version__parent_companies__country_id=parents_c_id)

        iy_null = (
            Q(active_version__initiation_year__isnull=True)
            if request.GET.get("iy_null")
            else Q()
        )
        if iy_min := request.GET.get("iy_min"):
            ret &= Q(active_version__initiation_year__gte=iy_min) | iy_null
        if iy_max := request.GET.get("iy_max"):
            ret &= Q(active_version__initiation_year__lte=iy_max) | iy_null

        if ioi_list := request.GET.getlist("cur_ioi"):
            unknown = (
                Q(active_version__current_intention_of_investment=[])
                if "UNKNOWN" in ioi_list
                else Q()
            )
            ret &= (
                Q(active_version__current_intention_of_investment__overlap=ioi_list)
                | unknown
            )

        if trans := request.GET.get("trans"):
            ret &= Q(active_version__transnational=trans == "true")

        if for_con := request.GET.get("for_con"):
            ret &= Q(active_version__forest_concession=for_con == "true")

        return ret

    def list(self, request: Request, *args, **kwargs):
        filters = self._parse_filter(request)
        deals = (
            DealHull.objects.exclude(active_version=None)
            .filter(filters)
            .prefetch_related("active_version")
            .prefetch_related("active_version__operating_company")
            .prefetch_related("country")
            .order_by("id")
        )
        print(deals.count())

        deals = deals[:10]
        return Response(
            [
                {
                    "id": d.id,
                    "country": {
                        "id": d.country.id,
                        "name": d.country.name,
                        "region": {"id": d.country.region_id},
                    }
                    if d.country_id
                    else None,
                    "fully_updated_at": d.fully_updated_at,  # for listing
                    "deal_size": d.active_version.deal_size,
                    "current_intention_of_investment": d.active_version.current_intention_of_investment,
                    "current_negotiation_status": d.active_version.current_negotiation_status,
                    "current_contract_size": d.active_version.current_contract_size,
                    "current_implementation_status": d.active_version.current_implementation_status,
                    "current_crops": d.active_version.current_crops,
                    "current_animals": d.active_version.current_animals,
                    "current_mineral_resources": d.active_version.current_mineral_resources,
                    "current_electricity_generation": d.active_version.current_electricity_generation,
                    "current_carbon_sequestration": d.active_version.current_carbon_sequestration,
                    "intended_size": d.active_version.intended_size,
                    "negotiation_status": d.active_version.negotiation_status,
                    "contract_size": d.active_version.contract_size,
                    "operating_company": {
                        "id": d.active_version.operating_company.id,
                        "name": d.active_version.operating_company.name,
                    }  # for map pin popover & listing
                    if d.active_version.operating_company_id
                    else None,
                    "top_investors": [
                        {
                            "id": ti.id,
                            "name": ti.name,
                            "classification": ti.classification,
                        }  # for listing
                        for ti in d.active_version.top_investors.all()
                        # TODO Filter deleted!
                    ],
                }
                for d in deals
            ]
        )


class Investor2ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InvestorHull.objects.all().prefetch_related(
        Prefetch("versions", queryset=InvestorVersion2.objects.order_by("-id"))
    )
    serializer_class = Investor2Serializer

    @action(
        name="Investor Instance",
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

    @action(methods=["get"], detail=True)
    def involvements_graph(self, request, pk=None, version_id=None):
        depth = int(request.GET.get("depth", 5))
        include_deals = request.GET.get("include_deals", "") == "true"
        instance: InvestorHull = self.get_object()
        return Response(instance.involvements_graph(depth, include_deals))


def field_choices(request):
    return JsonResponse(
        {
            "deal": {
                "intention_of_investment": INTENTION_OF_INVESTMENT_ITEMS,
                "negotiation_status": NEGOTIATION_STATUS_ITEMS,
                "implementation_status": IMPLEMENTATION_STATUS_ITEMS,
                "level_of_accuracy": LOCATION_ACCURACY_ITEMS,
                "nature_of_deal": NATURE_OF_DEAL_ITEMS,
            },
            "investor": {"classification": INVESTOR_CLASSIFICATION_ITEMS},
            "involvement": {"investment_type": INVESTMENT_TYPE_ITEMS},
        }
    )
