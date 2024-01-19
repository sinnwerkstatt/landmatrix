from rest_framework import serializers

from apps.accounts.models import User
from apps.landmatrix.serializers import RegionSerializer


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
    # country = CountryIDNameSerializer()
    country_id = serializers.PrimaryKeyRelatedField(read_only=True)
    region = RegionSerializer()

    class Meta:
        model = User
        fields = "__all__"
