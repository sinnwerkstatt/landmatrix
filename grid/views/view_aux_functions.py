from landmatrix.models.filter_condition import FILTER_VAR_ACT, FILTER_VAR_INV, get_filter_vars
from grid.views.browse_condition_form import BrowseConditionForm

from django.template import loader
from django.http import HttpResponse

import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def create_condition_formset():
    from django.forms.formsets import formset_factory
    from django.utils.functional import curry

    ConditionFormset = formset_factory(BrowseConditionForm, extra=0)
    ConditionFormset.form = staticmethod(
        curry(BrowseConditionForm, variables_activity=FILTER_VAR_ACT, variables_investor=FILTER_VAR_INV)
    )
    return ConditionFormset


def render_to_response(template_name, context, context_instance):
    """ Returns a HttpResponse whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments."""
    # Some deprecated arguments were passed - use the legacy code path
    return HttpResponse(render_to_string(template_name, context, context_instance))


def render_to_string(template_name, context, context_instance):
    return loader.render_to_string(template_name, context, context_instance)


def get_filter_name(filter_data):
    if filter_data[0] in FILTER_VAR_INV:
        return 'investor'
    return 'activity'


def get_filter_definition(filter_data):
    filter_data = filter_data[1]
    value = _parse_value(filter_data['value'])
    variable = filter_data['variable'][0]
    operator = filter_data['operator'][0]
    return {'{}__{}'.format(variable, operator): value}


def update_filters(filter_dict, filter):
    name = get_filter_name(filter)
    definition = get_filter_definition(filter)
    definition_key = list(definition.keys())[0]
    if filter_dict[name]['tags'].get(definition_key) and isinstance(filter_dict[name]['tags'][definition_key], list):
        filter_dict[name]['tags'][definition_key].extend(definition[definition_key])
    else:
        filter_dict[name]['tags'].update(definition)


def apply_filters_from_session(request, filter_dict):
    from api.views.filter import PresetFilter

    for filter in request.session.get('filters', {}).items():
        if 'variable' in filter[1]:
            update_filters(filter_dict, filter)
        elif 'preset_id' in filter[1]:
            preset = PresetFilter([filter[1]['preset_id']], filter[1].get('name'))
            for i, condition in enumerate(preset.filter.conditions()):
                update_filters(filter_dict, (filter[1].get('name')+'_{}'.format(i), condition))


def _parse_value(filter_value):
    if len(filter_value) > 1:
        return filter_value
    value = filter_value[0]
    if '[' in value:
        value = [str(v) for v in json.loads(value)]
    return value
