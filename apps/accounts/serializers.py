from rest_framework import serializers

from apps.accounts.models import User


class LeanUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "username", "role"]


class UserSerializer(serializers.ModelSerializer):
    country_id = serializers.PrimaryKeyRelatedField(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        # fields = "__all__"
        exclude = [
            "password",
            "groups",
            "region",
            "country",
            "user_permissions",
            "email_confirmed",
        ]
