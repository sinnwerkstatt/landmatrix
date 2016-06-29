try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import csv

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
import xlwt

from grid.views import AllDealsView, TableGroupView, DealDetailView


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


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
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Land Matrix')
        for i, h in enumerate([column['label'] for name, column in header.items()]):
            ws.write(0, i, h)
        for i, row in enumerate(data):
            for j, d in enumerate(row):
                # Force encoding (required for user input fields)
                d = str(d).encode('utf-8').decode('utf-8')
                ws.write(i+1, j, d)
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
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            filename)
        return response

    def export_csv(self, header, data, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            filename)
        writer = csv.writer(response, delimiter=";")
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
                            'Field': label,
                            'Value': field['value']
                        })
            else:
                for field in form.get_fields_display():
                    if field['name'].startswith('tg_') and not field['name'].endswith('_comment'):
                        continue
                    attributes.append({
                        'Field': field['label'],
                        'Value': field['value']
                    })
        return self.export(attributes, ['Field', 'Value'], format, filename=kwargs['deal_id'])
