from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema

from landmatrix.models.investor import HistoricalInvestor, InvestorBase, Investor
from api.serializers import HistoricalInvestorNetworkSerializer


class InvestorNetworkView(APIView):
    """
    Get investor network.
    Used within charts section.
    """
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "operational_stakeholder",
                required=True,
                location="query",
                description="Operating company ID",
                schema=coreschema.Integer(),
            ),
        ]
    )

    def _get_public_investor(self):
        # TODO: Cache result for user
        return Investor.objects.filter(investor_identifier=self.kwargs.get('investor_id')).first()

    def get_object(self):
        """
        Returns an investor object.
        """
        investor_id = self.request.GET.get('investor_id')
        history_id = self.request.GET.get('history_id')
        queryset = HistoricalInvestor.objects
        if not self.request.user.is_authenticated:
            i = self._get_public_investor()
            if not i:
                raise Http404('Investor %s is not public' % investor_id)
            queryset = queryset.public_or_deleted(self.request.user)
        try:
            if history_id:
                investor = queryset.get(id=history_id)
            else:
                investor = queryset.filter(investor_identifier=investor_id).latest()
        except ObjectDoesNotExist as e:
            raise Http404('Investor %s does not exist (%s)' % (investor_id, str(e)))

        #self.check_object_permissions(self.request, investor)

        return investor

    def get(self, request, format=None):
        # TODO: determine what operational_stakeholder_diagram does here -
        # it seems to just be passed back in the response.
        investor = self.get_object()
        serialized_response = HistoricalInvestorNetworkSerializer(investor, user=request.user)
        #parent_type=request.query_params.get('parent_type', 'parent_stakeholders'))

        response_data = serialized_response.data.copy()
        #response_data['index'] = investor_diagram

        return Response(response_data)
