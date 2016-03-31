from landmatrix.models.filter_preset import FilterPreset

from django.http.response import HttpResponse
from django.views.generic.base import TemplateView

import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

def create_preset_table():

    groups = FilterPreset.objects.values_list().distinct()

    table = {}
    for item in groups:
        newitem = {
            'id': item[0],
            'label': item[2]
        }
        if item[1] not in table:
            table[item[1]] = [newitem]
        else:
            table[item[1]].append(newitem)
    return table

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




