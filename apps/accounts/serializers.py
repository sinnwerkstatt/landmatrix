from rest_framework import serializers

from apps.serializer import ReadOnlyModelSerializer

from .models import User
from ..landmatrix.permissions import is_editor_or_higher


class LeanUserSerializer(ReadOnlyModelSerializer):
    full_name = serializers.SerializerMethodField(allow_null=True)

    def get_full_name(self, obj) -> str | None:
        request = self.context.get("request")

        if request and is_editor_or_higher(request.user):
            return obj.full_name

        return None

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
    is_contexthelp_editor = serializers.SerializerMethodField()

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
            "is_contexthelp_editor",
        ]

    @staticmethod
    def get_is_contexthelp_editor(obj) -> bool:
        return obj.groups.filter(name="Context Help Editor").exists()
