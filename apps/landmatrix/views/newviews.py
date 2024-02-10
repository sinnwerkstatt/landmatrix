from django.contrib.postgres.expressions import ArraySubquery
from django.db import OperationalError, transaction
from django.db.models import Prefetch, Q, F, Case, When, OuterRef
from django.db.models.functions import JSONObject
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from wagtail.models import Site

from apps.accounts.models import UserRole, User
from apps.landmatrix.models import choices
from apps.landmatrix.models.new import (
    DealHull,
    InvestorHull,
    DealVersion2,
    InvestorVersion2,
    DealWorkflowInfo2,
    InvestorWorkflowInfo2,
    DealTopInvestors2,
    Location,
)
from apps.landmatrix.permissions import IsReporterOrHigher, IsAdministrator
from apps.landmatrix.serializers import (
    DealSerializer,
    InvestorSerializer,
    DealVersionSerializer,
    InvestorVersionSerializer,
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
        ret &= Q(
            active_version__parent_companies__active_version__country_id=parents_c_id
        )

    # TODO Nuts This might not be working correctly yet. it does not include "no nature of deal", but the original filter did
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

    if trans := request.GET.get("trans"):
        ret &= Q(active_version__transnational=trans == "true")

    if for_con := request.GET.get("for_con"):
        ret &= Q(active_version__forest_concession=for_con == "true")

    return ret


def add_wfi(
    obj: DealHull | InvestorHull = None,
    obj_version: DealVersion2 | InvestorVersion2 = None,
    from_user: User = None,
    to_user_id: int = None,
    status_before: str = "",
    status_after: str = "",
    comment: str = "",
):
    if obj is None and obj_version is None:
        raise Exception

    if obj is None:
        obj = (
            obj_version.deal
            if isinstance(obj_version, DealVersion2)
            else obj_version.investor
        )

    kwargs = {
        "from_user": from_user,
        "to_user_id": to_user_id,
        "status_before": status_before,
        "status_after": status_after,
        "comment": comment or "",
    }
    if isinstance(obj, DealHull):
        return DealWorkflowInfo2.objects.create(
            deal=obj or obj_version.deal, deal_version=obj_version, **kwargs
        )
    else:
        return InvestorWorkflowInfo2.objects.create(
            investor=obj or obj_version.investor, investor_version=obj_version, **kwargs
        )


def _send_comment_to_user(
    obj: DealHull | InvestorHull,
    comment: str | None,
    from_user: User,
    to_user_id: int,
    version_id: int | None = None,
) -> None:
    receiver = User.objects.get(id=to_user_id)

    is_deal = isinstance(obj, DealHull)
    if is_deal:
        obj_desc = f"deal #{obj.id}"
        obj_url = f"/deal/{obj.id}/"
    else:
        obj_desc = f"investor {obj.active_version.name} (#{obj.id})"
        obj_url = f"/investor/{obj.id}/"

    if version_id:
        obj_url += f"{version_id}/"

    # build base_url
    _site = Site.objects.get(is_default_site=True)
    _port = f":{_site.port}" if _site.port not in [80, 443] else ""
    base_url = f"http{'s' if _site.port == 443 else ''}://{_site.hostname}{_port}"

    if comment:
        message = _(
            f"{from_user.full_name} has addressed you in a comment on {obj_desc}:"
        )
        message += "\n\n"
        message += comment
    else:
        message = _(f"{from_user.full_name} has updated {obj_desc}:")
    message += "\n\n" + _(f"Please review at {base_url + obj_url}")

    receiver.email_user("[Landmatrix] " + _("New comment"), message)


class VersionViewSet(viewsets.ReadOnlyModelViewSet):
    class Meta:
        abstract = True

    def get_permissions(self):
        if self.action in ["update", "destroy", "change_status"]:
            return [IsReporterOrHigher()]
        return [IsAdminUser()]

    @transaction.atomic
    def update(self, request, pk: int):
        ov1: DealVersion2 | InvestorVersion2 = get_object_or_404(self.queryset, pk=pk)

        if ov1.created_by_id != request.user.id and request.user.role < UserRole.EDITOR:
            raise PermissionDenied("MISSING_AUTHORIZATION")

        if not ov1.is_current_draft():
            raise PermissionDenied("EDITING_OLD_VERSION")

        data = request.data["version"]

        creating_new_version = ov1.created_by_id != request.user.id
        if creating_new_version:
            ov1.change_status(
                new_status="TO_DRAFT", user=request.user, to_user_id=request.user.id
            )

        serializer: DealVersionSerializer | InvestorVersionSerializer = (
            self.serializer_class(ov1, data=data, partial=True)
        )
        if serializer.is_valid(raise_exception=True):
            # this is untidy
            ov1 = serializer.save()
            if not creating_new_version:
                ov1.modified_by = request.user
                ov1.modified_at = timezone.now()

            serializer.save_submodels(data, ov1)
            ov1.save()

            return Response({"versionID": ov1.id})

    def destroy(self, request, pk: int):
        ov1: DealVersion2 | InvestorVersion2 = get_object_or_404(self.queryset, pk=pk)

        if ov1.created_by_id != request.user.id and request.user.role < UserRole.EDITOR:
            raise PermissionDenied("MISSING_AUTHORIZATION")

        old_draft_status = ov1.status

        if isinstance(ov1, DealVersion2):
            o1: DealHull = ov1.deal
        else:
            o1: InvestorHull = ov1.investor

        ov1.delete()

        if o1.versions.count() == 0:
            o1.delete()
        else:
            o1.draft_version = None
            o1.save()

            add_wfi(
                obj=o1,
                from_user=request.user,
                to_user_id=request.data.get("toUser"),
                status_before=old_draft_status,
                status_after="DELETED",
                comment=request.data.get("comment", "") or "",
            )

        return Response({})


class DealVersionViewSet(VersionViewSet):
    queryset = DealVersion2.objects.all()
    serializer_class = DealVersionSerializer

    @action(detail=True, methods=["put"])
    def change_status(self, request, pk: int):
        dv1: DealVersion2 = get_object_or_404(self.queryset, pk=pk)

        if not dv1.is_current_draft():
            raise PermissionDenied("EDITING_OLD_VERSION")

        to_user_id = request.data.get("toUser")

        dv1.change_status(
            new_status=request.data["transition"],
            user=request.user,
            fully_updated=request.data.get("fullyUpdated"),
            to_user_id=to_user_id,
            comment=request.data.get("comment", ""),
        )

        if request.data["transition"] == "TO_REVIEW" and request.data.get("toUser"):
            # if there was a request for improvement workflowinfo, email the requester
            old_wfi: DealWorkflowInfo2 | None = self.deal.workflowinfos.last()
            if (
                old_wfi
                and old_wfi.status_before in ["REVIEW", "ACTIVATION"]
                and old_wfi.status_after == "DRAFT"
                and old_wfi.to_user == to_user_id
            ):
                old_wfi.resolved = True
                old_wfi.save()
                _send_comment_to_user(
                    obj=dv1.deal,
                    comment="",
                    from_user=request.user,
                    to_user_id=old_wfi.from_user_id,
                    version_id=dv1.id,
                )

        if to_user := request.data.get("toUser"):
            _send_comment_to_user(
                obj=dv1.deal,
                comment=request.data.get("comment"),
                from_user=request.user,
                to_user_id=to_user,
                version_id=dv1.id,
            )

        return Response({"dealID": dv1.deal.id, "versionID": dv1.id})


class HullViewSet(viewsets.ReadOnlyModelViewSet):
    version_serializer_class = None

    class Meta:
        abstract = True

    def get_permissions(self):
        if self.action in [
            "retrieve",
            "list",
            "retrieve_version",
            "simple",
            "involvements_graph",
        ]:
            return [AllowAny()]
        if self.action in ["add_comment", "create", "update"]:
            return [IsReporterOrHigher()]
        if self.action in ["toggle_confidential", "toggle_deleted", "make_copy"]:
            return [IsAdministrator()]
        return [IsAdminUser()]

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        creating a new Version when calling "save" on an existing object
        """

        o1: DealHull | InvestorHull = self.get_object()
        ov1 = o1.add_draft(created_by=request.user)

        data = request.data["version"]

        serializer: DealVersionSerializer | InvestorVersionSerializer = (
            self.version_serializer_class(ov1, data=data, partial=True)
        )
        if serializer.is_valid(raise_exception=True):
            # this is untidy
            ov1: DealVersion2 | InvestorVersion2 = serializer.save()
            serializer.save_submodels(data, ov1)
            ov1.save()  # recalculating fields here.

        add_wfi(obj=o1, obj_version=ov1, from_user=request.user, status_after="DRAFT")

        return Response({"versionID": ov1.id})

    @action(detail=True, methods=["put"])
    def add_comment(self, request, *args, **kwargs):
        o1: DealHull | InvestorHull = self.get_object()

        to_user_id = request.data.get("toUser")

        add_wfi(
            obj=o1,
            obj_version=request.data.get("version"),
            from_user=request.user,
            to_user_id=to_user_id,
            comment=request.data.get("comment") or "",
        )

        if to_user_id:
            _send_comment_to_user(
                obj=o1,
                comment=request.data.get("comment"),
                from_user=request.user,
                to_user_id=to_user_id,
                version_id=o1.active_version.id if o1.active_version else None,
            )

        return Response({})

    @action(methods=["put"], detail=True)
    def toggle_deleted(self, request, *args, **kwargs):
        o1: DealHull | InvestorHull = self.get_object()
        o1.deleted = request.data["deleted"]
        o1.deleted_comment = request.data["comment"] if o1.deleted else ""
        # TODO Kurt we used to set modified by/at here too. but on the dealhull object doesnt make sense
        o1.save()

        add_wfi(
            obj=o1,
            from_user=request.user,
            comment=request.data.get("comment") or "",
            status_after="DELETED" if o1.deleted else "REACTIVATED",
        )

        return Response({})


class DealViewSet(HullViewSet):
    queryset = DealHull.objects.all().prefetch_related(
        Prefetch("versions", queryset=DealVersion2.objects.order_by("-id"))
    )
    serializer_class = DealSerializer
    version_serializer_class = DealVersionSerializer

    def get_queryset(self):
        if self.action in ["retrieve", "retrieve_version"]:
            return self.queryset.visible(self.request.user, "UNFILTERED")
        return self.queryset

    def list(self, request: Request, *args, **kwargs):
        return Response(
            DealHull.objects.active()
            .order_by("id")
            .visible(request.user, request.GET.get("subset", "PUBLIC"))
            .filter(_parse_filter(request))
            .annotate(
                selected_version=JSONObject(
                    deal_size="active_version__deal_size",
                    current_intention_of_investment="active_version__current_intention_of_investment",
                    current_negotiation_status="active_version__current_negotiation_status",
                    current_contract_size="active_version__current_contract_size",
                    current_implementation_status="active_version__current_implementation_status",
                    current_crops="active_version__current_crops",
                    current_animals="active_version__current_animals",
                    current_mineral_resources="active_version__current_mineral_resources",
                    current_electricity_generation="active_version__current_electricity_generation",
                    current_carbon_sequestration="active_version__current_carbon_sequestration",
                    intended_size="active_version__intended_size",
                    negotiation_status="active_version__negotiation_status",
                    contract_size="active_version__contract_size",
                    operating_company=Case(
                        When(
                            active_version__operating_company__active_version=None,
                            then=None,
                        ),
                        default=JSONObject(
                            id="active_version__operating_company_id",
                            selected_version=JSONObject(
                                name="active_version__operating_company__active_version__name",
                                name_unknown="active_version__operating_company__active_version__name_unknown",
                            ),
                        ),
                    ),
                    locations=ArraySubquery(
                        Location.objects.filter(
                            dealversion_id=OuterRef("active_version_id")
                        ).values(
                            json=JSONObject(
                                nid="nid",
                                point="point",
                                level_of_accuracy="level_of_accuracy",
                            )
                        )
                    ),
                    top_investors=(
                        ArraySubquery(
                            DealTopInvestors2.objects.exclude(
                                investorhull__active_version=None
                            )
                            .filter(investorhull__deleted=False)
                            .filter(dealversion2_id=OuterRef("active_version_id"))
                            .values(
                                json=JSONObject(
                                    id="investorhull_id",
                                    name="investorhull__active_version__name",
                                    classification="investorhull__active_version__classification",
                                )
                            )
                        )
                    ),
                )
            )
            .values("id", "country_id", "fully_updated_at", "selected_version")
        )

    @staticmethod
    def create(request, *args, **kwargs):
        country_id = request.data["country_id"]
        d1: DealHull = DealHull.objects.create(
            country_id=country_id, first_created_by=request.user
        )
        dv1 = d1.add_draft(created_by=request.user)

        DealWorkflowInfo2.objects.create(
            deal=d1,
            deal_version=dv1,
            from_user=request.user,
            status_after="DRAFT",
        )
        return Response({"dealID": d1.id, "versionID": dv1.id})

    @action(methods=["get"], url_path=r"(?P<version_id>\d+)", detail=True)
    def retrieve_version(self, request, pk: int, version_id: int):
        d1: DealHull = self.get_object()
        d1._selected_version_id = int(version_id)

        dv1: DealVersion2 = d1.versions.get(id=version_id)

        if (
            (request.user.is_authenticated and request.user.role >= UserRole.EDITOR)
            or dv1.created_by == request.user.id
            or (dv1.status == "ACTIVATED" and dv1.is_public)
        ):
            return Response(self.get_serializer(d1).data)

        raise PermissionDenied if request.user.is_authenticated else NotAuthenticated()

    @action(methods=["put"], detail=True)
    def toggle_confidential(self, request, *args, **kwargs):
        d1: DealHull = self.get_object()
        d1.confidential = request.data["confidential"]
        d1.confidential_comment = request.data["comment"]
        d1.save()

        confidential_str = (
            "SET_CONFIDENTIAL" if d1.confidential else "UNSET_CONFIDENTIAL"
        )
        DealWorkflowInfo2.objects.create(
            deal=d1,
            from_user=request.user,
            comment=f"[{confidential_str}] {request.data['comment']}",
        )

        return Response({})

    @action(methods=["put"], detail=True)
    def make_copy(self, request, *args, **kwargs):
        d1: DealHull = self.get_object()
        old_id = d1.id
        d1.id = None

        # make a copy of the current active_version and set it to draft on the new thing.
        # don't forget about locations, contracts,... foreign-keys etc...

        # TODO we need to copy more things here, right?
        # d1.created_by = request.user
        # d1.created_at = timezone.now()

        # d1.save()
        #
        # DealWorkflowInfo2.objects.create(
        #     deal=d1,
        #     # deal_version=dv1,
        #     from_user=request.user,
        #     status_after="DRAFT",
        #     comment=f"Copied from deal #{old_id}",
        # )

        # return Response({"dealID": d1.id, "versionID": dv1.id})


class InvestorVersionViewSet(VersionViewSet):
    queryset = InvestorVersion2.objects.all()
    serializer_class = InvestorVersionSerializer

    @action(detail=True, methods=["put"])
    @transaction.atomic
    def change_status(self, request, pk: int):
        iv1: InvestorVersion2 = get_object_or_404(self.queryset, pk=pk)

        if not iv1.is_current_draft():
            raise PermissionDenied("EDITING_OLD_VERSION")

        to_user_id = request.data.get("toUser")
        iv1.change_status(
            new_status=request.data["transition"],
            user=request.user,
            to_user_id=to_user_id,
            comment=request.data.get("comment", ""),
        )

        if request.data["transition"] == "TO_REVIEW" and to_user_id:
            # if there was a request for improvement workflowinfo, email the requester
            old_wfi: InvestorWorkflowInfo2 | None = iv1.investor.workflowinfos.last()
            if (
                old_wfi
                and old_wfi.status_before in ["REVIEW", "ACTIVATION"]
                and old_wfi.status_after == "DRAFT"
                and old_wfi.to_user_id == to_user_id
            ):
                old_wfi.resolved = True
                old_wfi.save()
                _send_comment_to_user(
                    obj=iv1.investor,
                    comment="",
                    from_user=request.user,
                    to_user_id=old_wfi.from_user_id,
                    version_id=iv1.id,
                )

        if to_user := request.data.get("toUser"):
            _send_comment_to_user(
                obj=iv1.investor,
                comment=request.data.get("comment"),
                from_user=request.user,
                to_user_id=to_user,
                version_id=iv1.id,
            )

        return Response({"investorID": iv1.investor.id, "versionID": iv1.id})


class InvestorViewSet(HullViewSet):
    queryset = InvestorHull.objects.all().prefetch_related(
        Prefetch("versions", queryset=InvestorVersion2.objects.order_by("-id"))
    )
    serializer_class = InvestorSerializer
    version_serializer_class = InvestorVersionSerializer

    @staticmethod
    def create(request, *args, **kwargs):
        i1: InvestorHull = InvestorHull.objects.create(first_created_by=request.user)
        iv1 = i1.add_draft(created_by=request.user)

        # there is more logic here, compared to "new deal" because new deal only ever gets a country
        data = request.data["version"]
        if data.get("country"):
            data["country_id"] = data.get("country", {}).get("id", None)
            del data["country"]

        serializer = InvestorVersionSerializer(iv1, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            dv1 = serializer.save()
            dv1.save()
            # no need to save submodels in this step. there are definitely no datasources defined here yet
            # serializer.save_submodels(data, dv1)

        InvestorWorkflowInfo2.objects.create(
            investor=i1,
            investor_version=iv1,
            from_user=request.user,
            status_after="DRAFT",
        )
        return Response({"investorID": i1.id, "versionID": iv1.id})

    @action(methods=["get"], url_path=r"(?P<version_id>\d+)", detail=True)
    def retrieve_version(self, request, pk: int, version_id: int):
        i1: InvestorHull = self.get_object()
        i1._selected_version_id = int(version_id)

        try:
            iv1: InvestorVersion2 = i1.versions.get(id=version_id)
        except InvestorVersion2.DoesNotExist:
            raise Http404

        if (
            (request.user.is_authenticated and request.user.role >= UserRole.EDITOR)
            or iv1.created_by == request.user.id
            or iv1.status == "ACTIVATED"
        ):
            return Response(self.get_serializer(i1).data)
        raise PermissionDenied if request.user.is_authenticated else NotAuthenticated

    @action(methods=["get"], detail=False)
    def simple(self, request):
        # TODO this might need an "also search for drafts option"
        return Response(
            InvestorHull.objects.exclude(deleted=True)
            .exclude(active_version=None)
            .annotate(name=F("active_version__name"))
            .values("id", "name")
        )

    @action(methods=["get"], detail=False)
    def deal_filtered(self, request):
        deals = (
            DealHull.objects.visible(request.user, request.GET.get("subset", "PUBLIC"))
            .exclude(active_version=None)
            .filter(deleted=False, confidential=False)
            .filter(_parse_filter(request))
            .values_list("active_version_id", flat=True)
        )

        ret = InvestorHull.objects.exclude(active_version=None).filter(
            child_deals__in=deals
        )

        if investor_id := request.GET.get("parent_company"):
            ret = ret.filter(id=investor_id)
        if country_id := request.GET.get("parent_company_country_id"):
            ret = ret.filter(active_version__country_id=country_id)

        return Response(InvestorHull.to_investor_list(ret))

    @action(methods=["get"], detail=True)
    def involvements_graph(self, request, *args, **kwargs):
        depth = int(request.GET.get("depth", 5))
        include_deals = request.GET.get("include_deals", "") == "true"
        show_ventures = request.GET.get("show_ventures", "") == "true"
        investor: InvestorHull = self.get_object()

        # TODO make sure it's a live version (active version)

        try:
            return Response(
                investor.involvements_graph(depth, include_deals, show_ventures)
            )
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
                "carbon_sequestration_certs": choices.CARBON_SEQUESTRATION_CERT_ITEMS,
                "minerals": choices.MINERALS_ITEMS,
                "water_source": choices.WATER_SOURCE_ITEMS,
                "not_public_reason": choices.NOT_PUBLIC_REASON_ITEMS,
                "actors": choices.ACTOR_ITEMS,
            },
            "datasource": {"type": choices.DATASOURCE_TYPE_ITEMS},
            "investor": {"classification": choices.INVESTOR_CLASSIFICATION_ITEMS},
            "involvement": {
                "investment_type": choices.INVESTMENT_TYPE_ITEMS,
                "parent_relation": choices.PARENT_RELATION_ITEMS,
            },
        }
    )
