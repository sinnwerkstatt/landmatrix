from apps.serializer import ReadOnlyModelSerializer

from .models import User


class LeanUserSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "username",
            "role",
            "is_active",
        ]


class UserSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "information",
            "country",
            "region",
            "role",
            "is_superuser",
            "is_staff",
            "is_active",
        ]
