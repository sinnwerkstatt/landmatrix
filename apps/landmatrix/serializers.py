from rest_framework import serializers

from apps.landmatrix.models import FieldDefinition
from apps.landmatrix.models.currency import Currency


class FieldDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldDefinition
        fields = "__all__"


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "code", "name", "symbol"]
