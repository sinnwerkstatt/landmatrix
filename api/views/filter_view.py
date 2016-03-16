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

        if request.user not in self.filters:
            self.filters[request.user] = {}

        stored_filters = request.session.get('filters', {})
        if action.lower() == 'set':
            new_filter = Filter(values['variable'], values['operator'], values['value'], values.get('name'))
            stored_filters[new_filter.name] = new_filter
            request.session['filters'] = stored_filters
            self.filters[request.user] = stored_filters
            # print('FilterView.dispatch', self.filters)
        elif action.lower() == 'remove':
            name = values.get('name').pop()
            # print('FilterView.dispatch', stored_filters)
            # print('FilterView.dispatch', name)
            stored_filters.pop(name, None)
            request.session['filters'] = stored_filters
            self.filters[request.user] = stored_filters
        return HttpResponse(json.dumps(stored_filters))

