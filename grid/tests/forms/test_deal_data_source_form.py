from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory

from grid.forms.deal_data_source_form import *
from grid.tests.views.base import BaseDealTestCase
from landmatrix.models import HistoricalActivity


class DealDataSourceFormTestCase(BaseDealTestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
    ]

    def setUp(self):
        super().setUp()
        self.form = DealDataSourceForm
        self.files = {
            'file-new': SimpleUploadedFile('file 1.pdf', b'123', content_type='application/pdf'),
        }
        self.data = {
            'file': 'file 1.pdf',
            'file_not_public': True,
            'name': 'name',
            'company': 'company',
            'email': 'root@localhost.com',
            'phone': '+123456789',
        }

    def test_clean_file(self):
        form = self.form(data=self.data, files=self.files)
        form.is_valid()
        data = form.clean_file()
        self.assertEqual('file-1.pdf', data.name)

    def test_get_fields_display_with_admin(self):
        form = self.form(initial=self.data)
        user = get_user_model().objects.get(username='administrator')
        fields_display = form.get_fields_display(user=user)
        fields_dict = dict((f['name'], f) for f in fields_display)
        self.assertIn('file', fields_dict.keys())
        self.assertIn('name', fields_dict.keys())
        self.assertIn('company', fields_dict.keys())
        self.assertIn('email', fields_dict.keys())
        self.assertIn('phone', fields_dict.keys())

    def test_get_fields_display_with_anonymous(self):
        form = self.form(initial=self.data)
        fields_display = form.get_fields_display(user=AnonymousUser())
        fields_dict = dict((f['name'], f) for f in fields_display)
        self.assertNotIn('file', fields_dict.keys())
        self.assertNotIn('name', fields_dict.keys())
        self.assertNotIn('company', fields_dict.keys())
        self.assertNotIn('email', fields_dict.keys())
        self.assertNotIn('phone', fields_dict.keys())


class AddDealDataSourceFormSetTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'activities',
    ]

    def setUp(self):
        self.formset = AddDealDataSourceFormSet
        self.request = RequestFactory()
        self.file = SimpleUploadedFile('file 1.pdf', b'123', content_type='application/pdf')
        self.request.FILES = {
            'data_source-0-file-new': self.file
        }
        self.initial = [
            {
                'file': 'file 1.pdf',
                'file_not_public': True,
                'name': 'name',
                'company': 'company',
                'email': 'root@localhost.com',
                'phone': '+123456789',
            }
        ]
        self.data = {
            'data_source-TOTAL_FORMS': 1,
            'data_source-INITIAL_FORMS': 0,
            'data_source-MIN_NUM_FORMS': 1,
            'data_source-MAX_NUM_FORMS': 1,
            'data_source-0-file': 'file 1.pdf',
            'data_source-0-file_not_public': True,
            'data_source-0-name': 'name',
            'data_source-0-company': 'company',
            'data_source-0-email': 'root@localhost.com',
            'data_source-0-phone': '+123456789',
        }


    def test_get_attributes(self):
        formset = self.formset(data=self.data, files=self.request.FILES, prefix='data_source')
        attributes = formset.get_attributes(request=self.request)
        self.assertEqual(1, len(attributes))
        self.assertGreater(len(attributes[0]['file'].get('value')), 0)

    def test_get_data(self):
        activity = HistoricalActivity.objects.get(id=10)
        data = self.formset.get_data(activity)
        self.assertEqual(1, len(data))
        self.assertIn('Media report', data[0].get('type'))

    def test_get_file_from_upload(self):
        formset = self.formset(data=self.data)
        uploaded = formset.get_file_from_upload(self.request.FILES, 0)
        self.assertGreater(len(uploaded), 0)

        uploaded = formset.get_file_from_upload(self.request.FILES, 1)
        self.assertEqual(None, uploaded)
