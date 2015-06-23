__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.views.generic import TemplateView
from django.utils.datastructures import MultiValueDict

import json, numbers

from landmatrix.models import BrowseCondition
from global_app.views.browse_condition_form import BrowseConditionForm
from global_app.views.dummy_activity_protocol import DummyActivityProtocol

DEFAULT_GROUP = "by-target-region"

FILTER_VAR_ACT = ["target_country", "location", "intention", "intended_size", "contract_size", "production_size", "negotiation_status", "implementation_status", "crops", "nature", "contract_farming", "url", "type", "company", "type"]
FILTER_VAR_INV = ["investor_name", "country"]
SINGLE_SQL_QUERY_COLUMNS = ['location', 'crop']

def parse_browse_filter_conditions(formset, order_by=None, limit=None):
    data = {
        "activity": {},
        "deal_scope": "",
        "investor": {},
        "order_by": [],
        "limit": "",
    }
    filters_act, filters_inv = {"tags":{}}, {"tags":{}}
    if formset:
        for i, form in enumerate(formset):
            fl = {}
            for j, (n, f) in enumerate(form.fields.items()):
                key = "%s-%d-%s"%(formset.prefix, i, n)
                if n == "value":
                    # is ybd field?
                    if formset.data.has_key("%s_0"%key):
                        # just take the first row of the field
                        value = formset.data.getlist("%s_0"%key)
                        year = formset.data.get("%s_1"%key)
                        fl.update({n:value, "year":year})
                    else:
                        value = formset.data.getlist(key)
                        fl.update({n:value})
                else:
                    value = formset.data.get(key)
                    fl.update({n:value})
            variable = fl.get("variable")
            op = fl.get("operator")
            values = fl.get("value")
            year = fl.get("year")
            #skip if no variable is selected
            if not variable:
                continue
            # variable is identifier
            if variable == "-1":
                identifier_filter = filters_act.get("identifier", [])
                identifier_filter.append({
                    "value": values[0] or "0",
                    "op": op,
                })
                filters_act["identifier"] = identifier_filter
            elif variable == "-2":
                # deal scope
                if len(values) == 2:
                    data["deal_scope"] = "all"
                elif len(values) == 1:
                    data["deal_scope"] = values[0] == "10" and "domestic" or values[0] == "20" and "transnational" or ""
            elif "inv_" in variable:
                variable = variable[4:]
                f = get_field_by_sh_key_id(variable)
                values = [year and "%s##!##%s" % (get_display_value_by_field(f, value), year) or get_display_value_by_field(f, value) for value in values]
                if f and "Region" in f.label:
                    # region values not stored at activity/investor
                    variable = "region"
                elif f and "Country" in f.label:
                    # countries are referred by keys
                    values = fl.get("value")
                filters_inv["tags"].update({"%s%s" % (variable, op and "__%s" % op or op): values})
            else:
                f = get_field_by_a_key_id(variable)
                if year:
                    values = ["%s##!##%s" % (get_display_value_by_field(f, value), year)]
                else:
                    values = [get_display_value_by_field(f, value) for value in values]
                if f:
                    if "Region" in f.label:
                        # region values not stored at activity/investor
                        variable = "region"
                    elif "Country" in f.label or "Crops" in f.label:
                        # countries and crops are referred by keys
                        values = fl.get("value")
                    elif "Negotiation status" in f.label:
                        variable = "pi_negotiation_status"
                filters_act["tags"].update({"%s%s" % (variable, op and "__%s" % op or op): values})
        data["activity"] = filters_act
        data["investor"] = filters_inv
    if order_by:
        for field in order_by:
            field_pre = ""
            field_GET = ""
            if len(field) > 0 and field[0] == "-":
                field_pre = "-"
                field = field[1:]
            try:
                if "Investor " in field:
                    form = get_field_by_sh_key_id(SH_Key.objects.get(key=field[9:]).id)
                else:
                    form = get_field_by_a_key_id(A_Key.objects.get(key=field).id)
                if isinstance(form, IntegerField):
                    field_GET = "+0"
            except:
                pass
            data["order_by"].append("%s%s%s" % (field_pre, field, field_GET))
    if limit:
        data["limit"] = limit
    return data


class TableGroupView(TemplateView):

    template_name = "getthedetail/table/group-by.html"
    LOAD_MORE_AMOUNT = 20
    DOWNLOAD_COLUMNS = ["deal_id", "target_country", "location", "investor_name", "investor_country", "intention", "negotiation_status", "implementation_status", "intended_size", "contract_size", "production_size", "nature_of_the_deal", "data_source", "contract_farming", "crop"]
    QUERY_LIMITED_GROUPS = ["target_country", "investor_name", "investor_country", "all", "crop"]


    def dispatch(self, request, *args, **kwargs):
        is_download = False
        context = {}
        GET = request.GET
        group = kwargs.get("group", DEFAULT_GROUP)
        group_value = kwargs.get("list", "")
        if group_value.endswith(".csv") or group.endswith(".csv"):
            is_download = True
            group = group.split(".")[0]
            group_value = group_value.split(".")[0]
            download_format = GET.get("download_format", "csv")
        # map url to group variable, cut possible .csv suffix
        group = group.replace("by-", "").replace("-", "_")
        items, query_result, filters = [], [], {}
        variables_activity, variables_investor = None, None
        name = group_value.split(".")[0]
        order_by = GET.get("order_by", group_value and "deal_id" or group) or group_value and "deal_id" or group
        starts_with = GET.get("starts_with", None)
        limit = 0
        load_more = int(GET.get("more", 50))
        if order_by == "all" or order_by == "database":
            order_by = "deal_id"
        variables_activity = ["target_country", "intention", "crops", "intended_size"]
        variables_investor = ["investor_name", "country"]
        group_columns_list = []
        ConditionFormset = self.create_condition_formset()
        rules = BrowseCondition.objects.filter(rule__rule_type="generic")
        if GET and GET.get("filtered") and not GET.get("reset", None):
            # set given filters
            current_formset_conditions = ConditionFormset(GET, prefix="conditions_empty")
            if current_formset_conditions.is_valid():
                filters = parse_browse_filter_conditions(current_formset_conditions, [order_by], limit)
        else:
            # set default filters
            filter_dict = MultiValueDict()
            for record, c in enumerate(rules):
                rule_dict = MultiValueDict({
                    "conditions_empty-%i-variable"% record: [c.variable],
                    "conditions_empty-%i-operator"% record: [c.operator]
                })
                # pass comma separated list as multiple values for operators in/not in
                if c.operator in ("in", "not_in"):
                    rule_dict.setlist("conditions_empty-%i-value"%record, c.value.split(","))
                else:
                    rule_dict["conditions_empty-%i-value"%record] = c.value
                filter_dict.update(rule_dict)
            filter_dict["conditions_empty-INITIAL_FORMS"] = len(rules)
            filter_dict["conditions_empty-TOTAL_FORMS"] = len(rules)
            filter_dict["conditions_empty-MAX_NUM_FORMS"] = ""
            current_formset_conditions = ConditionFormset(filter_dict, prefix="conditions_empty")
            if group == "database":
                filters = parse_browse_filter_conditions(None, [order_by], None)
                group = "all"
                load_more = None
            else:
                filters = parse_browse_filter_conditions(current_formset_conditions, [order_by], limit)
        group_columns = self._columns(group)
        # columns shown in deal list
        group_columns_list = ["deal_id", "target_country", "primary_investor", "investor_name", "investor_country", "intention", "negotiation_status", "implementation_status", "intended_size", "contract_size",]
        columns = (is_download and (group_value or group == "all") and self.DOWNLOAD_COLUMNS) or (group_value and group_columns_list) or group_columns
        filters["group_by"] = group
        filters["group_value"] = group_value
        filters["starts_with"] = starts_with
        ap = DummyActivityProtocol()
        """ IMPORTANT! we are patching certain column fields out, so they don't get executed within the large SQL query.
            instead we later send a single query for each column and add the resulting data back into the large result object """
        if any(special_column in columns for special_column in SINGLE_SQL_QUERY_COLUMNS):
            optimized_columns = deepcopy(columns)
            for col in SINGLE_SQL_QUERY_COLUMNS:
                # do not remove crop column if we expect a grouping in the sql string
                if group == "crop" and col == "crop":
                    continue
                if col in columns:
                    optimized_columns.remove(col)
        else:
            optimized_columns = columns

        request.POST = MultiValueDict({"data": [json.dumps({"filters": filters, "columns": optimized_columns})]})
        res = ap.dispatch(request, action="list_group").content
        print(res[:100])
        query_result = json.loads(res.decode())
        print(query_result['activities'][:10])

        if is_download or (not group_value and group not in self.QUERY_LIMITED_GROUPS) or starts_with:
            # dont limit query when download or group view
            limited_query_result =  query_result["activities"]
            load_more = None
        else:
            limited_query_result =  query_result["activities"][:load_more]

        single_column_results = {}
        activity_ids = None
        for col in SINGLE_SQL_QUERY_COLUMNS:
            # do not remove crop column if we expect a grouping in the sql string
            if col not in columns or (group == "crop" and col == "crop"):
                continue
            # get the activity ids from the large sql dataset
            # Assumption: dataset contains column deal_id in second column
            activity_ids = activity_ids or [str(row[0 + 1]) for row in limited_query_result]
            if activity_ids:
                cursor = connection.cursor()
                sql = SINGLE_SQL_QUERY_DICT[col] % (','.join(activity_ids))
                cursor.execute(sql)
                single_column_results.update({col: dict(cursor.fetchall())})

        for record in limited_query_result:
            offset = 1
            # iterate over database result
            if not record[0]:
                continue
            name = record[0]
            row = {}
            for j,c in enumerate(columns):
                print(record, j, c)
                # iterate over columns relevant for view or download
                j = j + offset
                # do not remove crop column if we expect a grouping in the sql string
                if c in SINGLE_SQL_QUERY_COLUMNS and not (group == "crop" and c == "crop"):
                    # artificially insert the data fetched from the smaller SQL query dataset, don't take it from the large set
                    # Assumption deal_id is second column in row!
                    offset -= 1
                    if record[1] in single_column_results[c]:
                        value = single_column_results[c][record[1]]
                    else:
                        value = None
                else:
                    value = record[j]

                if not value:
                    if c == "data_source":
                        offset = offset + 3
                    row.update({c: None})
                    continue
                if c == "data_source":
                    data_sources = {
                        "data_source_type": record[j],
                        "data_source_url": record[j+1],
                        "data_source_date": record[j+2],
                        "data_source_organization": record[j+3],
                    }
                    value = self.map_values_of_group(data_sources,  "%(data_source_date)s%(data_source_url)s%(data_source_organization)s%(data_source_type)s")
                    offset = offset + 3
                elif c == "intention":
                    # raise Exception, value
                    intentions = {}
                    for intention in set(value.split("##!##")):
                        if is_download:
                            if intention in INTENTION_MAP and len(INTENTION_MAP.get(intention)) > 1:
                                # skip intention if there are subintentions
                                continue
                            else:
                                intentions[intention] = 1
                        else:
                            intentions[get_intention(intention)] = 1
                    value = sorted(intentions.keys())
                elif c == "investor_name":
                    value = [len(inv.split("#!#")) > 1 and {"name": inv.split("#!#")[0],"id": inv.split("#!#")[1]} or "" for inv in value.split("##!##")]
                elif c == 'location':
                    value = value.split("##!##")
                elif c == "investor_country":
                    value = [inv.split("#!#")[0] for inv in value.split("##!##")]
                elif c == "investor_region":
                    value = [inv.split("#!#")[0] for inv in value.split("##!##")]
                elif c == 'crop':
                    value = [n.split("#!#")[0] for n in value.split("##!##")]
                elif c == 'latlon':
                    value = ["%s/%s (%s)" % (n.split("#!#")[0],n.split("#!#")[1], n.split("#!#")[2])  for n in value.split("##!##")]
                elif c == "negotiation_status":
                    value = [{"name": n.split("#!#")[0],"year": n.split("#!#")[1]} for n in value.split("##!##")]
                elif c == "implementation_status":
                    value = [{"name": n.split("#!#")[0],"year": n.split("#!#")[1]} for n in value.split("##!##")]
                elif c in ("intended_size", "production_size", "contract_size"):
                    value = value and value.split(",")[0]
                elif isinstance(value, numbers.Number):
                    value = int(value)
                elif "##!##" in value:
                    value = value.split("##!##")
                else:
                    # ensure array
                    value = [value,]
                row.update({c: value})
            items.append(row)
        if is_download and items:
            if download_format == "csv":
                return self.write_to_csv(columns, self.format_items_for_download(items, columns), "%s.csv" % group)
            elif download_format == "xls":
                return self.write_to_xls(columns, self.format_items_for_download(items, columns), "%s.xls" % group)
            elif download_format == "xml":
                return self.write_to_xml(columns, self.format_items_for_download(items, columns), "%s.xml" % group)

        else:
            context.update({
                "view": "get-the-detail",
                "data": {
                    "items": items,
                    "order_by": order_by,
                    "count": len(query_result["activities"])
                },
                "name": name,
                "columns": group_value and group_columns_list or group_columns,
                "filters": filters,
                "load_more": load_more and len(query_result["activities"]) > load_more and load_more + self.LOAD_MORE_AMOUNT or None,
                "group_slug": kwargs.get("group", DEFAULT_GROUP),
                "group_value": kwargs.get("list", None),
                "group": group.replace("_", " "),
                "empty_form_conditions": current_formset_conditions,
                "rules": rules,
            })
            return render_to_response(self.template_name, context,
                                      context_instance=RequestContext(request))

    def create_condition_formset(self):
        from django.forms.formsets import formset_factory
        from django.utils.functional import curry

        ConditionFormset = formset_factory(BrowseConditionForm, extra=0)
        ConditionFormset.form = staticmethod(
            curry(BrowseConditionForm, variables_activity=FILTER_VAR_ACT, variables_investor=FILTER_VAR_INV)
        )
        return ConditionFormset

        #return None

    def _columns(self, group):
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
        return columns[group]

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
        response = HttpResponse(mimetype='text/csv')
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
                    row.append(", ".join(row_item))
                else:
                    row.append(v)
            rows.append(row)
        return rows

    """
    Map different values of one group together. Ensures that values of a group are together
    e.g. group of data sources with different urls, types and dates
    """
    def map_values_of_group(self, value_list, format_string):
        output = []
        groups = {}
        keys = value_list.keys()
        for k,v in value_list.items():
            if not v:
                continue
            for s in v.split("##!##"):
                if "#!#" not in s:
                    continue
                gv = s.split("#!#")[0]
                g = s.split("#!#")[1]
                group = groups.get(g, {})
                group.update({
                    k: gv + " "
                })
                groups[g] = group
        for g,gv in groups.items():
            for k in keys:
                if k not in gv:
                    gv.update({k:""})
            output.append(format_string % gv)
        return output


class AllDealsView(TableGroupView):

    def dispatch(self, request, type, *args, **kwargs):
        kwargs["group"] = "all%s" % (type and type or "")
        return super(AllDealsView, self).dispatch(request, *args, **kwargs)
