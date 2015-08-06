__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.utils import timezone
from landmatrix.views import AjaxView
from landmatrix.tests.with_status import WithStatus

class TestAjaxView(WithStatus):
    """
        - when the values are selected from a list, operator in must return checkboxes, while is must return a select or radio button
    """

    example_values = {
        'id': 'key_id=-1&name=conditions_empty-0-value&operation=in', # id
        'deal scope': 'key_id=-2&name=conditions_empty-1-value&operation=is', # deal scope
        'crops': 'key_id=5248&value=30%2C40&name=conditions_empty-0-value&operation=is_empty', # crops
        'contract farming': 'key_id=5266&value=30%2C40&name=conditions_empty-0-value&operation=is_empty', # contract farming
        'data source type': 'key_id=5238&value=30%2C40&name=conditions_empty-0-value&operation=in', # data source type
        'fully updated': 'key_id=fully_updated&value=30%2C40&name=conditions_empty-0-value&operation=in', # fully updated is one of
        'fully updated by': 'key_id=fully_updated_by&value=30%2C40&name=conditions_empty-0-value&operation=in', # fully updated by is
        'implementation status': [
            'key_id=5258&value=30%2C40&name=conditions_empty-0-value&operation=in', # implementation status is one of
            'key_id=5258&value=30%2C40&name=conditions_empty-0-value&operation=is', # implementation status is
        ],
        'intended size': [
            'key_id=5230&value=30%2C40&name=conditions_empty-0-value&operation=is', # intended size is
            'key_id=5230&value=30%2C40&name=conditions_empty-0-value&operation=in', # intended size is one of
        ],
        'intention': [
            'key_id=5231&value=30%2C40&name=conditions_empty-0-value&operation=in', # intention
            'key_id=5231&value=30%2C40&name=conditions_empty-0-value&operation=is', # intention
        ],
        'investor country': 'key_id=inv_24055&value=30%2C40&name=conditions_empty-0-value&operation=in', # investor country
        'investor name': 'key_id=inv_24054&value=30%2C40&name=conditions_empty-0-value&operation=contains', # investor name
        'last modification': 'key_id=last_modification&value=30%2C40&name=conditions_empty-0-value&operation=is', # last modification
        'location': 'key_id=5227&value=30%2C40&name=conditions_empty-0-value&operation=is', # location
        'nature of the deal': 'key_id=5232&value=30%2C40&name=conditions_empty-0-value&operation=in', # nature of the deal
        'negotiation status': 'key_id=5233&value=30%2C40&name=conditions_empty-0-value&operation=in', # negotiation status
        'new url': 'key_id=5255&value=30%2C40&name=conditions_empty-0-value&operation=contains', # new url
        'organization': 'key_id=5239&value=30%2C40&name=conditions_empty-0-value&operation=contains', # organization
        'primary investor': 'key_id=inv_-2&value=30%2C40&name=conditions_empty-0-value&operation=in', # primary investor
        'target country': 'key_id=5228&value=30%2C40&name=conditions_empty-0-value&operation=in', # target country
    }

    fails_in_v1 = [
        'key_id=5282&value=30%2C40&name=conditions_empty-0-value&operation=lt', # current size in operation
        'key_id=5264&value=30%2C40&name=conditions_empty-0-value&operation=lt', # current size under contract
    ]

    def test_id(self):
        self._test_for_specific_attribute('id')

    def test_deal_scope(self):
        self._test_for_specific_attribute('deal scope')

    def test_crops(self):
        self._test_for_specific_attribute('crops')

    def test_contract_farming(self):
        self._test_for_specific_attribute('contract farming')

    def test_data_source_type(self):
        self._test_for_specific_attribute('data source type')

    def test_fully_updated(self):
        self._test_for_specific_attribute('fully updated')

    def _test_fully_updated_by(self):
        self._test_for_specific_attribute('fully updated by')

    def test_implementation_status(self):
        self._test_for_specific_attribute('implementation status')

    def test_intended_size(self):
        self._test_for_specific_attribute('intended size')

    def test_intention(self):
        self._test_for_specific_attribute('intention')

    def test_investor_country(self):
        self._test_for_specific_attribute('investor country')

    def test_investor_name(self):
        self._test_for_specific_attribute('investor name')

    def test_last_modification(self):
        self._test_for_specific_attribute('last modification')

    def test_location(self):
        self._test_for_specific_attribute('location')

    def test_nature_of_the_deal(self):
        self._test_for_specific_attribute('nature of the deal')

    def test_negotiation_status(self):
        self._test_for_specific_attribute('negotiation status')

    def test_new_url(self):
        self._test_for_specific_attribute('new url')

    def test_organization(self):
        self._test_for_specific_attribute('organization')

    def test_primary_investor(self):
        self._test_for_specific_attribute('primary investor')

    def test_target_country(self):
        self._test_for_specific_attribute('target country')

    def _test_for_specific_attribute(self, attribute):
        to_test = self.example_values[attribute]
        if not isinstance(to_test, list):
            to_test = [to_test]
        for value in to_test:
            response = self._get_url_following_redirects('/ajax/widget/values?'+value)
            print(response.content.decode('utf-8'))


    def _get_url_following_redirects(self, url):
        response = self.client.get(url)
        while response.status_code in range(300, 308):
            response = self.client.get(response.url)
        return response

