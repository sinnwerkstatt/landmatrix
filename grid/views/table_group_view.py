from collections import OrderedDict

from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.template.defaultfilters import slugify
from wagtailcms.models import WagtailRootPage

from grid.views.filter_widget_mixin import FilterWidgetMixin
from grid.views.browse_filter_conditions import get_field_label
from grid.forms.choices import intention_choices, INTENTION_AGRICULTURE_MAP, INTENTION_FORESTRY_MAP
from landmatrix.models import Country, Region, Crop
from api.views import ElasticSearchMixin


INTENTION_MAP = {}
for choice, value in intention_choices:
    if choice in INTENTION_AGRICULTURE_MAP.keys():
        INTENTION_MAP[choice] = {
            'value': _('Agriculture'),
            'slug': 'agriculture',
            'order_by': _('Agriculture'),
        }
    elif choice in INTENTION_FORESTRY_MAP.keys():
        INTENTION_MAP[choice] = {
            'value': _('Forestry'),
            'slug': 'forestry',
            'order_by': _('Forestry'),
        }
    INTENTION_MAP[choice] = {
        'value': value,
        'slug': slugify(choice),
        'order_by': value,
        #'is_parent': choices and len(choices) > 0
    }
    #if not choices:
    #    continue
    #for schoice, svalue in choices:
    #    INTENTION_MAP[schoice] = {
    #        'value': svalue,
    #        'slug': slugify(schoice),
    #        'parent': value,
    #        'order_by': '%s (%s)' % (value, svalue),
    #    }


class TableGroupView(FilterWidgetMixin, ElasticSearchMixin, TemplateView):

    LOAD_MORE_AMOUNT = 20
    QUERY_LIMITED_GROUPS = ["target_country", "operational_stakeholder_name",
                            "parent_stakeholder_country", "all", "crop"]
    DEFAULT_GROUP = "by-target-region"
    COLUMN_GROUPS = {
        "target_country": ["target_country_display", "target_region_display", "intention"],
        "target_region": ["target_region_display", "intention"],
        "investor_name": ["operating_company_investor_identifier", "operating_company_name",
                          "operating_company_fk_country_display", "intention"],
        "investor_country": ["investor_country_display", "intention"],
        "investor_region": ["investor_region_display",],
        "intention": ["intention",],
        "crop": ["crops",],
        "year": ["year", "intention"],
        "data_source_type": ["type", "intention"],
        "all": ["activity_identifier", "target_country_display", "top_investors",
                #"operating_company_fk_country_display",
                "intention", "current_negotiation_status_display",
                "current_implementation_status_display",
                "deal_size"] #"intended_size", "contract_size", ]
    }
    GROUP_COLUMNS_LIST = COLUMN_GROUPS["all"]
    GROUP_NAMES = {
        "operational_stakeholder_name": _("Investor name"),
        #"operational_stakeholder_country": _("Investor country"),
        #"operational_stakeholder_region": _("Investor region"),
    }
    COLUMN_LABELS_MAP = {
        # Activity
        'activity_identifier': _('ID'),
        'deal_count': _('Deals'),
        'availability': _('Availability'),
        'deal_size': _('Deal size'),
        'top_investors': _("Top investors"),
        'current_negotiation_status': _('Negotiation status'),
        'current_implementation_status': _('Implementation status'),
        'target_region': _('Target region'),
        # Activity overwrites
        'crops': _('Crops'),
        'type': _('Data source type'),
        # Investors
        # 'operational_stakeholder_country': _('Operating company country'),
        # 'operational_stakeholder_region': _('Operating company region'),
        'operational_stakeholder': _('Operating company'),
        'investor_country': _('Investor country'),
        'investor_region': _('Investor region'),
        'investor_id': _('Investor ID'),
        'investor_name': _('Investor name'),
        'operational_stakeholder_name': _('Operating company name'),
        'parent_stakeholder': _('Parent investors'),
        'parent_stakeholder_country': _('Parent investor country'),
        'parent_stakeholder_region': _('Parent investor region'),
        'parent_stakeholder_percentage': _('Parent investor percentages'),
        'parent_stakeholder_classification': _(
            'Parent investor classifications'),
        'parent_stakeholder_homepage': _('Parent investor homepages'),
        'parent_stakeholder_opencorporates_link': _(
            'Parent stakeholder Opencorporates links'),
        'parent_stakeholder_comment': _('Comment on parent investor'),
        'operating_company_investor_identifier': _('ID'),
        'operating_company_fk_country': _("Operating company country of registration/origin"),
        'operating_company_region': _("Operating company region of registration/origin"),
        'operating_company_classification': _("Operating company classification"),
        'operating_company_homepage': _("Operating company homepage"),
        'operating_company_opencorporates_link': _("Operating company Opencorporates link"),
        'operating_company_comment': _("Additional comment on Operating company"),
    }

    template_name = "group-by.html"
    debug_query = False
    group = None
    group_value = None

    def get_context_data(self, group, group_value=None):
        self.group = group or self.DEFAULT_GROUP
        self.group = self.group.replace("by-", "").replace("-", "_")
        self.group_value = group_value or ''
        context = super(TableGroupView, self).get_context_data()

        root = WagtailRootPage.objects.first()
        if root.data_introduction:
            context['introduction'] = root.data_introduction

        items = self.get_records()
        items = self.get_items(items)
        context.update({
            "view": "data",
            "data": {
                "items": items,
                "order_by": self.order_by,
                "count": self.num_results
            },
            "name": self.group_value,
            "columns": self.columns_dict,
            "load_more": self._load_more_amount(),
            "group_slug": self.group,
            "group_value": self.group_value,
            "group": self.GROUP_NAMES.get(self.group, self.group),
        })

        return context

    def get_records(self):
        query = self.create_query_from_filters()
        aggs = {}
        if self.group == 'all':
            order_by = self.order_by
        elif self.group_value:
            query = self.get_group_value_query(query)
            order_by = self.order_by
        else:
            query, aggs = self.get_group_aggs(query)
            # Order by is set in aggregation
            order_by = None

        # Search deals
        results = self.execute_elasticsearch_query(query, doc_type='deal', fallback=False,
                                                 sort=order_by, aggs=aggs)

        if aggs:
            results = results[self.group]['buckets']
        else:
            results = self.filter_returned_results(results)

        self.num_results = len(results)

        if self.limit_query():
            results = results[:self._load_more()]

        return results

    def get_group_value_query(self, query):
        if not 'bool' in query:
            query['bool'] = {}
        if not 'filter' in query['bool']:
            query['bool']['filter'] = []
        # Deslugify model choices
        if 'country' in self.group:
            country = Country.objects.get(slug=self.group_value)
            filter_value = country.id
        elif 'region' in self.group:
            region = Region.objects.get(slug=self.group_value)
            filter_value = region.id
        elif 'crop' in self.group:
            crop = Crop.objects.get(slug=self.group_value)
            filter_value = crop.id
        else:
            filter_value = self.group_value
        filter_field = self.COLUMN_GROUPS[self.group][0].replace('_display', '')
        query['bool']['filter'].append({
            'bool': {
                'filter': {
                    'term': {
                        filter_field: filter_value
                    }
                }
            }
        })
        return query

    def get_group_aggs(self, query):
        fields = self.COLUMN_GROUPS.get(self.group)
        aggs = {
            self.group: {
                'terms': {
                    'field': fields[0],
                    'size': 1000,
                    'order': self.order_by,
                },
                'aggs': {
                    'deal_size_sum': {
                        'sum': {
                            'field': 'deal_size'
                        }
                    },
                    'availability_avg': {
                        'avg': {
                            'field': 'availability'
                        }
                    }
                }
            }
        }
        # Add extra field for non-display value (required for filter)
        if '_display' in fields[0]:
            field = fields[0].replace('_display', '')
            aggs[self.group]['aggs'][field] = {
                'terms': {
                    'field': field
                }
            }
        # Collect terms for all other fields
        for field in fields[1:]:
            aggs[self.group]['aggs'][field] = {
                'terms': {
                    'field': field
                }
            }
        # Exclude empty
        if self.group != 'investor_name':
            query['bool']['must_not'].append({
                'term': {
                    fields[0]: ""
                }
            })
        return query, aggs

    def limit_query(self):
        """ Don't limit query when group view or export."""
        return not (
            (not self.group_value and self.group not in self.QUERY_LIMITED_GROUPS)
            or self.request.GET.get("starts_with", None)
        )

    def _load_more(self):
        load_more = int(self.request.GET.get("more", 50))
        if not self._filter_set(self.request.GET) and self.group == "database":
            load_more = None
        if not self.limit_query():
            load_more = None
        return load_more

    def _load_more_amount(self):
        if not self._load_more(): return None
        if self.num_results > self._load_more():
            return int(self._load_more()) + self.LOAD_MORE_AMOUNT
        return None

    def get_columns(self):
        columns = []
        if self.request.GET.get('columns'):
            columns = self.request.GET.getlist('columns')
            if 'activity_identifier' not in columns:
                columns = ['activity_identifier'] + columns
        elif self.group_value:
            columns = self.GROUP_COLUMNS_LIST
        else:
            try:
                columns = self.COLUMN_GROUPS[self.group]
                if self.group != 'all':
                    columns += ('deal_count', 'deal_size', 'availability')
            except KeyError:
                raise Http404(
                    _("Unknown group '%(group)s'.") % {'group': self.group})
        return columns

    @property
    def columns(self):
        return [c.replace('_display', '') for c in self.get_columns()]

    @property
    def columns_dict(self):
        """Get column information for template"""
        # Labels for all custom fields (fields that are not part of any form)
        columns = OrderedDict()
        order_by = self.get_order_by_field()[0]
        for i, name in enumerate(self.get_columns()):
            label = None
            column = name.replace('_display', '')
            if column in self.COLUMN_LABELS_MAP.keys():
                label = self.COLUMN_LABELS_MAP[column]
            else:
                label = get_field_label(column)
            columns[column] = {
                'label': label,
                'name': column,
            }
            if self.group != 'all' and not self.group_value:
                order_by_columns = ('deal_count', 'deal_size', 'availability')
                if i == 0 or name in order_by_columns:
                    columns[column]['order_by'] = '-'+name if name == order_by else name
            else:
                columns[column]['order_by'] = '-'+name if name == order_by else name

        return columns

    @property
    def filters(self):
        data = self.request.GET.copy()
        return self.get_filter_context(
            self.current_formset_conditions,
            self.order_by,
            self.group,
            self.group_value,
            data.get("starts_with")
        )

    @property
    def current_formset_conditions(self):
        data = self.request.GET.copy()
        return self.get_formset_conditions(
            self._filter_set(data), data, self.group
        )

    def get_items(self, results):
        if self.group and self.group != 'all' and not self.group_value:
            items = [self.get_group_item(item) for item in results]
            # Reorder required for intention (because subcategories have been renamed in _process_intention)
            #if self.group == 'intention' and not self.group_value:
            #    items_by_intention = dict((len(i['intention']) > 0 and str(i['intention'][
            # 'value'] or ''), i) for i in items)
            #    # Add extra lines for groups (agriculture and forestry)
            #    items = []
            #    for group_name, choices in grouped_intention_choices:
            #        group = OrderedDict()
            #        group['intention'] = [{'value': group_name, 'slug':slugify(group_name)},]
            #        group['deal_count'] = 0
            #        group['availability'] = 0
            #        group['availability_count'] = 0
            #        group_items = []
            #        for choice_value, choice_label in choices:
            #            if choice_label in items_by_intention.keys():
            #                item = items_by_intention[choice_label]
            #                item['intention']['parent'] = group
            #                group_items.append(item)
            #                group['deal_count'] += item['deal_count'][0]
            #                group['availability'] += item['availability'][0] or 0
            #                group['availability_count'] += 1
            #            else:
            #                item = OrderedDict()
            #                item['intention'] = [{'value': choice_label, 'slug':slugify(
            # choice_label), 'parent': group},]
            #                item['deal_count'] = 0
            #                item['availability'] = 0
            #                group_items.append(item)
            #        if group['availability']:
            #            group['availability'] = int(round(group['availability'] / group[
            # 'availability_count']))
            #            del group['availability_count']
            #        items.append(group)
            #        items.extend(group_items)
        else:
            items = [self.get_deal_item(item) for item in results]
        return items

    def get_deal_item(self, result):
        item = OrderedDict()
        for column in self.get_columns():
            if column in ('target_country', 'current_negotiation_status',
                          'current_implementation_status'):
                column += '_display'
            value = result.get(column, None)
            if value and hasattr(self, 'clean_{}'.format(column)):
                value = getattr(self, 'clean_{}'.format(column))(value, result)
            if not isinstance(value, (list, tuple)):
                value = [value,]
            column = column.replace('_display', '')
            item[column] = value
        return item

    def get_group_item(self, result):
        item = OrderedDict()
        columns = self.COLUMN_GROUPS[self.group]
        for i, column in enumerate(columns):
            if i == 0:
                value = {
                    'display': result['key'],
                    'value': result['key'],
                }
                column = column.replace('_display', '')
                if '_display' in columns[i]:
                    value['value'] = result[column]['buckets'][0]['key']
                if value and hasattr(self, 'clean_{}'.format(column)):
                    value = getattr(self, 'clean_{}'.format(column))(value, result)
                item[column] = value
            else:
                if column in result:
                    value = [i['key'] for i in result[column]['buckets']]
                else:
                    value = ''
                column = column.replace('_display', '')
                if value and hasattr(self, 'clean_{}'.format(column)):
                    value = getattr(self, 'clean_{}'.format(column))(value, result)
                if not isinstance(value, (list, tuple)):
                    value = [value, ]
                item[column] = value
        item['deal_count'] = [result['doc_count'],]
        item['deal_size'] = [int(result['deal_size_sum']['value']),]
        item['availability'] = [result['availability_avg']['value'],]
        return item

    def get_order_by_field(self):
        order_by = self.request.GET.getlist('order_by', [])
        if len(order_by) > 0 and order_by[0]:
            return order_by
        elif self.group and self.group != 'all' and not self.group_value:
            return [self.columns[0],]
        else:
            return ['activity_identifier',]

    @property
    def order_by(self):
        order_by = self.get_order_by_field()
        order_by = order_by[0]
        if order_by.startswith('-'):
            dir = 'desc'
            order_by = order_by[1:]
        else:
            dir = 'asc'
        if self.group != 'all' and not self.group_value:
            ORDER_MAP = {
                self.columns[0]: '_term',
                'deal_count': '_count',
                'deal_size': 'deal_size_sum',
                'availability': 'availability_avg',
            }
            order_by = ORDER_MAP.get(order_by, order_by)
        order_by = {order_by: dir}
        return order_by

    def clean_top_investors(self, value, result):
        investors = []
        for investor in value.split('|'):
            investor = investor.split('#')
            investors.append({'id': investor[0], 'name': investor[1]})
        return investors

    def clean_intention(self, value, result):
        if isinstance(value, (list, tuple)):
            intentions = [INTENTION_MAP.get(intention) for intention in value]
            return list(filter(None, intentions))
        elif isinstance(value, dict):
            if value['value'] in INTENTION_MAP:
                intention = INTENTION_MAP.get(value['value'])
                return {
                    'value': intention['value'],
                    'display': intention['value'],
                    'is_parent': False,
                }
            else:
                value['is_parent'] = True
                return value

    def clean_crops(self, value, result):
        if isinstance(value, dict):
            crop = Crop.objects.get(pk=value['value']).name
            return {
                'value': crop,
                'display': crop,
            }
        else:
            return Crop.objects.get(pk=value).name

    #def clean_target_country_display(self, value, result):
    #    values = list(zip(result.get('target_country', []), value))
    #    return values

    #def clean_target_region_display(self, value, result):
    #    values = list(zip(result.get('target_region', []), value))
    #    return values

    #def clean_investor_country_display(self, value, result):
    #    values = list(zip(result.get('investor_country', []), value))
    #    return values

    #def clean_investor_region_display(self, value, result):
    #    values = list(zip(result.get('investor_region', []), value))
    #    return values

    # def _process_investor_name(self, value):
    #     if not isinstance(value, list):
    #         value = [value]
    #     result = [
    #         {"name": inv.split("#!#")[0], "id": inv.split("#!#")[1]} if len(inv.split("#!#")) > 1 else inv
    #         for inv in value
    #     ]
    #     return result
    #
    # def _process_investor_classification(self, values):
    #     if not isinstance(values, list):
    #         values = [values]
    #
    #     processed = []
    #
    #     for value in values:
    #         processed_value = None
    #
    #         for choice in Investor.CLASSIFICATION_CHOICES:
    #             code, label = choice
    #             if str(code) == str(value):
    #                 processed_value = label
    #                 break
    #
    #         processed.append(processed_value or _('Unknown'))
    #
    #     return processed
    #
    # def _process_stitched_together_field(self, value):
    #     if not isinstance(value, list):
    #         value = [value]
    #     return [field and field.split("#!#")[0] or "" for field in value]
    #
    # def _process_year_based(self, value):
    #     split_values = [
    #         {
    #             "name": n.split("#!#")[0],
    #             "year": n.split("#!#")[1],
    #             "current": n.split("#!#")[2],
    #         } for n in value
    #     ]
    #
    #     # Sort values by year (last one is usually displayed)
    #     return sorted(split_values, key=lambda v: v['year'])
