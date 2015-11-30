__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .view_aux_functions import create_condition_formset, render_to_response
from .browse_filter_conditions import BrowseFilterConditions
from .intention_map import IntentionMap
from .download import Download
from landmatrix.models import BrowseCondition
from global_app.views.activity_protocol import ActivityProtocol

from django.views.generic import TemplateView
from django.utils.datastructures import MultiValueDict
from django.template import RequestContext

import json, numbers


class TableGroupView(TemplateView):

    LOAD_MORE_AMOUNT = 20
    DOWNLOAD_COLUMNS = [
        "deal_id", "target_country", "location", "investor_name", "investor_country", "intention", "negotiation_status",
        "implementation_status", "intended_size", "contract_size", "production_size", "nature_of_the_deal",
        "data_source_type", "data_source_url", "data_source_date", "data_source_organisation",
        "contract_farming", "crop"
    ]
    QUERY_LIMITED_GROUPS = ["target_country", "investor_name", "investor_country", "all", "crop"]
    GROUP_COLUMNS_LIST = [
        "deal_id", "target_country", "operational_stakeholder", "investor_name", "investor_country", "intention",
        "negotiation_status", "implementation_status", "intended_size", "contract_size",
    ]
    # GROUP_COLUMNS_LIST = [
    #     "deal_id", "target_country", "primary_investor", "investor_name", "investor_country", "intention",
    #     "negotiation_status", "implementation_status", "intended_size", "contract_size",
    # ]
    DEFAULT_GROUP = "by-target-region"

    template_name = "group-by.html"
    debug_query = False

    def is_download(self):
        return self.download_type is not None

    def dispatch(self, request, *args, **kwargs):

        self.request = request
        self.GET = request.GET

        self._set_group_value(**kwargs)
        self._set_download(**kwargs)
        self._set_group(**kwargs)
        self._set_filters()
        self._set_columns()

        query_result = self.get_records(request)

        items = self._get_items(query_result)

        return self.render(items, kwargs)

    def render(self, items, kwargs):
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
        return render_to_response(self.template_name, context, RequestContext(self.request))

    def download_format(self):
        return self.GET.get("download_format") if self.GET.get("download_format") \
            else self.download_type if self.download_type \
            else 'csv'

    def get_records(self, request):
        ap = ActivityProtocol()
        request.POST = MultiValueDict(
            {"data": [json.dumps({"filters": self.filters, "columns": self.columns})]}
        )
        ap.DEBUG = self.debug_query
        res = ap.dispatch(request, action="list_group").content
        query_result = json.loads(res.decode())

        self.num_results = len(query_result['activities'])
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
        if not self._filter_set() and self.group == "database":
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
#                self.debug_query = True
                return

    def _set_group(self, **kwargs):
        self.group = kwargs.get("group", self.DEFAULT_GROUP)
        if self.is_download():
            self.group = self.group.split(".")[0]
        # map url to group variable, cut possible .csv suffix
        self.group = self.group.replace("by-", "").replace("-", "_")
        if not self._filter_set() and self.group == "database":
            self.group = "all"

    def _filter_set(self):
        return self.GET and self.GET.get("filtered") and not self.GET.get("reset", None)

    def _set_columns(self):
        if self.is_download() and (self.group_value or self.group == "all"):
            self.columns = self.DOWNLOAD_COLUMNS
        elif self.group_value:
            self.columns = self.GROUP_COLUMNS_LIST
        else:
            self.columns = self._columns()

    def _set_filters(self):
        self.rules = BrowseCondition.objects.filter(rule__rule_type="generic")
        ConditionFormset = create_condition_formset()
        if self._filter_set():
            # set given filters
            self.current_formset_conditions = ConditionFormset(self.GET, prefix="conditions_empty")
        else:
            if self.group == "database":
                self.current_formset_conditions = None
            else:
                self.current_formset_conditions = ConditionFormset(self._get_filter_dict(), prefix="conditions_empty")

        self.filters = BrowseFilterConditions(self.current_formset_conditions, [self._order_by()], 0).parse()

        self.filters["group_by"] = self.group
        self.filters["group_value"] = self.group_value
        self.filters["starts_with"] = self.GET.get("starts_with", None)

    def _get_filter_dict(self):
        filter_dict = MultiValueDict()
        for record, c in enumerate(self.rules):
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
        filter_dict["conditions_empty-INITIAL_FORMS"] = len(self.rules)
        filter_dict["conditions_empty-TOTAL_FORMS"] = len(self.rules)
        filter_dict["conditions_empty-MAX_NUM_FORMS"] = ""
        return filter_dict

    def _get_download(self, items):
        download = Download(self.download_format(), self.columns, self.group)
        return download.get(items)

    def _get_items(self, query_result):
        return [ self._get_row(record, query_result) for record in query_result ]

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

        return sorted(intentions)

    def _process_investor_name(self, value):
        return [
            {"name": inv.split("#!#")[0], "id": inv.split("#!#")[1]} if len(inv.split("#!#")) > 1 else ""
            for inv in value
        ]

    def _process_stitched_together_field(self, value):
        return [field.split("#!#")[0] for field in value]

    def _process_name_and_year(self, value):
        return [{"name": n.split("#!#")[0], "year": n.split("#!#")[1]} for n in value]

    def _process_value(self, c, value):
        if not value: return None

        process_functions = {
            'intention': self._process_intention,
            'investor_name': self._process_investor_name,
            'investor_country': self._process_stitched_together_field,
            'investor_region': self._process_stitched_together_field,
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
            "investor_name": ["investor_name", "investor_country", "intention", "deal_count", "availability"],
            "investor_country": ["investor_country", "investor_region", "intention", "deal_count", "availability"],
            "investor_region": ["investor_region", "intention", "deal_count", "availability"],
            "intention": ["intention", "deal_count", "availability"],
            "crop": ["crop", "intention", "deal_count", "availability"],
            "year": ["year", "intention", "deal_count", "availability"],
            "data_source_type": ["data_source_type", "intention", "deal_count", "availability"],
            "all": ["deal_id", "target_country", "operational_stakeholder", "investor_name", "investor_country",
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

