from rest_framework import serializers

from apps.landmatrix.models import FieldDefinition


class FieldDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldDefinition
        fields = "__all__"
