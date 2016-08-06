from collections import OrderedDict

from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from landmatrix.models.filter_preset import FilterPreset
from landmatrix.models.investor import InvestorVentureInvolvement


class PassThruSerializer(serializers.BaseSerializer):
    '''
    Read only serializer that does nothing, just passed the JSON object
    we already have through.
    '''
    def to_representation(self, obj):
        return obj


class FilterPresetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterPreset
        exclude = ('is_default', 'overrides_default')


class UserSerializer(serializers.BaseSerializer):
    '''
    Returns a user as a list: [id, username, fullname].
    '''
    def to_representation(self, obj):
        return [obj.id, obj.username, obj.get_full_name() or obj.username]


class DealLocationSerializer(serializers.Serializer):
    point_lat = serializers.DecimalField(max_digits=11, decimal_places=8)
    point_lon = serializers.DecimalField(max_digits=11, decimal_places=8)
    intended_area = GeometryField()
    production_area = GeometryField()

    def to_representation(self, obj):
        '''
        Convert our binary polygon representation to a GEOSGeometry.
        '''
        for geo_field in ('intended_area', 'production_area'):
            if geo_field in obj and obj[geo_field]:
                if not isinstance(obj[geo_field], GEOSGeometry):
                    obj[geo_field] = GEOSGeometry(obj[geo_field], srid=4326)

        return super().to_representation(obj)


class DealSerializer(serializers.Serializer):
    '''
    Used to serialize the deal list view.
    '''
    deal_id = serializers.IntegerField()
    intention = serializers.CharField()
    intended_size = serializers.IntegerField()
    contract_size = serializers.IntegerField()
    production_size = serializers.IntegerField()
    investor = serializers.CharField()
    locations = serializers.ListField(child=DealLocationSerializer())

    def to_representation(self, obj):
        locations = []
        location_fields = self.fields['locations'].child.fields.keys()
        array_elements = [obj[field] for field in location_fields]
        split_elements = [elem.split(';') for elem in array_elements]

        for values in zip(*split_elements):
            location = {}
            for field_name, value in zip(location_fields, values):
                location[field_name] = value or None

            locations.append(location)

        obj['locations'] = locations

        return super().to_representation(obj)


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
    formatted like:
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
    {
        "operational_stakeholder": {
            "id": 123,
            "name": "",
            "fk_country": "",
            "classification": "",
            "parent_relation": "",
            "homepage": "",
            "opencorporates_link": "",
            "comment": "",
            "parent_stakeholders": [
                {
                    "id": 345,
                    "name": "",
                    [...]
                    "involvement": [
                        "percentage": "",
                        "investment_type": "",
                        "loans_amount": "",
                        "loans_currency": "",
                        "loans_date": "",
                        "comment": "",
                    ]
                },
                [...]
            ],
            "parent_investors": [
                [...]
            ]
        }
    }
    This is not REST, but it maintains compatibility with the existing API.
    '''

    def to_representation(self, obj, parent_types=['parent_stakeholders', 'parent_investors']):
        

        response = {}
        response["operational_stakeholder"] = {
            "id": obj.id,
            "name": obj.name,
            "fk_country": str(obj.fk_country),
            "classification": obj.get_classification_display(),
            "parent_relation": obj.get_parent_relation_display(),
            "homepage": obj.homepage,
            "opencorporates_link": obj.opencorporates_link,
            "comment": obj.comment,
        }
        involvements = InvestorVentureInvolvement.objects.filter(fk_venture=obj)
        for parent_type in parent_types:
            parents = []
            if parent_type == 'parent_investors':
                parent_involvements = involvements.investors()
            else:
                parent_involvements = involvements.stakeholders()
            for i, involvement in enumerate(parent_involvements):
                parent = involvement.fk_investor
                parents.append({
                    "id": parent.id,
                    "name": parent.name,
                    "fk_country": str(parent.fk_country),
                    "classification": parent.get_classification_display(),
                    "parent_relation": obj.get_parent_relation_display(),
                    "homepage": parent.homepage,
                    "opencorporates_link": parent.opencorporates_link,
                    "comment": parent.comment,
                    "involvement": {
                        "percentage": involvement.percentage,
                        "investment_type": involvement.investment_type,
                        "loans_amount": involvement.loans_amount,
                        "loans_currency": involvement.loans_currency,
                        "loans_date": involvement.loans_date,
                        "comment": involvement.comment,
                    }
                })
            response[parent_type] = parents

        return response


class NegotiationStatusSerializer(serializers.Serializer):
    name = serializers.CharField()
    deals = serializers.IntegerField()
    hectares = serializers.IntegerField()
