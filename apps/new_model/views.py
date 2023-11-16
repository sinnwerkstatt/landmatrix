from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.new_model.models import DealHull, InvestorHull, DealVersion2, InvestorVersion2
from apps.new_model.serializers import Deal2Serializer, Investor2Serializer


class Deal2ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DealHull.objects.all().prefetch_related(
        Prefetch("versions", queryset=DealVersion2.objects.order_by("-id"))
    )
    serializer_class = Deal2Serializer

    @action(
        name="Deal Instance",
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
