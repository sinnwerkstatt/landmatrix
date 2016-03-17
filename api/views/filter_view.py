from django.http.response import HttpResponse
from django.views.generic.base import TemplateView

import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class Filter(dict):

    filter_number = 0

    def __init__(self, variable, operator, value, name=None):
        Filter.filter_number += 1
        super().__init__(
            {'name': name if name else 'filter_{}'.format(Filter.filter_number),
             'variable': variable, 'operator': operator, 'value': value}
        )

    @property
    def name(self):
        return self['name']


class FilterView(TemplateView):

    filters = {}

    def dispatch(self, request, *args, **kwargs):
        values = dict(request.GET)
        values.update(request.POST)
        action = values.pop('action', '')
        if isinstance(action, list):
            action = action.pop()

        unique_user = _get_unique_frontend_user(request)

        if unique_user is None:
            return

        if unique_user not in FilterView.filters:
            FilterView.filters[unique_user] = {}

        stored_filters = request.session.get('filters', {})
        if action.lower() == 'set':
            set_filter(stored_filters, values)
        elif action.lower() == 'remove':
            remove_filter(stored_filters, values)

        _update_stored_filters(request, stored_filters, unique_user)
        return HttpResponse(json.dumps(stored_filters))


def set_filter(stored_filters, filter_values):
    new_filter = Filter(
        filter_values['variable'], filter_values['operator'], filter_values['value'],
        filter_values.get('name', [None]).pop()
    )
    stored_filters[new_filter.name] = new_filter


def remove_filter(stored_filters, filter_values):
    name = filter_values.get('name').pop()
    stored_filters.pop(name, None)


def _update_stored_filters(request, stored_filters, unique_user):
    request.session['filters'] = stored_filters
    FilterView.filters[unique_user] = stored_filters


def _get_unique_frontend_user(request):
    if request.user.is_authenticated():
        return request.user.username
    if not request.COOKIES:
        request.session.set_test_cookie()
    return request.session.session_key

