from django.shortcuts import redirect
from django.conf import settings
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

from landmatrix.models import Region, Country

import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

class DashboardFilterView(TemplateView):
    filters = {}

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        action = self.request.POST.get('action', 'clear')
        try:
            stored_filters = self.get_filters() if action.lower() == 'set' else {}
            DashboardFilterView.filters[self.request.user.username] = stored_filters
            self.request.session['dashboard_filters'] = stored_filters
            return HttpResponse(json.dumps(stored_filters))
        except ValueError as e:
            return HttpResponse(str(e), status=404)

    def get(self, *args, **kwargs):
        stored_filters = self.request.session['dashboard_filters']
        return HttpResponse(json.dumps(stored_filters))

    def get_filters(self):
        filters = {}
        data = self.request.POST
        if 'country' in data:
            country = Country.objects.get(pk=data.get('country'))
            if country:
                filters['country'] = [country.id,]
        elif 'region' in data:
            region = Region.objects.get(pk=data.get('region'))
            if region:
                filters['region'] = [region.id,]
        elif data.get('user'):
            user = User.objects.get(pk=data.get('user'))
            if user:
                filters['user'] = [user.id,]
        return filters
