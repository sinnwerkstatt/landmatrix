from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from landmatrix.models.investor import Investor
from api.serializers import InvestorNetworkSerializer

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class InvestorNetworkView(APIView):

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

        investor = get_object_or_404(Investor, pk=investor_id)
        self.check_object_permissions(self.request, investor)

        return investor

    def get(self, request, format=None):
        '''
        TODO: determine what operational_stakeholder_diagram does here -
        it seems to just be passed back in the response.
        '''
        operational_stakeholder = self.get_object()
        serialized_response = InvestorNetworkSerializer(operational_stakeholder)
        #parent_type=request.query_params.get('parent_type', 'parent_stakeholders'))

        response_data = serialized_response.data.copy()
        #response_data['index'] = investor_diagram

        return Response(response_data)
