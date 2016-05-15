class FakeQuerySetMixin:
    '''
    Mixin to handle passing requests to fake query sets.
    '''

    fake_queryset_class = None

    def get_queryset(self):
        queryset_class = self.fake_queryset_class
        queryset = queryset_class(self.request)

        return queryset.all()
