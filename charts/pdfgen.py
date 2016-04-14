'''
django-wkhtmltopdf almost works, however when piping a file to it, it has
trouble finding all assets.

Instead, just pass the URL and let wkhtmltopdf work its magic.
'''
from tempfile import NamedTemporaryFile

from django.http import FileResponse
from wkhtmltopdf.utils import wkhtmltopdf


def pdfize_url(url, filename):
    '''
    Take a url and return an HttpResponse object, containing a PDF
    version of the URL (with the filename given).
    '''
    pdf_output = NamedTemporaryFile(delete=True)
    wkhtmltopdf([url], output=pdf_output.name)

    response = FileResponse(pdf_output, content_type='application/pdf')
    header_text = 'attachment; filename="{}"'.format(filename)
    response['Content-Disposition'] = header_text

    return response
