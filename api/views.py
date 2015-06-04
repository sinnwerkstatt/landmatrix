__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.shortcuts import render
from landmatrix.models import Involvement
from rest_framework import viewsets
from api.serializers import InvolvementSerializer
from django.http import HttpResponse

class InvolvementViewSet(viewsets.ModelViewSet):
    queryset = Involvement.objects.all()
    serializer_class = InvolvementSerializer
