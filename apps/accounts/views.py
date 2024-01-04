from django.db.models.functions import Lower
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.accounts.models import User
from apps.landmatrix.permissions import IsReporterOrHigher
from apps.accounts.serializers import UserSerializer, UserListSerializer


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
