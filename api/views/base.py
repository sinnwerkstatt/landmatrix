'''
Abstract base classes for API views.
'''
from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.mixins import FakeQuerySetMixin
from api.serializers import PassThruSerializer


class FakeQuerySetListView(FakeQuerySetMixin, ListAPIView):
    '''
    Base view class that handles fake querysets (they return presentation
    ready data).
    '''
    serializer_class = PassThruSerializer


class FakeQuerySetRetrieveView(FakeQuerySetMixin, RetrieveAPIView):
    '''
    Base view class that handles fake querysets, but for cases where a
    single object is returned.
    '''
    serializer_class = PassThruSerializer

    def get_object(self):
        return self.get_queryset()  # Already a single object
