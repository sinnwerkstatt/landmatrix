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

    @extend_schema(
        parameters=[OpenApiParameter(
            name="country_id",
            description="Filter by country",
            required=False,
            type=int,
            many=True,
            )]
        )
    def list(self, request:Request, *args, **kwargs):
        ret = Q()
        if request.GET.get("country_id"):
            ret &= Q(deal__country_id__in=request.GET.getlist("country_id"))

        queryset = DealScore.objects.filter(ret)
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