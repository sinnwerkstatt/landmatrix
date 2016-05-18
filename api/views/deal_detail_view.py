from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from landmatrix.models.deal import Deal
from api.serializers import DealDetailSerializer


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealDetailView(APIView):
    '''
    This view takes a get request with a deal_id and list of attributes
    and returns those attributes for the deal given.

    E.g.:
    GET /api/deal?deal_id=1&attributes=foo&attributes=bar
    {"foo":"FOO","bar":"BAR"}

    This is not REST, but it maintains compatibility with the existing API.
    '''

    def get_object(self):
        try:
            deal = Deal(int(self.request.query_params['deal_id']))
        except KeyError:
            raise serializers.ValidationError(
                {'deal_id': _("This field is required.")})
        except ValueError:
            raise serializers.ValidationError(
                {'deal_id': _("An integer is required.")})
        except ObjectDoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, deal)

        return deal

    def get(self, request, format=None):
        deal = self.get_object()

        attributes = request.query_params.getlist('attributes', [])
        serialized_deal = DealDetailSerializer(deal, fields=attributes)

        return Response(serialized_deal.data)
