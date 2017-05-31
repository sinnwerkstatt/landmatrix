try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import unicodecsv as csv

from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict
from openpyxl import Workbook

from grid.views import AllDealsView, TableGroupView, DealDetailView, ChangeDealView
from api.views import ElasticSearchView


class ExportView(ElasticSearchView):
    # TODO: XLS is deprecated, should be removed in templates
    FORMATS = ['csv', 'xml', 'xls', 'xlsx']

    def get(self, request, *args, **kwargs):
        format = kwargs.pop('format')
        if format == 'xls':
            format = 'xlsx'
        query = self.create_query_from_filters()
        raw_result_list = self.execute_elasticsearch_query(query)

        # filter results
        items = self.filter_returned_results(raw_result_list)

        if format not in self.FORMATS:
            raise RuntimeError('Download format not recognized: ' + format)

        filename = 'export'
        return getattr(self, 'export_%s' % format)(
            self.get_data(items),
            "%s.%s" % (filename, format)
        )

    def export_xlsx(self, data, filename):
        response = HttpResponse(content_type="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        wb = Workbook()
        ws_deals = wb.create_sheet(title='Deals')
        ws_deals.append(data['headers'])
        for i, row in enumerate(data['items']):
            ws_deals.append(row)
        ws_involvements = wb.create_sheet(title='Involvements')
        ws_investors = wb.create_sheet(title='Investors')
        wb.save(response)
        return response

    def export_xml(self, header, data, filename):
        root = ET.Element('data')
        for r in data:
            row = ET.SubElement(root, "item")
            for i,h in enumerate([column['label'] for name, column in header.items()]):
                field = ET.SubElement(row, "field")
                field.text = str(r[i])
                field.set("name", h)
        xml = parseString(ET.tostring(root)).toprettyxml()
        response = HttpResponse(xml, content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response

    def export_csv(self, header, data, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        writer = csv.writer(response, delimiter=";", encoding='utf-8')
        #writer = csv.writer(response, delimiter=";", encoding='cp1252')
        # write csv header
        writer.writerow([column['label'] for name, column in header.items()])
        for row in data:
            writer.writerow([str(s) for s in row])
        return response

    @staticmethod
    def format_value(value, i=None):
        if not value:
            return ""
        # Formset?
        if i is not None:
            try:
                value = value[i]
            except IndexError:
                return ""
        row_item = []
        if isinstance(value, (tuple, list)):
            for lv in value:
                if isinstance(lv, dict):
                    year = lv.get("year", None)
                    current = lv.get("current", None)
                    name = lv.get("name", None)
                    vvalue = lv.get("value", None)
                    if name:
                        row_item.append("[%s:%s] %s" % (
                            year != "0" and year or "",
                            current and "current" or "",
                            name.strip(),
                        ))
                    # Required for intention
                    elif vvalue and not lv.get("is_parent", False):
                        row_item.append(str(vvalue).strip())
                        # else:
                        #    row_item.append("[]")
                elif isinstance(lv, (list, tuple)):
                    # Some vars take additional data for the template
                    # (e.g. investor name = {"id":1, "name":"Investor"}), export just the name
                    if len(lv) > 0 and isinstance(lv[0], dict):
                        year = lv.get("year", None)
                        current = lv.get("current", None)
                        name = lv.get("name", None)
                        if name:
                            row_item.append("[%s:%s] %s" % (
                                year != "0" and year or "",
                                current and "current" or "",
                                name.strip(),
                            ))
                            # else:
                            #    row_item.append("[]")
                    else:
                        row_item.append(str(lv).strip() or '')
                else:
                    row_item.append(str(lv).strip() or '')
            return ", ".join(filter(None, row_item))
        else:
            return str(value).strip() or ""

    def get_data(self, items):
        """ Get headers and format the data of the items to a proper download format.
            Returns an array of arrays, each row is an an array of data
        """
        data = {
            'headers': [],
            'items': [],
            'max': {},
        }
        # Get headers and max formset counts
        headers = []
        for form in ChangeDealView.FORMS:
            formset_name = hasattr(form, "form") and form.Meta.name or None
            form = formset_name and form.form or form
            # Is formset?
            if formset_name:
                # Get item with maximum forms
                data['max'][formset_name] = max([i.get('%s_count' % formset_name, 0) for i in items])
                for i in range(0, data['max'][formset_name]):
                    for field_name, field in form.base_fields.items():
                        headers.append('%s %i: %s' % (
                            form.form_title,
                            i + 1,
                            str(field.label),
                        ))
            else:
                for field_name, field in form.base_fields.items():
                    headers.append(str(field.label))
        data['headers'] = headers

        rows = []
        for item in items:
            row = []
            for form in ChangeDealView.FORMS:
                formset_name = hasattr(form, "form") and form.Meta.name or None
                form = formset_name and form.form or form
                # Is formset?
                if formset_name:
                    for i in range(0, data['max'][formset_name]):
                        for field_name, field in form.base_fields.items():
                            row.append(self.format_value(item.get(field_name), i).encode('unicode_escape').decode('utf-8'))
                else:
                    for field_name, field in form.base_fields.items():
                        row.append(self.format_value(item.get(field_name)).encode('unicode_escape').decode('utf-8'))
            rows.append(row)
        data['items'] = rows

        return data


class AllDealsExportView(AllDealsView, ExportView):
    def dispatch(self, request, *args, **kwargs):
        format = kwargs.pop('format')
        kwargs['group'] = 'all'
        context = super().get_context_data(*args, **kwargs)
        return self.export(
            context['data']['items'], context['columns'], format,
            filename=kwargs['group'])

    def _limit_query(self):
        return False


class TableGroupExportView(TableGroupView, ExportView):
    def dispatch(self, request, *args, **kwargs):
        format = kwargs.pop('format')
        context = super().get_context_data(*args, **kwargs)
        return self.export(
            context['data']['items'], context['columns'], format,
            filename=kwargs['group'])

    def _limit_query(self):
        return False


class DealDetailExportView(DealDetailView, ExportView):
    def dispatch(self, request, *args, **kwargs):
        format = kwargs.pop('format')
        context = super(DealDetailExportView, self).get_context_data(*args, **kwargs)
        attributes = []
        for form in context['forms']:
            if hasattr(form, 'forms'):
                for i, subform in enumerate(form.forms):
                    for field in subform.get_fields_display():
                        if field['name'].startswith('tg_') and not field['name'].endswith('_comment'):
                            continue
                        label = '%s %i %s' % (
                            subform.form_title,
                            i + 1,
                            field['label']
                        )
                        attributes.append({
                            'field': label,
                            'value': field['value']
                        })
            else:
                for field in form.get_fields_display():
                    if field['name'].startswith('tg_') and not field['name'].endswith('_comment'):
                        continue
                    attributes.append({
                        'field': field['label'],
                        'value': field['value']
                    })
        headers = OrderedDict()
        headers['field'] = {'label': _('Field')}
        headers['value'] = {'label': _('Value')}
        return self.export(attributes, headers, format, filename=kwargs['deal_id'])
