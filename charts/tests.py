from django.test import TestCase


from .pdfgen import pdfize_url


class PDFGenTests(TestCase):

    def test_pdfize_url_returns_streaminghttpresponse(self):
        response = pdfize_url('http://google.com', 'test.pdf')
        self.assertTrue(hasattr(response, 'streaming_content'))
        self.assertEqual('attachment; filename="test.pdf"',
                         response['Content-Disposition'])
