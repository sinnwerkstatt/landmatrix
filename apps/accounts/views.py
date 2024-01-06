import json

from django.db.models.functions import Lower
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.accounts import auth_flow
from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer, UserListSerializer
from apps.landmatrix.permissions import IsReporterOrHigher


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by(Lower("full_name"))

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserSerializer
        return UserListSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [AllowAny()]
        return [IsReporterOrHigher()]

    def retrieve(self, request, pk=None, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied()

        if request.user.is_staff and not pk == "me":
            user = get_object_or_404(self.queryset, pk=pk)
        else:
            user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


def register(request):
    data = json.loads(request.body)
    return JsonResponse(
        auth_flow.register(
            request,
            data["username"],
            data["first_name"],
            data["last_name"],
            data["email"],
            data["phone"],
            data["information"],
            data["password"],
            data["token"],
        )
    )


def register_confirm(request):
    data = json.loads(request.body)
    return JsonResponse(auth_flow.register_confirm(request, data["activation_key"]))


def login(request):
    data = json.loads(request.body)
    return JsonResponse(auth_flow.login(request, data["username"], data["password"]))


def logout(request):
    return JsonResponse(auth_flow.logout(request), safe=False)


def password_reset(request):
    data = json.loads(request.body)
    return JsonResponse(auth_flow.password_reset(data["email"], data["token"]))


def password_reset_confirm(request):
    data = json.loads(request.body)
    return JsonResponse(
        auth_flow.password_reset_confirm(
            data["uidb64"], data["token"], data["new_password1"], data["new_password2"]
        ),
        safe=False,
    )
