from pprint import pprint
from time import time

from django.db import connection
from django.utils.datastructures import MultiValueDict
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from grid.views.browse_filter_conditions import BrowseFilterConditions
from grid.views.view_aux_functions import (
    create_condition_formset, create_preset_table,
)

from .profiling_decorators import print_execution_time_and_num_queries
from landmatrix.models.browse_condition import BrowseCondition
from api.views.filter_view import set_filter, remove_filter, update_stored_filters, get_unique_frontend_user


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FilterWidgetMixin:

    rules = []
    # leave to test how transnational/domestic deals are filtered for
    # rules = BrowseCondition.objects.filter(rule__rule_type="generic")

    current_formset_conditions = None
    filters = None

    def create_preset_table(self):
        # moved the function to view_aux_functions because it is static
        # redirected from here in order to keep the interface
        return create_preset_table()

    def create_variable_table(self):
        # moved the function to view_aux_functions because it is static
        # redirected from here in order to keep the interface
        from grid.views.view_aux_functions import create_variable_table
        return create_variable_table()

    def example_set_filters(self):
        self.current_formset_conditions = self.get_formset_conditions(
            self._filter_set(self.GET), self.GET, self.rules, self.group
        )

        self.filters = self.get_filter_context(
            self.current_formset_conditions, self._order_by(), self.group, self.group_value,
            self.GET.get("starts_with", None)
        )

    def add_filter_context_data(self, context, request):
        context['request'] = request
        context['filters'] = self.filters
        context["empty_form_conditions"] = self.current_formset_conditions
        context["rules"] = self.rules

        variables = self.create_variable_table()
        context['variables'] = variables
        presets = self.create_preset_table()
        context['presets'] = presets

    @print_execution_time_and_num_queries
    def get_filter_context(self, formset_conditions, order_by=None, group_by=None, group_value=None, starts_with=None):
        filters = BrowseFilterConditions(formset_conditions, [order_by] if order_by else [], 0).parse()
        filters["group_by"] = group_by
        filters["group_value"] = group_value
        filters["starts_with"] = starts_with
        return filters

    def set_country_region_filter(self, data):
        filter_values = {}
        # Country or region filter set?
        if 'country' in data or 'region' in data:
            stored_filters = self.request.session.get('filters', {})
            unique_user = get_unique_frontend_user(self.request)
            if data.get('country'):
                filter_values['variable'] = 'target_country'
                filter_values['operator'] = 'is'
                filter_values['value'] = data.get('country')
                filter_values['name'] = str(_('Target country'))
                data.pop('country')
            elif data.get('region'):
                filter_values['variable'] = 'target_region'
                filter_values['operator'] = 'is'
                filter_values['value'] = data.get('region')
                filter_values['name'] = str(_('Target region'))
                data.pop('region')
            # Remove existing target country/region filters
            filters = filter(lambda f: f['variable'] in ('target_country', 'target_region'), stored_filters.values())
            for stored_filter in list(filters):
                remove_filter(stored_filters, stored_filter['name'])
            set_filter(stored_filters, filter_values)
            update_stored_filters(self.request, stored_filters, unique_user)

    @print_execution_time_and_num_queries
    def get_formset_conditions(self, filter_set, data, group_by=None):
        self.set_country_region_filter(data)
        ConditionFormset = create_condition_formset()
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
