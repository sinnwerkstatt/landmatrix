from django.db.models.functions import Lower
from rest_framework import permissions, viewsets

from apps.accounts.models import User
from apps.accounts.permissions import IsReporterOrHigher
from apps.accounts.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by(Lower("full_name"))
    permission_classes = [IsReporterOrHigher]
    serializer_class = UserSerializer
