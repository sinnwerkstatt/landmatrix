
from grid.views.filter_widget_mixin import FilterWidgetMixin

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .view_aux_functions import create_condition_formset, render_to_response
from .browse_filter_conditions import BrowseFilterConditions
from .intention_map import IntentionMap
from .download import Download
from grid.views.activity_protocol import ActivityProtocol

from django.views.generic import TemplateView
from django.utils.datastructures import MultiValueDict
from django.template import RequestContext

import json, numbers


from time import time

from django.db import connection
from django.db.backends.base.base import BaseDatabaseWrapper

class ExecutionTimer:

    def __init__(self, msg):
        self.old_db_buffer_length = BaseDatabaseWrapper.queries_limit
        BaseDatabaseWrapper.queries_limit = 100000
        self.message = msg
        self.start = time()
        self.num_queries_old = len(connection.queries)

    def __del__(self):
        print(self.message, time()-self.start, 's', len(connection.queries)-self.num_queries_old, 'queries')
        BaseDatabaseWrapper.queries_limit = self.old_db_buffer_length

    def touch(self):
        print(self.message, time()-self.start, 's', len(connection.queries)-self.num_queries_old, 'queries')

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

    def is_download(self):
        return self.download_type is not None

    def dispatch(self, request, *args, **kwargs):

        # timer = ExecutionTimer(type(self).__name__+'.dispatch()')

        self.request = request
        self.GET = request.GET

        self._set_group_value(**kwargs)
        self._set_download(**kwargs)
        self._set_group(**kwargs)
        self._set_filters()
        self._set_columns()

        query_result = self.get_records(request)

        items = self._get_items(query_result)
        render = self.render(items, kwargs)
        # timer.touch()
        return render

    def render(self, items, kwargs):

        # timer = ExecutionTimer(type(self).__name__+'.render()')

        if self.is_download() and items:
            return self._get_download(items)
        context = {
            "view": "get-the-detail",
            "cms_page": 'global',
            "data": {
                "items": items,
                "order_by": self._order_by(),
                "count": self.num_results
            },
            "name": self.group_value,
            "columns": self.group_value and self.GROUP_COLUMNS_LIST or self._columns(),
            "filters": self.filters,
            "load_more": self._load_more_amount(),
            "group_slug": kwargs.get("group", self.DEFAULT_GROUP),
            "group_value": kwargs.get("list", None),
            "group": self.group.replace("_", " "),
            "empty_form_conditions": self.current_formset_conditions,
            "rules": self.rules,
        }
        response = render_to_response(self.template_name, context, RequestContext(self.request))

        return response

    def download_format(self):
        return self.GET.get("download_format") if self.GET.get("download_format") \
            else self.download_type if self.download_type \
            else 'csv'

    def get_records(self, request):
        start = time()
        num_queries_old = len(connection.queries)
        ap = ActivityProtocol()
        request.POST = MultiValueDict(
            {"data": [json.dumps({"filters": self.filters, "columns": self.columns})]}
        )
        ap.DEBUG = self.debug_query
        res = ap.dispatch(request, action="list_group").content
        query_result = json.loads(res.decode())

        self.num_results = len(query_result['activities'])
        # print(type(self).__name__, 'get_records()', time()-start, 's', len(connection.queries)-num_queries_old, 'queries')
        if self._limit_query():
            return query_result["activities"][:self._load_more()]
        else:
            return query_result["activities"]

    def _limit_query(self):
        """ Don't limit query when download or group view."""
        return not (
            self.is_download()
            or (not self.group_value and self.group not in self.QUERY_LIMITED_GROUPS)
            or self.GET.get("starts_with", None)
        )

    def _load_more(self):
        load_more = int(self.GET.get("more", 50))
        if not self._filter_set(self.GET) and self.group == "database":
            load_more = None
        if not self._limit_query():
            load_more = None
        return load_more

    def _load_more_amount(self):
        if not self._load_more(): return None
        if self.num_results > self._load_more():
            return int(self._load_more()) + self.LOAD_MORE_AMOUNT
        return None

    def _set_group_value(self, **kwargs):
        self.group_value = kwargs.get("list", "")
        if self.group_value == 'none': self.group_value = ''
        if self.group_value.endswith(".csv") or kwargs.get("group", self.DEFAULT_GROUP).endswith(".csv"):
            self.group_value = self.group_value.split(".")[0]

    def _set_download(self, **kwargs):
        if not self.group_value: self._set_group_value(**kwargs)
        self.download_type = None
        for ext in Download.supported_formats():
            if self.group_value.endswith(ext) or kwargs.get("group", self.DEFAULT_GROUP).endswith('.'+ext):
                self.download_type = ext
                return

    def _set_group(self, **kwargs):
        self.group = kwargs.get("group", self.DEFAULT_GROUP)
        if self.is_download():
            self.group = self.group.split(".")[0]
        # map url to group variable, cut possible .csv suffix
        self.group = self.group.replace("by-", "").replace("-", "_")
        if not self._filter_set(self.GET) and self.group == "database":
            self.group = "all"

    def _set_columns(self):
        start = time()
        num_queries_old = len(connection.queries)
        if self.is_download() and (self.group_value or self.group == "all"):
            self.columns = self.DOWNLOAD_COLUMNS
        elif self.group_value:
            self.columns = self.GROUP_COLUMNS_LIST
        else:
            self.columns = self._columns()
        # print(type(self).__name__, '_set_columns()', time()-start, 's', len(connection.queries)-num_queries_old, 'queries')

    def _set_filters(self):
        start = time()
        num_queries_old = len(connection.queries)
        self.current_formset_conditions = self.get_formset_conditions(
            self._filter_set(self.GET), self.GET, self.group, self.rules
        )

        self.filters = self.get_filter_context(
            self.current_formset_conditions, self._order_by(), self.group, self.group_value,
            self.GET.get("starts_with", None)
        )
        # print(type(self).__name__, '_set_filters()', time()-start, 's', len(connection.queries)-num_queries_old, 'queries')

    def _get_download(self, items):
        download = Download(self.download_format(), self.columns, self.group)
        return download.get(items)

    def _get_items(self, query_result):
        start = time()
        num_queries_old = len(connection.queries)
        result_ = [self._get_row(record, query_result) for record in query_result]
        # print(type(self).__name__, '_get_items()', time()-start, 's', len(connection.queries)-num_queries_old, 'queries')
        return result_

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

        if self.is_download():
            intentions = [intention for intention in set(value) if not IntentionMap.has_subintentions(intention)]
        else:
            intentions = [IntentionMap.get_parent(intention) for intention in set(value)]

        return sorted(list(set(filter(None, intentions))))

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
        result = [{"name": inv} for inv in value]
        return result

    def _process_stitched_together_field(self, value):
        if not isinstance(value, list):
            value = [value]
        return [field.split("#!#")[0] for field in value]

    def _process_name_and_year(self, value):
        return [{"name": n.split("#!#")[0], "year": n.split("#!#")[1]} for n in value]

    def _process_value(self, c, value):
        if not value: return None
        process_functions = {
            'intention': self._process_intention,
            'investor_name': self._process_investor_name,
            'stakeholder_name': self._process_stakeholder_name,
#            'investor_country': self._process_stitched_together_field,
            'stakeholder_country': self._process_stitched_together_field,
#            'investor_region': self._process_stitched_together_field,
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
        order_by = self.GET.get("order_by", self.group_value and "deal_id" or self.group) \
                   or self.group_value and "deal_id" \
                   or self.group
        if order_by == "all" or order_by == "database":
            order_by = "deal_id"
        return order_by

    def _columns(self):
        columns = {
            "target_country": ["target_country", "target_region", "intention", "deal_count", "availability"],
            "target_region": ["target_region", "intention", "deal_count", "availability"],
            "stakeholder_name": ["stakeholder_name", "stakeholder_country", "intention", "deal_count", "availability"],
# stakeholder_region temporarily disabled until a more intelligent caching for the public interface variables is implemented
#            "stakeholder_country": ["stakeholder_country", "stakeholder_region", "intention", "deal_count", "availability"],
            "stakeholder_country": ["stakeholder_country", "intention", "deal_count", "availability"],
# intention temporarily disabled until a more intelligent caching for the public interface variables is implemented
#            "stakeholder_region": ["stakeholder_region", "intention", "deal_count", "availability"],
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

