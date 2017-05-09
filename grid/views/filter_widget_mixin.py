from pprint import pprint
from time import time
from collections import OrderedDict

from django.db import connection
from django.utils.datastructures import MultiValueDict
from django.http import Http404
from django.utils.translation import ugettext as _

from .profiling_decorators import print_execution_time_and_num_queries
from landmatrix.models.browse_condition import BrowseCondition
from landmatrix.models.filter_preset import FilterPreset, FilterPresetGroup
from api.filters import Filter, PresetFilter
from grid.fields import TitleField
from grid.forms.browse_condition_form import ConditionFormset
from grid.views.save_deal_view import SaveDealView
from grid.views.browse_filter_conditions import BrowseFilterConditions
from api.serializers import FilterPresetSerializer
from landmatrix.models.country import Country
from landmatrix.models.region import Region




def get_variable_table():
    '''
    Create an OrderedDict of group name keys with lists of dicts for each
    variable in the group (each dict contains 'name' and 'label' keys).

    This whole thing is static, and maybe should just be written out, but
    for now generate it dynamcially on app load.
    '''
    # for formsets, we want form.form
    deal_forms = [
        form.form if hasattr(form, 'form') else form
        for form in SaveDealView.FORMS
    ]
    variable_table = OrderedDict()
    group_items = []
    group_title = ''

    # Add an ID filter
    variable_table[_('Deal ID')] = [{
        'name': 'activity_identifier',
        'label': _("Deal ID"),
    }]

    for form in deal_forms:
        for field_name, field in form.base_fields.items():
            if isinstance(field, TitleField):
                if group_title and group_items:
                    variable_table[group_title] = group_items
                    group_items = []
                group_title = str(field.initial)
            else:
                group_items.append({
                    'name': field_name,
                    'label': field.label,
                })

    if group_title and group_items:
        variable_table[group_title] = group_items

    # TODO: this is fragile, rethink this whole mess
    if _('Operational company') in variable_table:
        stakeholder_extras = [
            {
                'name': 'operational_company_country',
                'label': _(
                    "Operational company country of registration/origin"),
            },
            {
                'name': 'operational_company_region',
                'label': _(
                    "Operational company region of registration/origin"),
            },
            {
                'name': 'operational_company_classification',
                'label': _("Operational company classification"),
            },
            {
                'name': 'operational_company_homepage',
                'label': _("Operational company homepage"),
            },
            {
                'name': 'operational_company_opencorporates_link',
                'label': _("Operational company Opencorporates link"),
            },
            {
                'name': 'operational_company_comment',
                'label': _("Additional comment on Operational company"),
            },
        ]
        variable_table[_('Operational company')].extend(stakeholder_extras)

    return variable_table


class FilterWidgetMixin:
    variable_table = get_variable_table()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: not sure rules is still used - check this and remove
        self.rules = []

    @property
    def filters(self):
        return self.get_filter_context(self.current_formset_conditions)

    @property
    def current_formset_conditions(self):
        data = self.request.GET.copy()
        filter_set = self._filter_set(data)
        conditions_formset = self.get_formset_conditions(filter_set, data)

        return conditions_formset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        set_default_filters = True
        if 'set_default_filters' in self.request.session and not self.request.session.get('set_default_filters'):
            set_default_filters = False
        context.update({
            'filters': self.filters,
            'empty_form_conditions': self.current_formset_conditions,
            'rules': self.rules,
            'variables': self.variable_table,
            'presets': FilterPresetGroup.objects.all(),
            'set_default_filters': set_default_filters,
            'status': self.status,
        })

        return context

    def get_filter_context(
            self, formset_conditions, order_by=None, group_by=None,
            group_value=None, starts_with=None):
        filters = BrowseFilterConditions(formset_conditions, [], 0).parse()

        filters['order_by'] = order_by # required for table group view
        filters['group_by'] = group_by
        filters['group_value'] = group_value
        filters['starts_with'] = starts_with

        return filters

    def set_country_region_filter(self, data):
        filter_values = {}
        # Country or region filter set?
        if data.get('country', None) or data.get('region', None):
            stored_filters = self.request.session.get('filters', {})
            if not stored_filters:
                stored_filters = {}
            if data.get('country', None):
                filter_values['variable'] = 'target_country'
                filter_values['operator'] = 'is'
                filter_values['value'] = data.get('country')
                try:
                    country = Country.objects.defer('geom').get(pk=data.get('country'))
                    filter_values['display_value'] = country.name
                except:
                    pass
                filter_values['name'] = 'country'
                filter_values['label'] = _('Target country')
                data.pop('country')
            elif data.get('region', None):
                filter_values['variable'] = 'target_region'
                filter_values['operator'] = 'is'
                filter_values['value'] = data.get('region')
                try:
                    region = Region.objects.get(pk=data.get('region'))
                    filter_values['display_value'] = region.name
                except:
                    pass
                filter_values['name'] = 'region'
                filter_values['label'] = str(_('Target region'))
                data.pop('region')
            # Remove existing target country/region filters
            filters = filter(lambda f: f.get('name') in ('country', 'region'), stored_filters.values())
            for stored_filter in list(filters):
                stored_filters.pop(stored_filter['name'], None)
            if filter_values:
                # Set filter
                new_filter = Filter(
                    variable=filter_values['variable'], operator=filter_values['operator'],
                    value=filter_values['value'], name=filter_values.get('name', None),
                    label=filter_values['label'], display_value=filter_values.get('display_value', None)
                )
                stored_filters[new_filter.name] = new_filter
                self.request.session['filters'] = stored_filters
        else:
            self.remove_country_region_filter()

    def remove_country_region_filter(self):
        stored_filters = self.request.session.get('filters', {})
        if stored_filters:
            stored_filters = dict(filter(lambda i: i[1].get('name', '') not in ('country', 'region'), stored_filters.items()))
        self.request.session['filters'] = stored_filters
        #stored_filters = self.request.session['filter_query_params']
        #stored_filters = dict(filter(lambda i: i[1].get('variable', '') not in ('target_country', 'target_region'), stored_filters.items()))
        self.request.session['filter_query_params'] = None

    def set_default_filters(self, data, disabled_presets=[], enabled_presets=[]):
        self.remove_default_filters()
        # Don't set default filters?
        if 'set_default_filters' in self.request.session:
            if not self.request.session.get('set_default_filters'):
                return
        if not disabled_presets:
            if hasattr(self, 'disabled_presets') and self.disabled_presets:
                disabled_presets = self.disabled_presets
        if not enabled_presets:
            if hasattr(self, 'enabled_presets') and self.enabled_presets:
                enabled_presets = self.enabled_presets
        stored_filters = self.request.session.get('filters', {})
        if not stored_filters:
            stored_filters = {}
        # Target country or region set?
        filter_names = [v.get('name', '') for k, v in stored_filters.items()]
        preset_ids = dict([(v.get('preset_id', ''), k) for k, v in stored_filters.items()])
        if ('country' in filter_names):
            # Use national presets
            for preset in FilterPreset.objects.filter(is_default_country=True):
                if preset.id in preset_ids.keys():
                    del stored_filters[preset_ids[preset.id]]
                if preset.id in disabled_presets:
                    continue
                if preset.id in enabled_presets:
                    del enabled_presets[enabled_presets.index(preset.id)]
                filter_name = 'default_preset_%i' % preset.id
                stored_filters[filter_name] = PresetFilter(
                    preset, name=filter_name, hidden=preset.is_hidden)
        else:
            # Use global presets
            for preset in FilterPreset.objects.filter(is_default_global=True):
                if preset.id in preset_ids.keys():
                    del stored_filters[preset_ids[preset.id]]
                if preset.id in disabled_presets:
                    continue
                filter_name = 'default_preset_%i' % preset.id
                stored_filters[filter_name] = PresetFilter(
                    preset, name=filter_name, hidden=preset.is_hidden)
        # Add enabled filters (if not already set)
        for preset_id in enabled_presets:
            if 'default_preset_%i' % preset_id not in stored_filters.keys():
                preset = FilterPreset.objects.get(pk=preset_id)
                if preset.id in preset_ids.keys():
                    del stored_filters[preset_ids[preset.id]]
                if preset.id in disabled_presets:
                    continue
                filter_name = 'default_preset_%i' % preset.id
                stored_filters[filter_name] = PresetFilter(
                    preset, name=filter_name, hidden=preset.is_hidden)
        self.request.session['filters'] = stored_filters
  
    def remove_default_filters(self):
        stored_filters = self.request.session.get('filters', {})
        if stored_filters:
            stored_filters = dict(filter(lambda i: 'default_preset' not in i[0], stored_filters.items()))
        self.request.session['filters'] = stored_filters

    @print_execution_time_and_num_queries
    def get_formset_conditions(self, filter_set, data, group_by=None):
        self.set_country_region_filter(data)
        self.set_default_filters(data)

        if filter_set:
            # set given filters
            result = ConditionFormset(data, prefix="conditions_empty")
        else:
            if group_by == "database":
                result = None
            else:
                result = ConditionFormset(self._get_filter_dict(self.rules), prefix="conditions_empty")
        return result

    def _filter_set(self, data):
        return data and data.get("filtered") and not data.get("reset", None)

    def _get_filter_dict(self, browse_rules):
        filter_dict = MultiValueDict()
        for record, c in enumerate(browse_rules):
            rule_dict = MultiValueDict({
                "conditions_empty-%i-variable" % record: [c.variable],
                "conditions_empty-%i-operator" % record: [c.operator]
            })
            # pass comma separated list as multiple values for operators in/not in
            if c.operator in ("in", "not_in"):
                rule_dict.setlist("conditions_empty-%i-value" % record, c.value.split(","))
            else:
                rule_dict["conditions_empty-%i-value" % record] = c.value
            filter_dict.update(rule_dict)
        filter_dict["conditions_empty-INITIAL_FORMS"] = len(browse_rules)
        filter_dict["conditions_empty-TOTAL_FORMS"] = len(browse_rules)
        filter_dict["conditions_empty-MAX_NUM_FORMS"] = ""
        return filter_dict

    @property
    def status(self):
        if self.request.user.is_staff and "status" in self.request.GET:
            return self.request.GET.getlist("status")
        return ['2','3'] # FIXME: Use Activity.STATUS_ACTIVE + Activity.STATUS_OVERWRITTEN
