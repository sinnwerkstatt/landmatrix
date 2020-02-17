import copy
import os
import shlex
import subprocess
import urllib.parse as urlparse
from itertools import chain
from tempfile import NamedTemporaryFile, TemporaryFile

from django.conf import settings
from django.http import FileResponse
from django.urls import reverse
from django.utils import six


def update_querystring(url, params):
    """
    django-wkhtmltopdf almost works, however when piping a file to it, it has trouble finding all assets.
    Instead, just pass the URL and let wkhtmltopdf (the script) work its magic.
    """
    parsed_url = urlparse.urlparse(url)
    query_string = dict(urlparse.parse_qsl(parsed_url[4]))
    query_string.update(params)
    encoded_qs = urlparse.urlencode(query_string)
    url_components = (
        parsed_url[0],
        parsed_url[1],
        parsed_url[2],
        parsed_url[3],
        encoded_qs,
        "",
    )
    new_url = urlparse.urlunparse(url_components)

    return new_url


NO_ARGUMENT_OPTIONS = ['--collate', '--no-collate', '-H', '--extended-help', '-g',
                       '--grayscale', '-h', '--help', '--htmldoc', '--license', '-l',
                       '--lowquality', '--manpage', '--no-pdf-compression', '-q',
                       '--quiet', '--read-args-from-stdin', '--readme',
                       '--use-xserver', '-V', '--version', '--dump-default-toc-xsl',
                       '--outline', '--no-outline', '--background', '--no-background',
                       '--custom-header-propagation', '--no-custom-header-propagation',
                       '--debug-javascript', '--no-debug-javascript',
                       '--default-header',
                       '--disable-external-links', '--enable-external-links',
                       '--disable-forms', '--enable-forms', '--images', '--no-images',
                       '--disable-internal-links', '--enable-internal-links', '-n',
                       '--disable-javascript', '--enable-javascript',
                       '--keep-relative-links',
                       '--load-media-error-handling',
                       '--disable-local-file-access', '--enable-local-file-access',
                       '--exclude-from-outline', '--include-in-outline',
                       '--disable-plugins',
                       '--enable-plugins', '--print-media-type',
                       '--no-print-media-type',
                       '--resolve-relative-links', '--disable-smart-shrinking',
                       '--enable-smart-shrinking', '--stop-slow-scripts',
                       '--no-stop-slow-scripts', '--disable-toc-back-links',
                       '--enable-toc-back-links', '--footer-line', '--no-footer-line',
                       '--header-line', '--no-header-line', '--disable-dotted-lines',
                       '--disable-toc-links', '--verbose']


def _options_to_args(**options):
    """
    Converts ``options`` into a list of command-line arguments.
    Skip arguments where no value is provided
    For flag-type (No argument) variables, pass only the name and only then if the value is True
    """
    flags = []
    for name in sorted(options):
        value = options[name]
        formatted_flag = '--%s' % name if len(name) > 1 else '-%s' % name
        formatted_flag = formatted_flag.replace('_', '-')
        accepts_no_arguments = formatted_flag in NO_ARGUMENT_OPTIONS
        if value is None or (value is False and accepts_no_arguments):
            continue
        flags.append(formatted_flag)
        if accepts_no_arguments:
            continue
        flags.append(six.text_type(value))
    return flags


def wkhtmltopdf(pages, output=None, **kwargs):  # pragma: no cover
    """
    Copied from wkhtmltopdf to improve error handling.
    If wkhtmltopdf fails, there's nothing we can do, but at least this version
    captures the output so it appears in the stack trace

    Converts html to PDF using http://wkhtmltopdf.org/.
    pages: List of file paths or URLs of the html to be converted.
    output: Optional output file path. If None, the output is returned.
    **kwargs: Passed to wkhtmltopdf via _extra_args() (See
              https://github.com/antialize/wkhtmltopdf/blob/master/README_WKHTMLTOPDF
              for acceptable args.)
              Kwargs is passed through as arguments. e.g.:
                  {'footer_html': 'http://example.com/foot.html'}
              becomes
                  '--footer-html http://example.com/foot.html'
              Where there is no value passed, use True. e.g.:
                  {'disable_javascript': True}
              becomes:
                  '--disable-javascript'
              To disable a default option, use None. e.g:
                  {'quiet': None'}
              becomes:
                  ''
    example usage:
        wkhtmltopdf(pages=['/tmp/example.html'],
                    dpi=300,
                    orientation='Landscape',
                    disable_javascript=True)
    """
    if isinstance(pages, str):
        # Support a single page.
        pages = [pages]

    if output is None:
        # Standard output.
        output = "-"

    # Default options:
    options = getattr(settings, "WKHTMLTOPDF_CMD_OPTIONS", None)
    if options is None:
        options = {"quiet": True}
    else:
        options = copy.copy(options)
    options.update(kwargs)

    # Force --encoding utf8 unless the user has explicitly overridden this.
    options.setdefault("encoding", "utf8")

    env = getattr(settings, "WKHTMLTOPDF_ENV", None)
    if env is not None:
        env = dict(os.environ, **env)

    cmd = "WKHTMLTOPDF_CMD"
    cmd = getattr(settings, cmd, os.environ.get(cmd, "wkhtmltopdf"))

    options_args = _options_to_args(**options)

    ck_args = list(chain(shlex.split(cmd), options_args, list(pages), [output]))
    print(ck_args)

    with TemporaryFile() as errors_tempfile:
        ck_kwargs = {"env": env, "stderr": errors_tempfile}

        try:
            output = subprocess.check_output(ck_args, **ck_kwargs)
        except subprocess.CalledProcessError as err:
            errors_tempfile.seek(0)
            wkhtmltopdf_output = errors_tempfile.read()
            raise err

    return output


class PDFResponse(FileResponse):
    def __init__(
        self,
        content,
        status=200,
        content_type="application/pdf",
        filename=None,
        *args,
        **kwargs,
    ):
        super().__init__(content, status=status, content_type=content_type)

        self.filename = filename
        if self.filename:
            header_text = 'attachment; filename="{}"'.format(self.filename)
            self["Content-Disposition"] = header_text
        else:
            del self["Content-Disposition"]


class PDFViewMixin:
    """
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
    """

    pdf_filename = None
    pdf_export_url = None
    pdf_render_url = None

    send_pdf_as_attachment = True
    pdf_rendering_context_name = "is_pdf_export"
    pdf_javascript_delay = 200

    def get(self, request, *args, format=None, **kwargs):
        if format and format.upper() == "PDF":
            # build a URL to generate HTML for the PDF view
            pdf_rendering_url = self.build_full_pdf_rendering_url(
                request, *args, **kwargs
            )
            pdf_filename = self.get_pdf_filename(request, *args, **kwargs)
            response = self.render_url_to_pdf_response(pdf_rendering_url, pdf_filename)
        else:
            # Render the PDF HTML
            context = self.get_context_data(**kwargs)
            pdf_export_url = self.get_pdf_export_url(request, *args, **kwargs)
            context["pdf_export_url"] = pdf_export_url

            if self.pdf_rendering_context_name in request.GET:
                context[self.pdf_rendering_context_name] = True

            response = self.render_to_response(context)

        return response

    def get_pdf_filename(self, request, *args, **kwargs):
        return self.pdf_filename

    def get_pdf_export_url(self, request, *args, **kwargs):
        return reverse(self.pdf_export_url, args=args, kwargs=kwargs)

    def get_pdf_render_url(self, request, *args, **kwargs):
        return reverse(self.pdf_render_url, args=args, kwargs=kwargs)

    def build_full_pdf_rendering_url(self, request, *args, **kwargs):
        pdf_render_url = self.get_pdf_render_url(request, *args, **kwargs)
        url = request.build_absolute_uri(pdf_render_url)
        url = update_querystring(url, {self.pdf_rendering_context_name: 1})

        return url

    def render_url_to_pdf_response(self, url, filename):
        pdf_output = NamedTemporaryFile(delete=True)

        wkhtmltopdf(
            [url],
            javascript_delay=self.pdf_javascript_delay or 0,
            output=pdf_output.name,
            load_error_handling="ignore",
            no_stop_slow_scripts=True,
            enable_javascript = True,
            debug_javascript = True,
        )

        response = PDFResponse(pdf_output, filename=filename)  # pragma: no cover

        return response  # pragma: no cover
