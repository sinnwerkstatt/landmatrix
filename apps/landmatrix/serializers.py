from rest_framework import serializers

from apps.landmatrix.models import FieldDefinition
from apps.landmatrix.models.country import Country, Region
from apps.landmatrix.models.currency import Currency


class FieldDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldDefinition
        fields = "__all__"


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "code", "name", "symbol"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "high_income", "code_alpha2", "deals"]
        # fields = ["id", "name", "region", "high_income", "slug", "code_alpha2"]

        #   //           id
        #   //           name
        #   //           code_alpha2
        #   //           slug
        #   //           point_lat
        #   //           point_lon
        #   //           point_lat_min
        #   //           point_lon_min
        #   //           point_lat_max
        #   //           point_lon_max
        #   //           observatory_page_id
        #   //           high_income
        #   //           deals {
        #   //             id
        #   //           }


class RegionSerializer(serializers.Serializer):
    class Meta:
        model = Region
        fields = ["id", "name", "observatory_page_id"]

        #   //           id
        #   //           name
        #   //           slug
        #   //           point_lat_min
        #   //           point_lon_min
        #   //           point_lat_max
        #   //           point_lon_max
        #   //           observatory_page_id
