'''
django-wkhtmltopdf almost works, however when piping a file to it, it has
trouble finding all assets.

Instead, just pass the URL and let wkhtmltopdf work its magic.
'''
import copy
import urllib.parse as urlparse
from tempfile import NamedTemporaryFile

from django.core.urlresolvers import reverse
from django.http import FileResponse
from wkhtmltopdf.utils import wkhtmltopdf


def _update_querystring(url, params):
    parsed_url = urlparse.urlparse(url)
    query_string = urlparse.parse_qs(parsed_url[4])
    query_string.update(params)
    encoded_qs = urlparse.urlencode(query_string)
    new_url = urlparse.urlunparse((parsed_url[0], parsed_url[1], parsed_url[2],
                                  parsed_url[3], encoded_qs, ''))

    return new_url


class PDFResponse(FileResponse):

    def __init__(self, content, status=200, content_type='application/pdf',
                 filename=None, *args, **kwargs):
        super().__init__(content, status=status, content_type=content_type)

        self.filename = filename
        if self.filename:
            header_text = 'attachment; filename="{}"'.format(self.filename)
            self['Content-Disposition'] = header_text
        else:
            del self['Content-Disposition']


class PDFViewMixin:
    '''
    PDFViewMixin allows regular views to be rendered as a PDF.

    It works by making another request to the server, to render an HTML page
    with the context variable 'is_pdf_export' set to True. wkhtmltopdf then
    saves the result to a PDF tempfile on disk, which is served as the
    response. This process is terribly inefficient, but it works.

    In general you will need to define two URLs for any view inheriting from
    PDFViewMixin:

        - one with a kwarg of format='PDF' (returns the PDFResponse)
        - one without that kwarg that returns a normal HTML response

    These URLs must be named and the names set as the class attributes
    `pdf_export_url` and `pdf_render_url` respectively. Unfortunately reversing
    them is just too error prone. Alternatively classes can implement
    get_pdf_export_url or get_pdf_render_url.

    Additionally, a `pdf_filename` class attribute (or get_pdf_filename) method
    are required to set the response filename.
    '''
    pdf_filename = None
    pdf_export_url = None
    pdf_render_url = None

    send_pdf_as_attachment = True
    pdf_rendering_context_name = 'is_pdf_export'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        if 'format' in kwargs and kwargs['format'].upper() == 'PDF':
            # build a URL to generate HTML for the PDF view
            pdf_rendering_url = self.build_full_pdf_rendering_url(request,
                                                                  *args,
                                                                  **kwargs)
            pdf_filename = self.get_pdf_filename(request, *args, **kwargs)
            response = self.render_url_to_pdf_response(pdf_rendering_url,
                                                       pdf_filename)
        else:
            context = self.get_context_data(**kwargs)
            pdf_export_url = self.get_pdf_export_url(request, *args, **kwargs)
            context['pdf_export_url'] = pdf_export_url

            if self.pdf_rendering_context_name in request.GET:
                # Render the PDF HTML
                context[self.pdf_rendering_context_name] = True

            response = self.render_to_response(context)

        return response

    def get_pdf_filename(self, request, *args, **kwargs):
        return self.pdf_filename

    def get_pdf_export_url(self, request, *args, **kwargs):
        return self.pdf_export_url

    def get_pdf_render_url(self, request, *args, **kwargs):
        '''Strip out the format arg, and reverse the URL'''
        kwargs_copy = copy.copy(kwargs)
        if 'format' in kwargs_copy:
            del kwargs_copy['format']
        return reverse(self.pdf_render_url, args=args, kwargs=kwargs_copy)

    def build_full_pdf_rendering_url(self, request, *args, **kwargs):
        pdf_render_url = self.get_pdf_render_url(request, *args, **kwargs)

        url = request.build_absolute_uri(pdf_render_url)
        url = _update_querystring(url, {self.pdf_rendering_context_name: 1})

        return url

    def render_url_to_pdf_response(self, url, filename):
        pdf_output = NamedTemporaryFile(delete=True)
        wkhtmltopdf([url], output=pdf_output.name)

        response = PDFResponse(pdf_output, filename=filename)

        return response
