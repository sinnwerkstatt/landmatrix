from django.shortcuts import render
from landmatrix.models import Involvement
from rest_framework import viewsets
from api.serializers import InvolvementSerializer
from django.http import HttpResponse

def index(request):
    return HttpResponse('ohai')

class InvolvementViewSet(viewsets.ModelViewSet):
    queryset = Involvement.objects.all()
    serializer_class = InvolvementSerializer
