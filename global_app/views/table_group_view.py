__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.views.generic import TemplateView
from django.utils.datastructures import MultiValueDict
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings
from django.db import connection

import json, numbers

from .view_aux_functions import parse_browse_filter_conditions
from landmatrix.models import BrowseCondition, ActivityAttributeGroup, Activity, Crop
from global_app.views.browse_condition_form import BrowseConditionForm
from global_app.views.dummy_activity_protocol import DummyActivityProtocol


INTENTION_MAP = {
    "Agriculture": ["Agriculture", "Biofuels", "Food crops", "Livestock", "Non-food agricultural commodities", "Agriunspecified"],
    "Forestry": ["Forestry", "For wood and fibre", "For carbon sequestration/REDD", "Forestunspecified"],
    "Mining": ["Mining",],
    "Tourism": ["Tourism",],
    "Land Speculation": ["Land Speculation",],
    "Industry":["Industry",],
    "Conservation": ["Conservation",],
    "Renewable Energy": ["Renewable Energy",],
    "Other": ["Other (please specify)",],
}

def get_intention(intention):
    for k,v in INTENTION_MAP.items():
        if intention in v:
            return k
    return intention

""" Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments."""
def render_to_response(template_name, context, context_instance):
    # Some deprecated arguments were passed - use the legacy code path
    content = loader.render_to_string(template_name, context, context_instance)

    return HttpResponse(content)


DEFAULT_GROUP = "by-target-region"
FILTER_VAR_ACT = ["target_country", "location", "intention", "intended_size", "contract_size", "production_size", "negotiation_status", "implementation_status", "crops", "nature", "contract_farming", "url", "type", "company", "type"]
FILTER_VAR_INV = ["investor_name", "country"]
SINGLE_SQL_QUERY_COLUMNS = ['location', 'crop']

class TableGroupView(TemplateView):

    template_name = "group-by.html"

    LOAD_MORE_AMOUNT = 20
    DOWNLOAD_COLUMNS = ["deal_id", "target_country", "location", "investor_name", "investor_country", "intention", "negotiation_status", "implementation_status", "intended_size", "contract_size", "production_size", "nature_of_the_deal", "data_source", "contract_farming", "crop"]
    QUERY_LIMITED_GROUPS = ["target_country", "investor_name", "investor_country", "all", "crop"]
    debug_query = False
    def _set_group_value(self, **kwargs):
        self.group_value = kwargs.get("list", "")
        if self.group_value == 'none': self.group_value = ''
        if self.group_value.endswith(".csv") or kwargs.get("group", DEFAULT_GROUP).endswith(".csv"):
            self.group_value = self.group_value.split(".")[0]

    def _set_download(self, **kwargs):
        if not self.group_value: self._set_group_value(**kwargs)
        self.is_download = self.group_value.endswith(".csv") or kwargs.get("group", DEFAULT_GROUP).endswith(".csv")

    def _set_group(self, **kwargs):
        self.group = kwargs.get("group", DEFAULT_GROUP)
        if self.is_download:
            self.group = self.group.split(".")[0]
        # map url to group variable, cut possible .csv suffix
        self.group = self.group.replace("by-", "").replace("-", "_")
        if not self._filter_set() and self.group == "database":
            self.group = "all"

    def _filter_set(self):
        return self.GET and self.GET.get("filtered") and not self.GET.get("reset", None)

    def load_more(self):
        load_more = int(self.GET.get("more", 50))
        if not self._filter_set() and self.group == "database":
            load_more = None
        if not self._limit_query():
            load_more = None
        return load_more

    group_columns_list = [
        "deal_id", "target_country", "primary_investor", "investor_name", "investor_country", "intention",
        "negotiation_status", "implementation_status", "intended_size", "contract_size",
    ]

    def dispatch(self, request, *args, **kwargs):

        self.request = request
        self.GET = request.GET

        self._set_group_value(**kwargs)
        self._set_download(**kwargs)
        self._set_group(**kwargs)
        self._set_filters()
        self._set_columns()

        query_result = self.get_records(request)

        items = self.get_items(query_result, self._single_column_results(query_result))

        return self.render(items, kwargs)

    def render(self, items, kwargs):
        if self.debug_query:
            print('*****', int(self.is_download), '***', items, '*****')
        if self.is_download and items:
            return self.get_download(self.GET.get("download_format", "csv"), items)

        context = {
            "view": "get-the-detail",
            "data": {
                "items": items,
                "order_by": self._order_by(),
                "count": self.num_results
            },
            "name": self.group_value,
            "columns": self.group_value and self.group_columns_list or self._columns(),
            "filters": self.filters,
            "load_more": self._load_more_amount(),
            "group_slug": kwargs.get("group", DEFAULT_GROUP),
            "group_value": kwargs.get("list", None),
            "group": self.group.replace("_", " "),
            "empty_form_conditions": self.current_formset_conditions,
            "rules": self.rules,
        }
        return render_to_response(self.template_name, context, context_instance=RequestContext(self.request))

    def get_records(self, request):
        ap = DummyActivityProtocol()
        request.POST = MultiValueDict(
            {"data": [json.dumps({"filters": self.filters, "columns": self._optimize_columns()})]}
        )
        ap.debug = self.debug_query
        res = ap.dispatch(request, action="list_group").content
        query_result = json.loads(res.decode())

        if not self._limit_query():
            # dont limit query when download or group view
            limited_query_result = query_result["activities"]
        else:
            limited_query_result = query_result["activities"][:self.load_more()]
        self.num_results = len(query_result['activities'])
        return limited_query_result

    def _set_columns(self):
        if self.is_download and (self.group_value or self.group == "all"):
            self.columns = self.DOWNLOAD_COLUMNS
        elif self.group_value:
            self.columns = self.group_columns_list
        else:
            self.columns = self._columns()

    def _limit_query(self):
        return not (
            self.is_download
            or (not self.group_value and self.group not in self.QUERY_LIMITED_GROUPS)
            or self.GET.get("starts_with", None)
        )

    def _load_more_amount(self):
        if not self.load_more(): return None
        if self.num_results > self.load_more():
            return int(self.load_more()) + self.LOAD_MORE_AMOUNT
        return None

    def _set_filters(self):
        self.filters = {}
        ConditionFormset = self._create_condition_formset()
        if self._filter_set():
            # set given filters
            self.current_formset_conditions = ConditionFormset(self.GET, prefix="conditions_empty")
            if self.current_formset_conditions.is_valid():
                self.filters = parse_browse_filter_conditions(self.current_formset_conditions, [self._order_by()], 0)
        else:
            # set default filters
            self.rules = BrowseCondition.objects.filter(rule__rule_type="generic")
            filter_dict = self._get_filter_dict()
            self.current_formset_conditions = ConditionFormset(filter_dict, prefix="conditions_empty")
            if self.group == "database":
                self.filters = parse_browse_filter_conditions(None, [self._order_by()], None)
            else:
                # TODO: make the following line work again
                # return parse_browse_filter_conditions(current_formset_conditions, [self._order_by()], limit)
                self.filters = {}

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

    def get_download(self, download_format, items):
        if download_format == "csv":
            return self.write_to_csv(
                self.columns, self.format_items_for_download(items, self.columns), "%s.csv" % self.group
            )
        elif download_format == "xls":
            return self.write_to_xls(
                self.columns, self.format_items_for_download(items, self.columns), "%s.xls" % self.group
            )
        elif download_format == "xml":
            return self.write_to_xml(
                self.columns, self.format_items_for_download(items, self.columns), "%s.xml" % self.group
            )
        raise RuntimeError('Download format not recognized: ' + download_format)

    def get_items(self, query_result, single_column_results):
        return [ self.get_row(record, single_column_results) for record in query_result ]

    def get_row(self, record, single_column_results):
        offset = 1
        # iterate over database result
        row = {}
        for j, c in enumerate(self.columns):
            # iterate over columns relevant for view or download
            j = j + offset

            value = record[j]
            # do not remove crop column if we expect a grouping in the sql string
            if c in SINGLE_SQL_QUERY_COLUMNS and not (self.group == "crop" and c == "crop"):
                # artificially insert the data fetched from the smaller SQL query dataset, don't take it from the large set
                # Assumption deal_id is second column in row!
                offset -= 1
                if record[1] in single_column_results[c]:
                    value = single_column_results[c][record[1]]
                else:
                    value = None

            if c == "data_source":
                value = self._process_data_source(j, record)
                offset = offset + 3

            row[c] = self._process_value(c, value)
        return row

    def _process_data_source(self, j, record):
        try:
            data_sources = {
                "data_source_type": record[j],
                "data_source_url": record[j + 1],
                "data_source_date": record[j + 2],
                "data_source_organization": record[j + 3],
            }
        except IndexError as e:
            print(e.__cause__)
            print(list(zip(self.columns, record)))
            print(j)
            raise e

        return self._map_values_of_group(
            data_sources, "%(data_source_date)s%(data_source_url)s%(data_source_organization)s%(data_source_type)s"
        )

    def _process_intention(self, value):
        if not isinstance(value, list): return [value]

        intentions = {}
        for intention in set(value):
            if self.is_download:
                if intention in INTENTION_MAP and len(INTENTION_MAP.get(intention)) > 1:
                    # skip intention if there are subintentions
                    continue
                else:
                    intentions[intention] = 1
            else:
                intentions[get_intention(intention)] = 1
        return sorted(intentions.keys())

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
            'latlon': lambda value: ["%s/%s (%s)" % (n.split("#!#")[0], n.split("#!#")[1], n.split("#!#")[2]) for n in value],
            'negotiation_status': self._process_name_and_year,
            'implementation_status': self._process_name_and_year,
            "intended_size": lambda value: value and value[0],
            "production_size": lambda value: value and value[0],
            "contract_size": lambda value: value and value[0],
        }
        if c in process_functions:
            return process_functions[c](value)
        elif isinstance(value, numbers.Number):
            return int(value)
        elif not isinstance(value, list):
            return [value, ]
        return value

    def _single_column_results(self, limited_query_result):
        """ The single columns SQL queries. """
        SINGLE_SQL_QUERY_DICT = {
            'location': """
                SELECT activity_identifier, ARRAY_AGG(DISTINCT aag.attributes->'location') AS location
                FROM """+ Activity._meta.db_table + " AS a JOIN " + ActivityAttributeGroup._meta.db_table+""" AS aag ON a.id = aag.fk_activity_id
                WHERE aag.attributes ? 'location' AND activity_identifier IN (%s)
                group by activity_identifier;
             """,
            'crop': """
                SELECT activity_identifier, ARRAY_AGG(DISTINCT CONCAT(crops.name, '#!#', crops.code )) AS crop
                FROM """ + Activity._meta.db_table + " AS a JOIN " + ActivityAttributeGroup._meta.db_table+""" AS aag ON a.id = aag.fk_activity_id
                JOIN """ + Crop._meta.db_table + """ AS crops ON CAST(aag.attributes->'crops' AS NUMERIC) = crops.id
                WHERE aag.attributes ? 'crops' and activity_identifier in (%s)
                group by activity_identifier;
             """
        }

        single_column_results = {}
        activity_ids = None
        for col in SINGLE_SQL_QUERY_COLUMNS:
            # do not remove crop column if we expect a grouping in the sql string
            if col not in self.columns or (self.group == "crop" and col == "crop"):
                continue
            # get the activity ids from the large sql dataset
            # Assumption: dataset contains column deal_id in second column
            activity_ids = activity_ids or [str(row[0 + 1]) for row in limited_query_result]
            if activity_ids:
                cursor = connection.cursor()
                sql = SINGLE_SQL_QUERY_DICT[col] % (','.join(activity_ids))
                cursor.execute(sql)
                single_column_results.update({col: dict(cursor.fetchall())})
        return single_column_results

    def _order_by(self):
        order_by = self.GET.get("order_by", self.group_value and "deal_id" or self.group) \
                   or self.group_value and "deal_id" \
                   or self.group
        if order_by == "all" or order_by == "database":
            order_by = "deal_id"
        return order_by

    """ IMPORTANT! we are patching certain column fields out, so they don't get executed within the large SQL query.
        instead we later send a single query for each column and add the resulting data back into the large result object"""
    def _optimize_columns(self):
        from copy import deepcopy
        if any(special_column in self.columns for special_column in SINGLE_SQL_QUERY_COLUMNS):
            optimized_columns = deepcopy(self.columns)
            for col in SINGLE_SQL_QUERY_COLUMNS:
                # do not remove crop column if we expect a grouping in the sql string
                if self.group == "crop" and col == "crop":
                    continue
                if col in self.columns:
                    optimized_columns.remove(col)
        else:
            optimized_columns = self.columns
        return optimized_columns

    def _create_condition_formset(self):
        from django.forms.formsets import formset_factory
        from django.utils.functional import curry

        ConditionFormset = formset_factory(BrowseConditionForm, extra=0)
        ConditionFormset.form = staticmethod(
            curry(BrowseConditionForm, variables_activity=FILTER_VAR_ACT, variables_investor=FILTER_VAR_INV)
        )
        return ConditionFormset

        #return None

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
            "all": ["deal_id", "target_country", "primary_investor", "investor_name", "investor_country",
                    "intention", "negotiation_status", "implementation_status", "intended_size",
                    "contract_size", ]
        }
        return columns[self.group]

    def write_to_xls(self, header, data, filename):
        response = HttpResponse(mimetype="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Landmatrix')
        for i,h in enumerate(header):
            ws.write(0, i,h)
        for i, row in enumerate(data):
            for j, d in enumerate(row):
                ws.write(i+1, j, d)
        wb.save(response)
        return response

    def write_to_xml(self, header, data, filename):
        root = ET.Element('data')
        for r in data:
            row = ET.SubElement(root, "item")
            for i,h in enumerate(header):
                field = ET.SubElement(row, "field")
                field.text = unicode(r[i])
                field.set("name", h)
        tree = ET.ElementTree(root)
        xml = parseString(ET.tostring(root)).toprettyxml()
        response = HttpResponse(xml, mimetype='text/xml')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response

    def write_to_csv(self, header, data, filename):
#        response = HttpResponse(mimetype='text/csv')
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        writer = csv.writer(response, delimiter=";")
        # write csv header
        writer.writerow(header)
        for row in data:
            writer.writerow([unicode(s).encode("utf-8") for s in row])
        return response

    """
    Format the data of the items to a propper download format.
    Returns an array of arrays, each row is an an array of data
    """
    def format_items_for_download(self, items, columns):
        rows = []
        for item in items:
            row = []
            for c in columns:
                v = item.get(c)
                row_item = []
                if isinstance(v, (tuple, list)):
                    for lv in v:
                        if isinstance(lv, dict):
                            year = lv.get("year", None)
                            name = lv.get("name", None)
                            if year and year != "0" and name:
                                row_item.append("[%s] %s" % (year, name))
                            elif name:
                                row_item.append(name)
                        elif isinstance(lv, (list, tuple)):
            # Some vars take additional data for the template (e.g. investor name = {"id":1, "name":"Investor"}), export just the name
                            if len(lv) > 0 and isinstance(lv[0], dict):
                                year = lv.get("year", None)
                                name = lv.get("name", None)
                                if year and year != "0" and name:
                                    row_item.append("[%s] %s" % (year, name))
                                elif name:
                                    row_item.append(name)
                            else:
                                row_item.append(lv)
                        else:
                            row_item.append(lv)
                    row.append(", ".join(filter(None, row_item)))
                else:
                    row.append(v)
            rows.append(row)
        return rows

    """
    Map different values of one group together. Ensures that values of a group are together
    e.g. group of data sources with different urls, types and dates
    """
    def _map_values_of_group(self, value_list, format_string):
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

