try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import unicodecsv as csv

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict
from django.utils.encoding import force_text
import xlwt

from grid.views import AllDealsView, TableGroupView, DealDetailView




class ExportView(TemplateView):
    template_name = 'export.html'
    FORMATS = ['csv', 'xml', 'xls']

    def export(self, items, columns, format, filename="test"):
        if format not in self.FORMATS:
            raise RuntimeError('Download format not recognized: ' + format)

        return getattr(self, 'export_%s' % format)(
            columns, self.format_items_for_download(items, columns),
            "%s.%s" % (filename, format))

    def export_xls(self, header, data, filename):
        response = HttpResponse(content_type="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        wb = xlwt.Workbook()#encoding='utf-8')
        ws = wb.add_sheet('Land Matrix')
        for i, h in enumerate([column['label'] for name, column in header.items()]):
            ws.write(0, i, str(h))
        for i, row in enumerate(data):
            for j, d in enumerate(row):
                ws.write(i+1, j, str(d))
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


    def format_items_for_download(self, items, columns):
        """ Format the data of the items to a proper download format.
            Returns an array of arrays, each row is an an array of data
        """
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
                            current = lv.get("current", None)
                            name = lv.get("name", None)
                            value = lv.get("value", None)
                            if name:
                                row_item.append("[%s:%s] %s" % (
                                    year != "0" and year or "",
                                    current and "current" or "",
                                    name,
                                ))
                            # Required for intention
                            elif value and not lv.get("is_parent", False):
                                row_item.append(str(value))
                            #else:
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
                                        name,
                                    ))
                                #else:
                                #    row_item.append("[]")
                            else:
                                row_item.append(str(lv) or '')
                        else:
                            row_item.append(str(lv) or '')
                    row.append(", ".join(filter(None, row_item)))
                else:
                    row.append(v or "")
            rows.append(row)
        return rows


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
