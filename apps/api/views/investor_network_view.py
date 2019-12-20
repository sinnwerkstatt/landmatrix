import coreapi
import coreschema
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView

from apps.api.serializers import (
    DealInvestorNetworkSerializer,
    InvestorNetworkSerializer,
)
from apps.landmatrix.models.investor import HistoricalInvestor


class DealInvestorNetworkView(APIView):
    """
    Get deal investor network.
    """

    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "investor_id",
                required=False,
                location="query",
                description="Investor ID",
                schema=coreschema.Integer(),
            ),
            coreapi.Field(
                "history_id",
                required=False,
                location="query",
                description="Investor version ID",
                schema=coreschema.Integer(),
            ),
        ]
    )
    serializer = DealInvestorNetworkSerializer

    def get_object(self):
        """
        Returns an investor object.
        """
        investor_id = self.request.GET.get("investor_id")
        history_id = self.request.GET.get("history_id")
        if history_id and not investor_id:
            investor_id = HistoricalInvestor.objects.get(
                id=history_id
            ).investor_identifier
        queryset = HistoricalInvestor.objects
        if not self.request.user.is_authenticated:
            queryset = queryset.public_or_deleted(self.request.user)
        try:
            investor = queryset.filter(investor_identifier=investor_id).latest()
        except ObjectDoesNotExist as e:
            raise Http404("Investor %s does not exist (%s)" % (investor_id, str(e)))

        # self.check_object_permissions(self.request, investor)

        return investor

    def get(self, request, format=None):
        # TODO: determine what operational_stakeholder_diagram does here -
        # it seems to just be passed back in the response.
        investor = self.get_object()
        serialized_response = self.serializer(investor, user=request.user)
        # parent_type=request.query_params.get('parent_type', 'parent_stakeholders'))

        response_data = serialized_response.data.copy()
        # response_data['index'] = investor_diagram

        return Response(response_data)


class InvestorNetworkView(DealInvestorNetworkView):
    """
    Get investor network.
    """

    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "investor_id",
                required=False,
                location="query",
                description="Investor ID",
                schema=coreschema.Integer(),
            ),
            coreapi.Field(
                "history_id",
                required=False,
                location="query",
                description="Investor version ID",
                schema=coreschema.Integer(),
            ),
            coreapi.Field(
                "depth",
                required=False,
                location="query",
                description="Depth",
                schema=coreschema.Integer(),
            ),
        ]
    )
    serializer = InvestorNetworkSerializer

    def get(self, request, format=None):
        investor = self.get_object()
        serializer = self.serializer(investor, user=request.user)
        depth = int(request.query_params.get("depth", "1"))
        show_deals = request.query_params.get("show_deals", "1") == "1"
        response_data = serializer.to_representation(
            investor, show_deals=show_deals, depth=depth
        )
        return Response(response_data)
