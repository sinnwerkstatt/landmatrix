from django.http.response import HttpResponse
from django.views.generic.base import TemplateView

import json

from api.views.filter import Filter, PresetFilter

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FilterView(TemplateView):

    filters = {}

    def dispatch(self, request, *args, **kwargs):

        action, values = _extract_parameters(request)

        unique_user = _get_unique_frontend_user(request)

        if unique_user not in FilterView.filters:
            FilterView.filters[unique_user] = {}

        try:
            stored_filters = request.session.get('filters', {})
            if action.lower() == 'set':
                set_filter(stored_filters, values)
            elif action.lower() == 'remove':
                remove_filter(stored_filters, values)

            _update_stored_filters(request, stored_filters, unique_user)
            return HttpResponse(json.dumps(stored_filters))
        except ValueError as e:
            return HttpResponse(str(e), status=404)


def set_filter(stored_filters, filter_values):
    if 'preset' in filter_values:
        new_filter = PresetFilter(filter_values['preset'], filter_values.get('name', [None]).pop())
    else:
        new_filter = Filter(
            filter_values['variable'], filter_values['operator'], filter_values['value'],
            filter_values.get('name', [None]).pop()
        )
    stored_filters[new_filter.name] = new_filter


def remove_filter(stored_filters, filter_values):
    name = filter_values.get('name').pop()
    stored_filters.pop(name, None)


def _extract_parameters(request):
    values = dict(request.GET)
    values.update(request.POST)
    action = values.pop('action', '')
    if isinstance(action, list):
        action = action.pop()
    return action, values


def _update_stored_filters(request, stored_filters, unique_user):
    request.session['filters'] = stored_filters
    FilterView.filters[unique_user] = stored_filters


def _get_unique_frontend_user(request):
    if request.user.is_authenticated():
        return request.user.username
    if not request.COOKIES:
        request.session.set_test_cookie()
    return request.session.session_key

