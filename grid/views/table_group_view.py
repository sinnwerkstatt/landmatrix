
from grid.views.filter_widget_mixin import FilterWidgetMixin

from .view_aux_functions import render_to_response
from grid.views.profiling_decorators import print_execution_time_and_num_queries
from .intention_map import IntentionMap
#from .download import Download
from grid.views.activity_protocol import ActivityProtocol

from django.views.generic import TemplateView
from django.utils.datastructures import MultiValueDict
from django.template import RequestContext

import json, numbers

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class TableGroupView(TemplateView, FilterWidgetMixin):

    LOAD_MORE_AMOUNT = 20
    DOWNLOAD_COLUMNS = [
        "deal_id", "target_country", "location", "stakeholder_name", "stakeholder_country", "intention", "negotiation_status",
        "implementation_status", "intended_size", "contract_size", "production_size", "nature_of_the_deal",
        "data_source_type", "data_source_url", "data_source_date", "data_source_organisation",
        "contract_farming", "crop"
    ]
    QUERY_LIMITED_GROUPS = ["target_country", "stakeholder_name", "stakeholder_country", "all", "crop"]
    GROUP_COLUMNS_LIST = [
        "deal_id", "target_country", "operational_stakeholder", "stakeholder_name", "stakeholder_country", "intention",
        "negotiation_status", "implementation_status", "intended_size", "contract_size",
    ]
    DEFAULT_GROUP = "by-target-region"

    template_name = "group-by.html"
    debug_query = False
    group = None
    group_value = None

    def get_context_data(self, group, group_value=None):
        context = super(TableGroupView, self).get_context_data()
        self.group = group or self.DEFAULT_GROUP
        self.group = self.group.replace("by-", "").replace("-", "_")
        self.group_value = group_value or ''

        self._set_filters()
        self._set_columns()

        query_result = self.get_records()
        items = self._get_items(query_result)

        context = {
            "view": "get-the-detail",
            "data": {
                "items": items,
                "order_by": self._order_by(),
                "count": self.num_results
            },
            "name": self.group_value,
            "columns": self.columns,
            "load_more": self._load_more_amount(),
            "group_slug": self.group,
            "group_value": self.group_value,
            "group": self.group.replace("_", " "),
            # "rules": self.rules,
        }
        self.add_filter_context_data(context, self.request)
        return context

    @print_execution_time_and_num_queries
    def get_records(self):
        ap = ActivityProtocol()
        self.request.POST = MultiValueDict(
            {"data": [json.dumps({"filters": self.filters, "columns": self.columns})]}
        )
        ap.DEBUG = self.debug_query
        res = ap.dispatch(self.request, action="list_group").content
        query_result = json.loads(res.decode())

        self.num_results = len(query_result['activities'])

        if self._limit_query():
            return query_result["activities"][:self._load_more()]
        else:
            return query_result["activities"]

    def _limit_query(self):
        """ Don't limit query when group view."""
        return not (
            (not self.group_value and self.group not in self.QUERY_LIMITED_GROUPS)
            or self.request.GET.get("starts_with", None)
        )

    def _load_more(self):
        load_more = int(self.request.GET.get("more", 50))
        if not self._filter_set(self.request.GET) and self.group == "database":
            load_more = None
        if not self._limit_query():
            load_more = None
        return load_more

    def _load_more_amount(self):
        if not self._load_more(): return None
        if self.num_results > self._load_more():
            return int(self._load_more()) + self.LOAD_MORE_AMOUNT
        return None

    @print_execution_time_and_num_queries
    def _set_columns(self):
        if self.group_value:
            self.columns = self.GROUP_COLUMNS_LIST
        else:
            self.columns = self._columns()

    @print_execution_time_and_num_queries
    def _set_filters(self):
        self.current_formset_conditions = self.get_formset_conditions(
            self._filter_set(self.request.GET), self.request.GET, self.group
        )

        self.filters = self.get_filter_context(
            self.current_formset_conditions, self._order_by(), self.group, self.group_value,
            self.request.GET.get("starts_with")
        )

    @print_execution_time_and_num_queries
    def _get_items(self, query_result):
        return [self._get_row(record, query_result) for record in query_result]

    def _get_row(self, record, query_result):
        # iterate over database result
        row = {}
        for j, c in enumerate(self.columns):
            # iterate over columns relevant for view or download
            value = record[j+1]
            row[c] = self._process_value(c, value)

        return row

    def _process_intention(self, value):
        if not isinstance(value, list):
            return [value]

        intentions = [IntentionMap.get_parent(intention) for intention in set(value)]

        return sorted(list(set(filter(None, intentions))))

    def _process_value(self, c, value):
        if not value: return None
        process_functions = {
            'intention': self._process_intention,
            'investor_name': self._process_investor_name,
            'stakeholder_name': self._process_stakeholder_name,
            'stakeholder_country': self._process_stitched_together_field,
            'stakeholder_region': self._process_stitched_together_field,
            'crop': self._process_stitched_together_field,
            'latlon': lambda v: ["%s/%s (%s)" % (n.split("#!#")[0], n.split("#!#")[1], n.split("#!#")[2]) for n in v],
            'negotiation_status': self._process_name_and_year,
            'implementation_status': self._process_name_and_year,
            "intended_size": lambda v: v and v[0],
            "production_size": lambda v: v and v[0],
            "contract_size": lambda v: v and v[0],
        }
        if c in process_functions:
            return process_functions[c](value)
        elif isinstance(value, numbers.Number):
            return int(value)
        elif not isinstance(value, list):
            return [value, ]
        return value

    def _order_by(self):
        order_by = self.request.GET.get("order_by", self.group_value and "deal_id" or self.group) \
                   or self.group_value and "deal_id" \
                   or self.group
        if order_by == "all" or order_by == "database":
            order_by = "deal_id"
        return order_by

    def _columns(self):
        print('_columns')
        if self.request.GET.get('columns'):
            return self.request.GET.getlist('columns')

        columns = {
            "target_country": ["target_country", "target_region", "intention", "deal_count", "availability"],
            "target_region": ["target_region", "intention", "deal_count", "availability"],
            "stakeholder_name": ["stakeholder_name", "stakeholder_country", "intention", "deal_count", "availability"],
#           region column disabled due to slowness resulting from additional JOIN
#            "stakeholder_country": ["stakeholder_country", "stakeholder_region", "intention", "deal_count", "availability"],
            "stakeholder_country": ["stakeholder_country", "intention", "deal_count", "availability"],
            "stakeholder_region": ["stakeholder_region", "deal_count", "availability"],
            "intention": ["intention", "deal_count", "availability"],
            "crop": ["crop", "intention", "deal_count", "availability"],
            "year": ["year", "intention", "deal_count", "availability"],
            "data_source_type": ["data_source_type", "intention", "deal_count", "availability"],
            "all": ["deal_id", "target_country", "operational_stakeholder", "stakeholder_name", "stakeholder_country",
                    "intention", "negotiation_status", "implementation_status", "intended_size",
                    "contract_size", ]
        }
        return columns[self.group]

    def _map_values_of_group(self, value_list, format_string):
        """ Map different values of one group together. Ensures that values of a group are together.
            e.g. group of data sources with different urls, types and dates."""
        output = []
        groups = {}
        keys = value_list.keys()
        for k,v in value_list.items():
            if not v:
                continue
            for s in v:
                if s is None or "#!#" not in s:
                    continue
                gv = s.split("#!#")[0]
                g = s.split("#!#")[1]
                group = groups.get(g, {})
                group.update({k: gv + " "})
                groups[g] = group
        for g,gv in groups.items():
            for k in keys:
                if k not in gv:
                    gv.update({k: ""})
            output.append(format_string % gv)
        return output


    def _process_investor_name(self, value):
        if not isinstance(value, list):
            value = [value]
        result = [
            {"name": inv.split("#!#")[0], "id": inv.split("#!#")[1]} if len(inv.split("#!#")) > 1 else inv
            for inv in value
        ]
        return result


    def _process_stakeholder_name(self, value):
        if not isinstance(value, list):
            value = [value]
        result = [
            {"name": inv.split("#!#")[0], "id": inv.split("#!#")[1]} if len(inv.split("#!#")) > 1 else inv
            for inv in value
        ]
        return result


    def _process_stitched_together_field(self, value):
        if not isinstance(value, list):
            value = [value]
        return [field.split("#!#")[0] for field in value]


    def _process_name_and_year(self, value):
        return [{"name": n.split("#!#")[0], "year": n.split("#!#")[1]or 0} for n in value]

