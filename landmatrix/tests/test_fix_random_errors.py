__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django.test import TestCase

class TestFixRandomErrors(TestCase):
    """ This testcase is for random errors that turn up during development and are not related to
        any feature we're developing at the moment
    """

    def test_deal_id_not_present_in_FROM_columns_when_filtering_by_production_size(self):
        self.client.get(
            self._get_string_filter_by_lt('production_size')
        )

    def test_deal_id_not_present_in_FROM_columns_when_filtering_by_contract_size(self):
        self.client.get(
            self._get_string_filter_by_lt('contract_size')
        )

    def test_deal_id_not_present_in_FROM_columns_when_filtering_by_intended_size(self):
        self.client.get(
            self._get_string_filter_by_lt('intended_size')
        )

    def _get_string_filter_by_lt(self, field):
        return '/en/global_app/all/' +\
               '?filtered=true&limit=&order_by=deal_id&prefix=conditions_empty&' +\
               'conditions_empty-TOTAL_FORMS=1&conditions_empty-INITIAL_FORMS=2&' +\
               'conditions_empty-0-variable=' + field +\
               '&conditions_empty-0-operator=lte&conditions_empty-0-value=345'
