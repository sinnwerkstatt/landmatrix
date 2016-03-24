from landmatrix.models.filter_preset import FilterPreset

from django.http.response import HttpResponse
from django.views.generic.base import TemplateView

import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FilterPresetView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        values = request.GET
        if 'show_groups' in values:
            groups = FilterPreset.objects.values_list('group', flat=True).distinct()
            return HttpResponse(json.dumps(tuple(groups)))

        objects = FilterPreset.objects
        if 'group' in values:
            objects = objects.filter(group=values['group'])
        presets = objects.values('id', 'group', 'name')
        return HttpResponse(json.dumps(tuple(presets)))




