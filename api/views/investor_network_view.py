from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema

from landmatrix.models.investor import HistoricalInvestor, InvestorBase
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

    def get_object(self):
        '''
        Returns an investor object.
        '''
        try:
            investor_id = int(
                self.request.query_params['operational_stakeholder'])
        except KeyError:
            raise serializers.ValidationError(
                {'operational_stakeholder': _("This field is required.")})
        except ValueError:
            raise serializers.ValidationError(
                {'operational_stakeholder': _("An integer is required.")})

        investor = get_object_or_404(HistoricalInvestor, pk=investor_id)
        if not self.request.user.is_authenticated():
            if investor.fk_status_id not in (InvestorBase.STATUS_ACTIVE, InvestorBase.STATUS_OVERWRITTEN):
                raise Http404("Investor is not public")
        self.check_object_permissions(self.request, investor)

        return investor

    def get(self, request, format=None):
        # TODO: determine what operational_stakeholder_diagram does here -
        # it seems to just be passed back in the response.
        operational_stakeholder = self.get_object()
        serialized_response = HistoricalInvestorNetworkSerializer(operational_stakeholder)
        #parent_type=request.query_params.get('parent_type', 'parent_stakeholders'))

        response_data = serialized_response.data.copy()
        #response_data['index'] = investor_diagram

        return Response(response_data)
