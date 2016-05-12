from collections import OrderedDict

from rest_framework import serializers

from landmatrix.models.investor import InvestorVentureInvolvement


class DealDetailSerializer(serializers.BaseSerializer):
    '''
    Limits deal attributes in the response to the attributes requested.
    '''

    def __init__(self, *args, **kwargs):
        self._requested_fields = kwargs.pop('fields', ())
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):
        obj_data = OrderedDict()

        for field_name in self._requested_fields:
            if field_name in obj.attributes.keys():
                obj_data[field_name] = str(obj.attributes[field_name])

        return obj_data


class InvestorNetworkSerializer(serializers.BaseSerializer):
    '''
    This serializer takes an investor and outputs a list of involvements
    formatted like so:
    {
        "nodes": [
            {"id": "stakeholders", "name": "Stakeholders"},
            {"id": "stakeholder_106406", "name": "Lao Thaihua Rubber Co"}
        ],
        "index": 4,
        "links": [
            {"source": 0, "target": 1, "value": 0.001}
        ]
    }
    This is not REST, but it maintains compatibility with the existing API.
    '''

    def to_representation(self, obj):
        '''
        TODO: split this up a bit, and use nested serializers.
        '''
        involvements = InvestorVentureInvolvement.objects.filter(
            fk_venture=obj)
        # TODO: these should be manager methods on involvements
        stakeholder_involvements = involvements.filter(role='ST')
        investor_involvements = involvements.filter(role='IN')

        nodes = []
        links = []

        # We are evaluating the queryset later anyways so don't bother with
        # .exists
        if bool(stakeholder_involvements):
            stakeholder_index = 0
            nodes.append({
                "name": "Stakeholders",
                "id": "stakeholders"
            })

        if bool(investor_involvements):
            investor_index = len(nodes)
            nodes.append({
                "name": "Investors",
                "id": "investors"
            })

        stakeholder_start_index = len(nodes)
        for involvement in stakeholder_involvements:
            nodes.append({
                'name': involvement.fk_investor.name,
                'id': 'stakeholder_{}'.format(involvement.fk_investor_id)
            })

        investor_start_index = len(nodes)
        for involvement in investor_involvements:
            nodes.append({
                'name': involvement.fk_investor.name,
                'id': 'investor_{}'.format(involvement.fk_investor_id)
            })

        for i, involvement in enumerate(stakeholder_involvements):
            links.append({
                'source': stakeholder_index,
                'target': stakeholder_start_index + i,
                'value': max(0.001, involvement.percentage)
            })

        for i, involvement in enumerate(investor_involvements):
            links.append({
                'source': investor_index,
                'target': investor_start_index + i,
                'value': max(0.001, involvement.percentage)
            })

        return {'nodes': nodes, 'links': links}
