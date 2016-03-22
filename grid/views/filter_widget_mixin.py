from pprint import pprint
from time import time

from django.db import connection

from grid.views.browse_filter_conditions import BrowseFilterConditions
from grid.views.view_aux_functions import create_condition_formset
from .profiling_decorators import print_execution_time_and_num_queries
from landmatrix.models.browse_condition import BrowseCondition


from django.utils.datastructures import MultiValueDict

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FilterWidgetMixin:

    rules = BrowseCondition.objects.filter(rule__rule_type="generic")

    current_formset_conditions = None
    filters = None

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

        if not self.current_formset_conditions.forms:
            return

        # YUK:
        varlist = self.current_formset_conditions.forms[0]._variables()  # 1. grab somones privates
        vardict = {}
        for item in varlist:
            try:
                int(item[0])    # 2. Typecast to filter fails
                continue
            except:             # 3. Totally overachieve!
                pass            # 4. Handle naught.

            if item[0] != '':  # 5. Filter more stuff
                vardict[item[0]] = item[1]  # 6. ??????
        context['variables'] = vardict    # 7. Profit!

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
