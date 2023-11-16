from rest_framework import serializers

from apps.landmatrix.models.country import Country
from apps.new_model.models import (
    DealVersion2,
    DealHull,
    Location,
    DataSource,
    Contract,
    Area,
)


class DealVersionVersionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealVersion2
        fields = [
            "id",
            "created_at",
            "created_by_id",
            "sent_to_review_at",
            "sent_to_review_by_id",
            "reviewed_at",
            "reviewed_by_id",
            "activated_at",
            "activated_by_id",
            "fully_updated",
            "status",
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class LocationAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    areas = LocationAreaSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = "__all__"


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class DealVersionSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    contracts = ContractSerializer(many=True, read_only=True)
    datasources = DataSourceSerializer(many=True, read_only=True)

    class Meta:
        model = DealVersion2
        fields = "__all__"


class Deal2Serializer(serializers.ModelSerializer):
    country = CountrySerializer()
    versions = DealVersionVersionsListSerializer(many=True)
    selected_version = DealVersionSerializer()

    class Meta:
        model = DealHull
        fields = "__all__"
