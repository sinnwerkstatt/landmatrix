import json

from django.db.models.functions import Lower
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts import auth_flow
from apps.accounts.models import User
from apps.accounts.serializers import LeanUserSerializer, UserSerializer
from apps.landmatrix.permissions import IsReporterOrHigher, is_admin

# unused, but maybe helpful
# def has_authorization_for_country(user: User, country: Country | int) -> bool:
#     if isinstance(country, int):
#         country = Country.objects.get(id=country)
#
#     if is_admin(user):
#         return True
#
#     if is_editor_or_higher(user):
#         if country == user.country:
#             return True
#         if user.region.country == country:
#             return True
#
#     return False


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserSerializer
        return LeanUserSerializer

    def get_queryset(self):
        return self.queryset.order_by(Lower("full_name"))

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsAuthenticated()]
        return [IsReporterOrHigher()]

    def retrieve(self, request, pk=None, *args, **kwargs):
        if is_admin(request.user) and not pk == "me":
            user = get_object_or_404(self.queryset, pk=pk)
        else:
            user = request.user

        serializer = self.get_serializer(user)
        return Response(serializer.data)


@extend_schema()
@api_view(["POST"])
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
