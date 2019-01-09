from collections import OrderedDict

from django.utils.datastructures import MultiValueDict
from django.utils.translation import ugettext as _
from django import forms

from landmatrix.models.filter_preset import FilterPreset, FilterPresetGroup
from api.filters import Filter, PresetFilter
from grid.fields import TitleField
from grid.forms.browse_condition_form import ConditionFormset
from grid.views.save_deal_view import SaveDealView
from grid.views.browse_filter_conditions import BrowseFilterConditions
from landmatrix.models.country import Country
from landmatrix.models.region import Region
from landmatrix.models.activity import Activity
from landmatrix.forms import ActivityFilterForm, InvestorFilterForm
from grid.forms.investor_form import OperationalCompanyForm, ParentInvestorForm, ParentStakeholderForm


def get_activity_variable_table():
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

    # Add Activity attributes
    variable_table[str(_('Deal'))] = []
    for field_name, field in ActivityFilterForm.base_fields.items():
        if field_name == 'id':
            continue
        variable_table[str(_('Deal'))].append({
            'name': field_name,
            'label': str(field.label),
        })

    # Add deal attributes
    exclude = ('intended_area', 'contract_area', 'production_area')
    for form in deal_forms:
        for field_name, field in form.base_fields.items():
            if field_name in exclude:
                continue
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

    # Add operating company attributes
    if _('Operating company') not in variable_table:
        variable_table[str(_('Operating company'))] = []
    for field_name, field in OperationalCompanyForm.base_fields.items():
        if field_name == 'id':
            continue
        variable_table[str(_('Operating company'))].append({
            'name': 'operating_company_%s' % field_name,
            'label': '%s %s' % (str(_('Operating company')), str(field.label)),
        })

    # Add parent company attributes
    variable_table[str(_('Parent company'))] = []
    for field_name, field in ParentStakeholderForm.base_fields.items():
        if field_name == 'id':
            continue
        variable_table[str(_('Parent company'))].append({
            'name': 'parent_stakeholder_%s' % field_name,
            'label': '%s %s' % (str(_('Parent company')), str(field.label)),
            })

    # Add tertiary investors/lenders attributes
    variable_table[str(_('Tertiary investor/lender'))] = []
    for field_name, field in ParentInvestorForm.base_fields.items():
        if field_name == 'id':
            continue
        variable_table[str(_('Tertiary investor/lender'))].append({
            'name': 'parent_investor_%s' % field_name,
            'label': '%s %s' % (str(_('Tertiary investor/lender')), str(field.label)),
         })

    return variable_table


def get_investor_variable_table():
    '''
    Create an OrderedDict of group name keys with lists of dicts for each
    variable in the group (each dict contains 'name' and 'label' keys).

    This whole thing is static, and maybe should just be written out, but
    for now generate it dynamcially on app load.
    '''
    variable_table = OrderedDict()
    group_items = []
    group_title = ''

    # Add investor attributes
    investor_variables = []
    for field_name, field in InvestorFilterForm.base_fields.items():
        if field_name == 'id':
            continue
        investor_variables.append({
            'name': field_name,
            'label': str(field.label),
        })
    variable_table[str(_('Investor'))] = investor_variables

    # Add parent company attributes
    pc_variables = []
    for field_name, field in ParentStakeholderForm.base_fields.items():
        if field_name == 'id':
            continue
        pc_variables.append({
            'name': 'parent_stakeholder_%s' % field_name,
            'label': '%s %s' % (str(_('Parent company')), str(field.label)),
            })
    variable_table[str(_('Parent company'))] = pc_variables

    # Add tertiary investors/lenders attributes
    til_variables = []
    for field_name, field in ParentInvestorForm.base_fields.items():
        if field_name == 'id':
            continue
        til_variables.append({
            'name': 'parent_investor_%s' % field_name,
            'label': '%s %s' % (str(_('Tertiary investor/lender')), str(field.label)),
         })
    variable_table[str(_('Tertiary investor/lender'))] = til_variables

    return variable_table

class FilterWidgetMixin:

    doc_type = 'deal'
    variable_table = get_activity_variable_table()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        if not self.request.session.get('%s:set_default_filters' % self.doc_type):
            # Disable and remove all default filters (including hidden)
            set_default_filters = False
            self.remove_default_filters()
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
            stored_filters = self.request.session.get('%s:filters' % self.doc_type, {})
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
                self.request.session['%s:filters' % self.doc_type] = stored_filters
        else:
            self.remove_country_region_filter()

    def remove_country_region_filter(self):
        stored_filters = self.request.session.get('%s:filters' % self.doc_type, {})
        if stored_filters:
            stored_filters = dict(filter(lambda i: i[1].get('name', '') not in ('country', 'region'), stored_filters.items()))
        self.request.session['%s:filters' % self.doc_type] = stored_filters
        #stored_filters = self.request.session['filter_query_params']
        #stored_filters = dict(filter(lambda i: i[1].get('variable', '') not in ('target_country', 'target_region'), stored_filters.items()))
        self.request.session['%s:filter_query_params' % self.doc_type] = None

    def set_default_filters(self, data, disabled_presets=[], enabled_presets=[]):
        self.remove_default_filters()
        # Don't set default filters?
        if not self.request.session.get('%s:set_default_filters' % self.doc_type):
            return
        if not disabled_presets:
            if hasattr(self, '%s:disabled_presets' % self.doc_type) and self.disabled_presets:
                disabled_presets = self.disabled_presets
        if not enabled_presets:
            if hasattr(self, '%s:enabled_presets' % self.doc_type) and self.enabled_presets:
                enabled_presets = self.enabled_presets
        stored_filters = self.request.session.get('%s:filters' % self.doc_type, {})
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
        self.request.session['%s:filters' % self.doc_type] = stored_filters
  
    def remove_default_filters(self):
        stored_filters = self.request.session.get('%s:filters' % self.doc_type, {})
        if stored_filters:
            stored_filters = dict(filter(lambda i: 'default_preset' not in i[0], stored_filters.items()))
        self.request.session['%s:filters' % self.doc_type] = stored_filters

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
        if self.request.user.is_authenticated() and "status" in self.request.GET:
            return self.request.GET.getlist("status")
        return ['2', '3'] # FIXME: Use Activity.STATUS_ACTIVE + Activity.STATUS_OVERWRITTEN
