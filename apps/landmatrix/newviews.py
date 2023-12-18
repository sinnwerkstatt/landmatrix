import json

from django.db import OperationalError
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.accounts.models import UserRole
from apps.landmatrix.models import choices
from apps.landmatrix.models.new import (
    DealHull,
    InvestorHull,
    DealVersion2,
    InvestorVersion2,
    DealWorkflowInfo2,
)
from apps.landmatrix.serializers import (
    Deal2Serializer,
    Investor2Serializer,
    DealVersionSerializer,
)


def _parse_filter(request: Request):
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
        ret &= Q(active_version__parent_companies__country_id=parents_c_id)

    # TODO This might not be working correctly yet. it does not include "no nature of deal", but the original filter did
    if nature := request.GET.getlist("nature"):
        all_nature = set([x["value"] for x in NATURE_OF_DEAL_ITEMS])
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

    if trans := request.GET.get("trans"):
        ret &= Q(active_version__transnational=trans == "true")

    if for_con := request.GET.get("for_con"):
        ret &= Q(active_version__forest_concession=for_con == "true")

    return ret


class DealVersionViewSet(viewsets.ModelViewSet):
    queryset = DealVersion2.objects.all()
    serializer_class = DealVersionSerializer

    def update(self, request, pk: int):
        if not request.user.is_authenticated or not request.user.role:
            raise PermissionDenied("MISSING_AUTHORIZATION")
        dv1: DealVersion2 = get_object_or_404(self.queryset, pk=pk)

        # TODO check all the permissions! (Creator, or different role or whatnot)

        serializer = self.serializer_class(
            dv1, data=request.data["version"], partial=True
        )

        if serializer.is_valid(raise_exception=True):
            # this is untidy
            dv1 = serializer.save()
            dv1.modified_by = request.user
            dv1.modified_at = timezone.now()
            dv1.save()
            serializer.save_submodels(request, dv1)

        return Response({})

    def destroy(self, request, pk: int):
        if not request.user.is_authenticated or not request.user.role:
            raise PermissionDenied("MISSING_AUTHORIZATION")
        dv1: DealVersion2 = get_object_or_404(self.queryset, pk=pk)

        if dv1.created_by_id != request.user.id and request.user.role < UserRole.EDITOR:
            raise PermissionDenied("MISSING_AUTHORIZATION")
        # TODO check all the permissions! (Creator, or different role or whatnot)

        old_draft_status = dv1.status
        dv1.delete()

        d1: DealHull = dv1.deal
        if d1.versions.count() == 0:
            d1.delete()
        else:
            d1.draft_version = None
            d1.save()
            DealWorkflowInfo2.objects.create(
                deal=d1,
                from_user=request.user,
                status_before=old_draft_status,
                status_after="DELETED",
                comment=request.data["comment"],
            )
        return Response({})

    @action(detail=True, methods=["put"])
    def change_status(self, request, pk: int):
        if not request.user.is_authenticated or not request.user.role:
            raise PermissionDenied("MISSING_AUTHORIZATION")
        dv1: DealVersion2 = get_object_or_404(self.queryset, pk=pk)

        if dv1.deal.draft_version_id != dv1.id:
            raise PermissionDenied("EDITING_OLD_VERSION")

        old_draft_status = dv1.status

        if request.data["transition"] == "TO_REVIEW":
            if not (
                dv1.created_by == request.user or request.user.role >= UserRole.EDITOR
            ):
                raise PermissionDenied("MISSING_AUTHORIZATION")
            draft_status = "REVIEW"
            dv1.status = "REVIEW"
            dv1.sent_to_review_at = timezone.now()
            dv1.sent_to_review_by = request.user
            if request.data.get("fullyUpdated"):
                dv1.fully_updated = True
            dv1.save()
        elif request.data["transition"] == "TO_ACTIVATION":
            if request.user.role < UserRole.EDITOR:
                raise PermissionDenied("MISSING_AUTHORIZATION")
            draft_status = "ACTIVATION"
            dv1.status = "ACTIVATION"
            dv1.sent_to_activation_at = timezone.now()
            dv1.sent_to_review_by = request.user
            dv1.save()
        elif request.data["transition"] == "ACTIVATE":
            if request.user.role < UserRole.ADMINISTRATOR:
                raise PermissionDenied("MISSING_AUTHORIZATION")
            draft_status = "ACTIVATED"
            dv1.status = "ACTIVATED"
            dv1.activated_at = timezone.now()
            dv1.activated_by = request.user
            dv1.save()
            d1: DealHull = dv1.deal
            d1.draft_version = None
            d1.active_version = dv1
            d1.save()

            dv1.workflowinfos.all().update(resolved=True)
        elif request.data["transition"] == "TO_DRAFT":
            if request.user.role < UserRole.EDITOR:
                raise PermissionDenied("MISSING_AUTHORIZATION")
            draft_status = "DRAFT"
            dv1.status = "DRAFT"
            dv1.id = None
            dv1.created_at = timezone.now()
            dv1.created_by_id = request.data["toUser"]
            dv1.save()

            d1 = dv1.deal
            d1.draft_version = dv1
            d1.save()
            # close remaining open feedback requests
            dv1.workflowinfos.filter(
                Q(status_before__in=["REVIEW", "ACTIVATION"])
                & Q(status_after="DRAFT")
                # TODO: https://git.sinntern.de/landmatrix/landmatrix/-/issues/404
                & (Q(from_user=request.user) | Q(to_user=request.user))
            ).update(resolved=True)
        else:
            raise ParseError("Invalid transition")

        # TODO do all the dealworkflowinfos
        DealWorkflowInfo2.objects.create(
            deal_id=dv1.deal_id,
            deal_version_id=dv1.id,
            from_user=request.user,
            to_user_id=request.data.get("toUser"),
            status_before=old_draft_status,
            status_after=draft_status,
            comment=request.data["comment"],
        )

        if to_user := request.data.get("toUser"):
            pass  # TODO
            # send_comment_to_user(obj, request.data["comment"], request.user, to_user, obj_version_id)

        return Response({"dealID": dv1.deal.id, "versionID": dv1.id})


class Deal2ViewSet(viewsets.ModelViewSet):
    queryset = DealHull.objects.all().prefetch_related(
        Prefetch("versions", queryset=DealVersion2.objects.order_by("-id"))
    )
    serializer_class = Deal2Serializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(
        name="Deal Instance",
        methods=["get"],
        url_path=r"(?P<version_id>\d+)",
        detail=True,
    )
    def retrieve_version(self, request, pk: int, version_id: int):
        instance = self.get_object()
        if version_id:
            instance._selected_version_id = version_id
        serializer = self.get_serializer(instance)
        dv1 = serializer.data
        # TODO check for permissions when viewing a draft
        if request.user.role > UserRole.EDITOR:
            ...
            # dv1.created_by_id

        return Response(dv1)

    def list(self, request: Request, *args, **kwargs):
        deals = DealHull.objects.visible(
            request.user, request.GET.get("subset", "PUBLIC")
        )
        filters = _parse_filter(request)
        deals = (
            deals.exclude(active_version=None)
            .filter(deleted=False, confidential=False)
            .filter(filters)
            .prefetch_related("active_version")
            .prefetch_related("active_version__operating_company")
            .prefetch_related("active_version__locations")
            .prefetch_related("country")
            .order_by("id")
        )

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
                        # TODO Investors are not filtered (e.g. "deleted")
                    ],
                    "locations": [
                        {
                            "nid": x.nid,
                            "point": json.loads(x.point.geojson) if x.point else None,
                        }
                        for x in d.active_version.locations.all()
                    ],
                }
                for d in deals
            ]
        )

    def create(self, request, *args, **kwargs):
        country_id = request.data["country_id"]
        d1 = DealHull.objects.create(country_id=country_id, created_by=request.user)
        dv1 = DealVersion2.objects.create(deal_id=d1.id, created_by=request.user)
        d1.draft_version = dv1
        d1.save()
        return Response({"dealID": d1.id, "versionID": dv1.id})

    def update(self, request, *args, **kwargs):
        return Response({})


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
        try:
            return Response(instance.involvements_graph(depth, include_deals))
        except OperationalError:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)


def field_choices(request):
    return JsonResponse(
        {
            "deal": {
                "intention_of_investment": choices.INTENTION_OF_INVESTMENT_ITEMS,
                "negotiation_status": choices.NEGOTIATION_STATUS_ITEMS,
                "implementation_status": choices.IMPLEMENTATION_STATUS_ITEMS,
                "level_of_accuracy": choices.LOCATION_ACCURACY_ITEMS,
                "nature_of_deal": choices.NATURE_OF_DEAL_ITEMS,
                "recognition_status": choices.RECOGNITION_STATUS_ITEMS,
                "negative_impacts": choices.NEGATIVE_IMPACTS_ITEMS,
                "benefits": choices.BENEFITS_ITEMS,
                "former_land_owner": choices.FORMER_LAND_OWNER_ITEMS,
                "former_land_use": choices.FORMER_LAND_USE_ITEMS,
                "ha_area": choices.HA_AREA_ITEMS,
                "community_consultation": choices.COMMUNITY_CONSULTATION_ITEMS,
                "community_reaction": choices.COMMUNITY_REACTION_ITEMS,
                "former_land_cover": choices.FORMER_LAND_COVER_ITEMS,
                "crops": choices.CROPS_ITEMS,
                "animals": choices.ANIMALS_ITEMS,
                "electricity_generation": choices.ELECTRICITY_GENERATION_ITEMS,
                "carbon_sequestration": choices.CARBON_SEQUESTRATION_ITEMS,
                "minerals": choices.MINERALS_ITEMS,
                "water_source": choices.WATER_SOURCE_ITEMS,
                "not_public_reason": choices.NOT_PUBLIC_REASON_ITEMS,
            },
            "investor": {"classification": choices.INVESTOR_CLASSIFICATION_ITEMS},
            "involvement": {"investment_type": choices.INVESTMENT_TYPE_ITEMS},
        }
    )
