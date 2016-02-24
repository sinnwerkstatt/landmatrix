from time import time

from django.db import connection

from grid.views.browse_filter_conditions import BrowseFilterConditions
from grid.views.view_aux_functions import create_condition_formset
from landmatrix.models.browse_condition import BrowseCondition

from django.utils.datastructures import MultiValueDict

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FilterWidgetMixin:

    rules = BrowseCondition.objects.filter(rule__rule_type="generic")

    def example_set_filters(self):
        self.current_formset_conditions = self.get_formset_conditions(
            self._filter_set(self.GET), self.GET, self.group, self.rules
        )

        self.filters = self.get_filter_context(
            self.current_formset_conditions, self._order_by(), self.group, self.group_value,
            self.GET.get("starts_with", None)
        )

    def get_filter_context(self, formset_conditions, order_by, group_by, group_value, starts_with):
        start = time()
        num_queries_old = len(connection.queries)
        filters = BrowseFilterConditions(formset_conditions, [order_by] if order_by else [], 0).parse()
        filters["group_by"] = group_by
        filters["group_value"] = group_value
        filters["starts_with"] = starts_with
        # print(type(self).__name__, 'get_filter_context()', time()-start, 's', len(connection.queries)-num_queries_old, 'queries')
        return filters

    def get_formset_conditions(self, filter_set, GET, group_by, browse_rules):
        start = time()
        num_queries_old = len(connection.queries)
        ConditionFormset = create_condition_formset()
        if filter_set:
            # set given filters
            result = ConditionFormset(GET, prefix="conditions_empty")
        else:
            if group_by == "database":
                result = None
            else:
                result = ConditionFormset(self._get_filter_dict(browse_rules), prefix="conditions_empty")
        # print(type(self).__name__, 'get_formset_conditions()', time()-start, 's', len(connection.queries)-num_queries_old, 'queries')
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
