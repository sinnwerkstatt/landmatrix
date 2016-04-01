from django.shortcuts import redirect
from django.conf import settings
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView

import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DashboardFilterView(TemplateView):

    filters = {}

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated():
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        action, values = _extract_parameters(request)

        unique_user = request.user.username

        try:
            stored_filters = get_filter(values) if action.lower() == 'set' else {}
            DashboardFilterView.filters[unique_user] = stored_filters
            request.session['dashboard_filters'] = stored_filters
            return HttpResponse(json.dumps(stored_filters))
        except ValueError as e:
            return HttpResponse(str(e), status=404)


def get_filter(filter_values):
    if filter_values.get('country'):
        return {'country': filter_values['country']}
    elif filter_values.get('region'):
        return {'region': filter_values['region']}
    else:
        raise ValueError('Neither country nor region in parameters: '+str(filter_values))


def _extract_parameters(request):
    values = dict(request.GET)
    values.update(request.POST)
    action = values.pop('action', '')
    if isinstance(action, list):
        action = action.pop()
    return action, values
