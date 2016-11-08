from collections import OrderedDict

from rest_framework.pagination import BasePagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param, remove_query_param


class FakeQuerySetPagination(BasePagination):
    '''
    Handle pagination for fake querysets. This only seems to work with deals...

    Note that unlike django pagination, we don't check if we are past the max
    number of pages, or return a count.
    '''
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    default_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        self.page_size = self.get_page_size(request)
        if not self.page_size:
            return None
        self.page_number = self.get_page_number(request)

        offset = (self.page_number - 1) * self.page_size
        queryset._set_limit('{},{}'.format(self.page_size, offset))

        self.request = request
        return list(queryset.all())

    def get_paginated_response(self, data):
        pagination = OrderedDict([
            ('next', self.get_next_link()),
        ])
        if self.page_number > 1:
            pagination['previous'] = self.get_previous_link()

        pagination['results'] = data

        return Response(pagination)

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return int(request.query_params[self.page_size_query_param])
            except (KeyError, ValueError, TypeError):
                pass

        return self.default_page_size

    def get_page_number(self, request):
        try:
            page_number = int(request.query_params.get(self.page_query_param))
        except (ValueError, TypeError):
            page_number = 1

        return page_number

    def get_next_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page_number + 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page_number - 1
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)
