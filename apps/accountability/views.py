from django.utils import timezone
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.db.models import Q, F, Prefetch
from django.db.models.functions import JSONObject
from django.contrib.postgres.expressions import ArraySubquery

from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer

from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.landmatrix.models.deal import DealHull

from apps.accountability.models import VggtChapter, VggtArticle, VggtVariable
from apps.accountability.models import DealScore, DealScoreVersion, DealVariable
from apps.accountability.models import Project
from apps.accountability.models import UserInfo, Bookmark

from apps.accountability.serializers import (
    VggtChapterSerializer,
    VggtArticleSerializer,
    VggtVariableSerializer,
)
from apps.accountability.serializers import (
    DealScoreSerializer,
    DealScoreVersionSerializer,
    DealVariableSerializer,
)
from apps.accountability.serializers import ProjectSerializer
from apps.accountability.serializers import (
    UserInfoSerializer,
    BookmarkSerializer,
    BookmarkBulkSerializer,
)

from apps.accountability.utils import openapi_filters_parameters_scoring, parse_filters

from apps.accountability.permissions import (
    IsAdministrator,
    IsReporterOrHigher,
    IsReporterOrHigherOrReadonly,
    IsOwnerOrEditorOrReadonly,
    IsUser,
)


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

    @extend_schema(parameters=openapi_filters_parameters_scoring)
    def get(self, request: Request, *args, **kwargs):
        queryset = (
            DealScore.objects.prefetch_related("deal")
            .filter(deal__confidential=False)
            .exclude(deal__active_version__isnull=True)
            .filter(parse_filters(request))
            .distinct()
            .annotate(
                country=JSONObject(id="deal__country__id", name="deal__country__name"),
                operating_company=JSONObject(
                    id="deal__active_version__operating_company__active_version__id",
                    name="deal__active_version__operating_company__active_version__name",
                ),
            )
        )
        serializer = DealScoreSerializer(queryset, many=True)
        return Response(serializer.data)


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
        return DealVariable.objects.get(
            deal_score__score__deal__pk=deal_id,
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
            variable = DealVariable.objects.get(
                deal_score__score__deal__pk=e["deal"],
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
