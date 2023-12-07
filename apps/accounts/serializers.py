from rest_framework import serializers

from apps.accounts.models import User
from apps.new_model.serializers import CountrySerializer, RegionSerializer


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "username",
            "role",
        ]


class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    region = RegionSerializer()

    class Meta:
        model = User
        fields = "__all__"
