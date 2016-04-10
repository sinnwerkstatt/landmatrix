'''
django-wkhtmltopdf almost works, however when piping a file to it, it has 
trouble finding all assets.

Instead, just pass the URL and let wkhtmltopdf work its magic.
'''
from tempfile import NamedTemporaryFile

from django.http import HttpResponse
from wkhtmltopdf.utils import wkhtmltopdf


def pdfize_url(url, filename):
    '''
    Take a url and return an HttpResponse object, containing a PDF
    version of the URL (with the filename given).
    '''
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(
        filename)

    with NamedTemporaryFile() as pdf_output:
        wkhtmltopdf([url], output=pdf_output.name)
        pdf_output.seek(0)
        response.write(pdf_output.read())

    return response
