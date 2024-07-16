from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics
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


class DealScoreList(generics.ListCreateAPIView):
    queryset = DealScore.objects.all()
    serializer_class = DealScoreSerializer

class DealScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealScore.objects.all()
    serializer_class = DealScoreSerializer


class DealVariableList(generics.ListCreateAPIView):
    queryset = DealVariable.objects.all()
    serializer_class = DealVariableSerializer

class DealVariableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DealVariable.objects.all()
    serializer_class = DealVariableSerializer