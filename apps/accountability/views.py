from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from rest_framework import viewsets, generics
from rest_framework.request import Request
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from apps.accountability.models import VggtChapter, VggtArticle, VggtVariable
from apps.accountability.models import DealScore, DealVariable

from apps.accountability.serializers import VggtChapterSerializer, VggtArticleSerializer, VggtVariableSerializer
from apps.accountability.serializers import DealScoreSerializer, DealVariableSerializer

from apps.accountability.utils import openapi_filters_parameters_scoring, parse_filters


# Tmp root view
def index(request):
    return HttpResponse("Hello world, this is accountability.")

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

    # def get_queryset(self):
    #     return super().get_queryset()

    @extend_schema(parameters=openapi_filters_parameters_scoring)
    def list(self, request:Request, *args, **kwargs):
        queryset = DealScore.objects.exclude(deal__active_version__is_public=False).filter(parse_filters(request)).order_by("deal").distinct()
        serializer = DealScoreSerializer(queryset, many=True)
        return Response(serializer.data)
        # return Response(
        #     self.get_queryset()
        #     .order_by("deal")
        #     .values("deal")
        # )


class DealScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealScore.objects.all()
    serializer_class = DealScoreSerializer


class DealVariableList(generics.ListCreateAPIView):
    queryset = DealVariable.objects.all()
    serializer_class = DealVariableSerializer

class DealVariableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealVariable.objects.all()
    serializer_class = DealVariableSerializer