from subprocess import CalledProcessError

from django.http import QueryDict
from django.test import TestCase, RequestFactory

from landmatrix.pdfgen import update_querystring, PDFResponse, PDFViewMixin


class PDFResponseTestCase(TestCase):

    def test_init_with_filename(self):
        filename = 'file.pdf'
        response = PDFResponse(b'', filename=filename)
        self.assertEqual(f'attachment; filename="{filename}"', response['Content-Disposition'])

    def test_init_without_filename(self):
        response = PDFResponse(b'', filename=None)
        self.assertEqual(False, hasattr(response, 'Content-Disposition'))


class PDFViewMixinTestCase(TestCase):

    def setUp(self):
        self.mixin = PDFViewMixin()
        self.mixin.get_context_data = lambda **kwargs: {}
        self.mixin.render_to_response = lambda c: c
        self.mixin.pdf_export_url = 'deal_detail_pdf'
        self.mixin.pdf_render_url = 'deal_detail'

        self.request = RequestFactory()
        self.request.build_absolute_uri = lambda u: f'http://localhost{u}'
        self.request.GET = QueryDict('is_pdf_export=1')

    def test_get(self):
        response_dict = self.mixin.get(self.request, deal_id=1)
        self.assertEqual({'pdf_export_url': '/deal/1.pdf', 'is_pdf_export': True}, response_dict)

    def test_get_with_pdf(self):
        with self.assertRaises(CalledProcessError):
            response = self.mixin.get(self.request, deal_id=1, format='PDF')

    def get_pdf_filename(self):
        self.mixin.pdf_filename = 'file.pdf'
        self.assertEqual('file.pdf', self.mixin.get_pdf_filename)

    def get_pdf_export_url(self):
        self.assertEqual('/deal/1.pdf', self.mixin.get_pdf_export_url(self.request, deal_id=1))

    def get_pdf_render_url(self):
        self.assertEqual('/deal/1/', self.mixin.get_pdf_export_url(self.request, deal_id=1))

    def test_build_full_pdf_rendering_url(self):
        url = self.mixin.build_full_pdf_rendering_url(self.request, deal_id=1)
        self.assertEqual('http://localhost/deal/1/?is_pdf_export=1', url)

    def test_render_url_to_pdf_response(self):
        with self.assertRaises(CalledProcessError):
            response = self.mixin.render_url_to_pdf_response('http://localhost', 'file.pdf')

    def test_update_querystring(self):
        url = 'http://www.example.com/path/?key=value'
        expected = 'http://www.example.com/path/?key=value&key2=value2'
        self.assertEqual(expected, update_querystring(url, {'key2': 'value2'}))
