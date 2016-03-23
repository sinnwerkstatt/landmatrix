from pprint import pprint
from time import time

from django.db import connection

from grid.views.browse_filter_conditions import BrowseFilterConditions
from grid.views.view_aux_functions import create_condition_formset
from grid.views.save_deal_view import SaveDealView

from .profiling_decorators import print_execution_time_and_num_queries
from landmatrix.models.browse_condition import BrowseCondition

from django.utils.datastructures import MultiValueDict

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FilterWidgetMixin:

    rules = BrowseCondition.objects.filter(rule__rule_type="generic")

    current_formset_conditions = None
    filters = None

    def create_variable_table(self):
        input_groups = []
        group_items = []
        group_title = ''
        for form_name, form in SaveDealView.FORMS:
            # FormSet (Spatial Data und Data source)
            if hasattr(form, 'form'):
                form = form.form
            for field_name, field in form.base_fields.items():
                if field_name.startswith('tg_'):
                    if group_title and len(group_items) > 0:
                        input_groups.append({
                            'label': group_title,
                            'items': group_items
                        })
                        group_items = []
                    group_title = str(field.initial)
                else:
                    group_items.append({
                        'name': field_name,
                        'label': str(field.label)
                    })

        if group_title and len(group_items):
            input_groups.append({
                'label': group_title,
                'items': group_items
            })

        return input_groups

    def example_set_filters(self):
        self.current_formset_conditions = self.get_formset_conditions(self._filter_set(self.GET), self.GET, self.rules,
                                                                      self.group)

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
        pprint(variables)
        context['variables'] = variables

    @print_execution_time_and_num_queries
    def get_filter_context(self, formset_conditions, order_by=None, group_by=None, group_value=None, starts_with=None):
        filters = BrowseFilterConditions(formset_conditions, [order_by] if order_by else [], 0).parse()
        filters["group_by"] = group_by
        filters["group_value"] = group_value
        filters["starts_with"] = starts_with

        return filters

    @print_execution_time_and_num_queries
    def get_formset_conditions(self, filter_set, GET, group_by=None):
        ConditionFormset = create_condition_formset()
        if filter_set:
            # set given filters
            result = ConditionFormset(GET, prefix="conditions_empty")
        else:
            if group_by == "database":
                result = None
            else:
                result = ConditionFormset(self._get_filter_dict(self.rules), prefix="conditions_empty")
        return result

    def _filter_set(self, GET):
        return GET and GET.get("filtered") and not GET.get("reset", None)

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
