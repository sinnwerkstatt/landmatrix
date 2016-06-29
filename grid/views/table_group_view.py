import json
import numbers

from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.utils.datastructures import MultiValueDict
from django.template import RequestContext

from api.query_sets.sql_generation.sql_builder import SQLBuilder
from grid.views.filter_widget_mixin import FilterWidgetMixin
from grid.views.profiling_decorators import \
    print_execution_time_and_num_queries
from grid.views.activity_protocol import ActivityProtocol
from .view_aux_functions import render_to_response, get_field_label
from grid.forms.choices import intention_choices
from django.utils.datastructures import SortedDict

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

INTENTION_MAP = {}
for choice, value, choices in intention_choices:
    INTENTION_MAP[choice] = {
        'value': value,
        'order_by': value,
    }
    if not choices:
        continue
    for schoice, svalue in choices:
        INTENTION_MAP[schoice] = {
            'value': svalue,
            'parent': value,
            'order_by': '%s (%s)' % (value, svalue),
        }

class TableGroupView(TemplateView, FilterWidgetMixin):

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
    DEFAULT_GROUP = "by-target-region"
    COLUMN_GROUPS = {
        "target_country": ["target_country", "target_region", "intention", "deal_count", "availability"],
        "target_region": ["target_region", "intention", "deal_count", "availability"],
        "investor_name": ["investor_name", "investor_country", "intention", "deal_count", "availability"],
#               region column disabled due to slowness resulting from additional JOIN
#                "investor_country": ["investor_country", "investor_region", "intention", "deal_count", "availability"],
        "investor_country": ["investor_country", "intention", "deal_count", "availability"],
        "investor_region": ["investor_region", "deal_count", "availability"],
        "intention": ["intention", "deal_count", "availability"],
        "crop": ["crop", "deal_count", "availability"],
        "year": ["year", "intention", "deal_count", "availability"],
        "data_source_type": ["data_source_type", "intention", "deal_count", "availability"],
        "all": ["deal_id", "target_country", "operational_stakeholder", "investor_country",
                "intention", "negotiation_status", "implementation_status", "intended_size",
                "contract_size", ]
    }

    template_name = "group-by.html"
    debug_query = False
    group = None
    group_value = None

    def get_context_data(self, group, group_value=None):
        context = super(TableGroupView, self).get_context_data()
        self.group = group or self.DEFAULT_GROUP
        self.group = self.group.replace("by-", "").replace("-", "_")
        self.group_value = group_value or ''

        query_result = self.get_records()
        items = self._get_items(query_result)
        context = {
            "view": "data",
            "data": {
                "items": items,
                "order_by": self.order_by,
                "count": self.num_results
            },
            "name": self.group_value,
            "columns": self.columns_dict,
            "status": self.status,
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
        # TODO: pass values rather than updating the request
        self.request.POST = MultiValueDict({
            "data": [json.dumps({
                "filters": self.filters,
                "columns": self.columns,
                "status": self.status
            })]
        })
        ap.DEBUG = self.debug_query
        res = ap.dispatch(self.request, action="list_group").content
        query_result = json.loads(res.decode())

        self.num_results = len(query_result['activities'])

        if self._limit_query():
            return query_result["activities"][:self._load_more()]
        else:
            return query_result["activities"]

    def _limit_query(self):
        """ Don't limit query when group view or export."""
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

    @property
    def columns(self):
        columns = []
        if self.request.GET.get('columns'):
            columns = self.request.GET.getlist('columns')
            if 'deal_id' not in columns:
                columns = ['deal_id'] + columns
        elif self.group_value:
            columns = self.GROUP_COLUMNS_LIST
        else:
            try:
                columns = self.COLUMN_GROUPS[self.group]
            except KeyError:
                raise Http404(
                    _("Unknown group '%(group)s'.") % {'group': self.group})
        return columns

    @property
    def columns_dict(self):
        """Get column information for template"""
        # Labels for all custom fields (fields that are not part of any form)
        COLUMN_LABELS_MAP = {
            'deal_id': _('#'),
            'deal_count': _('Deals'),
            'availability': _('Availability'),
            'investor_country': _('Operational company country'),
            'investor_region': _('Operational company region'),
            'operational_stakeholder': _('Operational company'),
            'investor_name': _('Operational company name'),
            'crop': _('Crop'),
            'data_source_type': _('Data source type'),
        }
        columns = SortedDict()
        for name in self.columns:
            label = None
            if name in COLUMN_LABELS_MAP.keys():
                label = COLUMN_LABELS_MAP[name]
            else:
                label = get_field_label(name)
            columns[name] = {
                'label': label,
                'order_by': name == self.order_by and '-'+name or name,
            }
        #columns = [col for col in columns if col in SQLBuilder.SQL_COLUMN_MAP.keys()]
        return columns

    @property
    def filters(self):
        data = self.request.GET.copy()
        return self.get_filter_context(
            self.current_formset_conditions, self.order_by, self.group, self.group_value,
            data.get("starts_with")
        )

    @property
    def current_formset_conditions(self):
        data = self.request.GET.copy()
        return self.get_formset_conditions(
            self._filter_set(data), data, self.group
        )

    @property
    def status(self):
        if self.request.user.is_staff and "status" in self.request.GET:
            return self.request.GET.getlist("status")
        else:
            return ["active", "overwritten"]

    @print_execution_time_and_num_queries
    def _get_items(self, query_result):
        items = [self._get_row(record, query_result) for record in query_result]
        # Reorder required for intention (because subcategories have been renamed in _process_intention)
        if self.group == 'intention':
            items = sorted(items, key=lambda i: i['intention'] and str(i['intention'][0]['order_by']) or '')
        return items

    def _get_row(self, record, query_result):
        # iterate over database result
        row = SortedDict()
        for j, c in enumerate(self.columns):
            # iterate over columns relevant for view or download
            value = record[j+1]
            row[c] = self._process_value(c, value)

        return row

    def _process_intention(self, value):
        if not isinstance(value, list):
            value = [value]
        intentions = [INTENTION_MAP.get(intention) for intention in value]
        return intentions

    def _process_value(self, column, value):
        if not value: return None
        process_functions = {
            'intention': self._process_intention,
            'investor_name': self._process_investor_name,
            'investor_name': self._process_investor_name,
            'investor_country': self._process_stitched_together_field,
            'investor_region': self._process_stitched_together_field,
            'crop': self._process_stitched_together_field,
            'latlon': lambda v: ["%s/%s (%s)" % (n.split("#!#")[0], n.split("#!#")[1], n.split("#!#")[2]) for n in v],
            'negotiation_status': self._process_name_and_year,
            'implementation_status': self._process_name_and_year,
            #"intended_size": lambda v: v,
            #"production_size": lambda v: v and v[0],
            #"contract_size": lambda v: v and v[0],
        }
        if column in process_functions:
            return process_functions[column](value)
        elif isinstance(value, numbers.Number):
            return int(value)
        elif not isinstance(value, list):
            return [value, ]
        return value

    @property
    def order_by(self):
        order_by = None
        if 'order_by' in self.request.GET:
            order_by = self.request.GET.get("order_by")
        elif self.group and self.group != 'all':
            order_by = self.group
        #elif self.group_value or order_by == "all" or order_by == "database"
        else:
            order_by = 'deal_id'
        return order_by

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


    def _process_investor_name(self, value):
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

