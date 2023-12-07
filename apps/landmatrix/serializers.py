from rest_framework import serializers

from apps.landmatrix.models import FieldDefinition
from apps.landmatrix.models.country import Country
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
        fields = ["id", "name", "high_income", "code_alpha2"]
        # fields = ["id", "name", "region", "high_income", "slug", "code_alpha2"]
