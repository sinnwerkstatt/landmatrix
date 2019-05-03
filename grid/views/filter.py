import datetime
from collections import OrderedDict

from django import forms
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDict
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from bootstrap3_datetime.widgets import DateTimePicker
from django.utils.translation import ugettext_lazy as _, ugettext as _

from api.filters import Filter, PresetFilter
from grid.forms.browse_condition_form import ConditionFormset

from grid.forms.investor_form import OperationalCompanyForm, ParentStakeholderForm, ParentInvestorForm
from grid.views.browse_filter_conditions import get_activity_field_by_key, get_investor_field_by_key, \
    BrowseFilterConditions
from grid.fields import YearMonthDateField, TitleField
from grid.views.utils import DEAL_FORMS
from landmatrix.forms import ActivityFilterForm, InvestorFilterForm
from landmatrix.models import FilterPresetGroup, Country, Region, FilterPreset


class FilterWidgetAjaxView(APIView):

    renderer_classes = (JSONRenderer,)

    TYPE_STRING = 'string'
    TYPE_NUMERIC = 'numeric'
    TYPE_BOOLEAN = 'boolean'
    TYPE_LIST = 'list'
    TYPE_AUTOCOMPLETE = 'autocomplete'
    TYPE_LIST_MULTIPLE = 'multiple'
    TYPE_DATE = 'date'
    FIELD_TYPE_MAPPING = OrderedDict((
        (YearMonthDateField, TYPE_DATE), # Placed before CharField since it inherits from CharField
        (forms.CharField, TYPE_STRING),
        (forms.IntegerField, TYPE_NUMERIC),
        (forms.BooleanField, TYPE_BOOLEAN),
        (forms.ChoiceField, TYPE_LIST),
        (forms.MultipleChoiceField, TYPE_LIST_MULTIPLE),
    ))
    FIELD_NAME_TYPE_MAPPING = {
        'activity_identifier': TYPE_NUMERIC,
        'fully_updated': TYPE_DATE,
        'fully_updated_date': TYPE_DATE,
        'updated_date': TYPE_DATE,
        'fully_updated_by': TYPE_LIST,
        'operational_stakeholder': TYPE_AUTOCOMPLETE,
        'target_country': TYPE_AUTOCOMPLETE,
    }
    TYPE_OPERATION_MAPPING = {
        TYPE_STRING: ('contains', 'is', 'is_empty'),
        TYPE_NUMERIC: ('lt', 'gt', 'gte', 'lte', 'is', 'is_empty'),
        TYPE_BOOLEAN: ('is', 'is_empty'),
        TYPE_LIST: ('is', 'not_in', 'in', 'is_empty'),
        TYPE_LIST_MULTIPLE: ('is', 'not_in', 'in', 'is_empty'),
        TYPE_DATE: ('lt', 'gt', 'gte', 'lte', 'is', 'is_empty'),
        TYPE_AUTOCOMPLETE: ('is', 'not_in', 'in', 'is_empty'),
    }
    OPERATION_WIDGET_MAPPING = {
        'is_empty': None,
    }
    TYPE_WIDGET_MAPPING = {
        TYPE_STRING: [
            {
                'operations': ('contains', 'is'),
                'widget': forms.TextInput,
            }
        ],
        TYPE_NUMERIC: [
            {
                'operations': ('lt', 'gt', 'gte', 'lte', 'is'),
                'widget': forms.NumberInput,
            }
        ],
        TYPE_BOOLEAN: [
            {
                'operations': ('is',),
                'widget': forms.Select,
            }
        ],
        TYPE_LIST: [
            {
                'operations': ('is',),
                'widget': forms.Select,
            },
            {
                'operations': ('not_in', 'in'),
                'widget': forms.CheckboxSelectMultiple,
            }
        ],
        TYPE_LIST_MULTIPLE: [
            {
                'operations': ('is',),
                'widget': forms.CheckboxSelectMultiple,
            },
            {
                'operations': ('not_in', 'in'),
                'widget': forms.CheckboxSelectMultiple,
            }
        ],
        TYPE_DATE: [
            {
                'operations': ('lt', 'gt', 'gte', 'lte', 'is'),
                'widget': DateTimePicker,
            }
        ],
        TYPE_AUTOCOMPLETE: [
            {
                'operations': ('is',),
                'widget': forms.Select,
            },
            {
                'operations': ('not_in', 'in'),
                'widget': forms.SelectMultiple,
            }
        ],
    }
    FIELD_NAME_MAPPING = {
        'operational_stakeholder': 'operating_company_id',
    }
    field_name = ''
    name = ''
    operation = ''
    doc_type = 'deal'

    def get(self, *args, **kwargs):
        """ render form to enter values for the requested field in the filter widget for the grid view
            form to select operations is updated by the javascript function update_widget() in /media/js/main.js
        """
        self.doc_type = kwargs.get('doc_type', 'deal')
        self.field_name = self.request.GET.get('key_id', '')
        self.name = self.request.GET.get('name', '')
        self.operation = self.request.GET.get('operation', '')

        return Response({
            'allowed_operations': self.get_allowed_operations(),
            'widget': self.render_widget()
        })

    @property
    def field(self):
        if not hasattr(self, '_field'):
            if self.field_name:
                # Deprecated?
                if "inv_" in self.field_name:
                    field = get_activity_field_by_key(self.field_name[4:])
                elif self.doc_type == 'investor':
                    field = get_investor_field_by_key(self.field_name)
                else:
                    field = get_activity_field_by_key(self.field_name)
                # MultiValueField?
                if isinstance(field, forms.MultiValueField):
                    # Get first field instead
                    field = field.fields[0]
                self._field = field
        return self._field

    @property
    def type(self):
        field = self.field
        if not hasattr(self, '_type'):
            # Get type by field class
            for field_class, field_type in self.FIELD_TYPE_MAPPING.items():
                if isinstance(field, field_class):
                    self._type = field_type
                    break
            # Get type by field name
            if self.field_name in self.FIELD_NAME_TYPE_MAPPING.keys():
                self._type = self.FIELD_NAME_TYPE_MAPPING.get(self.field_name)
            # Fallback to string
            if not hasattr(self, '_type'):
                self._type = self.TYPE_STRING
        return self._type

    @property
    def value(self):
        if not hasattr(self, '_value'):
            value = self.request.GET.get('value', '')
            if value:
                # Date?
                if self.type == self.TYPE_DATE:
                    value = datetime.strptime(value, "%Y-%m-%d")
            else:
                # Boolean?
                if self.type == self.TYPE_BOOLEAN:
                    value = 'True'
            # Make list
            if self.type in (self.TYPE_LIST, self.TYPE_LIST_MULTIPLE):
                self._value = value and value.split(',') or []
            else:
                self._value = value
        return self._value

    def get_allowed_operations(self):
        return self.TYPE_OPERATION_MAPPING[self.type]

    def get_attrs(self):
        # Merge custom with existing field attributes
        attrs = {
            'id': 'id_{}'.format(self.name),
        }
        if not self.field or not hasattr(self.field.widget, 'attrs'):
            return attrs
        if not self.type == self.TYPE_LIST_MULTIPLE and \
           not (self.type == self.TYPE_LIST and self.operation in ('in', 'not_in')):
            attrs['class'] = 'valuefield form-control'
        field_attrs = self.field.widget.attrs
        for key, value in field_attrs.items():
            if key in ('readonly',):
                continue
            if key in attrs and key == 'class':
                attrs[key] += ' %s' % field_attrs[key]
            else:
                attrs[key] = field_attrs[key]
        return attrs

    def get_widget_init_kwargs(self):
        kwargs = {}
        # Get boolean choices (Yes/No)
        if self.type == self.TYPE_BOOLEAN:
            kwargs['choices'] = [
                ('True', _('Yes')),
                ('False', _('No')),
            ]
        # Get list choices
        if self.type in (self.TYPE_LIST, self.TYPE_LIST_MULTIPLE):
            if self.field_name == 'fully_updated_by':
                users = User.objects.filter(groups__name__in=("Research admins",
                                            "Research assistants")).order_by("username")
                kwargs['choices'] = [(u.id, u.get_full_name() or u.username) for u in users]
            else:
                kwargs['choices'] = self.field.choices
        # Get date options
        if self.type == self.TYPE_DATE:
            kwargs['options'] = {
                "format": "YYYY-MM-DD",
                "inline": True,
            }
        return kwargs

    def get_widget_render_kwargs(self):
        return {
            'name': self.name,
            'value': self.value,
            'attrs': self.get_attrs()
        }

    def get_widget_class(self):
        operation_mappings = self.TYPE_WIDGET_MAPPING[self.type]
        widget = None
        for operation_mapping in operation_mappings:
            if self.operation in operation_mapping['operations']:
                widget = operation_mapping['widget']
        return widget

    def render_widget(self):
        widget = self.get_widget_class()
        if widget:
            widget = widget(**self.get_widget_init_kwargs())
            widget = self._pre_render_widget(widget)
            widget = widget.render(**self.get_widget_render_kwargs())
            widget = self._post_render_widget(widget)
        return widget

    def _pre_render_widget(self, widget):
        if self.type == self.TYPE_DATE:
            # See here: https://github.com/jorgenpt/django-bootstrap3-datetimepicker/commit/042dd1da3a7ff21010c1273c092cba108d95baeb#commitcomment-16877308
            widget.js_template = """
            <script>
                    $(function(){$("#%(picker_id)s:has(input:not([readonly],[disabled]))")
                    .datetimepicker(%(options)s);});
            </script>
            """
        return widget

    def _post_render_widget(self, widget):
        return widget


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
        for form in DEAL_FORMS
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
                if self.doc_type == 'deal':
                    filter_values['variable'] = 'target_country'
                    filter_values['label'] = _('Target country')
                else:
                    filter_values['variable'] = 'fk_country'
                    filter_values['label'] = _('Country of registration/origin')
                filter_values['operator'] = 'is'
                filter_values['value'] = data.get('country')
                try:
                    country = Country.objects.defer('geom').get(pk=data.get('country'))
                    filter_values['display_value'] = country.name
                except:
                    pass
                filter_values['name'] = 'country'
                data.pop('country')
            elif data.get('region', None):
                if self.doc_type == 'deal':
                    filter_values['variable'] = 'target_region'
                    filter_values['label'] = str(_('Target region'))
                else:
                    filter_values['variable'] = 'region'
                    filter_values['label'] = str(_('Region of registration/origin'))
                filter_values['operator'] = 'is'
                filter_values['value'] = data.get('region')
                try:
                    region = Region.objects.get(pk=data.get('region'))
                    filter_values['display_value'] = region.name
                except:
                    pass
                filter_values['name'] = 'region'
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
        # Don't set default filters? Set them by default (required e.g. for statistics).
        if not self.request.session.get('%s:set_default_filters' % self.doc_type, False):
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
        if self.request.user.is_authenticated and "status" in self.request.GET:
            return self.request.GET.getlist("status")
        return ['2', '3'] # FIXME: Use Activity.STATUS_ACTIVE + Activity.STATUS_OVERWRITTEN