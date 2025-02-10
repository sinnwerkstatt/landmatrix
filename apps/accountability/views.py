from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import Case, F, OuterRef, Prefetch, Q, When
from django.db.models.functions import JSONObject
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accountability.models import (
    Bookmark,
    DealScore,
    DealScoreVersion,
    DealVariable,
    Project,
    UserInfo,
    VggtArticle,
    VggtChapter,
    VggtVariable,
)
from apps.accountability.permissions import (
    IsAdministrator,
    IsOwnerOrEditorOrReadonly,
    IsReporterOrHigher,
    IsReporterOrHigherOrReadonly,
    IsUser,
)
from apps.accountability.serializers import (
    BookmarkBulkSerializer,
    BookmarkSerializer,
    DealScoreSerializer,
    DealScoreVersionSerializer,
    DealVariableSerializer,
    ProjectSerializer,
    UserInfoSerializer,
    VggtArticleSerializer,
    VggtChapterSerializer,
    VggtVariableSerializer,
)
from apps.accountability.utils import openapi_filters_parameters_scoring, parse_filters
from apps.landmatrix.models.deal import DealHull, DealVersion


# Tmp root view
def index(request):
    return HttpResponse("Hello world, this is accountability.")


# Add custom view to retrieve api > export > converter.py fields


class UserInfoList(generics.ListCreateAPIView):
    permission_classes = [IsReporterOrHigher]
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


class UserInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [IsReporterOrHigher]

    def get_object(self):
        # Return UserInfo for currently logged in user
        user = self.request.user

        if not user.is_anonymous:
            return UserInfo.objects.get(user=self.request.user)


class VggtChapterList(generics.ListCreateAPIView):
    queryset = VggtChapter.objects.all()
    serializer_class = VggtChapterSerializer


class VggtChapterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VggtChapter.objects.all()
    serializer_class = VggtChapterSerializer


class VggtArticleList(generics.ListCreateAPIView):
    queryset = VggtArticle.objects.all()
    serializer_class = VggtArticleSerializer


class VggtArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VggtArticle.objects.all()
    serializer_class = VggtArticleSerializer


class VggtVariableList(generics.ListCreateAPIView):
    queryset = VggtVariable.objects.all()
    serializer_class = VggtVariableSerializer


class VggtVariableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VggtVariable.objects.all()
    serializer_class = VggtVariableSerializer


class DealScoreList(generics.ListCreateAPIView):
    queryset = DealScore.objects.all()
    serializer_class = DealScoreSerializer
    permission_classes = [IsReporterOrHigherOrReadonly]

    def get_queryset(self):
        qs = self.queryset.prefetch_related(
            Prefetch(
                "deals",
                queryset=DealHull.objects.filter(
                    confidential=False, active_version__isnull=False
                ).prefetch_related(
                    Prefetch("versions", queryset=DealVersion.objects.order_by("-id"))
                ),
            )
        )
        return qs

    @extend_schema(parameters=openapi_filters_parameters_scoring)
    def get(self, request: Request, *args, **kwargs):
        return Response(
            self.get_queryset()
            .order_by("deal_id")
            .filter(parse_filters(request))
            .distinct()
            .values("deal")
            .annotate(
                id=F("deal"),
                ## Filters
                region_id=F("deal__country__region_id"),
                country=JSONObject(id="deal__country__id", name="deal__country__name"),
                deal_size=F("deal__active_version__deal_size"),
                negotiation_status=F(
                    "deal__active_version__current_negotiation_status"
                ),
                nature_of_deal=F("deal__active_version__nature_of_deal"),
                operating_company=Case(
                    When(
                        deal__active_version__operating_company__active_version=None,
                        then=None,
                    ),
                    default=JSONObject(
                        id=F("deal__active_version__operating_company_id"),
                        name=F(
                            "deal__active_version__operating_company__active_version__name"
                        ),
                    ),
                ),
                initiation_year=F("deal__active_version__initiation_year"),
                # involved_actors= TODO: add when needed, excluded for now, Pydantic field
                implementation_status=F("deal__active_version__implementation_status"),
                intention_of_investment=F(
                    "deal__active_version__current_intention_of_investment"
                ),
                crops=F("deal__active_version__current_crops"),
                animals=F("deal__active_version__current_animals"),
                minerals=F("deal__active_version__current_mineral_resources"),
                transnational=F("deal__active_version__transnational"),
                forest_concession=F("deal__active_version__forest_concession"),
                ## VGGTs Scoring information
                recognition_status=F("deal__active_version__recognition_status"),
                recognition_status_comment=F(
                    "deal__active_version__recognition_status_comment"
                ),
                displacement_of_people=F(
                    "deal__active_version__displacement_of_people"
                ),
                displaced_people=F("deal__active_version__displaced_people"),
                displaced_households=F("deal__active_version__displaced_households"),
                displaced_people_from_community_land=F(
                    "deal__active_version__displaced_people_from_community_land"
                ),
                displaced_people_within_community_land=F(
                    "deal__active_version__displaced_people_within_community_land"
                ),
                displaced_households_from_fields=F(
                    "deal__active_version__displaced_households_from_fields"
                ),
                displaced_people_on_completion=F(
                    "deal__active_version__displaced_people_on_completion"
                ),
                displacement_of_people_comment=F(
                    "deal__active_version__displacement_of_people_comment"
                ),
                promised_compensation=F("deal__active_version__promised_compensation"),
                received_compensation=F("deal__active_version__received_compensation"),
                community_consultation=F(
                    "deal__active_version__community_consultation"
                ),
                community_consultation_comment=F(
                    "deal__active_version__community_consultation_comment"
                ),
                land_conflicts=F("deal__active_version__land_conflicts"),
                land_conflicts_comment=F(
                    "deal__active_version__land_conflicts_comment"
                ),
                negative_impacts=F("deal__active_version__negative_impacts"),
                negative_impacts_comment=F(
                    "deal__active_version__negative_impacts_comment"
                ),
                materialized_benefits=F("deal__active_version__materialized_benefits"),
                materialized_benefits_comment=F(
                    "deal__active_version__materialized_benefits_comment"
                ),
                contract_farming=F("deal__active_version__contract_farming"),
                contract_farming_comment=F(
                    "deal__active_version__contract_farming_comment"
                ),
                promised_benefits=F("deal__active_version__promised_benefits"),
                promised_benefits_comment=F(
                    "deal__active_version__promised_benefits_comment"
                ),
                water_extraction_envisaged=F(
                    "deal__active_version__water_extraction_envisaged"
                ),
                water_extraction_envisaged_comment=F(
                    "deal__active_version__water_extraction_envisaged_comment"
                ),
                source_of_water_extraction=F(
                    "deal__active_version__source_of_water_extraction"
                ),
                community_reaction=F("deal__active_version__community_reaction"),
                community_reaction_comment=F(
                    "deal__active_version__community_reaction_comment"
                ),
                gender_related_information=F(
                    "deal__active_version__gender_related_information"
                ),
                purchase_price=F("deal__active_version__purchase_price"),
                purchase_price_area=F("deal__active_version__purchase_price_area"),
                purchase_price_currency=F(
                    "deal__active_version__purchase_price_currency"
                ),
                purchase_price_comment=F(
                    "deal__active_version__purchase_price_comment"
                ),
                annual_leasing_fee=F("deal__active_version__annual_leasing_fee"),
                annual_leasing_fee_currency=F(
                    "deal__active_version__annual_leasing_fee_currency"
                ),
                annual_leasing_fee_comment=F(
                    "deal__active_version__annual_leasing_fee_comment"
                ),
                presence_of_organizations=F(
                    "deal__active_version__presence_of_organizations"
                ),
                ## VGGTs Scores
                score=JSONObject(
                    deal_version=F("deal__active_version"),
                    status=F("deal__active_version__accountability_score__status"),
                    variables=(
                        ArraySubquery(
                            DealVariable.objects.filter(
                                deal_score=OuterRef(
                                    "deal__active_version__accountability_score"
                                )
                            ).values(
                                json=JSONObject(
                                    vggt_variable=F("vggt_variable"),
                                    status=F("status"),
                                    score=F("score"),
                                    scored_at=F("scored_at"),
                                    scored_by=F("scored_by"),
                                    assignee=F("assignee"),
                                )
                            )
                        )
                    ),
                ),
            )
        )

    # def get(self, request: Request, *args, **kwargs):
    #     queryset = (
    #         DealScore.objects.prefetch_related("deal")
    #         .filter(deal__confidential=False)
    #         .exclude(deal__active_version__isnull=True)
    #         .filter(parse_filters(request))
    #         .distinct()
    #         .annotate(
    #             country=JSONObject(id="deal__country__id", name="deal__country__name"),
    #             operating_company=JSONObject(
    #                 id="deal__active_version__operating_company__active_version__id",
    #                 name="deal__active_version__operating_company__active_version__name",
    #             ),
    #         )
    #     )
    #     serializer = DealScoreSerializer(queryset, many=True)
    #     return Response(serializer.data)


class DealScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealScore.objects.all()
    serializer_class = DealScoreSerializer
    permission_classes = [IsReporterOrHigherOrReadonly]


class DealScoreVersionList(generics.ListCreateAPIView):
    queryset = DealScoreVersion.objects.all()
    serializer_class = DealScoreVersionSerializer
    permission_classes = [IsReporterOrHigherOrReadonly]


class DealScoreVersionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealScoreVersion.objects.all()
    serializer_class = DealScoreVersionSerializer
    permission_classes = [IsReporterOrHigherOrReadonly]


class DealVariableList(generics.ListCreateAPIView):
    queryset = DealVariable.objects.all()
    serializer_class = DealVariableSerializer
    permission_classes = [IsReporterOrHigherOrReadonly]


# class DealVariableList(generics.ListCreateAPIView):
#     queryset = DealVariable.objects.all()
#     serializer_class = DealVariableSerializer
#     permission_classes = [IsReporterOrHigherOrReadonly]

#     @extend_schema(parameters=[
#         OpenApiParameter(name="deal", type="int", many=True),
#         OpenApiParameter(name="number", type="int", many=True)
#     ])
#     def get(self, request:Request, *args, **kwargs):
#         filters = Q()
#         if deal_list := request.GET.getlist("deal"):
#             filters &= Q()


# class DealVariableDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = DealVariable.objects.all()
#     serializer_class = DealVariableSerializer
#     permission_classes = [IsReporterOrHigherOrReadonly]


class DealVariableView(APIView):
    queryset = DealVariable.objects.all()
    serializer_class = DealVariableSerializer
    permission_classes = [IsReporterOrHigherOrReadonly]

    def get_queryset(self):
        deal_id = self.kwargs["deal"]
        vggt_variable_number = self.kwargs["variable"]
        deal = DealHull.objects.get(pk=deal_id)
        return DealVariable.objects.get(
            deal_score__deal_version=deal.active_version,
            vggt_variable__number=vggt_variable_number,
        )

    def get(self, request, deal, variable, format=None):
        queryset = self.get_queryset()
        serializer = DealVariableSerializer(queryset)
        return Response(serializer.data)

    def patch(self, request, deal, variable, format=None):
        queryset = self.get_queryset()
        serializer = DealVariableSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DealBulkAssigneeUpdate(APIView):
    queryset = DealVariable.objects.all()
    serializer_class = DealVariableSerializer
    permission_classes = [IsReporterOrHigher]

    def patch(self, request):
        to_update = request.data.get("to_update")
        assigneeID = request.data.get("assignee")

        for e in to_update:
            # Not sure if I can optimize this current_score + variable query with the method current_score()
            current_score = DealScore.objects.get(deal=e["deal"]).current_score()
            variable = DealVariable.objects.get(
                deal_score=current_score,
                vggt_variable__number=e["variable"],
            )
            serializer = DealVariableSerializer(
                instance=variable, data={"assignee": assigneeID}, partial=True
            )
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsReporterOrHigherOrReadonly]

    @extend_schema(parameters=[OpenApiParameter(name="id", type=int, many=True)])
    def get(self, request: Request, *args, **kwargs):
        filters = Q()
        if id_list := request.GET.getlist("id"):
            filters &= Q(id__in=id_list)
        queryset = Project.objects.filter(filters).order_by("-created_at").distinct()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrEditorOrReadonly]

    def perform_update(self, serializer):
        serializer.save(modified_at=timezone.now(), modified_by=self.request.user)


class UserProjects(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsReporterOrHigher]

    def get_queryset(self):
        # Return a list of all projects related by the user (owned or can edit)
        user = self.request.user
        if not user.is_anonymous:
            return Project.objects.filter(
                Q(owner=user) | Q(editors__id=user.id)
            ).distinct()


class BookmarkedProjects(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsReporterOrHigher]

    def get_queryset(self):
        # Return a list of all projects bookmarked by the user
        user = self.request.user

        if not user.is_anonymous:
            bookmarks = Bookmark.objects.filter(user=self.request.user).order_by(
                "order"
            )
            res = []
            # Retrieve projects in the "bookmark.order" order
            ids = bookmarks.values_list("project", flat=True)
            for id in ids:
                proj = Project.objects.get(pk=id)
                res.append(proj)
            return res


class BookmarkList(APIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsReporterOrHigher]

    def get_queryset(self):
        user = self.request.user
        if not user.is_anonymous:
            return Bookmark.objects.filter(user=user).order_by("order")

    def get_object(self, user, project):
        try:
            return Bookmark.objects.get(Q(user=user) & Q(project=project))
        except Bookmark.DoesNotExist():
            raise status.HTTP_400_BAD_REQUEST

    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer = BookmarkSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=BookmarkSerializer(many=True))
    def put(self, request, format=None):
        for item in request.data:
            bookmark = self.get_object(user=self.request.user, project=item["project"])
            data = {"order": item["order"]}
            serializer = BookmarkSerializer(instance=bookmark, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsReporterOrHigher, IsUser]

    def get_queryset(self):
        # Return a list of bookmarks for the currently logged in user
        user = self.request.user
        if not user.is_anonymous:
            return Bookmark.objects.filter(user=user)
