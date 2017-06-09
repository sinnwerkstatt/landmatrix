from django.http import Http404
from rest_framework.generics import RetrieveAPIView

from landmatrix.models import Activity
from api.serializers import DealDetailSerializer


class DealDetailView(RetrieveAPIView):
    '''
    This view returns all attributes related to a deal.
    '''
    serializer_class = DealDetailSerializer
    lookup_field = 'activity_identifier'

    def get_queryset(self):
        if self.request.user.is_authenticated() and self.request.user.is_staff:
            queryset = Activity.objects.all()
        else:
            queryset = Activity.objects.public(user)

        return queryset

    def get_object(self):
        '''
        Handle our DB weirdness where there are often multiple versions -
        just use the latest public one.

        TODO: this could be removed if we add a 'latest' activity queryset.
        '''
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        obj = queryset.filter(**filter_kwargs).order_by('-id').first()
        if obj is None:
            raise Http404

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
