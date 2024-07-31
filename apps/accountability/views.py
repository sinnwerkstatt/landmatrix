from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.db.models.functions import JSONObject
from django.utils import timezone

from rest_framework import viewsets, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.accountability.models import VggtChapter, VggtArticle, VggtVariable
from apps.accountability.models import DealScore, DealVariable, Project
from apps.accountability.models import UserInfo

from apps.accountability.serializers import VggtChapterSerializer, VggtArticleSerializer, VggtVariableSerializer
from apps.accountability.serializers import DealScoreSerializer, DealVariableSerializer, ProjectSerializer
from apps.accountability.serializers import UserInfoSerializer

from apps.accountability.utils import openapi_filters_parameters_scoring, parse_filters

from apps.accountability.permissions import IsAdministrator, IsReporterOrHigher, IsReporterOrHigherOrReadonly, IsOwnerOrEditorOrReadonly


# Tmp root view
def index(request):
    return HttpResponse("Hello world, this is accountability.")


class UserInfoList(generics.ListCreateAPIView):
    permission_classes = [IsReporterOrHigher]
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

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
    serializer_class = VggtArticleSerializer


class DealScoreList(viewsets.ModelViewSet):
    queryset = DealScore.objects.all()
    serializer_class = DealScoreSerializer

    @extend_schema(parameters=openapi_filters_parameters_scoring)
    def list(self, request:Request, *args, **kwargs):
        queryset = DealScore.objects.exclude(deal__active_version__is_public=False)\
                                    .filter(parse_filters(request))\
                                    .order_by("deal")\
                                    .distinct()
        serializer = DealScoreSerializer(queryset, many=True)
        return Response(serializer.data)


class DealScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealScore.objects.all()
    serializer_class = DealScoreSerializer


class DealVariableList(generics.ListCreateAPIView):
    queryset = DealVariable.objects.all()
    serializer_class = DealVariableSerializer

class DealVariableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealVariable.objects.all()
    serializer_class = DealVariableSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsReporterOrHigherOrReadonly]

    @extend_schema(parameters=[
        OpenApiParameter(name="id", type=int, many=True)
    ])
    def get(self, request:Request, *args, **kwargs):
        filters = Q()
        if id_list := request.GET.getlist("id"):
            filters &= Q(id__in=id_list)
        queryset = Project.objects.filter(filters)\
                                  .order_by("name")\
                                  .distinct()
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
            return Project.objects.filter(Q(owner=user) | Q(editors__id=user.id))


class BookmarkedProjects(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsReporterOrHigher]

    def get_queryset(self):
        # Return a list of all projects bookmarked by the user
        user = self.request.user

        if not user.is_anonymous:
            return UserInfo.objects.get(user=self.request.user).bookmarks