from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry
from django.urls import reverse
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from landmatrix.models import Activity, HistoricalInvestorVentureInvolvement, FilterPreset
from landmatrix.models.investor import InvestorBase, HistoricalInvestor


class FilterPresetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterPreset
        exclude = ('is_default', 'overrides_default')


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'full_name')


class RegionSerializer(serializers.BaseSerializer):
    """
    Returns a region as a list: [id, slug, title].
    """
    def to_representation(self, obj):
        return [obj.region.id, obj.region.slug, obj.title]


class DealLocationSerializer(serializers.Serializer):
    point_lat = serializers.DecimalField(max_digits=11, decimal_places=8)
    point_lon = serializers.DecimalField(max_digits=11, decimal_places=8)
    contract_area = GeometryField()
    intended_area = GeometryField()
    production_area = GeometryField()

    def to_representation(self, obj):
        """
        Convert our binary polygon representation to a GEOSGeometry.
        """
        # TODO: DRY, we should have a model with a list of these fields
        for geo_field in ('contract_area', 'intended_area', 'production_area'):
            if geo_field in obj and obj[geo_field]:
                if not isinstance(obj[geo_field], GEOSGeometry):
                    obj[geo_field] = GEOSGeometry(obj[geo_field], srid=4326)

        return super().to_representation(obj)


class DealSerializer(serializers.Serializer):
    """
    Used to serialize the deal list view.
    """
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

        # For our intfields, we sometimes get unexpected floats. Round those.
        for field in ('contract_size', 'intended_size', 'production_size'):
            value = obj[field]
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = round(float(value))
                    except ValueError:
                        value = None
                obj[field] = value

        obj['locations'] = locations

        return super().to_representation(obj)


class DealDetailSerializer(serializers.ModelSerializer):
    """
    Returns deal attributes.
    """
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = (
            'activity_identifier', 'fk_status', 'is_public',
            'deal_scope', 'negotiation_status', 'implementation_status',
            'deal_size', 'attributes'
        )

    def get_attributes(self, obj):
        return obj.attributes_as_dict


class HistoricalInvestorNetworkSerializer(serializers.BaseSerializer):
    """
    This serializer takes an investor and outputs a list of involvements
    formatted like:
    {
        "id": 123,
        "name": "",
        "country": "",
        "classification": "",
        "homepage": "",
        "opencorporates_link": "",
        "comment": "",
        "stakeholders": [
            {
                "id": 345,
                "name": "",
                [...] 
                "involvement": [
                    "parent_type": "stakeholder" // or "investor"
                    "percentage": "",
                    "investment_type": "",
                    "loans_amount": "",
                    "loans_currency": "",
                    "loans_date": "",
                    "comment": "",
                ],
                "stakeholders": [],
            },
            [...]
        ],
    }
    This is not REST, but it maintains compatibility with the existing API.
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def to_representation(self, obj, parent_types=['parent_stakeholders', 'parent_investors']):
        response = {
            "id": obj.id,
            "name": obj.name,
            "status": obj.fk_status.name,
            "investor_identifier": obj.investor_identifier,
            "country": str(obj.fk_country),
            "classification": obj.get_classification_display(),
            "homepage": obj.homepage,
            "opencorporates_link": obj.opencorporates_link,
            "comment": obj.comment,
            "url": reverse("investor_detail", kwargs={"investor_id": obj.investor_identifier}),
            "stakeholders": [],
        }
        involvements = HistoricalInvestorVentureInvolvement.objects.filter(fk_venture=obj)
        if self.user and not self.user.is_authenticated:
            involvements = involvements.filter(fk_investor__fk_status_id__in=(
                InvestorBase.STATUS_ACTIVE,
                InvestorBase.STATUS_OVERWRITTEN
            ))
        for parent_type in parent_types:
            parents = []
            if parent_type == 'parent_investors':
                parent_involvements = involvements.investors()
            else:
                parent_involvements = involvements.stakeholders()
            for i, involvement in enumerate(parent_involvements):
                # Always get latest version of parent investor
                parent_investor = HistoricalInvestor.objects.filter(investor_identifier=involvement.fk_investor.investor_identifier)
                if self.user and not self.user.is_authenticated:
                    parent_investor = parent_investor.filter(fk_status_id__in=(
                        InvestorBase.STATUS_ACTIVE,
                        InvestorBase.STATUS_OVERWRITTEN
                    ))
                parent_investor = parent_investor.latest()
                parent = self.to_representation(parent_investor, parent_types)
                parent["type"] = parent_type == 'parent_investors' and 2 or 1
                parent["involvement"] = {
                    "percentage": involvement.percentage,
                    "investment_type": involvement.get_investment_type_display(),
                    "loans_amount": involvement.loans_amount,
                    "loans_currency": str(involvement.loans_currency),
                    "loans_date": involvement.loans_date,
                    "parent_relation": involvement.get_parent_relation_display(),
                    "comment": involvement.comment,
                }
                parents.append(parent)
            response['stakeholders'].extend(parents)

        return response
