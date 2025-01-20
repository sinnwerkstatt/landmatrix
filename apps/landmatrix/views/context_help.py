from rest_framework import viewsets

from apps.landmatrix.models.context_help import ContextHelp
from apps.landmatrix.serializers import ContextHelpSerializer


class ContextHelpViewSet(viewsets.ModelViewSet):
    queryset = ContextHelp.objects.all()
    serializer_class = ContextHelpSerializer
