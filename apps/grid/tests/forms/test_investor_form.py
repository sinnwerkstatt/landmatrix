from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.grid.forms.investor_form import *
from apps.landmatrix.models import HistoricalInvestor


class BaseInvestorFormTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
    ]

    def setUp(self):
        self.initial = {
            'name': 'Testinvestor',
            'fk_country': '104',
            'classification': '10',
            'homepage': 'https://www.example.com',
            #'opencorporates_link': None,
            'comment': 'Test comment',
        }
        self.data = self.initial
        self.form = BaseInvestorForm(data=self.data)

    def test_init(self):
        form = BaseInvestorForm(initial=self.initial)
        self.assertEqual({104}, set(form.fields['fk_country'].queryset.values_list('pk', flat=True)))

    def test_save(self):
        self.assertEqual(True, self.form.is_valid())
        user = get_user_model().objects.get(username='reporter')
        hinvestor = self.form.save(user=user)
        self.assertEqual(HistoricalInvestor.STATUS_PENDING, hinvestor.fk_status_id)
        now = timezone.now()
        self.assertEqual(now.date(), hinvestor.history_date.date())
        self.assertEqual(user.id, hinvestor.history_user_id)

    def test_get_attributes(self):
        self.assertEqual(True, self.form.is_valid())
        attrs = self.form.get_attributes()
        self.assertEqual('Test comment', attrs.get('comment'))

    def test_get_data(self):
        self.assertEqual(True, self.form.is_valid())
        investor = HistoricalInvestor.objects.get(id=10)
        data = self.form.get_data(investor)
        self.assertEqual({}, data)

    def test_clean(self):
        # Duplicate name
        self.form.data['name'] = 'Test Investor #1'
        self.assertEqual(False, self.form.is_valid())
        self.assertEqual(['This name exists already.'], self.form.errors.get('name'))


class ExportInvestorFormTestCase(TestCase):

    fixtures = [
        'countries_and_regions',
        'users_and_groups',
        'status',
        'investors',
    ]

    def setUp(self):
        self.initial = {
            'name': 'Testinvestor',
            'fk_country': '104',
            'classification': '10',
            'homepage': 'https://www.example.com',
            #'opencorporates_link': None,
            'comment': 'Test comment',
        }
        self.data = self.initial
        self.form = BaseInvestorForm(data=self.data)

    def test_get_display_properties(self):
        doc = self.initial
        doc.update({
            'name': 'Testinvestor #1',
            'operating_company_fk_country': '104',
        })
        values_dict = ExportInvestorForm.get_display_properties(doc)
        display_keys = {'investor_identifier_display', 'fk_country_display', 'classification_display',
                        'opencorporates_link_display', 'fk_status_display', 'history_date_display',
                        'history_user_display', 'action_comment_display', 'id_display'}
        self.assertEqual(display_keys, set(values_dict.keys()))
        self.assertEqual('Myanmar', values_dict.get('fk_country_display'))
        self.assertEqual('Private company', values_dict.get('classification_display'))
        #self.assertEqual('Testinvestor', values_dict.get('name_display'))
        #self.assertEqual('Asia', values_dict.get('operating_company_region_display'))
