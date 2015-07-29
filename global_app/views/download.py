__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.http import HttpResponse


def write_to_xls(header, data, filename):
    import xlwt
    response = HttpResponse(content_type="application/ms-excel")
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

def write_to_xml(header, data, filename):
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
    from xml.dom.minidom import parseString

    root = ET.Element('data')
    for r in data:
        row = ET.SubElement(root, "item")
        for i,h in enumerate(header):
            field = ET.SubElement(row, "field")
            field.text = str(r[i])
            field.set("name", h)
    xml = parseString(ET.tostring(root)).toprettyxml()
    response = HttpResponse(xml, content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response

def write_to_csv(header, data, filename):
    import csv

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    writer = csv.writer(response, delimiter=";")
    # write csv header
    writer.writerow(header)
    for row in data:
        writer.writerow([str(s).encode("utf-8") for s in row])
    return response

""" Format the data of the items to a propper download format.
        Returns an array of arrays, each row is an an array of data
"""
def format_items_for_download(items, columns):
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


class Download:

    DOWNLOAD_ROUTINES = { 'csv': write_to_csv, 'xml': write_to_xml, 'xls': write_to_xls }

    def __init__(self, format, columns, group):
        self.format = format
        self.columns = columns
        self.group = group

    def get_download(self, items):
        if self.format not in self.supported_formats():
            raise RuntimeError('Download format not recognized: ' + self.format)

        return self.DOWNLOAD_ROUTINES[self.format](
            self.columns, format_items_for_download(items, self.columns), "%s.%s" % (self.group, self.format)
        )

    @classmethod
    def supported_formats(cls):
        return cls.DOWNLOAD_ROUTINES.keys()

